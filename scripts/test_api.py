"""Smoke test for the melanoma detection API."""

import sys
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image

API_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"


def make_test_image() -> bytes:
    image = Image.new("RGB", (224, 224), color=(180, 120, 90))
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


def main() -> None:
    print(f"Testing API at {API_URL}")

    health = requests.get(f"{API_URL}/health", timeout=30)
    health.raise_for_status()
    print("Health:", health.json())

    files = {"file": ("test_lesion.jpg", make_test_image(), "image/jpeg")}
    response = requests.post(f"{API_URL}/predict", files=files, timeout=60)
    response.raise_for_status()
    result = response.json()

    assert "prediction" in result
    assert "confidence" in result
    assert "risk_level" in result
    assert "disclaimer" in result

    print("Predict:", result)


if __name__ == "__main__":
    main()
