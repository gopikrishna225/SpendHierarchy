
from imp import reload
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

from dash.dependencies import Input, Output, State
import re
import dash
import pandas as pd
from dash.exceptions import PreventUpdate
import numpy as np
import graphviz
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image
import string
import base64
from dash import dash_table
import io
import time

from sqlalchemy import column
from anytree import Node,AnyNode
from anytree.exporter import UniqueDotExporter
from anytree.exporter import DotExporter
import pydot

(graph,) = pydot.graph_from_dot_file('somefile.dot')
graph.write_png('somefile.png')
# import cx_Oracle
# from sqlalchemy import types, create_engine

app = dash.Dash(suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.CERULEAN])

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 62.5,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#e8e9eb",
    "overflowY": "scroll",
    "height": "89%",
    "overflow-x": "hidden",
    "transition": "all 0.5s"
    
}

# SIDEBAR_STYLE = {
#     "position": "fixed",
#     "top": 62.5,
#     "left": "-18rem",
#     "bottom": 0,
#     "width": "18rem",
#     "height": "89%",
#     "z-index": 1,
#     "overflow-x": "hidden",
#     "transition": "all 0.5s",
#     "padding": "0rem 0rem",
#     "background-color": "#f8f9fa",
# }
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "17rem",
    "padding": "4rem 1rem",
    "background-color": "#d7d8db",
    "overflowY": "scroll",
}
# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE1 = {
    "margin-top":"3rem",
    "margin-left": "11rem",
    "margin-right": "1rem",
    "padding": "2rem 1rem",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 2rem",
}


BUTTON_HIDEN = {
    "margin-top":"3rem",
    "margin-left":"11rem"
    }

BUTTON_STYLE = {
    "margin-top":"3rem",
    }
