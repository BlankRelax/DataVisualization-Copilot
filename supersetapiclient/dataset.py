import requests
from supersetapiclient.base import BaseSupersetObject
from supersetapiclient.exceptions import DatasetNotCreatedError

# code to be refactored to have api calls as seperate functions
class Datasets(BaseSupersetObject):

    def __init__(self,
                base_url:str,
                headerAuth:str) -> None:
        
        self._base_url = base_url
        self._headerAuth = headerAuth
    
    def delete(self,
                         datasets:int|list[int],
                         verbose:bool=False):

        # put into list if given single integer as input to API call needs to be a list
        datasets=[datasets] if isinstance(datasets,int) else datasets 
        r = requests.delete(url=self._base_url+f'/api/v1/dataset/?q={datasets}',
                        headers=self._headerAuth)
        if verbose: print(r.json())
        self._update_info_all()
        if verbose: print("dataset info updated")

    def _update_info_all(self):
        # gets dictionary of datasets in form {id:name}
        r = requests.get(url=self._base_url+'/api/v1/dataset/',
                         headers=self._headerAuth).json()
        
        datasets_info:dict[int,str]={dataset['id']:dataset['table_name'] for dataset in r['result']}
        self._datasets_info = datasets_info
    
    @property
    def info_all(self)->dict[int,str]:
        self._update_info_all()
        return self._datasets_info
    
    def _update_info(self, id:str|int):
        # gets dictionary of dashboards in form {id:name}
        r = requests.get(url=self._base_url+f'/api/v1/dataset/{id}',
                         headers=self._headerAuth).json()
        result = r['result']
        dataset_info = {'id':result['id'],
                        'datasource':result['datasource_name'],
                         'title':result['table_name']}
        return dataset_info
    
    def info(self, id:str|int)->dict[str,str]:
        dataset_info=self._update_info(id=id)
        return dataset_info
        
    def create(self,
                           sql:str,
                           db_ids:dict[str,int],
                           table_name:str,
                           db_name:str='chinook',
                           verbose:bool=False):
        """Create dataset from SQL commands using superset API

        Params:
        SQL:str - the SQL command to be excecuted

        Returns: 
        None
        
        """
        table_name = table_name
        schema = "public"
        true=True
        
        #create new database with given sql
        r = requests.post(self._base_url+'/api/v1/dataset/',
                        headers=self._headerAuth,
                        json={"database": db_ids[db_name],
                        "external_url": "string",
                        "is_managed_externally": true,
                        "owners": [
                            1
                        ],
                        "schema": schema,
                        "sql": sql ,
                        "table_name": table_name })
        if verbose: print(r,r.json())
        if r.status_code!=201: raise DatasetNotCreatedError(dataset_name=table_name, r_error=r)
        else: print(f"dataset has been created with name {table_name}")
        excecuted_data_id =r.json()['id'] # e.g 31
        excecuted_data_uid:str=r.json()['data']['uid'] # e.g 31__table
        excecuted_data_type:str=r.json()['data']['type'] # e.g table
        excecuted_data_sql:str=r.json()['result']['sql'] # sql used to get data

        #get column names of newly created data
        dataset = requests.get(self._base_url+f"/api/v1/dataset/{excecuted_data_id}", headers=self._headerAuth)
        column_names = [column_dict['column_name'] for column_dict in dataset.json()['result']['columns']]
        
        #read to self
        self.excecuted_data_id = excecuted_data_id
        self.excecuted_data_uid = excecuted_data_uid
        self.excecuted_data_type = excecuted_data_type
        self.excecuted_data_sql = excecuted_data_sql
        self.column_names = column_names
        self.schema = schema
        self.table_name = table_name

        