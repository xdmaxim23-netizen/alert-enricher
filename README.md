# Alert Enricher

Servico de enriquecimento de alertas com IA que correlaciona webhooks do Alertmanager com logs do OpenSearch e envia analise inteligente de causa raiz para o Telegram.

## Arquitetura

```
                          +------------------+
  Alertmanager            |                  |          Telegram
  webhook POST  --------> |  Alert Enricher  | -------> 4 canais
                          |   (Flask 5001)   |          (infra/dev x hot/warm)
                          +--------+---------+
                                   |
                          +--------+---------+
                          |                  |
                   +------+------+    +------+------+
                   |  OpenSearch |    |   AI API    |
                   | (consulta   |    |  (analise)  |
                   |   de logs)  |    |             |
                   +-------------+    +-------------+
```

### Fluxo

1. **Receber** — Alertmanager dispara um webhook para `/webhook`
2. **Correlacionar** — Consulta o OpenSearch por logs do mesmo host dentro de uma janela de tempo configuravel (padrao 10 min)
3. **Analisar** — Envia metadados do alerta + logs correlacionados para uma API de IA para analise de causa raiz
4. **Rotear** — Envia mensagem enriquecida para o(s) canal(is) correto(s) do Telegram baseado na classificacao do alerta
5. **Reinjetar** — Posta o alerta enriquecido de volta no Alertmanager com label `enriched=true` e anotacoes da IA

## Roteamento de Alertas

Alertas sao roteados para equipes de **Infra**, **Dev** ou **ambas**, e dentro de cada equipe para um canal **Hot** (critico) ou **Warm** (aviso).

### Regras de Roteamento

| Condicao | Destino |
|----------|---------|
| `source=zabbix` (qualquer alerta) | Apenas Infra |
| Alerta no conjunto `AMBOS` | Infra + Dev |
| Alerta no conjunto `ONLY_INFRA` | Apenas Infra |
| Todo o resto | Apenas Dev |

### Canais por Severidade

| Severidade | Canal |
|------------|-------|
| `critical` | **Hot** (atencao imediata) |
| `warning` / outro | **Warm** (informacional) |

Isso resulta em 4 canais Telegram no total:

- `TELEGRAM_INFRA_HOT` — Alertas criticos de infra (Zabbix, hardware, kernel, disco)
- `TELEGRAM_INFRA_WARM` — Alertas de aviso de infra
- `TELEGRAM_DEV_HOT` — Alertas criticos de dev (pods, apps, bancos de dados)
- `TELEGRAM_DEV_WARM` — Alertas de aviso de dev

### Classificacao de Alertas

**AMBOS (Infra + Dev):** NodeNotReady, ProxyDown, DatabaseDown, DatabaseSlow, GTMDown, PreviewDown, CVRDown, OOMKiller, ConnectionRefused, DNSProblem, NetworkInterfaceFlapping, TCPRetransmitHigh, NetworkPacketLoss, EtcdProblem, EtcdHighLatency, HighLoadAverage, ImagePullLatency, CertificateExpiring, HighNodeUptime

**ONLY_INFRA:** ZombieProcesses, ReadOnlyFilesystem, DiskIOSaturation, FilesystemCorruptionProblem, IOErrors, DiskWriteLatency, DiskSmartHealth, NVMeHealth, RAIDDegraded, MemoryPressureHigh, ConntrackTableFull, ConntrackInsertFailed, HighMemoryUsage, ARPTableFull, FileDescriptorExhaustion, TCPTimeWaitExhaustion, SwapUsage, HardwareErrors, PowerSupplyProblem, FanFailure, KernelModuleLoadingProblems, KernelPanic, Segfault

**DEV (padrao):** Todo o resto — PodCrashLooping, HPAAtMaxReplicas, AppErrorRecorrente, KubeletProblem, etc.

## Exemplo de Mensagem no Telegram

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

### Icones por Origem

| Origem | Icone |
|--------|-------|
| Zabbix | 🔴 |
| Prometheus | 🟠 |
| OpenSearch | ⚪ |
| NPD (Node Problem Detector) | 🔵 |

## Configuracao

### Pre-requisitos

- Docker e Docker Compose
- Alertmanager configurado para enviar webhooks
- OpenSearch com dados de logs
- Token de bot Telegram + 4 IDs de chat/grupo

### Como Usar

```bash
# Clonar
git clone https://github.com/Vinicius-Costa14/alert-enricher.git
cd alert-enricher

# Configurar
cp .env.example .env
# Edite o .env com seus valores

# Rodar
docker compose up -d

# Configure o receiver de webhook do Alertmanager apontando para:
# http://<enricher-host>:5001/webhook
```

### Testando com Mock AI

O servico `mock-ai` incluso fornece respostas predefinidas para alertas comuns, permitindo testar o pipeline completo sem um backend de IA real:

```bash
docker compose up -d

# Enviar um alerta de teste
curl -X POST http://localhost:5001/webhook \
  -H "Content-Type: application/json" \
  -d '{"alerts":[{"labels":{"alertname":"PodCrashLooping","severity":"critical","source":"prometheus","host":"web01","cluster":"prod","az":"us-east-1"},"annotations":{"description":"Pod reiniciando mais de 5 vezes em 10 minutos"}}]}'
```

Um script de teste de integracao completo esta incluso:

```bash
./teste-completo.sh
```

## Variaveis de Ambiente

| Variavel | Descricao | Padrao |
|----------|-----------|--------|
| `ALERTMANAGER_URL` | Endpoint da API do Alertmanager | `http://10.10.10.41:9093` |
| `OPENSEARCH_URL` | Endpoint do OpenSearch | `http://10.10.10.45:9200` |
| `OPENSEARCH_USER` | Usuario do OpenSearch (opcional) | — |
| `OPENSEARCH_PASS` | Senha do OpenSearch (opcional) | — |
| `OPENSEARCH_INDEX` | Padrao de indice para consultas de logs | `logs-*` |
| `OPENSEARCH_HOST_FIELD` | Nome do campo para matching de host | `host.keyword` |
| `MAX_LOGS` | Maximo de entradas de log por alerta | `10` |
| `JANELA_MINUTOS` | Janela de tempo (minutos) para correlacao de logs | `10` |
| `AI_API_URL` | Endpoint da API de analise com IA | `http://10.10.10.50:5002/analyze` |
| `AI_TIMEOUT` | Timeout da API de IA em segundos | `15` |
| `TELEGRAM_TOKEN` | Token da API do Telegram Bot | — |
| `TELEGRAM_INFRA_HOT` | Chat ID para alertas criticos de infra | — |
| `TELEGRAM_INFRA_WARM` | Chat ID para alertas de aviso de infra | — |
| `TELEGRAM_DEV_HOT` | Chat ID para alertas criticos de dev | — |
| `TELEGRAM_DEV_WARM` | Chat ID para alertas de aviso de dev | — |

## Estrutura do Projeto

```
alert-enricher/
├── docker-compose.yml
├── .env.example
├── enricher/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py              # Endpoint de webhook + logica de roteamento
│   ├── config.py            # Configuracao baseada em variaveis de ambiente
│   ├── opensearch.py        # Consultas de correlacao de logs
│   ├── ai_client.py         # Cliente da API de IA
│   ├── alertmanager.py      # Reinjecao de alertas enriquecidos
│   └── notifier.py          # Formatacao e envio de mensagens Telegram
├── mock-ai/
│   ├── Dockerfile
│   └── app.py               # Respostas predefinidas para testes
└── teste-completo.sh        # Script de teste de integracao
```

## Licenca

MIT