config = {'modeBarButtonsToRemove': ['toggleSpikelines','hoverCompareCartesian','zoom2d','zoomIn2d',
                                     'zoomOut2d','resetScale2d','autoScale2d','select2d','pan2d','lasso2d'],
          'displaylogo': False
}
sidebar = html.Div(
    [
        html.H4("Data Analysis", className="display-15"),
        html.Hr(),
        dbc.Nav(
            [  
        dcc.Upload([
        'Drag and Drop or ',
        html.A('Select a File')
        ], style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
        },id='upload'),html.Br(),
            dbc.Collapse(
            dbc.Card(dbc.CardBody([
            dbc.Collapse(dcc.Dropdown(
            value=[],    
            id="radioitems"
        ),id='sheet_values',is_open=False),
        html.Br(), 
            dbc.Collapse(html.Div(
            dbc.Card(dbc.CardBody([ html.H4('Select Columns'),
            dbc.Checklist(
            id="columns",
            value=[])]),style={"width": "13rem"}),style={"maxHeight": "150px", "overflow": "scroll","overflow-x": "hidden"},
            className="no-scrollbars"),
            id='columns_collapse',is_open=False
            ), 
        html.Br(), 
            dbc.Collapse(html.Div(
            dbc.Card(dbc.CardBody([ html.H4('Select Filters'),
            dbc.Checklist(
            id="Filters",
            value=[])]),style={"width": "13rem"}),style={"maxHeight": "150px", "overflow": "scroll","overflow-x": "hidden"},
            className="no-scrollbars"),
            id='Filters_collapse',is_open=False
            )]),outline=True, color="dark"),id='card_collapse',is_open=False),                            
                           
            html.Br(),
                
              html.Button(
                "Apply Filters",
                id="y_collapse-button",
                className="mr-1",
                # color="primary",
                n_clicks=0,
                style={'background-color': '#38ACEC',
                'border': 'none',
                'color': 'white',
                'padding': '10px 32px',
                'text-align': 'center',
                'text-decoration': 'none',
                'display': 'inline-block',
                'font-size': '16px',
                'border-radius': '4px'}
            ),
            html.Br(),
            dbc.Collapse(
                dbc.Card(dbc.CardBody([
                    html.Div(dbc.Card(dbc.CardBody([
                    html.H4(id="columnName"),
              dbc.Checklist(
                id="column",
                value=[],inline=True
                )]),style={"width": "13rem"}),style={"maxHeight": "200px", "overflow": "scroll","overflow-x": "hidden"},
                className="no-scrollbars"),
            html.Br(),    
             dbc.Collapse(
                #  html.Br(),
                html.Div(dbc.Card(dbc.CardBody([
                    html.H4(id="columnName1"),
              dbc.Checklist(
                id="column1",
                # options=[{"label": o, "value": o} for o in df['Year'].unique()],
                value=[]
                )]),style={"width": "13rem"}),style={"maxHeight": "200px", "overflow": "scroll","overflow-x": "hidden"},
                className="no-scrollbars"),                                
                id="column1_collapse",
                is_open=False) ,html.Br(),
                dbc.Collapse(html.Div(
                dbc.Card(dbc.CardBody([ html.H4(id="columnName2"),
                dbc.Checklist(
                id="column2",
                value=[])]),style={"width": "13rem"}),style={"maxHeight": "200px", "overflow": "scroll","overflow-x": "hidden"},
                className="no-scrollbars"),
                id='column2_collapse',is_open=False,
                ),html.Br(),
                dbc.Collapse(html.Div(
                dbc.Card(dbc.CardBody([ html.H4(id="columnName3"),
                dbc.Checklist(
                id="column3",
                value=[])]),style={"width": "13rem"}),style={"maxHeight": "200px", "overflow": "scroll","overflow-x": "hidden",
                ".inner-border":"-webkit-scrollbar"},className="no-scrollbars"
                ),
                id='column3_collapse',is_open=False,
                ),html.Br(),
                dbc.Collapse(html.Div(
                dbc.Card(dbc.CardBody([ html.H4(id="columnName4"),
                dbc.Checklist(
                id="column4",
                value=[])]),style={"width": "13rem"}),style={"maxHeight": "200px", "overflow": "scroll",
                "overflow-x": "hidden","background": "transparent"},className="no-scrollbars"),
                id='column4_collapse',is_open=False,
                )]),
              outline=True, color="dark"),                                
                id="contract_collapse",
                is_open=False),  
            html.Br(),                                 
               html.Br(),                             
               html.Button(id="submit-button", className="mr-1", n_clicks=0,
                           style={'background-color': '#38ACEC',
                                  'border': 'none',
                                  'color': 'white',
                                  'padding': '10px 32px',
                                  'text-align': 'center',
                                  'text-decoration': 'none',
                                  'display': 'inline-block',
                                  'font-size': '16px',
                                  'border-radius': '4px'}), 
    ], vertical=True,
    pills=True)
    ],
    id='sidebar',
    style=SIDEBAR_STYLE,className="no-scrollbars"
)



content = html.Div(id="page-content1", style=CONTENT_STYLE,)
app.layout = html.Div([dcc.Location(id='page-2-display-value'),
            sidebar, content, html.Br(),dcc.Loading(id="loading-1",type="default",
            children=html.Div(id="loading-output-1"),className='_dash-loading-callback'),
            dcc.Store(id='side_click'),dcc.ConfirmDialog(id='confirm-danger',
        message='Graph size too large if you want to download it click ok'),dcc.Store(id='image-size'),
        dcc.Download(id="download-image")])

