# Deployment Guide

## Frontend on Vercel
1. Push the repository to GitHub.
2. Import the repository in Vercel.
3. Set Root Directory to `frontend`.
4. Build command: `npm run build`; output directory: `dist`.
5. Add `VITE_API_BASE_URL` with your deployed backend base URL. Note: VITE_ variables are visible to browser users; never put secrets there.

## Backend on Render
1. Create a Web Service connected to the same repository.
2. Set Root Directory to `backend`.
3. Build command: `pip install -r requirements.txt`.
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
5. Set `CORS_ORIGINS` to your exact deployed frontend origin. Set `MODEL_PATH` only if the weights are present on the service filesystem.
6. Check `/health` and `/docs`.

Free services can sleep and may not offer GPU support. Large models may need a paid or specialized host. Test the full flow from a phone/mobile network.
