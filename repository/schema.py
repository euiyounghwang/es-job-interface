from pydantic import BaseModel
from datetime import datetime
from pytz import timezone as tz
from enum import Enum
from typing import List, Union
import uuid
import sys


class Sort_Order(str, Enum):
    desc = 'DESC'
    asc = 'ASC'
    

    

class DB(BaseModel):
    ''' db_url/sql to get the records and deliver them into export application '''
    db_url: str = "jdbc:oracle:thin:test/test@test:1234/test_db"
    sql: str = "SELECT processname * from test_tb"
            
    def to_json(self):
        return {
            'db_url' : self.db_url,
            'sql' : self.sql
        }
    