def parse_data(contents, filename,opt,value):
    global df
    if opt is None:
        opt=0
    if contents:
        content_type, content_string = contents.split(",")
        # print(len(opt))
        decoded = base64.b64decode(content_string)
        if (len(opt)>1) and (len(value)>0) :
            # print(value)
            xl = pd.ExcelFile(io.BytesIO(decoded))
            df=pd.read_excel(xl,sheet_name=value)
            return df
        elif (len(opt)==1) or (len(opt)==0):
            if "csv" in filename:
                # Assume that the user uploaded a CSV or TXT file
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            elif ("xls" in filename) or ('xlsx' in filename):
                print(filename)
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
            elif ("txt" in filename) or ("tsv" in filename):
                # Assume that the user upl, delimiter = r'\s+'oaded an excel file
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), delimiter=r"\s+")
            # except Exception as e:
            #     print(e)
            #     return html.Div(["There was an error processing this file."])

        #     return df    
        # def data_disply(contents, filename):
        #     if contents:
        #         contents = contents[0]
        #         filename = filename[0]
        #         df = parse_data(contents, filename)
            # return df
            return df

@app.callback(Output("y_collapse-button","hidden"),
    [Input("columns","value"),
    Input("Filters","value")]) 
def applyFilters_collapse(value1,value2):
    if (len(value1)>0) and (len(value2)>0):
        return False
    return True
@app.callback(Output("side_click","data"),
    [Input("upload", "contents"), Input("upload", "filename"),
    Input('radioitems','options'),
    Input('radioitems','value')])
def data(contents, filename,opt,value):
    if opt is None:
        opt=[]
    if len(opt)>1:
        if (contents) and (len(value)>0):
            df1=parse_data(contents, filename,opt,value)
            return df1.to_dict('records')
    elif (len(opt)==1) or (len(opt)==0):
        if contents:
            df1=parse_data(contents, filename,opt,value)
            print(df1)
            return df1.to_dict('records')

@app.callback(
    Output("contract_collapse", "is_open"),
    [Input("y_collapse-button", "n_clicks")],
    [State("contract_collapse", "is_open")],
)
def y_toggle_collapse(n, is_open):
    if n :
        return not is_open
    return is_open

@app.callback(Output('column','options'),
    Output("columnName","children"),
    [Input("side_click","data"),
    Input("Filters","value")])
def first_filter(data,values):
    # try:
    if (data) and (len(values)>0):
        data=pd.DataFrame(data)
        # print([{"label":x,"value":x} for x in data[values[0]].unique()])
        data=data[data[values[0]].isnull()==False]

        return [{"label":x,"value":x} for x in data[values[0]].unique()],values[0]
    else:
        return [],''    
    # except:
    #     print("exit")
    #     return [],''

@app.callback(Output('column1_collapse','is_open'),
            [Input('column','value'),Input('column1','options')],
            # [State("check_collapse", "is_open")]
)
def collapse1(value,opt):
    # print(len(value))
    if (len(value)>0) and (len(opt)>0):
        return True
    return False

@app.callback(Output('column1','options'),
    Output("columnName1","children"),
    [Input("side_click","data"),
    Input("Filters","value")])
def second_filter(data,values):
    # try:
    if (data) and (len(values)>1):
        data=pd.DataFrame(data)
        data=data[data[values[1]].isnull()==False]
        # print([{"label":x,"value":x} for x in data[values[0]].unique()])
        return [{"label":x,"value":x} for x in data[values[1]].unique()],values[1]
    else:
        return [],'' 

@app.callback(Output('column2_collapse','is_open'),
            [Input('column1','value'),Input('column2','options')],
            # [State("check_collapse", "is_open")]
)
def collapse2(value,opt):
    # print(len(value))
    if (len(value)>0) and (len(opt)>0):
        return True
    return False

@app.callback(Output('column2','options'),
    Output("columnName2","children"),
    [Input("side_click","data"),
    Input("Filters","value")])
def third_filter(data,values):
    # try:
    if (data) and (len(values)>2):
        data=pd.DataFrame(data)
        data=data[data[values[2]].isnull()==False]
        # print(data[values[2]].isnull().sum())
        # print([{"label":x,"value":x} for x in data[values[0]].unique()])
        return [{"label":x,"value":x} for x in data[values[2]].unique()],values[2]
    else:
        return [],'' 

@app.callback(Output('column3_collapse','is_open'),
            [Input('column2','value'),Input("column3","options")],
            # [State("check_collapse", "is_open")]
)
def collapse3(value,opt):
    # print(len(value))
    if (len(value)>0) and (len(opt)>0):
        return True
    return False

