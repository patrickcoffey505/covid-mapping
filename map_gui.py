
from data_collection import curr_statesdata

import plotly.express as px

my_map = px.choropleth(data_frame = curr_statesdata,
                       locations = curr_statesdata.index,
                       locationmode = "USA-states", scope = 'usa',
                       color = 'value',
                       labels = {'locations':'state', 'color':'%positive'},
                       title = "Cumulative Covid Climate Map - Number of Cases Per Capita",
                       color_continuous_scale = 'reds',
                       hover_data = ['positive', 'population', 'value'])


my_map.show()
