from typing import Literal
from time import localtime
import json
import requests
from IPython.display import JSON
from .dashboards import Dashboards
from .dataset import Datasets
from .charts import Charts
from typing_cc.typing import viz_types

class SupersetAPIClient:
    def __init__(self,
                base_url:str,
                username:str,
                password:str) -> None:
        
        self._base_url = base_url
        
        # connect to superset instance
        payload = {'username':username,
                'password':password,
                'provider':'db',
                'refresh': 'True'
                }
        
        # login
        r = requests.post(self._base_url + '/api/v1/security/login', json=payload)
        access_token = r.json()['access_token']
        refresh_token = r.json()['refresh_token']
        self._headerAuth = {'Authorization':'Bearer ' + access_token}

        # get database names with  database id as value
        dbs_r = requests.get(self._base_url+'/api/v1/database/', headers=self._headerAuth)
        dbs = dbs_r.json() 

        db_ids:dict[str,int] = {}
        for db in dbs['result']:
            db_ids[db['database_name']] = db['id'] # e.g {'chinook': 5, 'examples': 1}

        db_scr = requests.get(base_url+f"/api/v1/database/{db_ids['chinook']}/schemas/", headers=self._headerAuth) # this fixes code to chinook
        db_sc:dict[list] = db_scr.json() # e.g {'result': ['information_schema', 'public']}
    
        self.db_ids= db_ids
        self.db_sc = db_sc 
        
        
        self.dashboards = Dashboards(base_url=self._base_url,
                                    headerAuth=self._headerAuth)
        self.dataset = Datasets(base_url=self._base_url,
                                headerAuth=self._headerAuth)
        self.chart = Charts(base_url=self._base_url,
                            headerAuth=self._headerAuth)

    def create_dashboard(self,
                        name:str,
                        verbose:bool=False,
                        published:Literal['true', 'false']='true'):
        """Function to new dashboard using superset API

        Params:
        name:str - name of new dashboard to create 

        Returns: 
        number of new dashboard
        """
        self.dashboards.create(name=name,
                               verbose=verbose,
                               published=published)

    def create_dataset(self,
                           sql:str,
                           table_name:str,
                           verbose:bool=False):
        """Function to excecute SQL commands and store it as a dataset all using superset API

        Params:
        SQL:str - the SQL command to be excecuted

        Returns: 
        None
        
        """
        self.dataset.create(
                           sql=sql,
                           db_ids=self.db_ids,
                           table_name=table_name,
                           verbose=verbose)
        
    
    def create_chart(self,
                          slice_name,
                          viz_type:viz_types,
                          verbose:bool,
                          dashboard_ids:list[int]|None=None,
                          ):
        """create data from previously excecuted sql query"""
        
        dashboard_ids = self.dashboards.user_dashboard_ids if dashboard_ids is None else dashboard_ids
        self.chart.create(slice_name=slice_name,
                                viz_type=viz_type,
                                dashboard_ids=dashboard_ids,
                                column_names=self.dataset.column_names,
                                excecuted_data_uid=self.dataset.excecuted_data_uid,
                                excecuted_data_id=self.dataset.excecuted_data_id,
                                schema=self.dataset.schema,
                                table_name=self.dataset.table_name,
                                excecuted_data_type=self.dataset.excecuted_data_type,
                                verbose=verbose)
                                
                                      
        
        
