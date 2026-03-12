import requests
from config import Config

def reenviar(labels, annotations, starts_at, analise, logs):
    logs_preview = "\n".join(
        f"[{l.get('@timestamp','')[:19]}] {l.get('severity') or l.get('log.level','')} - {l.get('message','')[:100]}"
        for l in logs[:5]
    )

    payload = [{
        "labels": {**labels, "enriched": "true"},
        "annotations": {
            **annotations,
            "summary":      analise.get("summary", ""),
            "root_cause":   analise.get("root_cause", ""),
            "suggestion":   analise.get("suggestion", ""),
            "logs_preview": logs_preview
        },
        "startsAt": starts_at
    }]

    try:
        resp = requests.post(
            f"{Config.ALERTMANAGER_URL}/api/v2/alerts",
            json=payload,
            timeout=5
        )
        print(f"[alertmanager] reenvio status: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"[alertmanager] erro ao reenviar: {e}")
