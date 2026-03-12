#!/bin/bash
AM="http://10.10.10.41:9093/api/v2/alerts"
H='Content-Type: application/json'

send() {
  curl -s -X POST "$AM" -H "$H" -d "$1" > /dev/null
  echo "  enviado"
  sleep 3
}

echo "=== [1/4] INFRA SOUREI - HOT ==="
echo "-> Zabbix: HighCPU"
send '[{"labels":{"alertname":"HighCPU","severity":"critical","source":"zabbix","host":"lab-mon01"},"annotations":{"description":"CPU acima de 90% por mais de 5 minutos"}}]'
echo "-> Zabbix: HostUnreachable"
send '[{"labels":{"alertname":"HostUnreachable","severity":"critical","source":"zabbix","host":"lab-bkp01"},"annotations":{"description":"Host nao responde ao agente Zabbix"}}]'
echo "-> NPD: DiskIOSaturation"
send '[{"labels":{"alertname":"DiskIOSaturation","severity":"critical","source":"npd","host":"lab-web01","cluster":"n8n","az":"SP"},"annotations":{"description":"I/O do disco saturado, iowait acima de 30%"}}]'
echo "-> NPD: MemoryPressureHigh"
send '[{"labels":{"alertname":"MemoryPressureHigh","severity":"critical","source":"npd","host":"lab-db01","cluster":"n8n","az":"SP"},"annotations":{"description":"Memoria disponivel abaixo de 100MB"}}]'

echo "=== [2/4] DEV SOUREI - HOT ==="
echo "-> Prometheus: PodCrashLooping"
send '[{"labels":{"alertname":"PodCrashLooping","severity":"critical","source":"prometheus","host":"lab-k3s","cluster":"n8n","az":"SP"},"annotations":{"description":"Pod reiniciando mais de 5 vezes em 10 minutos"}}]'
echo "-> Prometheus: DatabaseDown"
send '[{"labels":{"alertname":"DatabaseDown","severity":"critical","source":"prometheus","host":"lab-db01","cluster":"n8n","az":"SP"},"annotations":{"description":"Database nao responde ha 2 minutos"}}]'
echo "-> OpenSearch: AppErrorRecorrente"
send '[{"labels":{"alertname":"AppErrorRecorrente","severity":"critical","source":"opensearch","host":"lab-web01","cluster":"n8n","az":"SP"},"annotations":{"description":"Mais de 50 erros ERROR/FATAL nos ultimos 5 minutos"}}]'
echo "-> NPD: KubeletProblem"
send '[{"labels":{"alertname":"KubeletProblem","severity":"critical","source":"npd","host":"lab-k3s","cluster":"n8n","az":"SP"},"annotations":{"description":"Kubelet nao esta respondendo"}}]'

echo "=== [3/4] AMBOS — INFRA + DEV HOT ==="
echo "-> Prometheus: NodeNotReady"
send '[{"labels":{"alertname":"NodeNotReady","severity":"critical","source":"prometheus","host":"lab-k3s","cluster":"n8n","az":"SP"},"annotations":{"description":"Node saiu do estado Ready"}}]'
echo "-> NPD: EtcdProblem"
send '[{"labels":{"alertname":"EtcdProblem","severity":"critical","source":"npd","host":"lab-k3s","cluster":"n8n","az":"SP"},"annotations":{"description":"Etcd nao esta respondendo"}}]'
echo "-> NPD: DNSProblem"
send '[{"labels":{"alertname":"DNSProblem","severity":"critical","source":"npd","host":"lab-k3s","cluster":"n8n","az":"SP"},"annotations":{"description":"Resolucao DNS falhando no node"}}]'
echo "-> Prometheus: ProxyDown"
send '[{"labels":{"alertname":"ProxyDown","severity":"critical","source":"prometheus","host":"lab-web01","cluster":"n8n","az":"SP"},"annotations":{"description":"Proxy nao responde ao health check"}}]'

echo "=== [4/4] WARM ==="
echo "-> Zabbix: DiskWarning (INFRA WARM)"
send '[{"labels":{"alertname":"DiskWarning","severity":"warning","source":"zabbix","host":"lab-mon01"},"annotations":{"description":"Uso de disco acima de 75%"}}]'
echo "-> Prometheus: HPAAtMaxReplicas (DEV WARM)"
send '[{"labels":{"alertname":"HPAAtMaxReplicas","severity":"warning","source":"prometheus","host":"lab-k3s","cluster":"n8n","az":"SP"},"annotations":{"description":"HPA atingiu o limite maximo de replicas"}}]'
echo "-> NPD: NTPDrift (DEV WARM)"
send '[{"labels":{"alertname":"NTPDrift","severity":"warning","source":"npd","host":"lab-mon01","cluster":"n8n","az":"SP"},"annotations":{"description":"Drift de NTP acima de 500ms"}}]'

echo "=== Todos enviados — aguarda 30s e verifica os 4 grupos ==="
