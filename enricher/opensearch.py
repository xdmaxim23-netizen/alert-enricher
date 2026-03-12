import requests
from datetime import datetime, timedelta, timezone
from config import Config

def buscar_logs(host: str, starts_at: str, janela_min: int) -> list[dict]:
    try:
        ts_fim = datetime.fromisoformat(starts_at.replace("Z", "+00:00"))
    except Exception:
        ts_fim = datetime.now(timezone.utc)

    ts_inicio = ts_fim - timedelta(minutes=janela_min)

    query = {
        "size": Config.MAX_LOGS,
        "sort": [{"@timestamp": {"order": "desc"}}],
        "query": {
            "bool": {
                "filter": [
                    {"term":  {Config.OPENSEARCH_HOST_FIELD: host}},
                    {"range": {"@timestamp": {
                        "gte": ts_inicio.isoformat(),
                        "lte": ts_fim.isoformat()
                    }}}
                ]
            }
        },
        "_source": ["@timestamp", "message", "severity", "log.level", "pod", "namespace", "container"]
    }

    auth = (Config.OPENSEARCH_USER, Config.OPENSEARCH_PASS) if Config.OPENSEARCH_USER else None

    try:
        resp = requests.post(
            f"{Config.OPENSEARCH_URL}/{Config.OPENSEARCH_INDEX}/_search",
            json=query,
            auth=auth,
            verify=False,
            timeout=5
        )
        resp.raise_for_status()
        hits = resp.json().get("hits", {}).get("hits", [])
        return [h["_source"] for h in hits]
    except Exception as e:
        print(f"[opensearch] erro ao buscar logs: {e}")
        return []