@app.callback(Output('column3','options'),
    Output("columnName3","children"),
    [Input("side_click","data"),
    Input("Filters","value")])
def four_filter(data,values):
    # try:
    if (data) and (len(values)>3):
        data=pd.DataFrame(data)
        data=data[data[values[3]].isnull()==False]
        # print([{"label":x,"value":x} for x in data[values[0]].unique()])
        return [{"label":x,"value":x} for x in data[values[3]].unique()],values[3]
    else:
        return [],''   

@app.callback(Output('column4_collapse','is_open'),
            [Input('column3','value'),Input("column4","options")],
            # [State("check_collapse", "is_open")]
)
def collapse3(value,opt):
    # print(len(value))
    if (len(value)>0) and (len(opt)>0):
        return True
    return False

@app.callback(Output('column4','options'),
    Output("columnName4","children"),
    [Input("side_click","data"),
    Input("Filters","value")])
def four_filter(data,values):
    # try:
    if (data) and (len(values)>4):
        data=pd.DataFrame(data)
        data=data[data[values[4]].isnull()==False]
        # print([{"label":x,"value":x} for x in data[values[0]].unique()])
        return [{"label":x,"value":x} for x in data[values[4]].unique()],values[4]
    else:
        return [],''  
# @app.callback(Output('browsers','options'),
#     [Input('year','value')])

# def Quarter_value(n):
#     data=df.loc[df['Year'].isin(n),['Quarters']]
#     return[{"label": 'Q'+str(x), "value": x} for x in data['Quarters'].unique()]    



# @app.callback(
#     Output('submit-button', 'hidden'),
#     [Input('y_collapse-button','n_clicks')]
# )
# def show_button(n_clicks):
#       if (n_clicks%2 == 0):
#            return True
#       else:
#            return False
@app.callback(Output('card_collapse','is_open'),
    [Input("upload", "contents"),Input("y_collapse-button","n_clicks")])
def card(content,nclick):
    # print(nclick%2)
    if (content) and (nclick%2==0):
        return True
    elif nclick%2!=0:
        return False

@app.callback(Output('columns_collapse','is_open'),
    [Input("upload", "contents"),Input('radioitems','options'),
    Input('radioitems','value')])
def column_collapase(contents,options,value):
    if options is None:
        options=[]
    if len(options)>1:
        if (contents) and (len(value)>0):
            return True
        return False
    elif (len(options)==1) or (len(options)==0):
        if contents:
            return True
        return False

@app.callback(Output('Filters_collapse','is_open'),
    [Input('columns','value')])
def filter_collapse(value):
    if len(value)>0:
        return True
    return False

@app.callback(Output('sheet_values','is_open'),
    [Input("upload", "contents"),Input("radioitems",'options')])
def options_collapse(file,options):
    if options is None:
        options=[]
    if (file) and (len(options)>1):
        return True
    return False

@app.callback(Output("radioitems","options"),
        [Input("upload", "contents"), Input("upload", "filename")])
def options1(contents, filename):
    value=list()
    
    if (contents):
        if ("xlsx" in filename) or ("xls" in filename):
            content_type, content_string = contents.split(",")

            decoded = base64.b64decode(content_string)
        #     # try:
            xl = pd.ExcelFile(io.BytesIO(decoded))
            [value.append(y)for y in xl.sheet_names]
    # print(len(value))
    if len(value)>0:    
        return [{'label':x,'value':x} for x in value]
    else:
        return [] 
        # except:
        #     return []

@app.callback(Output('columns','options'),
    [Input("side_click","data"),Input('radioitems','options'),
    Input('radioitems','value')])
