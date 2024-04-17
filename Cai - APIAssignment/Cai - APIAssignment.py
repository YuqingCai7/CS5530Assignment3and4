import dash
from dash.dependencies import Input, Output
from dash import dcc, html
import requests
import plotly.graph_objs as go
from datetime import datetime, timedelta

API_KEY = 'd4227a7e1aca38c6c8551c41bca7be44'

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/litera/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Weather Dashboard", className="display-4 text-center mb-4"),
        html.Div(id='weather-output', className="text-center"),
        dcc.Interval(
            id='interval-component',
            interval=600000,
            n_intervals=0
        ),
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='temperature-trend', className="w-100")
        ], className="col-md-6"),
        html.Div([
            dcc.Graph(id='forecast', className="w-100")
        ], className="col-md-6")
    ], className="row")
])


@app.callback(Output('weather-output', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_weather(n):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q=Kansas%20City,US&appid={API_KEY}&units=imperial' 
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        output = html.Div([
            html.P(f"Weather: {weather_description}"),
            html.P(f"Temperature: {temperature}°F"), 
            html.P(f"Humidity: {humidity}%"),
            html.P(f"Wind Speed: {wind_speed} m/s")
        ], className="lead")
    except Exception as e:
        output = html.P("Failed to fetch weather data. Please try again later.", className="lead")

    return output

@app.callback(Output('temperature-trend', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_temperature_trend(n):
    try:
        url = f'http://api.openweathermap.org/data/2.5/forecast?q=Kansas%20City,US&appid={API_KEY}&units=imperial'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        timestamps = [datetime.fromtimestamp(entry['dt']) for entry in data['list']]
        temperatures = [entry['main']['temp'] for entry in data['list']]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=timestamps, y=temperatures, mode='lines', name='Temperature Trend'))
        fig.update_layout(title='Temperature Trend for the Next 5 Days',
                          xaxis_title='Date',
                          yaxis_title='Temperature (°F)')
    except Exception as e:
        fig = go.Figure()
        fig.update_layout(title='Temperature Trend',
                          xaxis_title='Date',
                          yaxis_title='Temperature (°F)',
                          annotations=[dict(text="Failed to fetch data", showarrow=False)])

    return fig

@app.callback(Output('forecast', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_forecast(n):
    try:
        url = f'http://api.openweathermap.org/data/2.5/forecast?q=Kansas%20City,US&appid={API_KEY}&units=imperial'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        timestamps = [datetime.fromtimestamp(entry['dt']) for entry in data['list']]
        descriptions = [entry['weather'][0]['description'] for entry in data['list']]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=timestamps, y=descriptions, name='Weather Forecast'))
        fig.update_layout(title='Weather Forecast for the Next 5 Days',
                          xaxis_title='Date',
                          yaxis_title='Weather Description')
    except Exception as e:
        fig = go.Figure()
        fig.update_layout(title='Weather Forecast',
                          xaxis_title='Date',
                          yaxis_title='Weather Description',
                          annotations=[dict(text="Failed to fetch data", showarrow=False)])

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

# http://localhost:8050/