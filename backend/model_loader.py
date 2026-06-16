from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn
from torchvision import models

CLASS_NAMES = ["benign", "melanoma"]
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "melanoma_model.pth"
# Screening threshold: flag melanoma if probability exceeds this (prioritizes catching real cases).
DEFAULT_MELANOMA_THRESHOLD = 0.35


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
        self.melanoma_threshold = checkpoint.get(
            "melanoma_threshold", DEFAULT_MELANOMA_THRESHOLD
        )
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def predict(self, tensor) -> dict:
        probabilities = self._predict_probabilities(tensor)
        return self._format_result(probabilities)

    def _predict_probabilities(self, tensor) -> torch.Tensor:
        """Average predictions over original + horizontal flip (test-time augmentation)."""
        tensor = tensor.to(self.device)
        variants = [tensor, torch.flip(tensor, dims=[3])]
        probs = []

        with torch.no_grad():
            for variant in variants:
                logits = self.model(variant)
                probs.append(torch.softmax(logits, dim=1)[0])

        return torch.stack(probs).mean(dim=0)

    def _format_result(self, probabilities: torch.Tensor) -> dict:
        benign_prob = probabilities[0].item()
        melanoma_prob = probabilities[1].item()

        is_melanoma = melanoma_prob >= self.melanoma_threshold
        prediction = "melanoma" if is_melanoma else "benign"
        confidence = melanoma_prob if is_melanoma else benign_prob

        return {
            "prediction": prediction,
            "confidence": round(confidence, 4),
            "risk_level": "high" if is_melanoma else "low",
            "melanoma_probability": round(melanoma_prob, 4),
            "benign_probability": round(benign_prob, 4),
            "threshold_used": self.melanoma_threshold,
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
