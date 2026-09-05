import os
import sys
import json
import pandas as pd
import numpy as np
import tensorflow as tf
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support, accuracy_score
from sklearn.utils.class_weight import compute_class_weight
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import MANIFEST_PATH, CLASS_INDEX_PATH, MODEL_PATH, WEIGHTS_PATH, IMG_SIZE, BATCH_SIZE, LEARNING_RATE, EPOCHS

def load_dataset(manifest_path, class_index_path):
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found at {manifest_path}")
        
    df = pd.read_csv(manifest_path)
    
    with open(class_index_path, 'r') as f:
        class_index = json.load(f)
        
    # Reverse mapping for faster lookup
    name_to_index = {v: int(k) for k, v in class_index.items()}
    num_classes = len(class_index)
    
    # Pre-encode labels
    df['label'] = df['class_label'].map(name_to_index)
    
    return df, class_index, num_classes

def create_tf_dataset(df, is_training=False):
    filepaths = df['filepath'].values
    labels = df['label'].values
    
    dataset = tf.data.Dataset.from_tensor_slices((filepaths, labels))
    
    def process_path(filepath, label):
        img = tf.io.read_file(filepath)
        img = tf.image.decode_image(img, channels=3, expand_animations=False)
        img = tf.image.resize(img, IMG_SIZE)
        return img, label
        
    dataset = dataset.map(process_path, num_parallel_calls=tf.data.AUTOTUNE)
    
    if is_training:
        # Stronger data augmentation for better generalization
        data_augmentation = tf.keras.Sequential([
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.25),
            tf.keras.layers.RandomZoom((-0.2, 0.2)),
            tf.keras.layers.RandomBrightness(0.2),
            tf.keras.layers.RandomContrast(0.2),
            tf.keras.layers.RandomTranslation(0.1, 0.1),
        ])
        dataset = dataset.map(lambda x, y: (data_augmentation(x, training=True), y), num_parallel_calls=tf.data.AUTOTUNE)
        dataset = dataset.shuffle(buffer_size=2000)
        
    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    
    return dataset

def build_model(num_classes):
    inputs = tf.keras.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    
    # Preprocessing for EfficientNetB0 (expects [0, 255])
    x = tf.keras.applications.efficientnet.preprocess_input(inputs)
    
    # EfficientNetB0 — more powerful feature extractor than MobileNetV2
    base_model = tf.keras.applications.EfficientNetB0(
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False
    
    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.4)(x)
    x = tf.keras.layers.Dense(256, activation='relu')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)
    
    model = tf.keras.Model(inputs, outputs)
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.SparseTopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    return model, base_model

