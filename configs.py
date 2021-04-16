# DB related config
HOST = "localhost"
USER = "root"
PASSWORD = "" # feel your own password
DATABASE = "exchange_api"
TABLE = "index"
SERVER_HOST = "localhost"
SERVER_PORT = 8080

# Exchange weights
# WEIGHT_STRATEGY = "equal"
WEIGHT_STRATEGY = "non_equal" # If not equal weighted, the following weights will be used
WEIGHTS = { "binance":0.2, "huobi":0.3, "ok": 0.5}

