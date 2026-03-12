import os

class Config:
    ALERTMANAGER_URL      = os.getenv("ALERTMANAGER_URL",      "http://10.10.10.41:9093")
    OPENSEARCH_URL        = os.getenv("OPENSEARCH_URL",        "http://10.10.10.45:9200")
    OPENSEARCH_USER       = os.getenv("OPENSEARCH_USER",       "")
    OPENSEARCH_PASS       = os.getenv("OPENSEARCH_PASS",       "")
    OPENSEARCH_INDEX      = os.getenv("OPENSEARCH_INDEX",      "logs-*")
    OPENSEARCH_HOST_FIELD = os.getenv("OPENSEARCH_HOST_FIELD", "host.keyword")
    MAX_LOGS              = int(os.getenv("MAX_LOGS",          "10"))
    JANELA_MINUTOS        = int(os.getenv("JANELA_MINUTOS",    "10"))
    AI_API_URL            = os.getenv("AI_API_URL",            "http://10.10.10.50:5002/analyze")
    AI_TIMEOUT            = int(os.getenv("AI_TIMEOUT",        "15"))
    TELEGRAM_TOKEN        = os.getenv("TELEGRAM_TOKEN",        "")
    TELEGRAM_INFRA_HOT    = os.getenv("TELEGRAM_INFRA_HOT",   "")
    TELEGRAM_INFRA_WARM   = os.getenv("TELEGRAM_INFRA_WARM",  "")
    TELEGRAM_DEV_HOT      = os.getenv("TELEGRAM_DEV_HOT",     "")
    TELEGRAM_DEV_WARM     = os.getenv("TELEGRAM_DEV_WARM",    "")
