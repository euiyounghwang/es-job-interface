
import jaydebeapi
import jpype
import datetime
import sys
import os
import json


class oracle_database:

    def __init__(self, logger, db_url) -> None:
        self.db_url = db_url
        self.logger = logger
        self.set_db_connection()
        

    def set_init_JVM(self):
        '''
        Init JPYPE StartJVM
        '''

        if jpype.isJVMStarted():
            return
        
        jar = r'./ojdbc8.jar'
        args = '-Djava.class.path=%s' % jar

        print('Python Version : ', sys.version)
        # print('JAVA_HOME : ', os.environ["JAVA_HOME"])
        print('Jpype Default JVM Path : ', jpype.getDefaultJVMPath())

        # jpype.startJVM("-Djava.class.path={}".format(JDBC_Driver))
        jpype.startJVM(jpype.getDefaultJVMPath(), args, '-Xrs')


    def set_init_JVM_shutdown(self):
        jpype.shutdownJVM() 
   

    def set_db_connection(self):
        ''' DB Connect '''
        self.logger.info(f"connect-str : {self.db_url}")
        
        StartTime = datetime.datetime.now()

        # -- Init JVM
        self.set_init_JVM()
        # --
        
        # - DB Connection
        self.db_conn = jaydebeapi.connect("oracle.jdbc.driver.OracleDriver", self.db_url)
        # --
        EndTime = datetime.datetime.now()
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]
        print("# DB Connection Running Time - {}".format(str(Delay_Time)))

    
    def set_db_disconnection(self):
        ''' DB Disconnect '''
        self.db_conn.close()
        print("Disconnected to Oracle database successfully!") 

    
    def get_db_connection(self):
        return self.db_conn
    

    ''' export list with dict based on str type'''
    def excute_oracle_query(self, sql):
        '''
        DB Oracle : Excute Query
        '''
        try:
            self.logger.info(f"excute_oracle_query : {sql}")
            # Creating a cursor object
            cursor = self.get_db_connection().cursor()

            # Executing a query
            cursor.execute(sql)
            
            # Fetching the results
            results = cursor.fetchall()
            cols = list(zip(*cursor.description))[0]
            # print(type(results), cols)

            json_rows_list = []
            for row in results:
                # print(type(row), row)
                json_rows_dict = {}
                for i, row in enumerate(list(row)):
                    json_rows_dict.update({cols[i] : row})
                json_rows_list.append(json_rows_dict)

            cursor.close()

            # logging.info(json_rows_list)
            
            return json_rows_list
        
        except Exception as e:
            self.logger.error(e)
    

    def excute_oracle_query_json(self, sql):
        '''
        DB Oracle : Excute Query
        '''
        try:
            self.logger.info(f"excute_oracle_query_json -> {sql}")
            # Creating a cursor object
            cursor = self.get_db_connection().cursor()

            # Executing a query
            cursor.execute(sql)
            
            # Fetching the results
            results = cursor.fetchall()
            cols = list(zip(*cursor.description))[0]
            # print(type(results), cols)

            json_rows_list = []
            for rows in results:
                # print(type(row), row)
                json_rows_dict = {}
                for i, row in enumerate(list(rows)):
                    if cols[i] == 'JSON_OBJECT':
                        each_json = str(row).replace("\"{", "'{").replace("\"}", "'}").replace("\"", '"').replace("'",'"')
                        # print(f"each-json : {each_json}, json : {json.loads(each_json)}")
                        '''print(f"json : {each_json}, type : {type(each_json)}")'''
                        json_rows_dict.update({str(cols[i]) : json.loads(each_json)})
                    else:
                        json_rows_dict.update({str(cols[i]) : str(row)})
                json_rows_list.append(json_rows_dict)

            cursor.close()

            # self.logger.info(json_rows_list)
            
            return json_rows_list
        
        except Exception as e:
            self.logger.error(e)