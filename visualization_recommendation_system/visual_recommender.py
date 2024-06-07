import pandas as pd
from typing import Generator, Literal
from typing_cc.typing import supported_viz_types, supported_viz_types_inv
from configs import examples_chinook, get_time
"""
depending on the data we are creating for the user, we may use certain visualization techniques
that compliment this type of data.

We need to determine what type of data we have created to determine a visualization types.
We can determine the type of data from the SQL function that is used to retrieve the data

Thus we aim to map certain aggregate functions and clauses to certain types of graphical 
visuals to recommend to the user
"""

class visual_recommender:

    def __init__(self) -> None:
        
        self._sql_features = ['AVG',
                    'COUNT',
                    'MAX',
                    'MIN',
                    'SUM',
                    'GROUP',
                    ]

        # dict[chart type:viz type]
        self._supported_viz_types =supported_viz_types
        self._supported_viz_types_inv = supported_viz_types_inv
    
    @property
    def supported_viz_types(self)-> dict[str,str]:
        return self._supported_viz_types
    
    @property
    def supported_viz_types_inv(self)-> dict[str,str]:
        return self._supported_viz_types_inv

    def parse_sql(self, sql:str)->dict[str,str]:
        """
        Parse an sql statement to identify aggregate functions and groupby

        parameters: sql - sql statement to parse
        
        returns: dict with keys:
            agg: the aggregate function using in the SQL statement
            agg_by: the column that was aggregated
            groupby: the column that was used to group the data

        """
        feature_dict={}
        sql_list=sql.split(" ")

        # loop through every sql feature check if it is in the sql statement
        for sql_feature in self._sql_features:
            for token in sql_list:
                if sql_feature in token:
                    if sql_feature=='GROUP': feature_dict['groupby']=sql_list[sql_list.index('GROUP')+2]
                    else:
                        # check if all the columns that are aggregated are contained within this token
                        # e.g SUM(InvoiceLine.UnitPrice * Quantity) would get split into [SUM(InvoiceLine.UnitPrice', '*', 'Quantity)]
                        # so it would not contain all aggregates
                        if token[-1] !=')': # token does not contain full aggregate
                            current_i = sql_list.index(token)
                            start_token = sql_list.index(token)
                            found_end=False
                            while not found_end:
                                if sql_list[current_i+1][-1]==')': found_end=True
                                current_i+=1
                            intended_token = " ".join(sql_list[start_token:current_i+1])
                            token=intended_token

                    
                        token_split = token.split("(")
                        feature_dict['agg']=token_split[0]
                        feature_dict['agg_by']=token_split[1][:-1]

        if 'groupby' not in feature_dict.keys(): feature_dict['GROUP']=False
        if 'agg' not in feature_dict.keys(): feature_dict['agg']=False
        if 'agg_by' not in feature_dict.keys(): feature_dict['agg_by']=False
            
        return feature_dict

    def user_pick_chart_type(self):
        
        supported_charts_list = list(self._supported_viz_types.keys())
        incorrect_input = True
        while incorrect_input:
            chart_type=input(f"Pick a chart type out of {supported_charts_list}: ")
            if chart_type in list(supported_charts_list):
                incorrect_input=False
            else: print("Please input supported chart type") 
        viz_type=self._supported_viz_types[chart_type]
        
        return viz_type

    def log_user_selected_viz_type(sql_query,selected_viz_type, feature_dict):

        df=pd.read_csv('f:\\Users\\hassa\\CareCognetics\\visualization_recommendation_system\\sql_query_metadata.csv')
        feature_dict['viz_type']= selected_viz_type
        feature_dict['sql_query'] = sql_query

        df_temp=pd.DataFrame(data=[feature_dict])

        df=pd.concat([df,df_temp], ignore_index=True)

        df.to_csv('f:\\Users\\hassa\\CareCognetics\\visualization_recommendation_system\\sql_query_metadata.csv', index=False)

        # release from memory
        del df

    def generate_visual_recommendations(self,
                                        sql:str,
                                        return_type:Literal['best','all_in_list']='best') -> str|list[str]|Generator[str, None, None]:

        feature_dict=self.parse_sql(sql=sql)

        df=pd.read_csv('f:\\Users\\hassa\\CareCognetics\\visualization_recommendation_system\\sql_query_metadata.csv')
        viz_type_frequency = dict(df[df['agg']==feature_dict['agg']]['viz_type'].value_counts())

        viz_type_frequency_sorted = dict(sorted(viz_type_frequency.items(), key=lambda item: item[1], reverse=True))

        if return_type=='best':
            return list(viz_type_frequency_sorted.keys())[0]
        elif return_type=='all_in_list':
            return list(viz_type_frequency_sorted.keys()) 
     
    
# for chart_type in visual_recommender().generate_visual_recommendations(sql=examples_chinook[-1]['query']):
#     print(chart_type)
#print(visual_recommender().generate_visual_recommendations(sql=examples_chinook[-1]['query'], return_type='best'))
