import dash
from dash.dependencies import Input, Output
from dash import dcc, html
import requests

API_KEY = 'd4227a7e1aca38c6c8551c41bca7be44'

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Weather Dashboard"),
    html.Div(id='weather-output'),
    dcc.Interval(
        id='interval-component',
        interval=600000, 
        n_intervals=0
    )
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
        ])
    except Exception as e:
        output = html.P("Failed to fetch weather data. Please try again later.")

    return output

if __name__ == '__main__':
    app.run_server(debug=True)

# http://localhost:8050/