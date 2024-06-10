from flask import Flask, request, jsonify
app = Flask(__name__)
from .client import SupersetAPIClient
from llm.sql_generator import invoke_full_chain

sc = SupersetAPIClient(base_url="http://localhost:8088",
                       username='admin',
                       password='admin')
@app.post("/chart")
def post_chart_from_sql_to_dash():

    """
    json payload format: {user_input:"string",
                          dashboard_ids:[]}
    """
    payload = request.get_json()
    # use LLM to create chart and dataset params
    sql_query, dataset_name, chart_type, viz_type, slice_name = invoke_full_chain(input=payload['user_input'])

    #create dataset using LLM generated params
    sc.create_dataset(sql=sql_query, table_name=dataset_name)

    # create chart and add to dashboard using previously created dataset and LLM generated params
    sc.create_chart(slice_name=slice_name,
                       viz_type=viz_type,
                    dashboard_ids=payload['dashboard_ids'])



