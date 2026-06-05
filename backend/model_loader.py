from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn
from torchvision import models

CLASS_NAMES = ["benign", "melanoma"]
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "melanoma_model.pth"


def build_model(num_classes: int = 2) -> nn.Module:
    model = models.resnet18(weights=None)
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_features, num_classes),
    )
    return model


class MelanomaPredictor:
    def __init__(self, model_path: Path = MODEL_PATH):
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found at {model_path}. "
                "Train on Kaggle (training/train_ham10000.ipynb) or run scripts/create_demo_model.py."
            )

        checkpoint = torch.load(model_path, map_location="cpu", weights_only=False)
        self.model = build_model()
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.eval()

        self.class_names = checkpoint.get("class_names", CLASS_NAMES)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def predict(self, tensor) -> dict:
        tensor = tensor.to(self.device)

        with torch.no_grad():
            logits = self.model(tensor)
            probabilities = torch.softmax(logits, dim=1)[0]

        confidence, predicted_idx = torch.max(probabilities, dim=0)
        prediction = self.class_names[predicted_idx.item()]
        confidence_value = round(confidence.item(), 4)

        return {
            "prediction": prediction,
            "confidence": confidence_value,
            "risk_level": "high" if prediction == "melanoma" else "low",
            "probabilities": {
                name: round(probabilities[i].item(), 4)
                for i, name in enumerate(self.class_names)
            },
        }


_predictor: Optional[MelanomaPredictor] = None


def get_predictor() -> MelanomaPredictor:
    global _predictor
    if _predictor is None:
        _predictor = MelanomaPredictor()
    return _predictor
