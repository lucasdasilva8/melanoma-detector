"""Check whether the saved model can detect melanoma or is stuck predicting benign."""

import sys
from io import BytesIO

import numpy as np
from PIL import Image

sys.path.insert(0, "backend")
from model_loader import MelanomaPredictor
from preprocess import preprocess_image


def main() -> None:
    predictor = MelanomaPredictor()
    melanoma_probs = []

    for _ in range(10):
        color = tuple(np.random.randint(20, 220, size=3).tolist())
        image = Image.new("RGB", (400, 400), color)
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        result = predictor.predict(preprocess_image(buffer.getvalue()))
        melanoma_probs.append(result["melanoma_probability"])

    max_mel = max(melanoma_probs)
    avg_mel = sum(melanoma_probs) / len(melanoma_probs)

    print(f"Threshold: {predictor.melanoma_threshold}")
    print(f"Max melanoma probability (random images): {max_mel:.2%}")
    print(f"Avg melanoma probability (random images): {avg_mel:.2%}")

    if max_mel < 0.10:
        print(
            "\n⚠️  Model appears stuck on 'benign' — it rarely assigns meaningful melanoma probability."
        )
        print("Fix: retrain on Kaggle using training/train_ham10000.ipynb and replace models/melanoma_model.pth")
    else:
        print("\nModel shows some melanoma sensitivity. Test with dermoscopic-style close-up lesion photos.")


if __name__ == "__main__":
    main()
