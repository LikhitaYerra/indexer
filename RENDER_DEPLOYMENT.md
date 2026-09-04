# Render Deployment (Highest Accuracy)

This deploys the **Python + spaCy transformer** backend (`en_core_web_trf`) and connects it to your GitHub Pages frontend.

## 1) Push latest code

```bash
cd /Users/likhitayerra/indexer
git add .
git commit -m "Add Render API backend for high-accuracy indexing"
git push
```

## 2) Create Render web service

1. Open [https://dashboard.render.com/](https://dashboard.render.com/)
2. Click **New +** -> **Blueprint**
3. Connect your GitHub repo: `LikhitaYerra/indexer`
4. Render will detect `render.yaml`
5. Click **Apply**

This creates a Docker web service named `indexer-api` with health check at `/health`.

## 3) Wait for initial build

- First build can take several minutes (transformer model is large).
- In Render logs, wait for `Uvicorn running on ...`
- Health URL should return JSON:

`https://<your-service>.onrender.com/health`

Expected response:

```json
{"ok": true, "model": "en_core_web_trf"}
```

## 4) Connect frontend to backend

1. Open your live page: `https://likhitayerra.github.io/indexer/`
2. In **Try It** section, paste your Render URL in **Render API URL**
   - Example: `https://indexer-api.onrender.com`
3. Upload `.docx` -> **Generate Index**

The page stores this URL in browser local storage for future use.

## 5) (Optional) Pre-fill API URL in code

If you want clients to avoid entering the URL manually:

- Edit `docs/script.js`
- Set:

```js
const DEFAULT_API_BASE = "https://<your-service>.onrender.com";
```

Then push changes.

## Notes

- `en_core_web_trf` gives best general accuracy here.
- Free/smaller plans may sleep; first request after idle can be slow.
- Keep `MAX_UPLOAD_MB` in `render.yaml` aligned with expected manuscript sizes.
