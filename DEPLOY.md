# Deployment Guide

Public URL after setup: **https://lucasdasilva8.github.io/melanoma-detector/**

The site needs two parts:
- **Frontend** → GitHub Pages (free, automatic)
- **Backend API** → Render (free tier, hosts the AI model)

---

## Part 1: GitHub Pages (frontend) — mostly automatic

The repo includes `.github/workflows/deploy-frontend.yml`. On every push to `main`, GitHub deploys the `frontend/` folder.

### One-time setup

1. Open https://github.com/lucasdasilva8/melanoma-detector/settings/pages
2. Under **Build and deployment** → **Source**, choose **GitHub Actions**
3. Push to `main` (or merge your feature branch into `main`)

Your site will be live at:
**https://lucasdasilva8.github.io/melanoma-detector/**

`frontend/config.js` auto-detects localhost vs production and points to the Render API when hosted on GitHub Pages.

---

## Part 2: Render (backend API) — one-time manual setup

GitHub Pages only hosts static files. The AI model runs on Render.

### Steps

1. Create a free account at https://render.com
2. Click **New** → **Blueprint**
3. Connect GitHub repo `lucasdasilva8/melanoma-detector`
4. Render reads `render.yaml` from the repo root
5. Click **Apply** — first deploy takes **10–20 minutes** (PyTorch is large)

Your API will be at something like:
**https://melanoma-detector-api.onrender.com**

Test it:

```bash
curl https://melanoma-detector-api.onrender.com/health
```

### If your Render URL is different

Edit `frontend/config.js` and update the production URL in the `API_URL` line, then push to `main`.

### Model file requirement

The backend needs `models/melanoma_model.pth` in the repo (tracked with Git LFS). Without it, the API returns 503.

```bash
git lfs install
git lfs track "models/melanoma_model.pth"
git add models/melanoma_model.pth .gitattributes
git commit -m "Add model for deployment"
git push
```

---

## Part 3: Verify end-to-end

1. Open https://lucasdasilva8.github.io/melanoma-detector/
2. Upload a test image
3. First request after idle may take **30–60 seconds** (Render free tier cold start)
4. You should see benign/melanoma probabilities

---

## Updating after retraining

1. Replace `models/melanoma_model.pth` locally
2. Commit and push to `main`
3. Render auto-redeploys the backend
4. GitHub Pages auto-redeploys the frontend

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Site loads but "Could not reach API" | Deploy Render backend; check URL in `config.js` |
| API returns 503 | Model missing from repo — push via Git LFS |
| Very slow first request | Render cold start — normal on free tier |
| CORS errors | Backend already allows all origins; redeploy if needed |

---

## Improving accuracy on phone photos

See [MODEL_IMPROVEMENT.md](MODEL_IMPROVEMENT.md).
