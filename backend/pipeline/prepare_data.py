import os
import sys
import json
import pandas as pd
import imagehash
from PIL import Image
from pathlib import Path
from sklearn.model_selection import train_test_split

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import CATTLE_DIR, BUFFALO_DIR, MANIFEST_PATH, CLASS_INDEX_PATH, TRAIN_RATIO, VAL_RATIO, TEST_RATIO, RANDOM_SEED

def clean_breed_name(name):
    # e.g., Red_Sindhi -> Red Sindhi
    return name.replace("_", " ").title().strip()

def prepare_data():
    records = []
    
    # Check if paths exist
    if not CATTLE_DIR.exists():
        print(f"Error: Cattle dir not found: {CATTLE_DIR}")
        return
    if not BUFFALO_DIR.exists():
        print(f"Error: Buffalo dir not found: {BUFFALO_DIR}")
        return

    # 1. Collect images
    for animal_type, source_dir in [("cattle", CATTLE_DIR), ("buffalo", BUFFALO_DIR)]:
        print(f"Scanning {animal_type} in {source_dir}...")
        for breed_dir in source_dir.iterdir():
            if not breed_dir.is_dir():
                continue
                
            canonical_breed = clean_breed_name(breed_dir.name)
            
            for img_path in breed_dir.glob("*"):
                if img_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    records.append({
                        "filepath": str(img_path.absolute()),
                        "canonical_breed": canonical_breed,
                        "animal_type": animal_type,
                        "source_folder": breed_dir.name
                    })

    df = pd.DataFrame(records)
    print(f"Initial count: {len(df)} images.")

    # Create distinct class label by combining animal_type and breed to avoid conflicts like Bargur
    df['class_label'] = df['animal_type'] + '_' + df['canonical_breed']

    # 2. Deduplicate using perceptual hashing
    print("Deduplicating via perceptual hashing (this may take a minute)...")
    hashes = {}
    duplicates = []
    
    # Optional: limit for testing, or parallelize. We will do it sequentially.
    valid_records = []
    
    for _, row in df.iterrows():
        try:
            with Image.open(row['filepath']) as img:
                # Convert to RGB early and resize for faster hashing
                h = str(imagehash.phash(img))
                
                if h in hashes:
                    duplicates.append(row['filepath'])
                else:
                    hashes[h] = row['filepath']
                    valid_records.append(row)
        except Exception as e:
            print(f"Skipping corrupt or unreadable image {row['filepath']}: {e}")

    df_clean = pd.DataFrame(valid_records)
    print(f"Found {len(duplicates)} duplicates. Kept {len(df_clean)} unique valid images.")

    # 3. Analyze counts and flag low-sample breeds
    counts = df_clean['class_label'].value_counts()
    low_sample = counts[counts < 50]
    if not low_sample.empty:
        print("\nWARNING - Low sample breeds (< 50 images):")
        print(low_sample)

    # 4. Stratified Split
    print("\nPerforming stratified split...")
    
    # We must ensure there are at least a few samples per class to stratify
    classes_to_keep = counts[counts >= 3].index
    df_filtered = df_clean[df_clean['class_label'].isin(classes_to_keep)].copy()
    
    if len(df_filtered) < len(df_clean):
        print(f"Dropped {len(df_clean) - len(df_filtered)} images from classes with < 3 samples (cannot stratify).")
        
    X = df_filtered.index
    y = df_filtered['class_label']
    
    # Split train and temp (val + test)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, train_size=TRAIN_RATIO, stratify=y, random_state=RANDOM_SEED
    )
    
    # Split temp into val and test
    relative_val_ratio = VAL_RATIO / (VAL_RATIO + TEST_RATIO)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, train_size=relative_val_ratio, stratify=y_temp, random_state=RANDOM_SEED
    )
    
    df_filtered['split'] = 'unassigned'
    df_filtered.loc[X_train, 'split'] = 'train'
    df_filtered.loc[X_val, 'split'] = 'val'
    df_filtered.loc[X_test, 'split'] = 'test'

    # 5. Generate class index mapping
    unique_classes = sorted(df_filtered['class_label'].unique())
    class_index = {idx: cls_name for idx, cls_name in enumerate(unique_classes)}
    
    # 6. Save outputs
    df_filtered.to_csv(MANIFEST_PATH, index=False)
    print(f"\nSaved manifest to {MANIFEST_PATH}")
    
    with open(CLASS_INDEX_PATH, 'w') as f:
        json.dump(class_index, f, indent=4)
    print(f"Saved class index to {CLASS_INDEX_PATH}")
    
    print("\nClass distribution in splits:")
    print(df_filtered.groupby(['class_label', 'split']).size().unstack(fill_value=0))

if __name__ == "__main__":
    prepare_data()
