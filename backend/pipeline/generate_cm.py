import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import tensorflow as tf
from pathlib import Path
import json

# Add backend directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from pipeline.config import PROCESSED_DATA_DIR, IMG_SIZE, BATCH_SIZE, MODEL_PATH, CLASS_INDEX_PATH

def generate_cm():
    with open(CLASS_INDEX_PATH, 'r') as f:
        class_index = json.load(f)
    num_classes = len(class_index)
    
    # Load model
    print("Loading model weights...")
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=IMG_SIZE + (3,),
        include_top=False,
        weights=None
    )
    x = base_model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    predictions = tf.keras.layers.Dense(num_classes, activation='softmax', name='dense_predictions')(x)
    model = tf.keras.models.Model(inputs=base_model.input, outputs=predictions)
    model.load_weights(MODEL_PATH, by_name=True)

    # Load test dataset
    test_dir = PROCESSED_DATA_DIR / 'test'
    test_ds = tf.keras.preprocessing.image_dataset_from_directory(
        test_dir,
        seed=42,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    y_true = []
    for images, labels in test_ds:
        y_true.extend(labels.numpy())
    
    print("Predicting...")
    y_pred_probs = model.predict(test_ds)
    y_pred = np.argmax(y_pred_probs, axis=1)

    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(20, 20))
    sns.heatmap(cm, annot=False, cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig(str(MODEL_PATH.parent / 'confusion_matrix.png'))
    print("Confusion matrix saved!")

if __name__ == '__main__':
    generate_cm()
