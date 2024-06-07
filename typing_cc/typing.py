from typing import Literal

supported_viz_types ={'bar chart':'echarts_timeseries_bar', 'pie chart':'pie', 'timeseries': 'echarts_timeseries_smooth' }
supported_viz_types_inv = {v: k for k, v in supported_viz_types.items()}

class viz_types(Literal['echarts_timeseries_bar', 'timeseries', 'echarts_timeseries_smooth']):
    ...
