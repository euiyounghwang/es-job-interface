from fastapi import APIRouter
import json
import datetime
from injector import logger, DBHandlerInject
from service.status_handler import (StatusHanlder, StatusException)
from repository.schema import DB
# from typing import Optional


app = APIRouter(
    prefix="/db",
)


'''
@app.get("/query", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:8001/cluster/health?es_url=http://localhost:9200", 
          summary="DB Query")
async def get_db_query(es_url="http://localhost:9200"):
    # logger.info(es_url)
    # response =  SearchAPIHandlerInject.get_es_health(es_url)
    # if isinstance(response, dict):
    #     logger.info('SearchOmniHandler:get_es_info - {}'.format(json.dumps(response, indent=2)))

    return {}
'''

@app.post("/get_db_query", description="db_query_execute", summary="db_query_execute")
async def get_db_query(request: DB):
    ''' Search to DB with SQL '''
    '''
    return :
    {
        "running_time": 0.49,
        "request_dbid": "test_db",
        "results": [
            {
            "PROCESSNAME": "test",
            "STATUS": "C",
            "ADDTS": "2024-05-24 17:37:01",
            "COUNT(*)": 1,
            "DBID": "test_db"
            }
        ]
    }
    '''
    StartTime, EndTime, Delay_Time = 0, 0, 0
    
    try:
        StartTime = datetime.datetime.now()
        
        # logger.info("api_controller doc: {}".format(json.dumps(doc, indent=2)))
        # request_json = {k : v for k, v in request}
        request_json = request.to_json()
        logger.info("get_db_query : {}".format(json.dumps(request_json, indent=2)))
        response_json = await DBHandlerInject.query(request_json)
        
        EndTime = datetime.datetime.now()
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]

        logger.info('Metrics : {}'.format(Delay_Time))

        #-- target DB
        db_id_list = str(request_json.get("db_url")).split("/")
        db_id = db_id_list[len(db_id_list)-1]
        
        return {"running_time" : float(Delay_Time), "request_dbid" : db_id, "results" : response_json}
       
    except Exception as e:
        logger.error(e)
        return StatusException.raise_exception(e)
    
        