import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import sqlite3
from database import *
from helper_function import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

table_params = ['NOPAT','Sales','COS Other','Gross Profit','Fixed Expenses','Variable Expenses','EBIT']
year = range(2013, 2017)
df = pd.read_csv('data.csv')

table = dash_table.DataTable(
        id = 'line chart data',
        columns = [{'name':' ', 'id':"data"}]+[{'name':str(i), 'id':str(i)} for i in list(df.columns.values)[1:]],
        data =df.to_dict('records'),
        editable = True
    )


line_chart = dcc.Graph(
    id = 'line chart',
    figure = create_figure_by_df(pd.read_csv('data.csv'))
)


search_company = html.Div([
    dbc.Row([
        dbc.Col(dbc.Input(id = "search company", placeholder= "company name", type = "text",), width = 15),
        dbc.Col(dbc.Button("Search",id = 'search company button',style = {'margin-left': 4})  ) 
    ]),
    
    html.Br(),
    html.Div(id = "company information"),
    html.Br()
])

rank_attribute = ['id','name','year']
rank_value = ['bid','bname','year'] #actual attribute name in database
dropdown_option = []
for i in range(len(rank_value)):
    dropdown_option.append({'label':rank_attribute[i],
                            'value':rank_value[i]})

app.layout = html.Div([
    dbc.Row([
        search_company
    ], justify="center"),

    dbc.Row([
        dbc.Col(html.H4('Scoreboard'),width = 1,style = {'marginLeft':'50px','marginRight':'10px'}),
        dbc.Col(dcc.Dropdown(
            id = 'attribute-dropdown',
            options = dropdown_option,
            value = 'bid',
        ),width = 1)
    ],style= { 'align':"left", 'marginBottom':'20px'}, justify = 'center'),

    dbc.Row(id='scoreboard-section', children= [
    ], justify="center"),
    dbc.Row([
        dbc.Col(table,width = 4, style = {'marginTop': 85,'marginLeft': 50} ),
        dbc.Col(line_chart,width = 7)
    ],)
],  style = {'marginTop': 85,'marginLeft': 50} )

@app.callback(
    Output('line chart','figure'),
    [Input('line chart data','data'),
    Input('line chart data','columns')]
)
def display_line_chart(rows,columns):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    return create_figure_by_df(df)

@app.callback(
    Output('company information','children'),
    [Input('search company button','n_clicks')],
    [State('search company','value')]
)
def display_company_info(n_clicks,c_name):
    if n_clicks == 0 or n_clicks is None:
        raise PreventUpdate
    result = get_company_info(c_name)
    if result == None:
        return html.P("No result")
    else:
        return format_company_info(result)
    
@app.callback(
    Output('scoreboard-section','children'),
    [Input('attribute-dropdown','value')]
)
def show_scoreboard(value):
    if value is None or value is "":
        raise PreventUpdate
    companies = get_ranking_companies(value,5)
    result = []
    for i in companies:
        result.append(format_scoreboard(i))
    return result

def format_company_info(data):
    return html.P(["bid: "+data[0],html.Br(),
                   "bname: "+data[1],html.Br(),
                   "btype: "+data[2],html.Br(),
                   "year: "+ str(data[3]),html.Br(), ])

def format_scoreboard(data):
    return dbc.Card(dbc.CardBody([
        html.H4(data[1]),
        html.Br(),
        html.P(["bid: "+data[0],html.Br(),
                   "btype: "+data[2],html.Br(),
                   "year: "+ str(data[3]),html.Br(), ]),
    ]),style = {'marginLeft': 50})

if __name__ == '__main__':
    app.run_server(debug=True)