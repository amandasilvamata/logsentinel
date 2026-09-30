# LogSentinel frontend

React + Vite interface for the existing FastAPI log analyzer. The frontend sends the selected `.log` or `.txt` file to `POST http://127.0.0.1:8000/analyze` as `FormData` under the field name `file`. No sample data is substituted for API results.

## Run

Start the Python API at `http://127.0.0.1:8000`, then:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The Vite dev server uses that exact origin because it is the origin currently allowed by FastAPI CORS.

## Checks

```bash
npm run lint
npm run build
```
