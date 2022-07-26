import dash
from dash.dependencies import Output, Input, State, ClientsideFunction
from dash import dcc
from dash import html
from dash import callback_context
import plotly.graph_objs as go
import plotly.io as plt_io
from collections import deque
import pandas as pd
import dash_extendable_graph as deg
from flask_login.utils import login_required
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# to be able to integrate the dash app into a flask app, we need to include it in a function and call it in the app.py file.
def create_dash_application(flask_app):
    credentials = {
    "type": "service_account",
    "project_id": "data-collection-354621",
    "private_key_id": "c0e8d6766f5ba18810ecfb9521883f8fb98fb040",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCm+J6VA4w+33PT\nTFhG42HNiFjdHet/EVTpUOTpRLeuL7zzFijuEFXZcHH9FkmP8u9GrIwXpkHwKiKp\n6UprqAMy6Ncxbn/N2sH73XiklxZiHZ1Sq7YZkrXz8D/J2iUxI5i5IvriSyBhHiVI\nXZuFFc418OQTmqueAbJdXw8Kg4JxpOOd9JUfmAe+27331NJj1v0I01jICw+PUPPH\norfTUdg8rEby8gp19MG/WZRXeIGXfMjyqT4h6Z9Xxs0P0cM1iB2hPMH8VYAzHpO3\nIkYFjCKgMTkbyIQ4N1s2iqYWE0VorchoO4W13mNkW+fxP8T0wnfeQOtSTaUMGdk0\nQzpULXotAgMBAAECggEAIGIOq5rtC9KdrajcZB88fDbJ+VSQtGvBmqCgTOeRcjx6\n+nBdTtKnO801pl64tKzqoDvdzcZmenRJlceTse57dFe5SLKEIgIf5j/NYqqU4kGZ\nHgwEfNA57s41KOpglTewqpNwsgvdA0jr9S2GeJjCji6ipXS1fScaF0bU7XaVCYIf\nlgqw8lPYVYhqO3Jv8vBO6/+5D0VX9rTT5cCgBMbJpzgs3B1JUH6cTdbBlycYiozw\nk3IPNqlWDpR1ddj4VA89GzCkIxDmP0pZcuRRl9XxWLHt6c15nIxULHOxUmWbWfgu\nLJ4M62xOH5nFb+uBO7nsrsBOVaG+obHeivOi0KxTkQKBgQDTUEw8bV0IL8g5VWoL\nRKriEv0nEY3J5FqF3sBQ163CrECS18B0ssbLd9w4aBoWG4GyWR7HtvF+Z++mI0Sf\nhRfiwZYoa+3KZ/c1yAGVP8TJ51embxQtb5U6O5/yHnBNX+I+qE+h2QVvXm0mW6Fn\n/Ks1JaDwTreVlbhDteYlgHmzZQKBgQDKR8qBa6vYFdf00la6zuLBVmYjtxC36mkR\nn3C9+7cg+UmSxG8jBke8fHV3III58epzDGlOvGhefSsWkEHjxY4BPfmxv8FmqAve\nsIZNIf4lZoTJtv+oSHp6JePUV4dM6pVLwqLMW98DwUt5Rmfoysp8UgccIwjT3e9r\nw/JRzA5TKQKBgDUx958WoN7YuHzGZcWkaagzw4q8PodedvNQWfV/9fwVxMOykH5Q\nKv85kzSX8Ek0b3foO3lnMm/x1kBqjHHj3Vl2Bkjyso/LkE33pX5e6TkyhbweJmQx\nvM1GCUO4KekwhBHl6PYDXfzlNnD7jCxTTP46FMOp7Uk4wYQ6HE/AgeKJAoGBAJdB\nGWavCV9Z7hKuGZY0TxB8t4FrSQANMyWvUFFvYF8yqNYrNmM9NfT2J6u9TkNf5ozC\nshfjADPvaoHDutFDjszU99n25foKHF4XJ0WT7oMu5ooi4YaHM7YUkQjdrllQa/Sr\nhKpE5Dzdk78Ka3aB9OkDOTfL5rTuFjJB4fdSG0AJAoGAXhXOj3fo3K2/48V/Dvfm\na73AWB8yerrBLcYghVCE5cMkG9CipTmMgHA/Dxis361sQs3zEsme/H6uflvwY7Rn\n5UkX3QfaBcxkqtzKC/R0HrHS5Ha+YoPDfhb9+mwZ5c8zjVceckG90fyYMzHMzOmY\npZCNifNVwf/rh5L5rBO3mjA=\n-----END PRIVATE KEY-----\n",
    "client_email": "data-updater@data-collection-354621.iam.gserviceaccount.com",
    "client_id": "107583909672954724121",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/data-updater%40data-collection-354621.iam.gserviceaccount.com"
    }


    # create our custom_dark theme from the plotly_dark template
    plt_io.templates["custom_dark"] = plt_io.templates["plotly_dark"]

    # set the paper_bgcolor and the plot_bgcolor to a new color
    plt_io.templates["custom_dark"]['layout']['paper_bgcolor'] = '#30404D'
    plt_io.templates["custom_dark"]['layout']['plot_bgcolor'] = '#30404D'

    # you may also want to change gridline colors if you are modifying background
    plt_io.templates['custom_dark']['layout']['yaxis']['gridcolor'] = '#4f687d'
    plt_io.templates['custom_dark']['layout']['xaxis']['gridcolor'] = '#4f687d'

    X = deque(maxlen=1000)
    X.append(1)
    Y = deque(maxlen=1000)
    Y.append(1)

    # define the function to get the data  
    def get_currency_data(n_rows: int, currency: str):
        gsheetid='1shHL1obVZ6lgzl0xOOHHHxc9AlA5XcfQVs1Q4Hc93eE'
        if n_rows == 1:
            sheet_name = currency + "1"
        else:
            sheet_name=currency
        gsheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, sheet_name)
        df = pd.read_csv(gsheet_url)
        df = df.iloc[:n_rows]
        df = df.iloc[::-1]
        return df

    # this blank fig function makes us avoid seeing the base dash graph template 
    def blank_fig():
        fig = go.Figure(go.Scatter(x=[1, 2], y = [0, 10000], mode= 'lines', line=dict(color="rgba(0, 0, 0, 0)"),))
        fig.update_layout(template = None,
                         plot_bgcolor="rgba( 0, 0, 0, 0)",
                         paper_bgcolor="rgba( 0, 0, 0, 0)",)
        fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
        fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
        return fig
    # start the dash application 
    app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dashboard/", external_scripts=['/static/main.js'],external_stylesheets=['/static/style.css'])
    # the app layout 
    app.layout = html.Div([
        # The currency dropdown
    html.Div([dcc.Dropdown(id = 'dropdown', options = ['BTC', 'ETH', 'SOL'], value = 'BTC', clearable = False, className = 'dropdown'),
            # The period dropdown 
            dcc.Dropdown(id = 'period', options = [{'label': '1h', 'value': 720},
                                                    {'label': '4h', 'value': 2880},
                                                    {'label': '12h', 'value': 8640},
                                                    {'label': '24h', 'value': 17280},
                                                    {'label': '1 week', 'value': 120960},], value = 720, clearable = False, className = 'dropdown')], id = 'dropdown_container'),
    html.Div(children=[
        # The update interval 
        dcc.Interval(
            id='graph-update',
            interval=1 * 5000
            ),
            # This dummy div is used as the output of the callback function for the mutual hover
        html.Div(id="dummy"),
        # These store components store the hover data, the whole data of the selected period and the last row of data respectively. 
        dcc.Store(id = 'last_hover'), 
        dcc.Store(id = 'currency_data'),
        dcc.Store(id = 'currency_data1'),
        # The graphs
        html.Div([
            # dcc.Graph(id='live-graph',),
            deg.ExtendableGraph(
            id='live-graph',
            figure = blank_fig()
        ),
        ], id = 'graph1'),

        html.Div([
            # dcc.Graph(id='live-graph2',style={'display': 'inline-block'}),
            deg.ExtendableGraph(
            id='live-graph2',
            className = 'graph',
            figure = blank_fig()
        ),
        ], id = 'graph2'),

        html.Div([
            # dcc.Graph(id='live-graph3',style={'display': 'inline-block'}),
            deg.ExtendableGraph(
            id='live-graph3',
            figure = blank_fig()
        ),
        ], id = 'graph3'),

        html.Div([
            # dcc.Graph(id='live-graph4',style={'display': 'inline-block'}),
            deg.ExtendableGraph(
            id='live-graph4',
            figure = blank_fig()
        ),
        ], id = 'graph4'),

        html.Div([
            # dcc.Graph(id='live-graph4',style={'display': 'inline-block'}),
            deg.ExtendableGraph(
            id='binance_ratio',
            figure = blank_fig()
        ),
        ], id = 'graph_ratio1'),
        html.Div([
            # dcc.Graph(id='live-graph4',style={'display': 'inline-block'}),
            deg.ExtendableGraph(
            id='ftx_ratio',
            figure = blank_fig()
        ),
        ], id = 'graph_ratio2'),
        html.Div([
            # dcc.Graph(id='live-graph4',style={'display': 'inline-block'}),
            deg.ExtendableGraph(
            id='bybit_ratio',
            figure = blank_fig()
        ),
        ], id = 'graph_ratio3'),

        html.Div([
            # dcc.Graph(id='live-graph5',style={'display': 'inline-block'}),
            deg.ExtendableGraph(
            id='live-graph5',
            figure = blank_fig()
        ),
        ], id = 'graph5'),

        html.Div([
            # dcc.Graph(id='live-graph6',style={'display': 'inline-block'}),
            deg.ExtendableGraph(
            id='live-graph6',
            figure = blank_fig()
        ),
        ], id = 'graph6'),

        html.Div([
            # dcc.Graph(id='live-graph7',style={'display': 'inline-block'}),
            deg.ExtendableGraph(
            id='live-graph7',
            figure = blank_fig()
        ),
        ], id = 'graph7'),
        
    ], id = 'main', className = 'main')
    ])


    # The callbacks for the graphs. 
    # The callback structure for the graphs is similar to one another. 
    # each graph has 2 callbacks, one to update the last trace of data and the other to make the graph(give it the whole data )
    @app.callback([Output('live-graph', 'extendData'),
                Output('live-graph', 'prependData')],
                [Input('currency_data1', 'data'),
                Input('period', 'value')],
                State('live-graph', 'figure'))
    def update_extendData(data, n_rows, existing):
        
        oi = pd.DataFrame(data)
        dict_mark = existing['data'][0]['y']
        diff = (max(dict_mark) - min(dict_mark))/5
        x_new = oi['Time'].iloc[0]
        y_new = oi['Mark_Average'].iloc[0]
        return [[dict(x=[x_new], y=[y_new])], [0], n_rows], [[dict(x=[x_new, x_new], y=[min(dict_mark)-diff, max(dict_mark)+diff])], [1], 2]


    @app.callback(Output('live-graph', 'figure'),
                [Input('currency_data', 'data')])
    def update_graph_scatter(data):

        oi = pd.DataFrame(data)

        dict_mark = oi['Mark_Average']
        diff = (max(dict_mark) - min(dict_mark))/5
        fig = go.Figure()
        fig.add_trace(go.Scatter(
                        x=oi["Time"],
                        y=oi["Mark_Average"],
                        name='',
                        mode= 'lines',
                        line=dict(color="#34ff4e"),
                        ))
        fig.add_trace(go.Scatter(
                        x=[oi['Time'].iloc[-1], oi['Time'].iloc[-1]],
                        y=[min(dict_mark)-diff, max(dict_mark)+diff],
                        name='',
                        mode= 'lines',
                        line=dict(color="rgba(0, 0, 0, 0)"),
                        hoverinfo='skip',
                        ), )
        fig.update_layout(title="Mark Price [Avg - FTX, ByBit, Nance]", 
                        template = 'custom_dark',
                        showlegend = False,
                        hovermode = 'x'
                        )
        return fig



    @app.callback([Output('live-graph2', 'extendData'),
                Output('live-graph2', 'prependData')],
                [Input('currency_data1', 'data'),
                Input('period', 'value')],
                State('live-graph2', 'figure'))
    def update_extendData(data, n_rows, existing):

        oi = pd.DataFrame(data)

        dict_oi = existing['data'][0]['y']
        diff = (max(dict_oi) - min(dict_oi))/5
        x_new = oi['Time'].iloc[-1]
        y_new = oi['BINANCE_OI'].iloc[-1]
        return [[dict(x=[x_new], y=[y_new])], [0], n_rows], [[dict(x=[x_new, x_new], y=[min(dict_oi)-diff, max(dict_oi)+diff])], [1], 2]



    @app.callback(Output('live-graph2', 'figure'),
                [Input('currency_data', 'data')])
    def update_graph_scatter(data):

        oi = pd.DataFrame(data)

        dict_oi = oi['BINANCE_OI']
        diff = (max(dict_oi) - min(dict_oi))/5
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
                        x=oi["Time"],
                        y=oi["BINANCE_OI"],
                        name='',
                        mode= 'lines',
                        line=dict(color="#f50a97"),
                        ))
        fig.add_trace(go.Scatter(
                        x=[oi['Time'].iloc[-1], oi['Time'].iloc[-1]],
                        y=[min(dict_oi)-diff, max(dict_oi)+diff],
                        name='',
                        mode= 'lines',
                        line=dict(color="rgba(0, 0, 0, 0)"),
                        hoverinfo='skip'
                        ), )
        fig.update_layout(title="Binance OI [In Millions]", template = 'custom_dark', showlegend = False, hovermode="x", margin = dict(t = 30, b = 10))
        return fig





    @app.callback([Output('live-graph3', 'extendData'),
                Output('live-graph3', 'prependData')],
                [Input('currency_data1', 'data'),
                Input('period', 'value')],
                State('live-graph3', 'figure'))
    def update_extendData(data, n_rows, existing):

        oi = pd.DataFrame(data)


        dict_oi = existing['data'][0]['y']
        diff = (max(dict_oi) - min(dict_oi))/5
        x_new = oi['Time'].iloc[-1]
        y_new = oi['FTX_OI'].iloc[-1]
        return [[dict(x=[x_new], y=[y_new])], [0], n_rows], [[dict(x=[x_new, x_new], y=[min(dict_oi)-diff, max(dict_oi)+diff])], [1], 2]


    @app.callback(Output('live-graph3', 'figure'),
                [Input('currency_data', 'data')])
    def update_graph_scatter(data):

        oi = pd.DataFrame(data)


        dict_oi = oi['FTX_OI']
        diff = (max(dict_oi) - min(dict_oi))/5


        fig = go.Figure()
        fig.add_trace(go.Scatter(
                        x=oi["Time"],
                        y=oi["FTX_OI"],
                        name='',
                        mode= 'lines',
                        line=dict(color="#f50a97")
                        ))
        fig.add_trace(go.Scatter(
                        x=[oi['Time'].iloc[-1], oi['Time'].iloc[-1]],
                        y=[min(dict_oi)-diff, max(dict_oi)+diff],
                        name='',
                        mode= 'lines',
                        line=dict(color="rgba(0, 0, 0, 0)"),
                        hoverinfo='skip'
                        ), )
        fig.update_layout(title="FTX OI [In Millions]", template = 'custom_dark', showlegend = False, hovermode = 'x', margin = dict(t = 30, b = 10))
        return fig


    @app.callback([Output('live-graph4', 'extendData'),
                Output('live-graph4', 'prependData')],
                [Input('currency_data1', 'data'),
                Input('period', 'value')],
                State('live-graph4', 'figure'))
    def update_extendData(data, n_rows, existing):

        oi = pd.DataFrame(data)


        dict_oi = existing['data'][0]['y']
        diff = (max(dict_oi) - min(dict_oi))/5

        x_new = oi['Time'].iloc[-1]
        y_new = oi['BYBIT_OI'].iloc[-1]
        return [[dict(x=[x_new], y=[y_new])], [0], n_rows], [[dict(x=[x_new, x_new], y=[min(dict_oi)-diff, max(dict_oi)+diff])], [1], 2]

    @app.callback(Output('live-graph4', 'figure'),
                [Input('currency_data', 'data')])
    def update_graph_scatter(data):

        oi = pd.DataFrame(data)

        dict_oi = oi['BYBIT_OI']
        diff = (max(dict_oi) - min(dict_oi))/5

        fig = go.Figure()
        fig.add_trace(go.Scatter(
                        x=oi["Time"],
                        y=oi["BYBIT_OI"],
                        name='',
                        mode= 'lines',
                        line=dict(color="#f50a97")
                        ))
        fig.add_trace(go.Scatter(
                        x=[oi['Time'].iloc[-1], oi['Time'].iloc[-1]],
                        y=[min(dict_oi)-diff, max(dict_oi)+diff],
                        name='',
                        mode= 'lines',
                        line=dict(color="rgba(0, 0, 0, 0)"),
                        hoverinfo='skip'
                        ), )
        fig.update_layout(title="ByBit OI [In Millions]", template = 'custom_dark', showlegend = False, hovermode = 'x', margin = dict(t = 30, b = 10))
        return fig
    #######################################################################################################

    @app.callback([Output('binance_ratio', 'extendData'),
                Output('binance_ratio', 'prependData')],
                [Input('currency_data1', 'data'),
                Input('period', 'value')],
                State('binance_ratio', 'figure'))
    def update_extendData(data, n_rows, existing):

        oi = pd.DataFrame(data)


        dict_oi = existing['data'][0]['y']
        diff = (max(dict_oi) - min(dict_oi))/5

        x_new = oi['Time'].iloc[-1]
        y_new = oi['BINANCE_Ratio'].iloc[-1]
        return [[dict(x=[x_new], y=[y_new])], [0], n_rows], [[dict(x=[x_new, x_new], y=[min(dict_oi)-diff, max(dict_oi)+diff])], [1], 2]

    @app.callback(Output('binance_ratio', 'figure'),
                [Input('currency_data', 'data')])
    def update_graph_scatter(data):

        oi = pd.DataFrame(data)


        dict_oi = oi['BINANCE_Ratio']
        diff = (max(dict_oi) - min(dict_oi))/5

        fig = go.Figure()
        fig.add_trace(go.Scatter(
                        x=oi["Time"],
                        y=oi["BINANCE_Ratio"],
                        name='',
                        mode= 'lines',
                        line=dict(color="#f50a97")
                        ))
        fig.add_trace(go.Scatter(
                        x=[oi['Time'].iloc[-1], oi['Time'].iloc[-1]],
                        y=[min(dict_oi)-diff, max(dict_oi)+diff],
                        name='',
                        mode= 'lines',
                        line=dict(color="rgba(0, 0, 0, 0)"),
                        hoverinfo='skip'
                        ), )
        fig.update_layout(title="Binance Ratio", template = 'custom_dark', showlegend = False, hovermode = 'x', margin = dict(t = 30, b = 10))
        return fig



    @app.callback([Output('ftx_ratio', 'extendData'),
                Output('ftx_ratio', 'prependData')],
                [Input('currency_data1', 'data'),
                Input('period', 'value')],
                State('ftx_ratio', 'figure'))
    def update_extendData(data, n_rows, existing):

        oi = pd.DataFrame(data)

        dict_oi = existing['data'][0]['y']
        diff = (max(dict_oi) - min(dict_oi))/5

        x_new = oi['Time'].iloc[-1]
        y_new = oi['FTX_Ratio'].iloc[-1]
        return [[dict(x=[x_new], y=[y_new])], [0], n_rows], [[dict(x=[x_new, x_new], y=[min(dict_oi)-diff, max(dict_oi)+diff])], [1], 2]

    @app.callback(Output('ftx_ratio', 'figure'),
                [Input('currency_data', 'data')])
    def update_graph_scatter(data):

        oi = pd.DataFrame(data)


        dict_oi = oi['FTX_Ratio']
        diff = (max(dict_oi) - min(dict_oi))/5

        fig = go.Figure()
        fig.add_trace(go.Scatter(
                        x=oi["Time"],
                        y=oi["FTX_Ratio"],
                        name='',
                        mode= 'lines',
                        line=dict(color="#f50a97")
                        ))
        fig.add_trace(go.Scatter(
                        x=[oi['Time'].iloc[-1], oi['Time'].iloc[-1]],
                        y=[min(dict_oi)-diff, max(dict_oi)+diff],
                        name='',
                        mode= 'lines',
                        line=dict(color="rgba(0, 0, 0, 0)"),
                        hoverinfo='skip'
                        ), )
        fig.update_layout(title="FTX Ratio", template = 'custom_dark', showlegend = False, hovermode = 'x', margin = dict(t = 30, b = 10))
        return fig



    @app.callback([Output('bybit_ratio', 'extendData'),
                Output('bybit_ratio', 'prependData')],
                [Input('currency_data1', 'data'),
                Input('period', 'value')],
                State('bybit_ratio', 'figure'))
    def update_extendData(data, n_rows, existing):

        oi = pd.DataFrame(data)


        dict_oi = existing['data'][0]['y']
        diff = (max(dict_oi) - min(dict_oi))/5

        x_new = oi['Time'].iloc[-1]
        y_new = oi['BYBIT_Ratio'].iloc[-1]
        return [[dict(x=[x_new], y=[y_new])], [0], n_rows], [[dict(x=[x_new, x_new], y=[min(dict_oi)-diff, max(dict_oi)+diff])], [1], 2]

    @app.callback(Output('bybit_ratio', 'figure'),
                [Input('currency_data', 'data')])
    def update_graph_scatter(data):

        oi = pd.DataFrame(data)


        dict_oi = oi['BYBIT_Ratio']
        diff = (max(dict_oi) - min(dict_oi))/5

        fig = go.Figure()
        fig.add_trace(go.Scatter(
                        x=oi["Time"],
                        y=oi["BYBIT_Ratio"],
                        name='',
                        mode= 'lines',
                        line=dict(color="#f50a97")
                        ))
        fig.add_trace(go.Scatter(
                        x=[oi['Time'].iloc[-1], oi['Time'].iloc[-1]],
                        y=[min(dict_oi)-diff, max(dict_oi)+diff],
                        name='',
                        mode= 'lines',
                        line=dict(color="rgba(0, 0, 0, 0)"),
                        hoverinfo='skip'
                        ), )
        fig.update_layout(title="ByBit Ratio", template = 'custom_dark', showlegend = False, hovermode = 'x', margin = dict(t = 30, b = 10))
        return fig



    @app.callback([Output('live-graph5', 'extendData'),
                Output('live-graph5', 'prependData')],
                [Input('currency_data1', 'data'),
                Input('period', 'value'),],
                State('live-graph5', 'figure'))
    def update_extendData(data, n_rows, existing):

        oi = pd.DataFrame(data)


        dict_oi = existing['data'][0]['y']
        diff = (max(dict_oi) - min(dict_oi))/5

        x_new = oi['Time'].iloc[-1]
        y_new = oi['BINANCE_Funding'].iloc[-1]
        return [[dict(x=[x_new], y=[y_new])], [0], n_rows], [[dict(x=[x_new, x_new], y=[min(dict_oi)-diff, max(dict_oi)+diff])], [1], 2]


    @app.callback(Output('live-graph5', 'figure'),
                [Input('currency_data', 'data')])
    def update_graph_histo(data):

        oi = pd.DataFrame(data)


        dict_oi = oi['BINANCE_Funding']
        diff = (max(dict_oi) - min(dict_oi))/5


        fig = go.Figure()
        fig.add_trace(go.Scatter(
                        x=oi["Time"],
                        y=oi["BINANCE_Funding"],
                        name='',
                        mode= 'lines',
                        line=dict(color="#9a11e5")
                        ))
        fig.add_trace(go.Scatter(
                        x=[oi['Time'].iloc[-1], oi['Time'].iloc[-1]],
                        y=[min(dict_oi)-diff, max(dict_oi)+diff],
                        name='',
                        mode= 'lines',
                        line=dict(color="rgba(0, 0, 0, 0)"),
                        hoverinfo='skip'
                        ), )
        fig.update_layout(title="Binance Funding", template = 'custom_dark', showlegend = False, hovermode = 'x')
        return fig




    @app.callback([Output('live-graph6', 'extendData'),
                Output('live-graph6', 'prependData')],
                [Input('currency_data1', 'data'),
                Input('period', 'value')],
                State('live-graph6', 'figure'))
    def update_extendData(data, n_rows, existing):

        oi = pd.DataFrame(data)


        dict_oi = existing['data'][0]['y']
        diff = (max(dict_oi) - min(dict_oi))/5
        x_new = oi['Time'].iloc[-1]
        y_new = oi['FTX_Funding'].iloc[-1]
        return [[dict(x=[x_new], y=[y_new])], [0], n_rows], [[dict(x=[x_new, x_new], y=[min(dict_oi)-diff, max(dict_oi)+diff])], [1], 2]



    @app.callback(Output('live-graph6', 'figure'),
                [Input('currency_data', 'data')])
    def update_graph_histo(data):

        oi = pd.DataFrame(data)


        dict_oi = oi['FTX_Funding']
        diff = (max(dict_oi) - min(dict_oi))/5


        fig = go.Figure()
        fig.add_trace(go.Scatter(
                        x=oi["Time"],
                        y=oi["FTX_Funding"],
                        name='',
                        mode= 'lines',
                        line=dict(color="#9a11e5")
                        ))
        fig.add_trace(go.Scatter(
                        x=[oi['Time'].iloc[-1], oi['Time'].iloc[-1]],
                        y=[min(dict_oi)-diff, max(dict_oi)+diff],
                        name='',
                        mode= 'lines',
                        line=dict(color="rgba(0, 0, 0, 0)"),
                        hoverinfo='skip'
                        ), )
        fig.update_layout(title="FTX Funding", template = 'custom_dark', showlegend = False, hovermode = 'x')
        return fig

    @app.callback([Output('live-graph7', 'extendData'),
                Output('live-graph7', 'prependData')],
                [Input('currency_data1', 'data'),
                Input('period', 'value')],
                State('live-graph7', 'figure'))
    def update_extendData(data, n_rows, existing):

        oi = pd.DataFrame(data)

        dict_oi = existing['data'][0]['y']
        diff = (max(dict_oi) - min(dict_oi))/5

        x_new = oi['Time'].iloc[-1]
        y_new = oi['BYBIT_Funding'].iloc[-1]
        return [[dict(x=[x_new], y=[y_new])], [0], n_rows], [[dict(x=[x_new, x_new], y=[min(dict_oi)-diff, max(dict_oi)+diff])], [1], 2]



    @app.callback(Output('live-graph7', 'figure'),
                [Input('currency_data', 'data')])
    def update_graph_histo(data):

        oi = pd.DataFrame(data)

        dict_oi = oi['BYBIT_Funding']
        diff = (max(dict_oi) - min(dict_oi))/5


        fig = go.Figure()
        fig.add_trace(go.Scatter(
                        x=oi["Time"],
                        y=oi["BYBIT_Funding"],
                        name='',
                        mode= 'lines',
                        line=dict(color="#9a11e5")
                        ))
        fig.add_trace(go.Scatter(
                        x=[oi['Time'].iloc[-1], oi['Time'].iloc[-1]],
                        y=[min(dict_oi)-diff, max(dict_oi)+diff],
                        name='',
                        mode= 'lines',
                        line=dict(color="rgba(0, 0, 0, 0)"),
                        hoverinfo='skip'
                        ), )
        fig.update_layout(title="Bybit Funding", template = 'custom_dark', showlegend = False, hovermode = 'x')
        return fig



        # This callback stores the hover data into the store component with the id last_hover

    @app.callback(
        Output('last_hover', 'data'),
        [Input('live-graph', 'hoverData'),
        Input('live-graph2', 'hoverData'),
        Input('live-graph3', 'hoverData'),
        Input('live-graph4', 'hoverData'),
        Input('binance_ratio', 'hoverData'),
        Input('ftx_ratio', 'hoverData'),
        Input('bybit_ratio', 'hoverData'),
        Input('live-graph5', 'hoverData'),
        Input('live-graph6', 'hoverData'),
        Input('live-graph7', 'hoverData'),]
    )
    def store_data(g1, g2, g3, g4, g5, g6, g7, g8, g9, g10):
        data = callback_context.triggered[0]['value']
        return data


    # This clientside callback controls the mutual hover on all the charts through calling the function trigger_hover from main.js file in the static folder 
    app.clientside_callback(
        ClientsideFunction(namespace="clientside", function_name="trigger_hover"),
        Output("dummy", "data-hover"),
        [Input("last_hover", "data")],
    )

        #the following callbacks store the data into the store components
    @app.callback(
        Output('currency_data', 'data'),
        [Input('dropdown', 'value'),
        Input('period', 'value')],
    )
    def update_data(currency, n_rows):
        n_rows = int(n_rows)
        columns = ["Time", 'BINANCE_Mark_Price', 'BINANCE_OI', 'BINANCE_Funding', "BYBIT_Mark_Price", "BYBIT_OI",
                    "BYBIT_Funding", "FTX_Mark_Price", "FTX_OI", "FTX_Funding", "Mark_Average", "BINANCE_Ratio", "BYBIT_Ratio",
                    "FTX_Ratio"]
        try:
            scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
            client0 = gspread.authorize(creds)
            sheet = client0.open("currency_data").worksheet(currency)
            data_full = pd.DataFrame.from_dict(sheet.get(f"A2:N{n_rows}"))
            data_full.columns = columns
            try:
                data_full['Time']
            except:
                data_full = pd.DataFrame.from_dict(sheet.get(f"A2:k{n_rows}"))
            data_full[data_full.columns[1:]] = data_full[data_full.columns[1:]].astype(float)
            data_full = data_full.iloc[::-1]

        except:
            print('failed')
            data_full = get_currency_data(n_rows, currency)
            try:
                data_full['Time']
            except:
                data_full = get_currency_data(n_rows, currency)
            data_full = data_full[data_full.columns[0:14]]
        return data_full.to_dict('records')

    @app.callback(
        Output('currency_data1', 'data'),
        Input('dropdown', 'value'),
        Input('graph-update', 'n_intervals')
    )
    def update_data(currency, n_intervals):
        data_1 = get_currency_data(1, currency)
        try:
            data_1['Time']
        except:
            data_1 = get_currency_data(1, currency)
        data_1 = data_1[data_1.columns[0:14]]
        
        return data_1.to_dict('records')

    # require login for all the function in this route 
    for view_function in app.server.view_functions:
        if view_function.startswith(app.config.url_base_pathname):
            app.server.view_functions[view_function] = login_required(
                app.server.view_functions[view_function]
            )
    #return the app
    return app

