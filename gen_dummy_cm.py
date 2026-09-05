import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from pathlib import Path

# Create a dummy confusion matrix just to fix the broken image link temporarily
# until the user retrains the model properly.
cm = np.random.randint(0, 100, size=(10, 10))
plt.figure(figsize=(10, 10))
sns.heatmap(cm, annot=False, cmap='Blues')
plt.title('Confusion Matrix (Dummy Data - Retrain to update)')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')

out_path = Path('backend/models/confusion_matrix.png')
out_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(str(out_path))
plt.close()
print('Dummy confusion matrix saved.')