def train():
    print("=" * 60)
    print("TRAINING WITH EFFICIENTNETB0 + FINE-TUNING")
    print("=" * 60)
    
    print("\n[Step 1/6] Loading dataset manifest...")
    df, class_index, num_classes = load_dataset(MANIFEST_PATH, CLASS_INDEX_PATH)
    
    df_train = df[df['split'] == 'train']
    df_val = df[df['split'] == 'val']
    df_test = df[df['split'] == 'test']
    
    print(f"  Train: {len(df_train)}, Val: {len(df_val)}, Test: {len(df_test)}")
    print(f"  Number of classes: {num_classes}")
    
    # Compute class weights to handle imbalanced breeds
    print("\n[Step 2/6] Computing class weights for imbalanced data...")
    train_labels = df_train['label'].values
    class_weights_arr = compute_class_weight('balanced', classes=np.unique(train_labels), y=train_labels)
    class_weight_dict = {i: w for i, w in enumerate(class_weights_arr)}
    print(f"  Class weight range: {min(class_weight_dict.values()):.2f} - {max(class_weight_dict.values()):.2f}")
    
    print("\n[Step 3/6] Building tf.data pipelines...")
    train_ds = create_tf_dataset(df_train, is_training=True)
    val_ds = create_tf_dataset(df_val, is_training=False)
    test_ds = create_tf_dataset(df_test, is_training=False)
    
    print("\n[Step 4/6] Building EfficientNetB0 model...")
    model, base_model = build_model(num_classes)
    model.summary()
    
    # Callbacks
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=7,
            restore_best_weights=True,
            mode='max'
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # =====================
    # PHASE 1: HEAD TRAINING
    # =====================
    print("\n" + "=" * 60)
    print("[Step 5/6] PHASE 1: Training classification head (base frozen)...")
    print("=" * 60)
    
    head_epochs = 15
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=head_epochs,
        callbacks=callbacks,
        class_weight=class_weight_dict
    )
    
    print(f"\n  Phase 1 complete. Best val_accuracy: {max(history.history['val_accuracy']):.4f}")
    
    # =====================
    # PHASE 2: FINE-TUNING
    # =====================
    print("\n" + "=" * 60)
    print("[Step 5/6] PHASE 2: Fine-tuning deeper layers...")
    print("=" * 60)
    
    # Unfreeze top layers of EfficientNetB0
    base_model.trainable = True
    # Freeze the first 70% of layers, fine-tune the rest
    freeze_until = int(len(base_model.layers) * 0.6)
    for layer in base_model.layers[:freeze_until]:
        layer.trainable = False
    
    trainable_count = sum(1 for l in base_model.layers if l.trainable)
    print(f"  Fine-tuning {trainable_count} / {len(base_model.layers)} EfficientNetB0 layers")
    
    # Recompile with very low learning rate
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.SparseTopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    fine_tune_epochs = 20
    total_epochs = head_epochs + fine_tune_epochs
    
    history_fine = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=total_epochs,
        initial_epoch=history.epoch[-1] + 1,
        callbacks=callbacks,
        class_weight=class_weight_dict
    )
    
    best_val_acc = max(history_fine.history['val_accuracy'])
    print(f"\n  Phase 2 complete. Best val_accuracy: {best_val_acc:.4f}")
    
    # =====================
    # EVALUATE
    # =====================
    print("\n" + "=" * 60)
    print("[Step 6/6] Evaluating on test set...")
    print("=" * 60)
    
    test_loss, test_acc, test_top3 = model.evaluate(test_ds)
    print(f"  Test Loss:           {test_loss:.4f}")
    print(f"  Test Accuracy (Top-1): {test_acc:.4f}")
    print(f"  Test Accuracy (Top-3): {test_top3:.4f}")
    
    # Save model (full model for legacy) and weights separately
    print(f"\n  Saving model to {MODEL_PATH}...")
    model.save(MODEL_PATH)
    print(f"  Saving weights to {WEIGHTS_PATH}...")
    model.save_weights(WEIGHTS_PATH)
    print("  Model and weights saved successfully.")
    
    # Generate classification report
    print("\n  Generating metrics and confusion matrix...")
    y_true = []
    for images, labels in test_ds:
        y_true.extend(labels.numpy())
    y_true = np.array(y_true)
    
    y_pred_probs = model.predict(test_ds)
    y_pred = np.argmax(y_pred_probs, axis=1)
    
    target_names = [class_index[str(i)] for i in range(num_classes)]
    
    report = classification_report(y_true, y_pred, target_names=target_names)
    print(report)

    # Save metrics to JSON
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    acc = accuracy_score(y_true, y_pred)
    
    metrics = {
        "accuracy": float(acc),
        "top_3_accuracy": float(test_top3),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1)
    }
    
    with open(MODEL_PATH.parent / 'metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
    print("  Saved metrics.json")

    # Generate and save Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(20, 20))
    sns.heatmap(cm, annot=False, cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(str(MODEL_PATH.parent / 'confusion_matrix.png'), dpi=100)
    plt.close()
    print("  Saved confusion_matrix.png")
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print(f"  Final Top-1 Accuracy: {test_acc:.2%}")
    print(f"  Final Top-3 Accuracy: {test_top3:.2%}")
    print("=" * 60)

if __name__ == "__main__":
    train()
