from fastapi import APIRouter
import json
import datetime
from injector import logger, DBHandlerInject
from service.status_handler import (StatusHanlder, StatusException)
from repository.schema import DB
# from typing import Optional


app = APIRouter(
    prefix="/ingestion",
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
        