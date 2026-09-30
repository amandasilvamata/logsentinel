from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.parser import parse_lines
from backend.detector import (
    detect_brute_force,
    detect_root_attacks,
    detect_success_after_failures
)


app = FastAPI()

# Permite que o front-end acesse esta API durante o desenvolvimento.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "name": "LogSentinel API",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/analyze")
async def analyze_log(file: UploadFile):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was provided."
        )

    if not file.filename.endswith((".log", ".txt")):
        raise HTTPException(
            status_code=400,
            detail="Only .log and .txt files are allowed."
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    try:
        text = contents.decode("utf-8")

    except UnicodeDecodeError:
        # Se o arquivo não puder ser interpretado como UTF-8,
        # devolvemos um erro em vez de deixar a API quebrar.
        raise HTTPException(
            status_code=400,
            detail="The file must contain UTF-8 text."
        )

    lines = text.splitlines()

    events = parse_lines(lines)

    brute_force_alerts = detect_brute_force(events)
    root_alerts = detect_root_attacks(events)
    success_alerts = detect_success_after_failures(events)

    alerts = (
        brute_force_alerts
        + root_alerts
        + success_alerts
    )
    
    severity_summary = {
        "medium": 0,
        "high": 0,
        "critical": 0
    }

    for alert in alerts:
        severity = alert["severity"]

        if severity in severity_summary:
            severity_summary[severity] += 1


    return {
        "file": {
            "name": file.filename,
            "events_found": len(events)
        },
        "summary": {
            "alerts_found": len(alerts),
            "severity": severity_summary
        },
        "alerts": alerts
    }