"""Create a demo model checkpoint for local API smoke testing.

This uses ImageNet-pretrained ResNet18 weights with a random classification head.
Predictions are NOT medically meaningful — train on Kaggle for real results.
"""

from pathlib import Path

import torch
import torch.nn as nn
from torchvision import models

CLASS_NAMES = ["benign", "melanoma"]
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "models" / "melanoma_model.pth"


def build_model(num_classes: int = 2) -> nn.Module:
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_features, num_classes),
    )
    return model


def main() -> None:
    model = build_model()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    checkpoint = {
        "model_state_dict": model.state_dict(),
        "class_names": CLASS_NAMES,
        "note": "Demo model for local testing only. Train on Kaggle for real predictions.",
    }
    torch.save(checkpoint, OUTPUT_PATH)
    print(f"Saved demo model to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
