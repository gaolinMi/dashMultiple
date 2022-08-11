
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import pandas as pd

app = Dash(__name__)
server = app.server

df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(df['Indicator Name'].unique(),
        'Fertility rate, total (births per woman)',
        id = 'xcolumn'),
        dcc.RadioItems(['Linear', 'Log'], 'Linear', id = 'xtype', inline = True)
        ], style = {'width': '48%', 'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(df['Indicator Name'].unique(),
        'Life expectancy at birth, total (years)',
        id = 'ycolumn'),
        dcc.RadioItems(['Linear', 'Log'], 'Linear', id = 'ytype', inline = True)
        ], style = {'width': '48%', 'float': 'right', 'display': 'inline-block'}),    
    
    dcc.Graph(id = 'indicatorGraph'),
    
    dcc.Slider(id = 'yearSlider', min = df['Year'].min(), max = df['Year'].max(),
               step = None, value = df['Year'].max(),
               marks = {str(yr):str(yr) for yr in df['Year'].unique()})
    ])

@app.callback(
    Output('indicatorGraph', 'figure'),
    Input('xcolumn', 'value'),
    Input('xtype', 'value'),
    Input('ycolumn', 'value'),
    Input('ytype', 'value'),
    Input('yearSlider', 'value')
    )
def update_graph(xc, xt, yc, yt, yr):
    dff = df[df['Year'] == yr]
    
    fig = px.scatter(x = dff[dff['Indicator Name'] == xc]['Value'], 
                     y = dff[dff['Indicator Name'] == yc]['Value'], 
                     hover_name = dff[dff['Indicator Name'] == yc]['Country Name'])
    
    fig.update_layout(margin={'l': 80, 'b': 80, 't': 50, 'r': 0}, hovermode='closest')
    
    fig.update_xaxes(title = xc,
                     type = 'linear' if xt == 'Linear' else 'log')
    
    fig.update_yaxes(title = yc,
                     type = 'linear' if yt == 'Linear' else 'log')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug = True)
    
    
