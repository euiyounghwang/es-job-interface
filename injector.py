from config.log_config import create_log
from dotenv import load_dotenv
# import yaml
import json
import os
from service.db_service import DBHandler

load_dotenv()
    
# Initialize & Inject with only one instance
logger = create_log()


def read_config_json(path):
    with open(path, "r") as read_file:
        data = json.load(read_file)
        return data

sql_repo = read_config_json("./repository/config.json")

DBHandlerInject = DBHandler(logger, sql_repo)