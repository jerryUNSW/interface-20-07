import plotly.graph_objects as go

############## line chart
table_params = ['NOPAT','Sales','COS Other','Gross Profit','Fixed Expenses','Variable Expenses','EBIT']
def create_figure_by_df(df):
    data_dict = {}
    for i in range(len(table_params)):
        row = list(df.iloc[i])
        data_dict[row[0]] = row[1:]
    x_value = list(df.columns.values)[1:]
    x_value = [str(i) for i in x_value]
    fig = go.Figure()
    for key,value in data_dict.items():
        fig.add_trace(go.Scatter(x = x_value,y = value, name = key, line=dict(width = 2)))
    fig.update_layout(xaxis_type='category')
    return fig