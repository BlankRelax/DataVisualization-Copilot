import requests
from typing import Literal
from supersetapiclient.base import BaseSupersetObject

# code to be refactored to have api calls as seperate functions
class Dashboards(BaseSupersetObject):
     
    def __init__(self, base_url, headerAuth):
        self.user_dashboard_ids:list[int]=[] # dashboard ids created by user within current session
        self._base_url = base_url
        self._headerAuth = headerAuth

        r = requests.get(url=self._base_url+'/api/v1/dashboard/',
                         headers=self._headerAuth).json()
        
        dashboards_info:dict[int:str]={dbd['id']:dbd['dashboard_title'] for dbd in r['result']}
        self._dashboards_info = dashboards_info
    
    def _update_info_all(self):
        # gets dictionary of dashboards in form {id:name}
        r = requests.get(url=self._base_url+'/api/v1/dashboard/',
                         headers=self._headerAuth).json()
        
        dashboards_info:dict[int,str]={dbd['dashboard_title']:dbd['id'] for dbd in r['result']}
        self._dashboards_info = dashboards_info
    
    @property
    def info_all(self)->dict[int,str]:
        self._update_info_all()
        return self._dashboards_info
    
    def _update_info(self, id:str|int, verbose:bool=False):
        # gets dictionary of dashboards in form {id:name}
        r = requests.get(url=self._base_url+f'/api/v1/dashboard/{id}',
                         headers=self._headerAuth)
        if verbose: print(r,r.json())
        result = r.json()['result']
        dashboard_info = {'id':result['id'],
                         'charts':result['charts'],
                         'title':result['dashboard_title']}
        return dashboard_info
    
    def info(self, id:str|int, verbose:bool=False)->dict[str,str]:
        dashboard_info=self._update_info(id=id, verbose=verbose)
        return dashboard_info
    
    def create(self,
               name:str,
               verbose:bool=False,
               published:Literal['true', 'false']='true',
                ) -> None:
        """Function to create new dashboard using superset API

        Params:
        name:str - name of new dashboard to create 

        Returns: 
        number of new dashboard
        """

        r = requests.post(url=self._base_url+'/api/v1/dashboard/',
                        headers=self._headerAuth,
                        json={"dashboard_title": name,
                              "published":published})
        if verbose: print(r, r.json()) 
        user_dashboard_id = r.json()['id']
        
        self.user_dashboard_ids.append(user_dashboard_id)

    def delete(self,
                         dashboards:int|list[int],
                         verbose:bool=False):

        # put into list if given single integer as input to API call needs to be a list
        dashboards=[dashboards] if isinstance(dashboards,int) else dashboards 
        r = requests.delete(url=self._base_url+f'/api/v1/dashboard/?q={dashboards}',
                        headers=self._headerAuth)
        if verbose: print(r.json())
        self._update_info_all()
        for num in dashboards:
            if num in self.user_dashboard_ids:
                self.user_dashboard_ids.remove(num)
        if verbose: print("dashboard info updated")
    
    def get_permalink(self,id:str|int):
        r = requests.post(url=self._base_url+f'/api/v1/dashboard/{str(id)}/permalink',
                        headers=self._headerAuth,
                        json={}).json()
        return r['url']
    
    def post_embed(self,
                id:str,
                allowed_domains:list[str],
                verbose:bool=False)->str:
        """use to create a dashboard's embedded configuration with a set of allowed domains,
            if allowed domains is empty then it will be set to superset host ip
            
            Params:
            id:str - dashboard id
            allowed_domains:list[str] - list of allowed domains that can embed this dashboard in the form 
                                        "http://IP_address/"
            Returns:
            embedded sdk 
        
        """
         
        r = requests.post(url=self._base_url+f'/api/v1/dashboard/{id}/embedded',
                        headers=self._headerAuth,
                        json={'allowed_domains':allowed_domains})
        if verbose: print(r)
        embedded_sdk = r.json()['result']['uuid']
        return embedded_sdk
    
    def get_embed(self,
                id:str,
                verbose:bool=False)->str:
        """use to get an existing dashboard's embedded configuration and a set of allowed domains
        
            Params:
            id:str - dashboard id
            
            Returns:
            embedded sdk 
        """
        r = requests.get(url=self._base_url+f'/api/v1/dashboard/{id}/embedded',
                        headers=self._headerAuth,
                        )
        if verbose: print(r)
        embedded_sdk = r.json()['result']['uuid']
        return embedded_sdk
    
    def delete_embed(self,
                id:str,
                verbose:bool=False)->str:
        """deletes an existing dashboard's embedded configuration
        
            Params:
            id:str - dashboard id
            
            Returns:
            confirmation of action string
        """
        r = requests.delete(url=self._base_url+f'/api/v1/dashboard/{id}/embedded',
                        headers=self._headerAuth,
                        )
        if verbose: print(r)
        if r.status_code==200:
            return "dashboard embed sdk successfully deleted"
        else: 
            return "error in deleting dashboard"
        
    def get_link(self,id:str|int)->str:
        return f"{self._base_url}/superset/dashboard/{id}?standalone=true"
    
    def add_chart(dashboard_id:str|int, chart_id:str|int)->None:
        pass
    
    def favourite():
        pass
    def unfavourite():
        pass



    