def column_names(data,opt,value):
    # print(opt)
    # print(data)
    if opt is None:
        opt=[]
    columns=list()
    if len(opt)>1:
        if (data) and (len(value)>0):
            df=pd.DataFrame(data)
            # print(df)
            [columns.append(x) for x in df.columns]
        # print([{'label':x,'value':x} for x in columns])         
    elif (len(opt)==1) or (len(opt)==0):
        if (data):
            df=pd.DataFrame(data)
            # print(df)
            [columns.append(x) for x in df.columns]
        # print([{'label':x,'value':x} for x in columns])    
    return [{'label':x,'value':x} for x in columns]

@app.callback(Output('Filters','options'),
    [Input("side_click","data"),Input('radioitems','options'),
    Input('radioitems','value'),Input("Filters","value")])
def column_names(data,opt,value,value1):
    columns=list()
    # print(opt)
    if opt is None:
        opt=[]
    if (len(opt)>1):
        if (data) and (len(value)>0):
            df=pd.DataFrame(data)
            # print(df)
            [columns.append(x) for x in df.columns]
        # print([{'label':x,'value':x} for x in columns])         
    elif (len(opt)==1) or (len(opt)==0) or (opt is None):
        if (data):
            df=pd.DataFrame(data)
            # print(df)
            [columns.append(x) for x in df.columns]
        # print([{'label':x,'value':x} for x in columns])
    if len(value1)==5:
        options=list()
        for i in df.columns:
            if i in value1:
                options.append({'label':i,'value':i})
            else:
                options.append({'label':i,'value':i,"disabled": True})
        return options
    else:    
        return [{'label':x,'value':x} for x in columns]

@app.callback(Output('column_collapse','is_open'),
    [Input('upload','contents')])
def column_collapse(content):
    if content:
        return True
    return False  

@app.callback(Output('submit-button','children'),
    [Input("submit-button","n_clicks")])
def button_name(n_clicks):
    if n_clicks%2==0:
        return ["Generate Graph"]
    elif n_clicks%2!=0:
        return ["Back To Grid"]

@app.callback(Output('confirm-danger','displayed'),
            [Input('image-size','data')])
def display_conifm(value):
    if int(value)>1000:
        return True
    return False
@app.callback(Output('download-image','data'),
    [Input('confirm-danger','submit_n_clicks')]) 
def download_image(n_clicks):
    # print(n_clicks)
    if n_clicks is None:
        n_clicks=0
    # if (n_clicks is None):
    #     return []
    if (int(n_clicks)>0):
        return dcc.send_file("assets\\root.png") 

loc_fun={
        1:'df1.loc[df1[filters[0]].isin(value),:]',
        2:'df1.loc[(df1[filters[0]].isin(value))&(df1[filters[1]].isin(value1)),:]',
        3:"df1.loc[(df1[filters[0]].isin(value))&(df1[filters[1]].isin(value1))&(df1[filters[2]].isin(value2)),:]",
        4:"""df1.loc[(df1[filters[0]].isin(value))&(df1[filters[1]].isin(value1))&(df1[filters[2]].isin(value2))&
        (df1[filters[3]].isin(value3)),:]""",
        5:"""df1.loc[(df1[filters[0]].isin(value))&(df1[filters[1]].isin(value1))&(df1[filters[2]].isin(value2))&
        (df1[filters[3]].isin(value3))&(df1[filters[4]].isin(value4)),:]"""}


len_fun={
        1:"[len(value)]",
        2:"[len(value),len(value1)]",
        3:"[len(value),len(value1),len(value2)]",
        4:"[len(value),len(value1),len(value2),len(value3)]",
        5:"[len(value),len(value1),len(value2),len(value3),len(value4)]"}

graph_sorted={2:"{columns[0]:len(final_data[columns[0]].unique()),columns[1]:len(final_data[columns[1]].unique())}",
            3:"""{columns[0]:len(final_data[columns[0]].unique()),columns[1]:len(final_data[columns[1]].unique()),
                columns[2]:len(final_data[columns[2]].unique())}""",
            4:"""{columns[0]:len(final_data[columns[0]].unique()),columns[1]:len(final_data[columns[1]].unique()),
                columns[2]:len(final_data[columns[2]].unique()),columns[3]:len(final_data[columns[3]].unique())}"""}


