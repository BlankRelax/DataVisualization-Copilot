# https://flask-appbuilder.readthedocs.io/en/latest/rest_api.html
from flask import Flask, request, jsonify, Response
from flask_appbuilder.api import expose, BaseApi
from flask_appbuilder import AppBuilder, SQLA
from supersetapiclient.client import SupersetAPIClient
from llm.sql_generator import invoke_full_chain

app = Flask(__name__)
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

class SupersetAPIClientAPI(BaseApi):

    resource_name = 'ssclient'

    @expose("/login", methods=["POST"])
    def login(self)->Response:
        """activates supersetclient connection
        ---
        post:
          summary: logs in to Superset instance at 'base_url' provided 
          with provided username and password
          requestBody:
            description: user_inputs and dashboard_ids(optional)
            required: true
            content:
              application/json:
                schema:
                  {"base_url":"string",
                  "username":"string",
                  "password":"string"}
         
        responses:
            200:
            description: login has been successful and you can start to 
            interact with the superset instance through our wrapped API
            content:
                application/json:
                schema:
                    type: object
                    properties:
                    message:
                        type: string
                """
        if request.method=='POST':
            payload=request.get_json()
            base_url = payload['base_url']
            username = payload['username']
            password = payload['password']

            sc = SupersetAPIClient(base_url=base_url,
                       username=username,
                       password=password)
            self.sc = sc
            return self.response(200, message='SupersetAPIClient is now active')

    @expose("/embed", methods=["POST","GET","DELETE"])
    def embed_dashboard(self)->Response:
        """creates embedded sdk
        ---
        post:
          summary: creates a new embed token for a dashboard that 
          gives viewing permission to certain domains 
          requestBody:
            description: id, allowed_domains, verbose
            required: true
            content:
              application/json:
                schema:
                  {"id":"string",
                  "allowed_domains":[],
                  "verbose":"boolean"}
         
        responses:
            200:
            description: embed sdk has been retreived successfully
            content:
                application/json:
                schema:
                    type: object
                    properties:
                    message:
                        type: dict
            ---
        get:
          summary: gets an already existing embed token for a dashboard that 
          gives viewing permission to certain domains 
          requestBody:
            description: id, verbose
            required: true
            content:
              application/json:
                schema:
                  {"id":"string",
                  "verbose":"boolean"}
         
        responses:
            200:
            description: embed sdk has been retreived successfully
            content:
                application/json:
                schema:
                    type: object
                    properties:
                    message:
                        type: dict
                ---
        delete:
          summary: deletes an existing embed sdk of a dashboard 
          requestBody:
            description: id, verbose
            required: true
            content:
              application/json:
                schema:
                  {"id":"string",
                  "verbose":"boolean"}
         
        responses:
            200:
            description: embed sdk has been deleted successfully
            content:
                application/json:
                schema:
                    type: object
                    properties:
                    message:
                        type: string
                """
        if request.method=='POST':
            payload = request.get_json()
            id = payload['id']
            allowed_domains = payload['allowed_domains']
            verbose=payload['verbose']   
            embed_sdk=self.sc.dashboards.post_embed(id=id,
                                          allowed_domains=allowed_domains,
                                          verbose=verbose)
            return self.response(200, message={'embed_sdk':embed_sdk})
        elif request.method=='GET':
            payload = request.get_json()
            id = payload['id']
            verbose=payload['verbose']   
            embed_sdk=self.sc.dashboards.get_embed(id=id,
                                          verbose=verbose)
            return self.response(200, message={'embed_sdk':embed_sdk})
        elif request.method=='DELETE':
            payload = request.get_json()
            id = payload['id']
            verbose=payload['verbose']   
            return_m=embed_sdk=self.sc.dashboards.delete_embed(id=id,
                                          verbose=verbose)
            return self.response(200, message=return_m)
            
    @expose("/dashboard", methods=["POST"])
    def create_dashboard(self)->Response:
        """Creates a new chart
        ---
        post:
          summary: creates a new dataset using LLM generated SQL from user input as prompt,
          generates required chart and pushes it into a dashboard 
          requestBody:
            description: user_inputs and dashboard_ids(optional)
            required: true
            content:
              application/json:
                schema:
                  {"user_input":"string",
                  "dashboard_ids":[]}
         
        responses:
            200:
            description: chart has been created and displayed on dashboard
            content:
                application/json:
                schema:
                    type: object
                    properties:
                    message:
                        type: string
                """
        if request.method=='POST':
            payload = request.get_json()
            name= payload['name']
    
            self.sc.create_dashboard(name=name)
            return self.response(200, message='Dashbaord created')
        
    @expose("/chart", methods=["POST"])
    def post_chart_from_sql_to_dash(self)->Response:
        """Creates a new chart
        ---
        post:
          summary: creates a new dataset using LLM generated SQL from user input as prompt,
          generates required chart and pushes it into a dashboard 
          requestBody:
            description: user_inputs and dashboard_ids(optional)
            required: true
            content:
              application/json:
                schema:
                  {"user_input":"string",
                  "dashboard_ids":[]}
         
        responses:
            200:
            description: chart has been created and displayed on dashboard
            content:
                application/json:
                schema:
                    type: object
                    properties:
                    message:
                        type: string
                """
        if request.method=='POST':
            payload = request.get_json()
            user_input= payload['user_input']
            dashboard_ids=payload['dashboard_ids']
            # use LLM to create chart and dataset params
            sql_query, dataset_name, chart_type, viz_type, slice_name = invoke_full_chain(input=user_input)

            #create dataset using LLM generated params
            self.sc.create_dataset(sql=sql_query, table_name=dataset_name, verbose=False)

            # create chart and add to dashboard using previously created dataset and LLM generated params
            self.sc.create_chart(slice_name=slice_name,
                            viz_type=viz_type,
                            dashboard_ids=dashboard_ids)
            return self.response(200, message='Chart created and added to Dashboard')
        
appbuilder.add_api(SupersetAPIClientAPI)


# http://127.0.0.1:5000/api/v1/resource_name/chart
# {"user_input": "make a 2d scatter for revenue against genre", "dashboard_ids":[31]}

# http://127.0.0.1:5000/api/v1/resource_name/login
# {"base_url":"http://localhost:8088",
# "username":"admin",
# "password":"admin"}