
import json
from service.status_handler import (StatusHanlder, StatusException)
from service.oracle_class import oracle_database
import requests


class DBHandler(object):
    
    def __init__(self, logger):
        self.logger = logger
        
    
    async def query(self, oas_query=None):
        ''' query '''
        if not oas_query:
            oas_query = {}

        self.logger.info('query:oas_query - {}'.format(json.dumps(oas_query, indent=2)))

        if oas_query.get("db_url"):
            database_object = oracle_database(oas_query.get("db_url"))
        try:

            result_json_value = database_object.excute_oracle_query(oas_query.get("sql"))
            print(result_json_value, type(result_json_value))

            return json.loads(str(result_json_value).replace("'",'"'))
    
        except Exception as e:
           return StatusException.raise_exception(str(e))
        
        finally:
            if database_object:
                database_object.set_db_disconnection()
                # database_object.set_init_JVM_shutdown()
        
        
