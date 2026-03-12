# Alert Enricher

AI-powered alert enrichment service that correlates Alertmanager webhooks with OpenSearch logs and sends intelligent root cause analysis to Telegram.

## Architecture

```
                          +------------------+
  Alertmanager            |                  |          Telegram
  webhook POST  --------> |  Alert Enricher  | -------> 4 channels
                          |   (Flask 5001)   |          (infra/dev x hot/warm)
                          +--------+---------+
                                   |
                          +--------+---------+
                          |                  |
                   +------+------+    +------+------+
                   |  OpenSearch |    |   AI API    |
                   |  (log query)|    |  (analysis) |
                   +-------------+    +-------------+
```

### Flow

1. **Receive** — Alertmanager fires a webhook to `/webhook`
2. **Correlate** — Queries OpenSearch for logs from the same host within a configurable time window (default 10 min)
3. **Analyze** — Sends alert metadata + correlated logs to an AI API for root cause analysis
4. **Route** — Sends enriched message to the correct Telegram channel(s) based on alert classification
5. **Re-inject** — Posts the enriched alert back to Alertmanager with `enriched=true` label and AI annotations

## Alert Routing

Alerts are routed to **Infra**, **Dev**, or **both** teams, and within each team to a **Hot** (critical) or **Warm** (warning) channel.

### Routing Rules

| Condition | Destination |
|-----------|-------------|
| `source=zabbix` (any alert) | Infra only |
| Alert in `AMBOS` set | Infra + Dev |
| Alert in `ONLY_INFRA` set | Infra only |
| Everything else | Dev only |

### Severity Channels

| Severity | Channel |
|----------|---------|
| `critical` | **Hot** (immediate attention) |
| `warning` / other | **Warm** (informational) |

This gives 4 Telegram channels total:

- `TELEGRAM_INFRA_HOT` — Critical infra alerts (Zabbix, hardware, kernel, disk)
- `TELEGRAM_INFRA_WARM` — Warning-level infra alerts
- `TELEGRAM_DEV_HOT` — Critical dev alerts (pods, apps, databases)
- `TELEGRAM_DEV_WARM` — Warning-level dev alerts

### Alert Classification

**AMBOS (Infra + Dev):** NodeNotReady, ProxyDown, DatabaseDown, DatabaseSlow, GTMDown, PreviewDown, CVRDown, OOMKiller, ConnectionRefused, DNSProblem, NetworkInterfaceFlapping, TCPRetransmitHigh, NetworkPacketLoss, EtcdProblem, EtcdHighLatency, HighLoadAverage, ImagePullLatency, CertificateExpiring, HighNodeUptime

**ONLY_INFRA:** ZombieProcesses, ReadOnlyFilesystem, DiskIOSaturation, FilesystemCorruptionProblem, IOErrors, DiskWriteLatency, DiskSmartHealth, NVMeHealth, RAIDDegraded, MemoryPressureHigh, ConntrackTableFull, ConntrackInsertFailed, HighMemoryUsage, ARPTableFull, FileDescriptorExhaustion, TCPTimeWaitExhaustion, SwapUsage, HardwareErrors, PowerSupplyProblem, FanFailure, KernelModuleLoadingProblems, KernelPanic, Segfault

**DEV (default):** Everything else — PodCrashLooping, HPAAtMaxReplicas, AppErrorRecorrente, KubeletProblem, etc.

## Example Telegram Message

```
🔴 [ZABBIX] INFRA HOT
━━━━━━━━━━━━━━━━━━━━━━
Alerta: HighCPU
Host: lab-mon01
Detalhe: CPU acima de 90% por mais de 5 minutos
━━━━━━━━━━━━━━━━━━━━━━
📌 Resumo: CPU sustentada acima do threshold
🔍 Causa raiz: Processo consumindo recursos excessivos
✅ Sugestao:
1. top -c para identificar processo
2. Verificar cron jobs
3. Escalar se persistir
━━━━━━━━━━━━━━━━━━━━━━
📋 Logs correlacionados:
[2026-03-11 14:30:05] WARN - High CPU detected on pid 1234
[2026-03-11 14:29:58] ERROR - OOM pressure increasing
```

### Source Icons

| Source | Icon |
|--------|------|
| Zabbix | 🔴 |
| Prometheus | 🟠 |
| OpenSearch | ⚪ |
| NPD (Node Problem Detector) | 🔵 |

## Setup

### Prerequisites

- Docker and Docker Compose
- Alertmanager configured to send webhooks
- OpenSearch with log data
- Telegram bot token + 4 channel/group chat IDs

### Quick Start

```bash
# Clone
git clone https://github.com/Vinicius-Costa14/alert-enricher.git
cd alert-enricher

# Configure
cp .env.example .env
# Edit .env with your values

# Run
docker compose up -d

# Configure Alertmanager webhook receiver pointing to:
# http://<enricher-host>:5001/webhook
```

### Testing with Mock AI

The included `mock-ai` service provides predefined responses for common alerts, so you can test the full pipeline without a real AI backend:

```bash
docker compose up -d

# Send a test alert
curl -X POST http://localhost:5001/webhook \
  -H "Content-Type: application/json" \
  -d '{"alerts":[{"labels":{"alertname":"PodCrashLooping","severity":"critical","source":"prometheus","host":"web01","cluster":"prod","az":"us-east-1"},"annotations":{"description":"Pod reiniciando mais de 5 vezes em 10 minutos"}}]}'
```

A full integration test script is included:

```bash
./teste-completo.sh
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ALERTMANAGER_URL` | Alertmanager API endpoint | `http://10.10.10.41:9093` |
| `OPENSEARCH_URL` | OpenSearch endpoint | `http://10.10.10.45:9200` |
| `OPENSEARCH_USER` | OpenSearch username (optional) | — |
| `OPENSEARCH_PASS` | OpenSearch password (optional) | — |
| `OPENSEARCH_INDEX` | Index pattern for log queries | `logs-*` |
| `OPENSEARCH_HOST_FIELD` | Field name for host matching | `host.keyword` |
| `MAX_LOGS` | Max log entries to fetch per alert | `10` |
| `JANELA_MINUTOS` | Time window (minutes) for log correlation | `10` |
| `AI_API_URL` | AI analysis API endpoint | `http://10.10.10.50:5002/analyze` |
| `AI_TIMEOUT` | AI API timeout in seconds | `15` |
| `TELEGRAM_TOKEN` | Telegram Bot API token | — |
| `TELEGRAM_INFRA_HOT` | Chat ID for critical infra alerts | — |
| `TELEGRAM_INFRA_WARM` | Chat ID for warning infra alerts | — |
| `TELEGRAM_DEV_HOT` | Chat ID for critical dev alerts | — |
| `TELEGRAM_DEV_WARM` | Chat ID for warning dev alerts | — |

## Project Structure

```
alert-enricher/
├── docker-compose.yml
├── .env.example
├── enricher/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py              # Webhook endpoint + routing logic
│   ├── config.py            # Environment-based configuration
│   ├── opensearch.py        # Log correlation queries
│   ├── ai_client.py         # AI API client
│   ├── alertmanager.py      # Re-inject enriched alerts
│   └── notifier.py          # Telegram message formatting + delivery
├── mock-ai/
│   ├── Dockerfile
│   └── app.py               # Predefined responses for testing
└── teste-completo.sh        # Integration test script
```

## License

MIT
