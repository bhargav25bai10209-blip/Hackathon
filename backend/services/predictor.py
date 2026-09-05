import os
import sys
import json
import io
import numpy as np
import tensorflow as tf
from PIL import Image
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import WEIGHTS_PATH, CLASS_INDEX_PATH, IMG_SIZE

class BreedPredictor:
    def __init__(self):
        self.model = None
        self.class_index = None
        self._load_resources()

    def _load_resources(self):
        if not WEIGHTS_PATH.exists():
            print(f"Warning: Model weights not found at {WEIGHTS_PATH}")
            return
            
        if not CLASS_INDEX_PATH.exists():
            print(f"Warning: Class index not found at {CLASS_INDEX_PATH}")
            return
            
        print("Loading model and class index...")
        with open(CLASS_INDEX_PATH, 'r') as f:
            self.class_index = json.load(f)

        num_classes = len(self.class_index)
        print(f"Building EfficientNetB0 model architecture ({num_classes} classes)...")
        
        # Build the EXACT same architecture as train_model.py
        inputs = tf.keras.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
        x = tf.keras.applications.efficientnet.preprocess_input(inputs)
        
        base_model = tf.keras.applications.EfficientNetB0(
            input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
            include_top=False,
            weights='imagenet'
        )
        x = base_model(x, training=False)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.4)(x)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.3)(x)
        outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)
        
        self.model = tf.keras.Model(inputs, outputs)
        
        print(f"Loading trained weights from {WEIGHTS_PATH}...")
        self.model.load_weights(WEIGHTS_PATH)
        print("Model loaded successfully!")


    def predict(self, image_bytes: bytes, top_k=3):
        if self.model is None or self.class_index is None:
            raise RuntimeError("Model or class index not loaded.")
            
        # Read and preprocess image
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img = img.resize(IMG_SIZE)
        img_array = tf.keras.preprocessing.image.img_to_array(img)  # Returns values in [0, 255]
        img_array = np.expand_dims(img_array, axis=0)  # Create batch of 1
        # NOTE: preprocess_input is built INTO the model, so we feed raw [0, 255] values
        
        # Predict
        predictions = self.model.predict(img_array)[0]
        
        # Get top-k
        top_indices = np.argsort(predictions)[-top_k:][::-1]
        
        results = []
        for i in top_indices:
            class_name = self.class_index[str(i)]
            confidence = float(predictions[i])
            results.append({
                "class_label": class_name,
                "confidence": confidence
            })
            
        return results

# Singleton instance
predictor = BreedPredictor()
