import sys
sys.path
if 'f:\\Users\\hassa\\carecognitics_backend' not in sys.path:
    sys.path.append('f:\\Users\\hassa\\carecognitics_backend')
import json
import requests
from typing_cc.typing import viz_types
from supersetapiclient.base import BaseSupersetObject

class Charts(BaseSupersetObject):

    def __init__(self, base_url:str, headerAuth:dict) -> None:
        self._base_url = base_url
        self._headerAuth = headerAuth
    
    def delete(self,
                         charts:int|list[int],
                         verbose:bool=False):

        # put into list if given single integer as input to API call needs to be a list
        charts=[charts] if isinstance(charts,int) else charts 
        r = requests.delete(url=self._base_url+f'/api/v1/chart/?q={charts}',
                        headers=self._headerAuth)
        if verbose: print(r.json())
        self._update_info_all()
        if verbose: print("dashboard info updated")

    def _update_info_all(self):
        # gets dictionary of charts in form {id:name}
        r = requests.get(url=self._base_url+'/api/v1/chart/',
                         headers=self._headerAuth).json()
        
        charts_info:dict[int,str]={chart['slice_name']:chart['id'] for chart in r['result']}
        self._charts_info = charts_info
    
    @property
    def info_all(self)->dict[int,str]:
        self._update_info_all()
        return self._charts_info
    
    def _update_info(self, id:str|int, verbose:bool=False):
        # gets dictionary of dashboards in form {id:name}
        r = requests.get(url=self._base_url+f'/api/v1/chart/{id}',
                         headers=self._headerAuth)
        if verbose: print(r, r.json())
        result = r.json()['result']
        chart_info = {result['id']:'id',
                      result['dashboards'][0].pop("json_metadata"):'dashboards',
                      result['slice_name']:'title'}
        return chart_info
    
    def info(self, id:str|int, verbose:bool=False)->dict[str,str]:
        chart_info=self._update_info(id=id, verbose=verbose)
        return chart_info
        

    def _create_barchart(self,
    slice_name:str,
    dashboard_ids:list[int],
    column_names,
    excecuted_data_uid,
    excecuted_data_id,
    schema,
    table_name,
    excecuted_data_type,
    true=True,
    false=False,
    null=None)->dict[str]:
        """
        create a "echarts_timeseries_bar" schema to create a barchart for API payload

        Params:
        slice_name:str - name of slice to be created

        Returns:
        json payload for chart creation
        """
        # TODO: make "label" into a run-time parameter created by the LLM
        #       make "slice_name into a run-time parameter created by the LLM"
          
        metrics=[{"expressionType":"SIMPLE","column":{"advanced_data_type":null,"certification_details":null,"certified_by":null,
                "column_name":column_names[1],"description":null,"expression":null,"filterable":true,"groupby":true,"id":null,"is_certified":false,
                "is_dttm":false,"python_date_format":null,"type":"DECIMAL","type_generic":0,"verbose_name":null,"warning_markdown":null},"aggregate":"SUM",
                "sqlExpression":null,"datasourceWarning":false,"hasCustomLabel":false,"label":" ","optionName":null}]
    
        params={"datasource":excecuted_data_uid,
                "viz_type":"echarts_timeseries_bar",
                "x_axis":column_names[0],
                "time_grain_sqla":"P1D",
                "x_axis_sort_asc":true,
                "x_axis_sort_series":"name",
                "x_axis_sort_series_ascending":true,
                "metrics":metrics,
                "groupby":[],
                "adhoc_filters":[],
                "order_desc":true,
                "row_limit":10000,
                "truncate_metric":true,
                "show_empty_columns":true,
                "comparison_type":"values",
                "annotation_layers":[],
                "forecastPeriods":10,
                "forecastInterval":0.8,
                "orientation":"vertical",
                "x_axis_title_margin":15,
                "y_axis_title_margin":15,
                "y_axis_title_position":"Left",
                "sort_series_type":"sum",
                "color_scheme":"supersetColors",
                "only_total":true,
                "show_legend":true,
                "legendType":"scroll",
                "legendOrientation":"top",
                "x_axis_time_format":"smart_date",
                "y_axis_format":"SMART_NUMBER",
                "truncateXAxis":true,
                "y_axis_bounds":[null,null],
                "rich_tooltip":true,
                "tooltipTimeFormat":"smart_date",
                "extra_form_data":{},
                "dashboards":[]}

        payload = {"cache_timeout": null,
                "certification_details": null,
                "certified_by": null,
                "dashboards": dashboard_ids,
                "datasource_id": excecuted_data_id,
                "datasource_name": f"{schema}.{table_name}",
                "datasource_type": excecuted_data_type,
                "description": 'null',
            "params":json.dumps(params),
                "slice_name":slice_name,
                "viz_type":"echarts_timeseries_bar"}
        return payload
    
    def _create_pie(self,
    slice_name:str,
    dashboard_ids:list[int],
    column_names,
    excecuted_data_uid,
    excecuted_data_id,
    schema,
    table_name,
    excecuted_data_type,
    true=True,
    false=False,
    null=None
    )->dict[str]:
        """
        create a "pie" schema to create a piechart for API payload

        Params:
        slice_name:str - name of slice to be created

        Returns:
        json payload for chart creation
        """

        # TODO: make "label" into a run-time parameter created by the LLM
        #       make "slice_name into a run-time parameter created by the LLM"

        metric=[{"expressionType":"SIMPLE","column":{"advanced_data_type":null,"certification_details":null,"certified_by":null,
                "column_name":column_names[1],"description":null,"expression":null,"filterable":true,"groupby":true,"id":null,"is_certified":false,
                "is_dttm":false,"python_date_format":null,"type":"DECIMAL","type_generic":0,"verbose_name":null,"warning_markdown":null},"aggregate":"SUM",
                "sqlExpression":null,"datasourceWarning":false,"hasCustomLabel":false,"label":null,"optionName":null}]
        
        params={"datasource":excecuted_data_uid,
                "viz_type":"pie",
                "groupby":[column_names[0]],
                "metric":metric,
                "adhoc_filters":[],
                "row_limit":100,
                "sort_by_metric":true,
                "color_scheme":"supersetColors",
                "show_labels_threshold":5,
                "show_legend":true,
                "legendType":"scroll",
                "legendOrientation":"top",
                "label_type":"key",
                "number_format":"SMART_NUMBER",
                "date_format":"smart_date",
                "show_labels":true,
                "labels_outside":true,"outerRadius":70,"innerRadius":30,"extra_form_data":{},"dashboards":[]}
    
        payload = {"cache_timeout": null,
                "certification_details": null,
                "certified_by": null,
                "dashboards": dashboard_ids,
                "datasource_id": excecuted_data_id,
                "datasource_name": f"{schema}.{table_name}",
                "datasource_type": excecuted_data_type,
                "description": 'null',
            "params":json.dumps(params),
                "slice_name":slice_name,
                "viz_type":"pie"}
        return payload
    
    def _create_timeseries(self,
                        slice_name:str,
                        dashboard_ids:list[int],
                        column_names,
                        excecuted_data_uid,
                        excecuted_data_id,
                        schema,
                        table_name,
                        excecuted_data_type,
                        true=True,
                        false=False,
                        null=None)->dict[str]:
        
        metrics=[{"expressionType":"SIMPLE","column":{"advanced_data_type":null,"certification_details":null,"certified_by":null,
        "column_name":column_names[1],"description":null,"expression":null,"filterable":true,"groupby":true,"id":null,
        "is_certified":false,"is_dttm":false,"python_date_format":null,"type":"LONGINTEGER","type_generic":0,"verbose_name":null,
        "warning_markdown":null},"aggregate":"AVG","sqlExpression":null,"datasourceWarning":false,"hasCustomLabel":false,
        "label":column_names[1],"optionName":null}]
        
        params =  {"datasource":excecuted_data_uid,
        "viz_type":"echarts_timeseries_line",
        "x_axis":column_names[0],
        "time_grain_sqla":"P3M",
        "x_axis_sort_asc":true,
        "x_axis_sort_series":"name",
        "x_axis_sort_series_ascending":true,
        "metrics":metrics,
        "groupby":[],
        "adhoc_filters":[{"clause":"WHERE","subject":"month","operator":"TEMPORAL_RANGE","comparator":"No filter","expressionType":"SIMPLE"}],
        "order_desc":true,
        "row_limit":10000,
        "truncate_metric":true,
        "show_empty_columns":true,
        "comparison_type":"values",
        "annotation_layers":[],
        "forecastPeriods":10,
        "forecastInterval":0.8,
        "x_axis_title_margin":15,
        "y_axis_title_margin":15,
        "y_axis_title_position":"Left",
        "sort_series_type":"sum",
        "color_scheme":"supersetColors",
        "seriesType":"line",
        "only_total":true,
        "opacity":0.2,
        "markerSize":6,
        "show_legend":true,
        "legendType":"scroll",
        "legendOrientation":"top",
        "x_axis_time_format":"smart_date",
        "rich_tooltip":true,
        "tooltipTimeFormat":"smart_date",
        "y_axis_format":"SMART_NUMBER",
        "truncateXAxis":true,
        "y_axis_bounds":[null,null],
        "extra_form_data":{},
        "dashboards":[]}

        payload = {"cache_timeout": null,
                "certification_details": null,
                "certified_by": null,
                "dashboards": dashboard_ids,
                "datasource_id": excecuted_data_id,
                "datasource_name": f"{schema}.{table_name}",
                "datasource_type": excecuted_data_type,
                "description": 'null',
                "params":json.dumps(params),
                "slice_name":slice_name,
                "viz_type":"echarts_timeseries_line"}   
        return payload
    
    def _create_table(self,
                        slice_name:str,
                        dashboard_ids:list[int],
                        column_names,
                        excecuted_data_uid,
                        excecuted_data_id,
                        schema,
                        table_name,
                        excecuted_data_type,
                        true=True,
                        false=False,
                        null=None
                        )->dict[str]:
        metrics=[{"expressionType":"SIMPLE","column":{"advanced_data_type":null,"certification_details":null,"certified_by":null,
                  "column_name":column_names[1],"description":null,"expression":null,"filterable":true,"groupby":true,
                  "id":null,"is_certified":false,"is_dttm":false,"python_date_format":null,"type":"DECIMAL","type_generic":0,
                  "verbose_name":null,"warning_markdown":null},"aggregate":"AVG","sqlExpression":null,"datasourceWarning":false,
                  "hasCustomLabel":false,"label":column_names[1],"optionName":null}]
        
        params= {"datasource":excecuted_data_uid,
                 "viz_type":"table",
                 "query_mode":"aggregate",
                 "groupby":[column_names[0]],
                 "time_grain_sqla":"P1D",
                 "temporal_columns_lookup":{},
                 "metrics":metrics,
                "all_columns":[],
                "percent_metrics":[],
                "adhoc_filters":[],
                "order_by_cols":[],
                "row_limit":1000,
                "server_page_length":10,
                "order_desc":true,
                "table_timestamp_format":"smart_date",
                "show_cell_bars":true,
                "color_pn":true,
                "extra_form_data":{},
                "dashboards":[]}
        
        payload = {"cache_timeout": null,
                "certification_details": null,
                "certified_by": null,
                "dashboards": dashboard_ids,
                "datasource_id": excecuted_data_id,
                "datasource_name": f"{schema}.{table_name}",
                "datasource_type": excecuted_data_type,
                "description": 'null',
                "params":json.dumps(params),
                "slice_name":slice_name,
                "viz_type":"table"} 
        return payload
    
    def _create_scatter(self,
                        slice_name:str,
                        dashboard_ids:list[int],
                        column_names,
                        excecuted_data_uid,
                        excecuted_data_id,
                        schema,
                        table_name,
                        excecuted_data_type,
                        true=True,
                        false=False,
                        null=None)->dict[str]:
        
        metrics={"expressionType":"SIMPLE",
                  "column":{"advanced_data_type":null,"certification_details":null,"certified_by":null,"column_name":column_names[1],
                  "description":null,"expression":null,"filterable":true,"groupby":true,"id":null,"is_certified":false,"is_dttm":false,
                  "python_date_format":null,"type":"DOUBLE PRECISION","type_generic":0,"verbose_name":null,"warning_markdown":null},
                  "aggregate":"AVG",
                  "sqlExpression":null,
                  "datasourceWarning":false,
                  "hasCustomLabel":false,
                  "label":column_names[1],
                  "optionName":null},
                 

        params = {"datasource":excecuted_data_uid,
        "viz_type":"echarts_timeseries_scatter",
        "x_axis":column_names[0],
        "time_grain_sqla":"P1D",
        "xAxisForceCategorical":false,
        "x_axis_sort_asc":true,
        "x_axis_sort_series":"name",
        "x_axis_sort_series_ascending":true,
        "metrics":metrics,
        "groupby":[],
        "adhoc_filters":[{"clause":"WHERE","subject":"order_date","operator":"TEMPORAL_RANGE","comparator":"No filter","expressionType":"SIMPLE"}],
        "order_desc":true,
        "row_limit":10000,
        "truncate_metric":true,
        "show_empty_columns":true,
        "comparison_type":"values",
        "annotation_layers":[],
        "forecastPeriods":10,
        "forecastInterval":0.8,
        "x_axis_title":column_names[0],
        "x_axis_title_margin":15,
        "y_axis_title":"sales",
        "y_axis_title_margin":50,
        "y_axis_title_position":"Left",
        "sort_series_type":"sum",
        "color_scheme":"d3Category20c",
        "only_total":true,
        "markerSize":6,
        "show_legend":true,
        "legendType":"scroll",
        "legendOrientation":"top",
        "x_axis_time_format":"smart_date",
        "rich_tooltip":true,
        "tooltipTimeFormat":"smart_date",
        "y_axis_format":"SMART_NUMBER",
        "truncateXAxis":true,
        "y_axis_bounds":[null,null],
        "extra_form_data":{},
        "dashboards":[]}

        payload = {"cache_timeout": null,
                "certification_details": null,
                "certified_by": null,
                "dashboards": dashboard_ids,
                "datasource_id": excecuted_data_id,
                "datasource_name": f"{schema}.{table_name}",
                "datasource_type": excecuted_data_type,
                "description": 'null',
                "params":json.dumps(params),
                "slice_name":slice_name,
                "viz_type":"echarts_timeseries_scatter"} 
        return payload
        
       
    def create(self,
                        
                        slice_name,
                        viz_type:viz_types,
                        dashboard_ids:list[int|str]|None,
                        column_names,
                        excecuted_data_uid,
                        excecuted_data_id,
                        schema,
                        table_name,
                        excecuted_data_type,
                        verbose:bool=False
                        ):
        if viz_type == "echarts_timeseries_bar":
            r=requests.post(self._base_url+'/api/v1/chart/',
                            headers=self._headerAuth,
                            json=self._create_barchart(slice_name=slice_name,
                            dashboard_ids=dashboard_ids,
                            column_names=column_names,
                            excecuted_data_uid=excecuted_data_uid,
                            excecuted_data_id=excecuted_data_id,
                            schema=schema,
                            table_name=table_name,
                            excecuted_data_type=excecuted_data_type))
            if verbose: print(r,r.json())
            return r.json()
        elif viz_type == "pie":
            r=requests.post(self._base_url+'/api/v1/chart/',
                            headers=self._headerAuth,
                            json=self._create_pie(slice_name=slice_name,
                            dashboard_ids=dashboard_ids,
                            column_names=column_names,
                            excecuted_data_uid=excecuted_data_uid,
                            excecuted_data_id=excecuted_data_id,
                            schema=schema,
                            table_name=table_name,
                            excecuted_data_type=excecuted_data_type))
            if verbose: print(r,r.json())
            return r.json()
        elif viz_type=='echarts_timeseries_line':
            r=requests.post(self._base_url+'/api/v1/chart/',
                            headers=self._headerAuth,
                            json=self._create_timeseries(slice_name=slice_name,
                            dashboard_ids=dashboard_ids,
                            column_names=column_names,
                            excecuted_data_uid=excecuted_data_uid,
                            excecuted_data_id=excecuted_data_id,
                            schema=schema,
                            table_name=table_name,
                            excecuted_data_type=excecuted_data_type))
            if verbose: print(r,r.json())
            return r.json()
        elif viz_type=='table':
            r=requests.post(self._base_url+'/api/v1/chart/',
                            headers=self._headerAuth,
                            json=self._create_table(slice_name=slice_name,
                            dashboard_ids=dashboard_ids,
                            column_names=column_names,
                            excecuted_data_uid=excecuted_data_uid,
                            excecuted_data_id=excecuted_data_id,
                            schema=schema,
                            table_name=table_name,
                            excecuted_data_type=excecuted_data_type))
            if verbose: print(r,r.json())
            return r.json()
        elif viz_type=='echarts_timeseries_scatter':
            r=requests.post(self._base_url+'/api/v1/chart/',
                            headers=self._headerAuth,
                            json=self._create_scatter(slice_name=slice_name,
                            dashboard_ids=dashboard_ids,
                            column_names=column_names,
                            excecuted_data_uid=excecuted_data_uid,
                            excecuted_data_id=excecuted_data_id,
                            schema=schema,
                            table_name=table_name,
                            excecuted_data_type=excecuted_data_type))
            if verbose: print(r,r.json())
            return r.json()

