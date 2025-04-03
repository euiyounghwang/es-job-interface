from fastapi import APIRouter
import json
import datetime
from injector import logger, DBHandlerInject
from service.status_handler import (StatusHanlder, StatusException)
from repository.schema import DB, DB_Ingestion, DB_Ingestion_JSON_VW
# from typing import Optiona


app = APIRouter(
    prefix="/ingestion",
)



@app.post("/get_json_view", status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="get_json_view", summary="get JSON_VW name for ingestion")
async def get_json_view(request: DB_Ingestion_JSON_VW):
    ''' Search to DB with SQL '''
    '''
    return :
    [
        {
            "PROCESS_NAME": "SRC",
            "JSON_SRC_VW": "TEST_SRC_JSON_VW"
        },
        ..
    ]
    '''
    StartTime, EndTime, Delay_Time = 0, 0, 0
    
    try:
        StartTime = datetime.datetime.now()
        
        # logger.info("api_controller doc: {}".format(json.dumps(doc, indent=2)))
        # request_json = {k : v for k, v in request}
        request_json = request.to_json()
        logger.info("get_json_view : {}".format(json.dumps(request_json, indent=2)))
        
        response_json = await DBHandlerInject.get_master_query(request_json)
                
        EndTime = datetime.datetime.now()
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]

        logger.info('Metrics : {}'.format(Delay_Time))

        #-- target DB
        db_id_list = str(request_json.get("db_url")).split("/")
        db_id = db_id_list[len(db_id_list)-1]
        
        return {"running_time" : float(Delay_Time), "request_dbid" : db_id, "total" : len(response_json), "results" : response_json}
        # return response_json
       
    except Exception as e:
        logger.error(e)
        return StatusException.raise_exception(e)
        



@app.post("/get_records_sql", status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="get_records_sql", summary="get records between queue/json_vw tables for ingestion using manual SQL")
async def get_records(request: DB_Ingestion):
    ''' Search to DB with SQL '''
    '''
    return :
    [
        {
            "PROCESS_NAME": "SRC",
            "JSON_SRC_VW": "TEST_SRC_JSON_VW"
        },
        ..
    ]
    '''
    StartTime, EndTime, Delay_Time = 0, 0, 0
    
    try:
        StartTime = datetime.datetime.now()
        
        # logger.info("api_controller doc: {}".format(json.dumps(doc, indent=2)))
        # request_json = {k : v for k, v in request}
        request_json = request.to_json()
        logger.info("get_records : {}".format(json.dumps(request_json, indent=2)))
        
        response_json = await DBHandlerInject.get_records_sql(request_json)
                
        EndTime = datetime.datetime.now()
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]

        logger.info('Metrics : {}'.format(Delay_Time))

        #-- target DB
        db_id_list = str(request_json.get("db_url")).split("/")
        db_id = db_id_list[len(db_id_list)-1]
        
        return {"running_time" : float(Delay_Time), "request_dbid" : db_id, "total" : len(response_json), "results" : response_json}
        # return response_json
       
    except Exception as e:
        logger.error(e)
        return StatusException.raise_exception(e)
        