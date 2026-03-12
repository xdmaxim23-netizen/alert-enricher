import requests
from config import Config

ICONE = {"zabbix": "🔴", "prometheus": "🟠", "opensearch": "⚪", "npd": "🔵"}

def _chat_id(grupo, severity):
    if grupo == "infra":
        return Config.TELEGRAM_INFRA_HOT if severity == "critical" else Config.TELEGRAM_INFRA_WARM
    return Config.TELEGRAM_DEV_HOT if severity == "critical" else Config.TELEGRAM_DEV_WARM

def _fila(severity):
    return "HOT" if severity == "critical" else "WARM"

def _logs_fmt(logs):
    if not logs:
        return "Nenhum log encontrado na janela de tempo."
    linhas = []
    for log in logs:
        ts = log.get("@timestamp", "")[:19].replace("T", " ")
        sev = log.get("severity") or log.get("log.level", "")
        msg = log.get("message", "")[:120]
        linhas.append(f"[{ts}] {sev} - {msg}")
    return "\n".join(linhas)

def enviar(grupo, alertname, severity, source, host, cluster, az, descricao, analise, logs):
    icone = ICONE.get(source, "⚪")
    fila = _fila(severity)
    chat_id = _chat_id(grupo, severity)
    logs_txt = _logs_fmt(logs)
    cluster_info = f" | <b>Cluster:</b> {cluster} — AZ:{az}" if cluster else ""

    msg = (
        f"{icone} <b>[{source.upper()}] {grupo.upper()} {fila}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>Alerta:</b> {alertname}\n"
        f"<b>Host:</b> {host}{cluster_info}\n"
        f"<b>Detalhe:</b> {descricao}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 <b>Resumo:</b> {analise.get('summary', '')}\n"
        f"🔍 <b>Causa raiz:</b> {analise.get('root_cause', '')}\n"
        f"✅ <b>Sugestao:</b>\n{analise.get('suggestion', '')}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 <b>Logs correlacionados:</b>\n"
        f"<pre>{logs_txt}</pre>"
    )

    try:
        requests.post(
            f"https://api.telegram.org/bot{Config.TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"},
            timeout=10
        )
    except Exception as e:
        print(f"[notifier] erro telegram {grupo}: {e}")
