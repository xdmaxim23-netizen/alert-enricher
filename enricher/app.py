from flask import Flask, request, jsonify
from opensearch import buscar_logs
from ai_client import interpretar
from alertmanager import reenviar
from notifier import enviar
from config import Config

app = Flask(__name__)

AMBOS = {"NodeNotReady","ProxyDown","DatabaseDown","DatabaseSlow","GTMDown","PreviewDown","CVRDown","OOMKiller","ConnectionRefused","DNSProblem","NetworkInterfaceFlapping","TCPRetransmitHigh","NetworkPacketLoss","EtcdProblem","EtcdHighLatency","HighLoadAverage","ImagePullLatency","CertificateExpiring","HighNodeUptime"}
ONLY_INFRA = {"ZombieProcesses","ReadOnlyFilesystem","DiskIOSaturation","FilesystemCorruptionProblem","IOErrors","DiskWriteLatency","DiskSmartHealth","NVMeHealth","RAIDDegraded","MemoryPressureHigh","ConntrackTableFull","ConntrackInsertFailed","HighMemoryUsage","ARPTableFull","FileDescriptorExhaustion","TCPTimeWaitExhaustion","SwapUsage","HardwareErrors","PowerSupplyProblem","FanFailure","KernelModuleLoadingProblems","KernelPanic","Segfault"}

def grupos_para(alertname, source):
    if source == "zabbix":
        return ["infra"]
    if alertname in AMBOS:
        return ["infra", "dev"]
    if alertname in ONLY_INFRA:
        return ["infra"]
    return ["dev"]

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json()
    for alert in payload.get("alerts", []):
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})
        starts_at = alert.get("startsAt", "")
        alertname = labels.get("alertname", "")
        severity = labels.get("severity", "")
        source = labels.get("source", "")
        host = labels.get("host", "")
        cluster = labels.get("cluster", "")
        az = labels.get("az", "")
        descricao = annotations.get("description", "")
        logs = buscar_logs(host=host, starts_at=starts_at, janela_min=Config.JANELA_MINUTOS)
        analise = interpretar(alert={"alertname": alertname, "severity": severity, "source": source, "host": host, "cluster": cluster, "az": az, "description": descricao}, logs=logs, window_minutes=Config.JANELA_MINUTOS)
        for grupo in grupos_para(alertname, source):
            enviar(grupo=grupo, alertname=alertname, severity=severity, source=source, host=host, cluster=cluster, az=az, descricao=descricao, analise=analise, logs=logs)
        reenviar(labels=labels, annotations=annotations, starts_at=starts_at, analise=analise, logs=logs)
    return jsonify({"status": "ok"}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
