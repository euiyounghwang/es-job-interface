
import json
from service.status_handler import (StatusHanlder, StatusException)
from service.oracle_class import oracle_database
import requests


class DBHandler(object):
    
    def __init__(self, logger, sql_repo):
        self.logger = logger
        self.sql_repo = sql_repo
        
    
    async def query(self, oas_query=None):
        ''' query '''
        if not oas_query:
            oas_query = {}

        self.logger.info('query:oas_query - {}'.format(json.dumps(oas_query, indent=2)))

        if oas_query.get("db_url"):
            database_object = oracle_database(self.logger, oas_query.get("db_url"))
        try:

            result_json_value = database_object.excute_oracle_query(oas_query.get("sql"))
            self.logger.info(result_json_value)
            
            return json.loads(str(result_json_value).replace("'",'"'))
    
        except Exception as e:
           return StatusException.raise_exception(str(e))
        
        finally:
            if database_object:
                database_object.set_db_disconnection()
                # database_object.set_init_JVM_shutdown()
        

    ''' Get SRC VIEW from JSON DATA'''
    async def get_master_query(self, oas_query=None):
        ''' query '''
        if not oas_query:
            oas_query = {}

        self.logger.info('query:get_master_query - {}'.format(oas_query))

        if oas_query.get("db_url"):
            database_object = oracle_database(self.logger, oas_query.get("db_url"))
        try:

            ''' master query'''
            if not self.sql_repo.get("json_src_view_sql", ""):
                return {}
            result_json_value = database_object.excute_oracle_query(self.sql_repo.get("json_src_view_sql", ""))
            # print(result_json_value, type(result_json_value))

            return json.loads(str(result_json_value).replace("'",'"'))
            # return result_json_value
    
        except Exception as e:
           return StatusException.raise_exception(str(e))
        
        finally:
            if database_object:
                database_object.set_db_disconnection()


    ''' Get records JSON DATA using mansql sql'''
    async def get_records_sql(self, oas_query=None):
        ''' query '''
        if not oas_query:
            oas_query = {}

        self.logger.info('query:get_master_query - {}'.format(oas_query))

        if oas_query.get("db_url"):
            database_object = oracle_database(self.logger, oas_query.get("db_url"))
        try:

            ''' master query'''
            if not self.sql_repo.get("json_src_view_sql", ""):
                return {}
            result_json_value = database_object.excute_oracle_query(self.sql_repo.get("json_src_view_sql", ""))
            # print(result_json_value, type(result_json_value))

            json_src_raw_data = json.loads(str(result_json_value).replace("'",'"'))

            ''' save to dict for json_src_vw'''
            saved_json_vw_dict = {}
            for row in json_src_raw_data:
                saved_json_vw_dict.update({row.get("PROCESS_NAME") : row.get("JSON_SRC_VW")})
            self.logger.info(f"saved_json_vw_dict - {json.dumps(saved_json_vw_dict, indent=2)}")

            ''' read real sql'''
            repo = database_object.excute_oracle_query_json(oas_query.get("sql", ""))
            
            self.logger.info(json.dumps(repo, indent=2))
            
            return repo
    
        except Exception as e:
           return StatusException.raise_exception(str(e))
        
        finally:
            if database_object:
                database_object.set_db_disconnection()
        
        
