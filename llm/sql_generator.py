import sys
sys.path
if 'f:\\Users\\hassa\\carecognitics_backend' not in sys.path:
    sys.path.append('f:\\Users\\hassa\\carecognitics_backend')
from typing import Literal
import ast
from langchain_community.vectorstores import FAISS
from operator import itemgetter
from langchain_cohere import ChatCohere, CohereEmbeddings

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.example_selectors import SemanticSimilarityExampleSelector

from sqlalchemy import create_engine
import pandas as pd

from langchain.chains import LLMChain, SequentialChain
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

from configs import examples_chinook, schema_chinook_postgre

from typing_cc.typing import supported_viz_types, supported_viz_types_inv

model_name: Literal['Cohere', 'OpenAI', 'llama'] = 'Cohere'

def get_schema(_):
    return schema_chinook_postgre

def trim_sql_query(query):   
    output=" ".join(query.split('\n')[1:-1])
    return output

# def trim_messages(chain_input):
#     max_history_length = 4 # must be even number

#     # store last two messages
#     last_2_messages = chat_history_for_chain.messages[-2:]

#     #remove last two messages to replace with clean versions
#     del chat_history_for_chain.messages[-2:]

#     # add clean messages
#     if len(last_2_messages)>=2:
#         chat_history_for_chain.add_user_message(last_2_messages[0])
#         chat_history_for_chain.add_ai_message(last_2_messages[1].content)

#     # delete first two messages in chat history if length exceeds limit
#     if len(chat_history_for_chain.messages)>max_history_length:
#         del chat_history_for_chain.messages[:2]

supported_chart_types_list = list(supported_viz_types.keys())
    

API_key = "3E7jiyBcx2wQHDkScs76tLv5Akevpx5kXLOf0nKk"
llm = ChatCohere(cohere_api_key=API_key)

# Create a template for the initial SQL chain using Dynamic few-shot prompting
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples_chinook,
    CohereEmbeddings(cohere_api_key=API_key),
    FAISS,
    k=5,
    input_keys=["input"],
)

prefix="""A user has given you a question: {input}. 
Write an SQL query in PostgreSQL given the schema: {schema} to extract the relevant information needed to answer the question. Unless stated otherwise, only return 2 columns 
Only return an SQL Query and no other text.  
Unless otherwise specificed, do not return more than {top_k} rows.
."""

example_prompt = PromptTemplate.from_template("User input: {input}\nSQL query: {query}")
prompt_sql = FewShotPromptTemplate(example_selector=example_selector,
                                    example_prompt=example_prompt,
                                    prefix=prefix,
                                    suffix="User input: {input}\nSQL query: ",
                                    input_variables=["input", "top_k", "schema"],)
sql_chain = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt_sql
    | llm
    | StrOutputParser()
    )

prompt_chart_type = PromptTemplate.from_template( 
                       f"""given the user input and SQL query, recommend a suitable visualization types out of the list: {supported_chart_types_list} 
                           make sure to match the case the charts in the list """+
                       """\nUser input: {input}
                       SQL query: {query}
                       ONLY RETURN THE CHART TYPE AND NO OTHER TEXT
                        """
                           )
chart_type_recommender_chain = (
                      prompt_chart_type
                    | llm
                    |StrOutputParser()
                    ) 

prompt_dataset_name = PromptTemplate.from_template( 
                       """given the user input and SQL query, recommend a suitable name for this dataset 
                       \nUser input: {input}
                       SQL query: {query}
                       ONLY RETURN THE DATASET NAME AND NO OTHER TEXT
                        """
                           )
dataset_name_chain = (
                      prompt_dataset_name
                    | llm
                    |StrOutputParser()
                    ) 

prompt_slice_name = PromptTemplate.from_template( 
                       """given the User input, SQL query and chart type
                       produce a suitable title for the visualization that is accurate and precise.
                       User input: {input}
                       SQL query: {query}
                       chart_type: {chart_type}
                       ONLY RETURN THE TITLE AND NO OTHER TEXT
                        """
                           )
slice_name_recommendor_chain = (
                     prompt_slice_name
                    | llm
                    |StrOutputParser()
                    ) 





# chain that returns sql, chart type and slice name
full_chain = ({"input":itemgetter("input"), "query": sql_chain}|
              RunnablePassthrough.assign(dataset_name=dataset_name_chain)|
              RunnablePassthrough.assign(chart_type=chart_type_recommender_chain)|
              RunnablePassthrough.assign(slice_name=slice_name_recommendor_chain))

# results=full_chain.invoke({'input':"show me a bar chart of the most popular artists in the USA", "top_k":3})
# print(results['query'])
# print(results['dataset_name'])
# print(results['chart_type'])
# print(results['slice_name'])

def invoke_sql_chain(input:str):
    final_output=sql_chain.invoke({'input': input, 'top_k': 3})
    return(final_output)

def invoke_slice_recommendor_chain(input:str):
    slice_name = slice_name_recommendor_chain.invoke({'input': input, 'top_k': 3})
    return slice_name

def invoke_chart_type_recommender_chain(input:str):
    viz_type = chart_type_recommender_chain.invoke({'input': input, 'top_k': 3})
    return viz_type

def invoke_full_chain(input:str):
    results = full_chain.invoke({'input':input, "top_k":3})
    sql_query=trim_sql_query(results['query'])
    dataset_name=results['dataset_name']
    chart_type=results['chart_type']
    viz_type = supported_viz_types[chart_type.lower()]
    slice_name=results['slice_name']
    return sql_query, dataset_name, chart_type, viz_type, slice_name