@app.callback(Output("submit-button","hidden"),
    [Input("Filters","value"),Input("column","value"),
    Input('column1',"value"),Input('column2',"value"),
    Input("column3","value"),Input("column4","value")])
def generateGraph(filters,value,value1,value2,value3,value4):
    # print(value1)
    if len(filters)>0:
        valueslen=eval(len_fun[len(filters)])
        print(valueslen)
        if all(valueslen)>0:
            return False
        return True
    else:
        return True


@app.callback([Output("page-content1","children"),
     Output("loading-output-1", "style"),Output('image-size','data')],   
    [Input('columns','value'),Input("side_click","data"),Input("Filters","value"),
    Input("column","value"),Input('column1',"value"),Input('column2',"value"),
    Input("column3","value"),Input("column4","value"),Input("submit-button","n_clicks")])
def output_data(columns,data,filters,value,value1,value2,value3,value4,n_clicks):
    if len(filters)>0:
        # print(eval(len_fun[len(filters)]))
        lenValues=eval(len_fun[len(filters)])
        # lenValues.append(len(columns))
        if (data) and (all(lenValues)>0) and (n_clicks%2 == 0):
            df1=pd.DataFrame(data)
            filter_data=eval(loc_fun[len(filters)])
            final_data=filter_data.loc[:,columns]
            time.sleep(1)
            return dash_table.DataTable(final_data.to_dict('records'), [{"name": i, "id": i} for i in final_data.columns],
            style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px',
            'color': 'black',
            'backgroundColor': 'white',
            'border': '1px solid black'
            },style_cell_conditional=[ 
                {"if": {"column_id": c}, "textAlign": "center"} for c in final_data.columns
            ],
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }],
        style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold',
        'border': '1px solid black',
        "textAlign": "center"
    },style_table={"width":"950px"},
    ),{"align":"center"},'0'
        elif (all(lenValues)>0) and (n_clicks%2 != 0):
            df1=pd.DataFrame(data)
            filter_data=eval(loc_fun[len(filters)])
            final_data=filter_data.loc[:,columns]
            # print(final_data)
            listAlphabets=list(string.ascii_uppercase)+list(string.ascii_lowercase)
            if (len(columns)>1):
                keyValue=len(columns)
                if len(columns)>4:
                    keyValue=4
                columns=eval(graph_sorted[keyValue])
                columns={k:j for k,j in sorted(columns.items(),key=lambda item:item[1])}
                columns=list(columns.keys())
            else:
                columns=columns    
            root = AnyNode(id="Hierarchy")
            rootnode=dict()
            # print(rootnode)
            try:
                for i,j in enumerate(final_data[columns[0]].unique()):
                    name=re.sub(r'[\s\W]','',str(j))
                    rootnode[f"s{i}"]=j
                    globals()[f"s{i}"] = AnyNode(id=j)
            # print(rootnode)
            except:
                []
            try:    
                subnode={}
                for key,value in rootnode.items():
                    subNode_Data=final_data.loc[final_data[columns[0]]==value,[columns[1]]]
                    for i,j in enumerate(subNode_Data[columns[1]].unique()):
                        name=re.sub(r'[\s\W]','',str(j))
                        subnode[f"s{name}{listAlphabets[i]}"]=j
                        globals()[f"s{name}{listAlphabets[i]}"] = AnyNode(id=j, parent=eval(key))
                        listAlphabets.remove(listAlphabets[i])
            except:
                []
            try:

                # print(subnode)        
                subnode1={} 
                subnode_test=subnode.copy()            
                for key,value in rootnode.items():
                    subNode_Data=final_data.loc[final_data[columns[0]]==value,:]
                    value_check=[]
                    for key1,value1 in list(subnode_test.items()):
                        if value1 not in value_check:
                            subNode_Data1=subNode_Data.loc[subNode_Data[columns[1]]==value1,:]
                            value_check.append(value1)
                            # print(value_check)
                        # print(subNode_Data1)
                    
                            for i,j in enumerate(subNode_Data1[columns[2]].unique()):
                                # print(key1)
                                name=re.sub(r'[\s\W]','',str(j))
                                subnode1[f"s{name}{listAlphabets[i]}"]=j
                                globals()[f"s{name}{listAlphabets[i]}"] = AnyNode(id=j, parent=eval(key1))
                                listAlphabets.remove(listAlphabets[i])
                                try:
                                    if len(subnode_test)>1:
                                        subnode_test.pop(key1)
                                except:
                                    pass        
                        else:
                            pass
            except:
                [] 



            # print(subnode) 
            # print(subnode1) 
            try:       
                subnode2={} 
                subnode_test=subnode.copy()
                subnode1_test=subnode1.copy()            
                for key,value in rootnode.items():
                    subNode_Data=final_data.loc[final_data[columns[0]]==value,:]
                    # print(subnode1_test)
                    value_check=[]
                    for key1,value1 in list(subnode_test.items()):
                        if value1 not in value_check:
                            subNode_Data1=subNode_Data.loc[subNode_Data[columns[1]]==value1,:]
                            value_check.append(value1)
                            # print(value_check)
                        # print(subNode_Data1)
                            value_check1=[]
                        # key_check=[]
                            for key2,value2 in list(subnode1_test.items()):
                                if value2 not in value_check1:
                                    subNode_Data2=subNode_Data1.loc[subNode_Data1[columns[2]]==value2,:]
                                    value_check1.append(value2)
                                    # key_check.append(key2)
                                    print(subNode_Data2)
                                    for i,j in enumerate(subNode_Data2[columns[3]].unique()):
                                        # print(key2)
                                        name=re.sub(r'[\s\W]','',str(j))
                                        subnode2[f"s{name}{listAlphabets[i]}"]=j
                                        globals()[f"s{name}{listAlphabets[i]}"] = AnyNode(id=j, parent=eval(key2))
                                        listAlphabets.remove(listAlphabets[i])

                                        try:
                                            if len(subnode_test)>1:
                                                subnode_test.pop(key1)                                            
                                            if len(subnode1_test)>1:
                                                subnode1_test.pop(key2)
                                        except:
                                            pass  
                                else:
                                    pass                

                        else:
                            pass            
            except:
                []
                 
                                   
            # print(subnode1)
            # try:            
            # subnode2={}
            # subnode_test=subnode.copy()
            # subnode1_test=subnode1.copy()  

            # for key,value in rootnode.items():
            #     subNode_Data=final_data.loc[final_data[columns[0]]==value,:]
            #     value_check=[]
            #     value_check1=[]
            #     # print(subnode_test)
            #     # print(subnode1_test) 
            #     for key1,value1 in list(subnode_test.items()):
            #         if value1 not in value_check:
            #             subNode_Data1=subNode_Data.loc[subNode_Data[columns[1]]==value1,:]
            #             value_check.append(value1)
            #             # print(value_check)

                                
                        
            #             # print(value_check1)
            #             for key2,value2 in list(subnode1_test.items()):
            #                 if value2 not in value_check1:
            #                     print(value2)
            #                     subNode_Data2=subNode_Data1.loc[subNode_Data1[columns[2]]==value2,:]
            #                     value_check1.append(value2)
            #                     # print(len(subnode1_test))
            #                     # print(subNode_Data2)

                                
            #             # print(subNode_Data2)
            #                     for i,j in enumerate(subNode_Data2[columns[3]].unique()):
            #                         # print(subnode1_test)
            #                         print(key2)
            #                         name=re.sub(r'[\s\W]','',str(j))
            #                         subnode2[f"s{name}{listAlphabets[i]}"]=j
            #                         globals()[f"s{name}{listAlphabets[i]}"] = AnyNode(id=j, parent=eval(key2))
            #                         listAlphabets.remove(listAlphabets[i])
            #                         # print(subnode1_test)
            #                         # if (len(subnode_test)>1):    
            #                         #     subnode_test.pop(key1)
            #                         # if (len(subnode1_test)>1):
            #                         #     subnode1_test.pop(key2)
            #                         # print(subnode_test)

            #                 else:
            #                     pass
            #         else:
            #             pass 
            # except:
            #     []                           
            # print(subnode2)
            # subnode3={}
            # subnode_test=subnode.copy()
            # subnode1_test=subnode1.copy()
            # subnode2_test=subnode2.copy()
            # for key,value in rootnode.items():         
            #     subNode_Data=final_data.loc[final_data[columns[0]]==value,:]
            #     value_check=[]
            #     for key1,value1 in list(subnode_test.items()):
            #         if value1 not in value_check:
            #             subNode_Data1=subNode_Data.loc[subNode_Data[columns[1]]==value1,:]
            #             value_check.append(value1)

            #             value_check1=[]
            #             for key2,value2 in list(subnode1_test.items()):
            #                 if value2 not in value_check1:
            #                     subNode_Data2=subNode_Data1.loc[subNode_Data1[columns[2]]==value2,:]
            #                     value_check1.append(value2)
            #                     if (len(subnode1_test)>1) and (len(subnode1_test)>1):
            #                         subnode1_test.pop(key2)
            #                         subnode_test.pop(key1)                                                  
            #                     value_check2=[]
            #                     for key3,value3 in list(subnode2_test.items()):
            #                         if  value3 not in value_check2:
            #                             subNode_Data3=subNode_Data2.loc[subNode_Data2[columns[3]]==value3,:] 
            #                             value_check2.append(value3)
            #                             if len(subnode2_test)>1:
            #                                 subnode2_test.pop(key3)
            #                                 print(subnode2_test)  
            #                             # print(subNode_Data3)         
            #                             for i,j in enumerate(subNode_Data3[columns[4]].unique()):
            #                                 # print(j)
            #                                 name=re.sub(r'[\s\W]','',str(j))
            #                                 subnode3[f"{listAlphabets[i]}s{name}"]=j
            #                                 print(key3)
            #                                 globals()[f"{listAlphabets[i]}s{name}"] = AnyNode(id=j, parent=eval(key3))

            #                                 # if len(subnode2_test)>1:
            #                                 #     subnode2_test.pop(key3) 
                        
            #                         else:
            #                             pass
            #                 else:
            #                     pass           
            #         else:
            #             pass        
            # print(subnode3)
            UniqueDotExporter(s0,
                nodeattrfunc=lambda n: 'shape=box,label="%s"' % (n.id)).to_picture('root.jpg')             
            image_filename = r'C:\Users\Gopi\OneDrive - PiLog India Private Limited\Desktop\spendHierarchy\root.jpg' # replace with your own image
            img=Image.open(image_filename)
            width,height = img.size
            print(width,height)
            encoded_image = base64.b64encode(open(image_filename, 'rb').read())
 
            return (dbc.Card(dbc.CardBody(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))),
            style={"width":f"{width+25}px"}),{"align":"center"},width)
        else:
            return dbc.Card([
                dbc.CardBody([
                    html.H3("Welcome to DashBoard", className="card-title"),
                    # html.P("Click on '☰ ' to get or collapse Sidebar."),
                    html.P("Select required values in the Sidebar to Generate Graphs.",className='card-text')
                    ])
                ],color='secondary',inverse=True),{"align":"center"},'0'
    
    else:
        return dbc.Card([
            dbc.CardBody([
                html.H3("Welcome to DashBoard", className="card-title"),
                # html.P("Click on '☰ ' to get or collapse Sidebar."),
                html.P("Select required values in the Sidebar to Generate Graphs.",className='card-text')
                ])
            ],color='secondary',inverse=True),{"align":"center"},'0'
 
if __name__ == "__main__":
    app.run_server(port=8000)
