# UAV Object Detection — Starter Project

A starter repository for the research project **Explainable and Uncertainty-Aware UAV Object Detection under Adverse Environmental Conditions**.

## Included
- React + Vite + TypeScript frontend dashboard
- FastAPI backend with health and image-upload prediction endpoints
- Optional Ultralytics YOLO inference when you provide compatible weights
- Deployment instructions for Vercel (frontend) and Render (backend)
- Experiment plan, dataset notes, blank results template, and architecture notes

## Important limitations
This starter does **not** include a trained model, VisDrone dataset, measured benchmark results, or a D-RISE implementation. The API runs in clearly labeled demo mode when `MODEL_PATH` is empty and will not invent detections. Do not report demo output or blank result placeholders as research evidence.

## Run locally
### Backend (Python 3.10+)
```bash
cd backend
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Copy .env.example to .env, then:
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Visit `http://127.0.0.1:8000/health` and `http://127.0.0.1:8000/docs`.

### Frontend (Node.js 20+ recommended)
```bash
cd frontend
npm install
# Copy .env.example to .env
npm run dev
```
Open the local URL Vite prints, usually `http://localhost:5173`.

## Enable real YOLO inference
1. Put compatible weights in `backend/weights/` (this folder is ignored by Git).
2. Copy `backend/.env.example` to `backend/.env`.
3. Set `MODEL_PATH=weights/best.pt` to the real file name.
4. Install `ultralytics` with `pip install ultralytics`.
5. Restart the API. The hosting service must have enough memory/compute for the model.

## GitHub upload
From the project root:
```bash
git init
git add .
git commit -m "Initial UAV object detection project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```
Replace the URL with your actual GitHub repository URL. Do not commit `.env`, passwords, API keys, datasets, private images, or large model weights.

## Deploy
- **Vercel frontend:** import the GitHub repo; set Root Directory to `frontend`, build command `npm run build`, output directory `dist`, and `VITE_API_BASE_URL` to your deployed backend URL.
- **Render backend:** create a Python web service; set Root Directory to `backend`, build command `pip install -r requirements.txt`, start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Set `CORS_ORIGINS` to the exact deployed frontend origin.
- See `docs/DEPLOYMENT.md` for details. Free hosts can sleep and may not support GPU inference.

## Research next steps
Use the official VisDrone dataset and follow its terms. Define clean baseline and controlled corruption experiments, train/evaluate both baseline and augmentation variants on fixed splits, then add calibration/error-ranking metrics with a documented matching protocol and explanation-stability evaluation. Record configurations and only report values actually measured.
