import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
PIPELINE_DIR = BASE_DIR / "pipeline"

ORIGIN_DIR = BASE_DIR.parent
CATTLE_DIR = ORIGIN_DIR / "cattle"
BUFFALO_DIR = ORIGIN_DIR / "buffalo"

MANIFEST_PATH = DATA_DIR / "manifest.csv"
CLASS_INDEX_PATH = DATA_DIR / "class_index.json"
BREED_REGION_MAP_PATH = DATA_DIR / "breed_region_map.json"

MODEL_PATH = MODELS_DIR / "breed_model.h5"
WEIGHTS_PATH = MODELS_DIR / "breed_model.weights.h5"

# Hyperparameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
LEARNING_RATE = 1e-4
EPOCHS = 20
RANDOM_SEED = 42

# Train/Val/Test split
TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15
