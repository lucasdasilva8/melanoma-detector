# Deployment Guide

Deploy the backend to **Render** (free tier) and the frontend to **GitHub Pages**.

## Prerequisites

- GitHub account
- [Render](https://render.com) account (free)
- Trained model at `models/melanoma_model.pth`

## 1. Push to GitHub

```bash
git add .
git commit -m "Initial melanoma detection app"
git remote add origin https://github.com/YOUR_USERNAME/melanoma-detector.git
git push -u origin main
```

> **Note:** `melanoma_model.pth` is gitignored by default (~45 MB). For Render deployment, either:
> - Use [Git LFS](https://git-lfs.github.com/) to track the model file, or
> - Upload the model to cloud storage and download it in `render.yaml` build step

## 2. Deploy backend (Render)

1. Go to [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint**
2. Connect your GitHub repo
3. Render reads `render.yaml` automatically
4. Set environment variable if needed: none required for basic setup
5. Deploy — first build takes ~10–15 min (PyTorch is large)

Your API will be at: `https://melanoma-detector-api.onrender.com` (or similar)

Test it:

```bash
curl https://YOUR-API-URL.onrender.com/health
```

## 3. Deploy frontend (GitHub Pages)

1. Update `frontend/config.js` with your Render API URL:

```javascript
window.APP_CONFIG = {
  API_URL: "https://YOUR-API-URL.onrender.com",
};
```

2. Enable GitHub Pages:
   - Repo → **Settings** → **Pages**
   - Source: **Deploy from branch**
   - Branch: `main` → folder: `/frontend`

3. Your site will be at: `https://YOUR_USERNAME.github.io/melanoma-detector/`

## 4. CORS

The backend already allows all origins (`allow_origins=["*"]`). For production, consider restricting to your GitHub Pages domain.

## Cold starts

Render free tier spins down after inactivity. First request after idle may take 30–60 seconds. This is normal for free hosting.

## Alternative: Netlify for frontend

1. Connect repo to [Netlify](https://netlify.com)
2. Base directory: `frontend`
3. Publish directory: `frontend`
4. Update `config.js` with your API URL before deploying
