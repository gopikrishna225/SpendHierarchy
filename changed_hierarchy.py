
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
import datetime as dt
import dash
import pandas as pd
from dash.exceptions import PreventUpdate
import numpy as np
import graphviz
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image
import string
from skimage import io
import base64
import os
from dash import dash_table
os.environ["PATH"] += os.pathsep + 'C:/ProgramData/Anaconda3/Library/bin/graphviz/'
# import cx_Oracle
# from sqlalchemy import types, create_engine

pilog_logo = "https://www.piloggroup.com/img/header/logo-header.png"

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content1')
])

app = dash.Dash(suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.CERULEAN])


# data=pd.ExcelFile(r'C:\Users\gopik\Downloads\QAFAC Spend Analysis Rev1-03.01.22.xlsx')
data=pd.ExcelFile(r'./QAFAC Spend Analysis Rev1-03.01.22.xlsx')
df = pd.read_excel(data,sheet_name='Data')
table=pd.pivot_table(df,values=['Item','Value in USD'],index=['Year','Contract'],aggfunc={'Item':np.sum,'Value in USD':np.sum})
table.reset_index(inplace=True)
df['Document_Date_month']=df['Document Date'].dt.month
table_month=pd.pivot_table(df,values=['Item','Value in USD'],index=['Year','Contract','Document_Date_month'],aggfunc={'Item':np.sum,'Value in USD':np.sum})
table_month.reset_index(inplace=True)
target=[]
for rate in df['Document_Date_month']:
    if(rate==1)or(rate==2)or(rate==3):
        target.append(1)
    elif(rate==4)or(rate==5)or(rate==6):
        target.append(2)
    elif(rate==7)or(rate==8)or(rate==9):
        target.append(3)
    else:
        target.append(4)
