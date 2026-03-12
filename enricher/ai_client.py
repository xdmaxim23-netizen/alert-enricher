import requests
from config import Config

def interpretar(alert: dict, logs: list[dict], window_minutes: int) -> dict:
    payload = {
        "alert":          alert,
        "logs":           logs,
        "window_minutes": window_minutes
    }
    try:
        resp = requests.post(Config.AI_API_URL, json=payload, timeout=Config.AI_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ai_client] erro: {e}")
        return {
            "summary":    alert.get("description", "Sem resumo"),
            "root_cause": "IA indisponível no momento",
            "suggestion": "Verificar manualmente"
        }
