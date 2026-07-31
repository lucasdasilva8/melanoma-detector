# Melanoma Detection AI + Website

Educational skin lesion screening tool. Upload a close-up photo of a skin lesion and get an AI-assisted risk assessment.

**This is not a medical diagnosis. See a dermatologist for any concerning skin changes.**

## Project structure

```
melanoma-detector/
├── backend/          # FastAPI inference API
├── frontend/         # Upload website (HTML/CSS/JS)
├── models/           # Place melanoma_model.pth here after Kaggle training
├── training/         # Kaggle training notebook
└── scripts/          # Helper scripts
```

## Quick start (local)

### 1. Train the model (Kaggle — free GPU)

1. Create a [Kaggle](https://www.kaggle.com) account.
2. Open [HAM10000](https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000) and [Skin_Lesion_Dataset](https://www.kaggle.com/datasets/billalmanzoor/skin-lesion-dataset).
3. Create a new **GPU notebook** and upload `training/train_ham10000.ipynb`.
4. **Add Input** for both datasets. Run all cells. Download `melanoma_model.pth` when done.
5. Place the file in `models/melanoma_model.pth`.

For a quick local smoke test without training, run:

```bash
python scripts/create_demo_model.py
```

### 2. Start the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3. Start the frontend

```bash
cd frontend
python -m http.server 3000
```

Open http://localhost:3000 and upload a test image.

## Deployment

Live site (after setup): **https://lucasdasilva8.github.io/melanoma-detector/**

See [DEPLOY.md](DEPLOY.md) for GitHub Pages + Render setup.

## Improving accuracy on phone photos

1. Add **Skin_Lesion_Dataset** on Kaggle (`billalmanzoor/Skin_Lesion_Dataset`) — ISIC 2019 + MED-NODE + PAD-UFES-20, merged automatically in Cell 5
2. Retrain with `training/train_ham10000.ipynb`
3. See [MODEL_IMPROVEMENT.md](MODEL_IMPROVEMENT.md) for the full guide

## Disclaimer

This tool is for educational purposes only. It was trained on dermatoscopic images (HAM10000) and may not perform well on casual phone photos. Always consult a qualified healthcare professional for medical advice.
