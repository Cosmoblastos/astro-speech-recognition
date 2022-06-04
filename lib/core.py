import os
import json
from redis import Redis

def read_json(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return json.load(f)


local_path = os.path.dirname(os.path.abspath(__file__))
global_config = read_json(os.path.join(local_path, "../config/global.json"))

env = global_config["env"] or "development"
general_output_lang = global_config["output_lang"] or "es-ES"
general_output_lang = general_output_lang.split("-")[0]
# other frameworks configuration
redis_config = read_json(os.path.join(local_path, "../config/redis.json"))[env]
dialogs = read_json(os.path.join(local_path, "../config/dialogs.json"))[general_output_lang]


redis_db = Redis(
	host=redis_config["host"], \
	port=redis_config["port"], \
	db=redis_config["db"], \
    username=redis_config["username"], \
    password=redis_config["password"]
)