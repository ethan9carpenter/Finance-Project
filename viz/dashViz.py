import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime
from iexfinance.stocks import get_historical_data

app = dash.Dash()
app.config['suppress_callback_exceptions'] = True

def getData(ticker, start, end, what='close'):
    data = get_historical_data(ticker, start, end, output_format='pandas')
    data = data[what]
    data.name = ticker
    return data

def getCorrelations(data, otherData, maxShift, minShift=0, shiftFactor=1, neg=True):
    correlations = []
    data = data.shift(minShift-1)
    
    for _ in range(1+maxShift-minShift):
        data = data.shift(shiftFactor)
        corr = data.corr(otherData)
        if not neg and corr < 0:
            corr = -corr
        correlations.append(corr)
    return correlations

def children():
    graph = html.Div(id='graph')
    input1 = html.Div(children=[
        html.Div('Ticker to Predict'),
        dcc.Input(id='ticker1', value='', type='text')
        ])
    input2 = html.Div(children=[
        html.Div('Predictive Ticker'),
        dcc.Input(id='ticker2', value='', type='text')
        ])
    dayInput = html.Div(children=[
        html.Div('Max Day Shift'),
        dcc.Input(id='dayShift', value='', type='number')
        ])
    children = input1, input2, dayInput, graph
    
    return children

app.layout = html.Div(children=children())

inputs = [Input(component_id='ticker1', component_property='value'), 
     Input(component_id='ticker2', component_property='value'),
     Input(component_id='dayShift', component_property='value')]
output = Output(component_id='graph', component_property='children')

@app.callback(output, inputs)
def updateGraph(ticker1, ticker2, dayShift):
    try:
        tickData1 = getData(ticker1, start=datetime(2015, 1, 1), end=datetime(2018, 12, 31))
        tickData2 = getData(ticker2, start=datetime(2015, 1, 1), end=datetime(2018, 12, 31))
        
        corr = getCorrelations(tickData1, tickData2, int(dayShift))
        
        line = {'x': list(range(dayShift+1)), 
                'y': corr, 
                'name': 'How {} predicts {}'.format(ticker2, ticker1), 
                'type': 'line'}
        
        layout = {'title': 'How {} predicts {}'.format(ticker2.upper(), ticker1.upper()),
                  'xaxis': {'dtick': 1, 'title': '{} Date minus {} Date'.format(ticker1.upper(), ticker2.upper())},
                  'yaxis': {'title': 'Correlation Coefficient'}}

        return dcc.Graph(id='stock', figure={'data': [line], 'layout': layout})
    except Exception:
        return html.Div("Please enter valid tickers")
    
if __name__ == '__main__':
    app.run_server(debug=True)