df['Quarters']=target
table_quarter=pd.pivot_table(df,values=['Item','Value in USD'],index=['Year','Contract','Quarters'],aggfunc={'Item':np.sum,'Value in USD':np.sum})
table_quarter.reset_index(inplace=True)
df.sort_values(by=['Year','Quarters'],inplace=True)

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
    ".inner-border":"-webkit-scrollbar",
    # "display": "none"           
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
        html.H4("Spend Analysis", className="display-15"),
        html.Hr(),
        dbc.Nav(
            [
            html.Br(),                          
            html.Br(),            
              dbc.Button(
                "Spend",
                id="y_collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            
            dbc.Collapse(
                dbc.Card(dbc.CardBody([
                    html.H4('Contract',className="card-title"),
              dcc.Dropdown(
                id="contract",
                options=[{"label": o, "value": o} for o in df['Contract'].unique()],
                multi=True,
                value=[]
                ),
            html.Br(),    
             dbc.Collapse(
                #  html.Br(),
                dbc.Card(dbc.CardBody([
                    html.H4('Year',className="card-title"),
              dcc.Checklist(
                id="year",
                # options=[{"label": o, "value": o} for o in df['Year'].unique()],
                value=[]
                )])),                                
                id="year_collapse",
                is_open=False) ,html.Br(),
                dbc.Collapse(
                dbc.Card(dbc.CardBody([ html.H4('Quarters'),
                dcc.Checklist(
                id="browsers",
                value=[])])),
                id='check_collapse',is_open=False,
                ),html.Br(),
                dbc.Collapse(html.Div(
                dbc.Card(dbc.CardBody([ html.H4('Material Group'),
                dcc.Checklist(
                id="material_group",
                value=[])])),style={"maxHeight": "200px", "overflow": "scroll","overflow-x": "hidden",
                ".inner-border":"-webkit-scrollbar"},className="no-scrollbars"
                ),
                id='material_collapse',is_open=False,
                ),html.Br(),
                dbc.Collapse(html.Div(
                dbc.Card(dbc.CardBody([ html.H4('Currency'),
                dcc.Checklist(
                id="currency",
                value=[])])),style={"maxHeight": "200px", "overflow": "scroll",
                "overflow-x": "hidden","background": "transparent"},className="no-scrollbars"),
                id='currency_collapse',is_open=False,
                )]),
              outline=True, color="dark"),                                
                id="contract_collapse",
                is_open=False),  
            html.Br(),                                 
               html.Br(),                             
               html.Button(id="submit-button", className="mr-1", n_clicks=0, type='submit',
                           style={'background-color': '#38ACEC',
                                  'border': 'none',
                                  'color': 'white',
                                  'padding': '15px 32px',
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



content = html.Div(id="page-content1", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Store(id='side_click'),
    dcc.Location(id='page-2-display-value'), sidebar, content
                    ])


@app.callback(
    Output("contract_collapse", "is_open"),
    [Input("y_collapse-button", "n_clicks")],
    [State("contract_collapse", "is_open")],
)
def y_toggle_collapse(n, is_open):
    if n :
        return not is_open
    return is_open

@app.callback(Output('material_collapse','is_open'),
    Input('browsers','value'))
def material(value):
    if len(value)>0:
        return True
    return False        

@app.callback(Output('material_group','options'),
    [Input('year','value'),
    Input('browsers','value')])
def material_values(year,quarter):
    material_data=df.loc[(df['Year'].isin(year)) & (df['Quarters'].isin(quarter)),['Material Group']] 
    return[{'label':x,'value':x} for x in material_data['Material Group'].unique()]

@app.callback(Output('currency_collapse','is_open'),
    Input('material_group','value'))
def material(value):
    if len(value)>0:
        return True
    return False        

@app.callback(Output('currency','options'),
    [Input('year','value'),
    Input('browsers','value'),
    Input('material_group','value')])
def material_values(year,quarter,material_value):
    currency_data=df.loc[(df['Year'].isin(year)) & (df['Quarters'].isin(quarter)) & 
                                                (df['Material Group'].isin(material_value)),['Currency']] 
    return[{'label':x,'value':x} for x in currency_data['Currency'].unique()]


@app.callback(Output('year','options'),
    [Input('contract','value')])
def year_values(values):
    year_data=df.loc[df['Contract'].isin(values),['Year']]
    # print([{'label':x,'value':x} for x in year_data['Year'].unique()])
    return[{'label':x,'value':x} for x in year_data['Year'].unique()]

@app.callback(Output('year_collapse','is_open'),
            [Input('contract','value')],
            # [State("check_collapse", "is_open")]
)
def year_collapse(value):
    # print(len(value))
    if len(value)>0:
        return True
    return False

@app.callback(Output('check_collapse','is_open'),
            [Input('year','value')],
            # [State("check_collapse", "is_open")]
)
def check_collapse(value):
    # print(len(value))
    if len(value)>0:
        return True
    return False

@app.callback(Output('browsers','options'),
    [Input('year','value')])
def Quarter_value(n):
    data=df.loc[df['Year'].isin(n),['Quarters']]
    return[{"label": 'Q'+str(x), "value": x} for x in data['Quarters'].unique()]    



@app.callback(
    Output('submit-button', 'hidden'),
    [Input('y_collapse-button','n_clicks')]
)
def show_button(n_clicks):
      if (n_clicks%2 == 0):
           return True
      else:
           return False

@app.callback(Output('submit-button','children'),
    [Input("submit-button","n_clicks")])
def button_name(n_clicks):
    if n_clicks%2==0:
        return ["Generate Graph"]
    elif n_clicks%2!=0:
        return ["Back To Grid"]

@app.callback(
    Output("page-content1", "children"),
    [Input("contract",'value'),
    Input("year",'value'),
    Input("browsers",'value'),
    Input('material_group','value'),
    Input('currency','value'),
    Input("submit-button",'n_clicks')]
)           
def date_content(value1,value2,value3,value4,value5,n):
    print(value1)
    filter_data=df.loc[(df['Contract'].isin( value1)) & (df['Year'].isin(list(value2))) & (df['Quarters'].isin(list(value3))) & 
    (df['Material Group'].isin(value4)) & (df['Currency'].isin(value5)),
    :]
    filter_data1=filter_data.loc[:,['Vendor','Contract','Item','Value in USD','Material','Class','Material Group','Currency']]

    # bar_layout = {"xaxis": {"title": 'Item','showgrid':False,"color":"white"}, 
    #               "yaxis": {"title": 'Value In USD','showgrid':False,"color":"white"},'plot_bgcolor':'rgba(0, 0, 0, 0)',
    #               'paper_bgcolor':'rgba(0, 0, 0, 0)','template':'plotly_dark','font':{'color':'white'},
    #               'title':'Bar Chart','hovermode':'closest','hoverdata':{'Material No.':True,
    #                                                                          'Net Value':True}}
    values=[len(value1),len(value2),len(value3),len(value4),len(value5)]
    if all(values) == 0:
        n=0
        return dbc.Card([
            dbc.CardBody([
                html.H3("Welcome to DashBoard", className="card-title"),
                # html.P("Click on '☰ ' to get or collapse Sidebar."),
                html.P("Select required values in the Sidebar to Generate Graphs.",className='card-text')
                ])
            ],color='secondary',inverse=True)
    elif all(values) > 0 and (n%2 == 0):
        return dash_table.DataTable(filter_data1.to_dict('records'), [{"name": i, "id": i} for i in filter_data1.columns],
          style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        'lineHeight': '15px',
        'color': 'black',
        'backgroundColor': 'white',
        'border': '1px solid black'
        },
        style_cell_conditional=[ 
                {"if": {"column_id": c}, "textAlign": "center"} for c in filter_data1.columns
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
    },style_header_conditional=[{"textAlign": "center"}],style_table={'minWidth': '100%'},
    css=[{"textAlign": "center"}])        
    elif (all(values) > 0) and (n%2 != 0):
        print(n)
        dot = graphviz.Digraph('SpendAnalysis', comment='The Round Table',format='png')  
        dot.attr('node', shape='box')    
        # dot.attr(rankdir='LR',) 
        contract=filter_data.loc[filter_data['Contract']=='Contract'] 
        non_contract=filter_data.loc[filter_data['Contract']=='Non Contract']
        print(contract)
        contract_items={}
        for i in contract['Year'].unique():
            amount=contract.loc[contract['Year'] == i,['Item']]
            contract_items[i]=amount['Item'].sum()

        Noncontract_items={}  
        for j in non_contract['Year'].unique():
            amount1=non_contract.loc[non_contract['Year'] == j,['Item']]
            Noncontract_items[j]=amount1['Item'].sum()
        spend_year={}  
        for k in contract['Year'].unique():
            spend=contract.loc[contract['Year'] == k,['Item','Value in USD']]
            spend_year[spend['Item'].sum()]=spend['Value in USD'].sum()
        spend_year1={}
        for l in non_contract['Year'].unique():
            spend1=non_contract.loc[non_contract['Year'] == l,['Item','Value in USD']]
            spend_year1[spend1['Item'].sum()]=spend1['Value in USD'].sum()

        currency_values={}
        currency_amount={}
        item_count={}
        for m in contract['Year'].unique():
            currency=contract.loc[contract['Year'] == m,['Item','Value in USD','Quarters']]
            currency_values[m]=list(currency['Quarters'].unique())
            # item_sum=currency['Item'].sum()
            for n in currency['Quarters'].unique():
                total_currency=currency.loc[currency['Quarters']==n,['Value in USD','Item']]
                currency_amount[total_currency['Item'].sum()]=total_currency['Value in USD'].sum()
                item_count[str(n)+str(m)]=total_currency['Item'].sum()

        currency_values1={}
        currency_amount1={}
        item_count1={}                
        for m in non_contract['Year'].unique():
            currency1=non_contract.loc[non_contract['Year'] == m,['Item','Value in USD','Quarters']]
            currency_values1[m]=list(currency1['Quarters'].unique())
            # item_sum1=currency1['Item'].sum()
            for n in currency1['Quarters'].unique():
                total_currency=currency1.loc[currency1['Quarters']==n,['Value in USD','Item']]
                currency_amount1[total_currency['Item'].sum()]=total_currency['Value in USD'].sum()  
                item_count1[str(n)+str(m)]=total_currency['Item'].sum()
        contract_size=contract['Year'].unique().size+1
        nonContract_size=non_contract['Year'].unique().size

        listAlphabets=list(string.ascii_uppercase)
        final_id1=listAlphabets
        final_id1.remove('Y')
        final_id1.remove('Z')
        listAlphabets1=list(string.ascii_lowercase)
        # items_id=listAlphabets1[:contract_size]
        # items_id1=listAlphabets1[contract_size:nonContract_size+contract_size]
        final_id=listAlphabets1+[i for i in range(0,10)]
        # spend_id=listAlphabets1[nonContract_size+contract_size:nonContract_size+contract_size*2]
        # spend_id1=listAlphabets1[nonContract_size+contract_size*2:(nonContract_size*2)+(contract_size*2)]
        # print(spend_id1)
        edge_values=[]
        dot.node('Y','Spend Analysis',fillcolor="yellow")
        # edge_values.append('YZ')
        # dot.node('Z', str("{:.2f}".format(float(filter_data['Value in USD'].sum()))))
        contract_ids={}
        for idx2,val in enumerate(filter_data['Contract'].unique()): 
            dot.node(final_id[idx2], str(val))
            edge_values.append('Y'+final_id[idx2])
            contract_ids[val]=final_id[idx2]
            final_id.remove(final_id[idx2])
        contract_id={}    
        for idx1,val1 in enumerate(contract['Year'].unique()):
            dot.node(final_id[idx1], str(val1))
            edge_values.append(contract_ids['Contract']+final_id[idx1])
            contract_id[val1]=final_id[idx1]
            final_id.remove(final_id[idx1])
        Noncontract_id={}
        for idx,val2 in enumerate(non_contract['Year'].unique()):
            dot.node(final_id[idx], str(val2))
            edge_values.append(contract_ids['Non Contract']+final_id[idx])
            Noncontract_id[val2]=final_id[idx]
            final_id.remove(final_id[idx])
        print(edge_values)
        # item_id={}    
        # for idx3,(key,val3) in enumerate(contract_items.items()):
        #     dot.node(items_id[idx3],str(val3))
        #     edge_values.append(contract_id[key]+items_id[idx3])
        #     item_id[val3]=items_id[idx3]
        # item_id1={}    
        # for idx4,(key,val4) in enumerate(Noncontract_items.items()):
        #     dot.node(items_id1[idx4],str(val4))
        #     edge_values.append(Noncontract_id[key]+items_id1[idx4])
        #     item_id1[val4]=items_id1[idx4]
        # final_id1=final_id+final_id1
        currency_id={}    
        for key,val5 in currency_values.items():
            for ind,valu in enumerate(val5):
                dot.node(final_id[ind],str(valu))
                edge_values.append(contract_id[key]+final_id[ind])
                currency_id[str(valu)+str(key)]=final_id[ind]
                final_id.remove(final_id[ind])
        currency_id1={}
        # print(final_id)
        
        for key,val6 in currency_values1.items():
            for ind1,valu1 in enumerate(val6):
                dot.node(final_id1[ind1],str(valu1))
                edge_values.append(Noncontract_id[key]+final_id1[ind1])
                currency_id1[str(valu1)+str(key)]=final_id1[ind1]
                final_id1.remove(final_id1[ind1]) 
        # print(currency_id.keys(),currency_amount.keys())
        spend_amount={}      
        for idx5,(key,val7) in enumerate(item_count.items()):
            # dot.node(str(final_id[idx5]),str(val7))
            dot.edge(currency_id[key],str(val7))
            # edge_values.append(currency_id[key]+str(final_id[idx5]))
            # spend_amount[val7]=str(final_id[idx5])
            # final_id.remove(final_id[idx5])
        spend_amount1={}
        for idx6,(key,val8) in enumerate(item_count1.items()):
            # dot.node(str(final_id[idx6]),str(val8))
            dot.edge(currency_id1[key],str(val8))
            # spend_amount1[val8]=str(final_id[idx6])
            # final_id.remove(final_id[idx6])  
        # spend_amount={}      
        for idx5,(key,val7) in enumerate(currency_amount.items()):
            # dot.node(str(final_id[idx5]),str("{:.2f}".format(val7)))
            dot.edge(str(key),str("{:.2f}".format(val7)))
            # spend_amount[val7]=final_id[idx5]
            # final_id.remove(final_id[idx5])
        # spend_amount1={}
        print(final_id1)
        for idx6,(key,val8) in enumerate(currency_amount1.items()):
            # dot.node(str(final_id[idx6]),str("{:.2f}".format(val8)))
            dot.edge(str(key),str("{:.2f}".format(val8)))
            # spend_amount1[val8]=final_id1[idx6]
            # final_id.remove(final_id[idx6])
        

        # for idx5,(key,val5) in enumerate(spend_year.items()):
        #     dot.node(spend_id[idx5],str("{:.2f}".format(float(val5))))
        #     edge_values.append(item_id[key]+spend_id[idx5])
        # for idx6,(key,val6) in enumerate(spend_year1.items()):
        #     dot.node(spend_id1[idx6],str("{:.2f}".format(float(val6))))
        #     edge_values.append(item_id1[key]+spend_id1[idx6]) 

        # dot.node('K',str(filter_data['Quarters'].unique()[0]))
        # dot.node('M',str(filter_data['Quarters'].unique()[1]))
        # dot.node('J',)
        # print(non_contract)
        print(edge_values)
        dot.edges(edge_values)
        # dot.edge('B', 'L', constraint='false')
        dot.render(directory='assets')
        # img=io.imread('assets\\SpendAnalysis.gv.png')
        # try:
        #     img = np.array(Image.open('doctest-output\\Spend Analysis.gv.png'))
        # except OSError:
        #     raise PreventUpdate
        # fig = go.Figure()
        # fig.add_trace(go.Scatter(x=filter_data['Item'], y=filter_data['Value in USD'], fill='tozeroy'))
        # fig.update_layout(xaxis={'title':'Item','showgrid':False},yaxis={'title':'Value In USD','showgrid':False},title='Area Chart',plot_bgcolor='rgba(0, 0, 0, 0)',
        # paper_bgcolor='rgba(0, 0, 0, 0)',font={'color':'white'},hovermode='y unified')  
        # fig = px.imshow(img, color_continuous_scale="gray", binary_string=False, zmin=50, zmax=200,height=835,width=539)
        # fig.update_layout(coloraxis_showscale=False)
        # fig.update_xaxes(showticklabels=False)
        # fig.update_yaxes(showticklabels=False)
        # fig.update_layout(hovermode=False)
        image_filename = 'assets\\SpendAnalysis.gv.png' # replace with your own image
        encoded_image = base64.b64encode(open(image_filename, 'rb').read())
        # return dbc.Card(dbc.CardBody([dcc.Graph(config=config,figure=fig)
        #         ])),
        return dbc.Card(dbc.CardBody(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))))
 
      


if __name__ == "__main__":
    app.run_server(port=8000)
