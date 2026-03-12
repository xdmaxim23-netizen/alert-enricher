from flask import Flask, request, jsonify

app = Flask(__name__)

SUGESTOES = {
    "KubeletProblem": {"summary": "Kubelet parou de responder", "root_cause": "Provavel falha no containerd ou esgotamento de recursos do node", "suggestion": "1. systemctl status kubelet\n2. systemctl restart kubelet\n3. journalctl -u kubelet -n 50"},
    "NodeNotReady": {"summary": "Node K8s fora do estado Ready", "root_cause": "Kubelet ou rede do node com problema", "suggestion": "1. kubectl describe node\n2. Verificar kubelet e containerd\n3. Checar conectividade com API server"},
    "PodCrashLooping": {"summary": "Pod reiniciando em loop", "root_cause": "Erro na aplicacao, falta de recursos ou misconfiguration", "suggestion": "1. kubectl logs <pod> --previous\n2. kubectl describe pod <pod>\n3. Verificar limites de memoria/CPU"},
    "DatabaseDown": {"summary": "Database nao esta respondendo", "root_cause": "Servico parado, conexoes esgotadas ou disco cheio", "suggestion": "1. Verificar status do container\n2. Checar logs do banco\n3. Verificar espaco em disco"},
    "OOMKilling": {"summary": "Processo morto por OOM killer", "root_cause": "Memoria disponivel abaixo do threshold de eviction", "suggestion": "1. free -h\n2. kubectl top nodes\n3. Verificar limits nos pods"},
    "DiskIOSaturation": {"summary": "Disco com I/O saturado", "root_cause": "iowait acima de 30%", "suggestion": "1. iostat -x 1 5\n2. iotop\n3. Identificar processo com maior I/O"},
}

DEFAULT = {"summary": "Alerta detectado pelo sistema de monitoramento", "root_cause": "Analise baseada nos logs coletados", "suggestion": "1. Verificar logs do host\n2. Checar status dos servicos\n3. Escalar se persistir"}

@app.route("/analyze", methods=["POST"])
def analyze():
    body = request.get_json()
    alertname = body.get("alert", {}).get("alertname", "")
    logs = body.get("logs", [])
    resposta = SUGESTOES.get(alertname, DEFAULT).copy()
    if logs:
        msgs = [l.get("message", "") for l in logs[:3] if l.get("message")]
        if msgs:
            resposta["root_cause"] += "\n\nLogs relevantes:\n" + "\n".join(f"-> {m[:100]}" for m in msgs)
    return jsonify(resposta), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "mode": "mock"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
