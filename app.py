from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

province_population = {
    'British Columbia': 5020302,
    'Alberta': 4345737,
    'Saskatchewan': 1168423,
    'Manitoba': 1360396,
    'Ontario': 14446515,
    'Quebec': 8433301,
    'New Brunswick': 772094,
    'Nova Scotia': 965382,
    'Northwest Territories': 44598,
    'Prince Edward Island': 154748,
    'Newfoundland and Labrador': 523790,
    'Yukon': 40369,
    'Nunavut': 38787
}

# GETTING THE DATA
import pandas as pd

url = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'
url1 = 'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv'
url_provincial_correctional_institutions = 'https://data.ontario.ca/dataset/ecb75ea0-8b72-4f46-a14a-9bd54841d6ab/resource/1f95eda9-53b5-448e-abe0-afc0b71581ed/download/correctionsinmatecases.csv'

df = pd.read_csv(url)
df = df[(df['Country/Region'] == 'Canada')]

df['cases_as_percent_of_population'] = 100 * df['Confirmed'] / (df['Province/State'].map(province_population))
df['recovered_as_percent_of_population'] = 100 * df['Recovered'] / (df['Province/State'].map(province_population))
df['deaths_as_percent_of_population'] = 100 * df['Deaths'] / (df['Province/State'].map(province_population))

df['cases_per_day'] = df['Confirmed'].diff().apply(lambda x: x if x >= 0 else 0)
df['recovered_per_day'] = df['Recovered'].diff().apply(lambda x: x if x >= 0 else 0)
df['deaths_per_day'] = df['Deaths'].diff().apply(lambda x: x if x >= 0 else 0)

data = {}

provinces = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador',
             'Northwest Territories', 'Nova Scotia', 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan',
             'Yukon']

for i in provinces:
    index_value = df[(df['Province/State'] == i)]['cases_per_day'].idxmax()
    num_of_most_cases = df['cases_per_day'].loc[index_value]
    num_of_most_cases = f'{int(num_of_most_cases):,}'  # this adds commas to the numbers
    most_cases_date = datetime.strptime(df['Date'].loc[index_value], '%Y-%m-%d').strftime(
        "%b %d")  # pass month and year e.g. Jul 31

    cumulative_num_cases = df[(df['Province/State'] == i)]['Confirmed'][-1:].values[0]
    cumulative_num_cases = f'{int(cumulative_num_cases):,}'  # this adds commas to the numbers
    cumulative_num_cases_date = datetime.strptime(df[(df['Province/State'] == i)]['Date'][-1:].values[0],
                                                  '%Y-%m-%d').strftime("%b %d")

    new_cases = df[(df['Province/State'] == i)]['cases_per_day'][-1:].values[0]
    new_cases = f'{int(new_cases):,}'  # this adds commas to the numbers
    new_deaths = df[(df['Province/State'] == i)]['deaths_per_day'][-1:].values[0]
    new_deaths = f'{int(new_deaths):,}'  # this adds commas to the numbers

    data[i] = {
        'most_daily_cases': {'num_of_cases': num_of_most_cases, 'date': most_cases_date},
        'cumulative_num_cases': {'num_of_cases': cumulative_num_cases, 'date': cumulative_num_cases_date},
        'latest': {'new_cases': new_cases, 'new_deaths': new_deaths}
    }

df1 = pd.read_csv(url1)

categories = [
    'Confirmed Negative',
    'Presumptive Negative',
    'Presumptive Positive',
    'Confirmed Positive',
    'Resolved',
    'Deaths',
    'Total Cases',
    'Total patients approved for testing as of Reporting Date',
    'Total tests completed in the last day',
    'Under Investigation',
    'Number of patients hospitalized with COVID-19',
    'Number of patients in ICU with COVID-19',
    'Number of patients in ICU on a ventilator with COVID-19',
    'Total Positive LTC Resident Cases',
    'Total Positive LTC HCW Cases',
    'Total LTC Resident Deaths',
    'Total LTC HCW Deaths']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# the line below is only required when running on a server (e.g. Heroku)
server = app.server

app.layout = html.Div(children=[
    html.H1('COVID-19 in Canada'),
    html.Hr(),
    html.P('This dashboard gives a general overview of how COVID-19 incidents are trending in Canada and Ontario.'),

    html.Div([
        html.Div([html.P("")], className='mini_container firstRow firstColumn firstCell'),
        html.Div([html.P("Alberta")], className='mini_container firstRow'),
        html.Div([html.P("British Columbia")], className='mini_container firstRow'),
        html.Div([html.P("Manitoba")], className='mini_container firstRow'),
        html.Div([html.P("New Brunswick")], className='mini_container firstRow'),
        html.Div([html.P("Newfoundland and Labrador")], className='mini_container firstRow'),
        html.Div([html.P("Northwest Territories")], className='mini_container firstRow'),
        html.Div([html.P("Nova Scotia")], className='mini_container firstRow'),
        html.Div([html.P("Ontario")], className='mini_container firstRow'),
        html.Div([html.P("Prince Edward Island")], className='mini_container firstRow'),
        html.Div([html.P("Saskatchewan")], className='mini_container firstRow'),
        html.Div([html.P("Yukon")], className='mini_container firstRow')
    ], className="row flex-display"),

    html.Div([
        html.Div([html.P("Confirmed Cases")], className='mini_container secondRow firstColumn'),
        html.Div([
            html.P(data['Alberta']['cumulative_num_cases']['num_of_cases']),
            html.P(data['Alberta']['cumulative_num_cases']['date'])
        ], className='mini_container secondRow'),
        html.Div([
            html.P(data['British Columbia']['cumulative_num_cases']['num_of_cases']),
            html.P(data['British Columbia']['cumulative_num_cases']['date'])
        ], className='mini_container secondRow'),
        html.Div([
            html.P(data['Manitoba']['cumulative_num_cases']['num_of_cases']),
            html.P(data['Manitoba']['cumulative_num_cases']['date'])
        ], className='mini_container secondRow'),
        html.Div([
            html.P(data['New Brunswick']['cumulative_num_cases']['num_of_cases']),
            html.P(data['New Brunswick']['cumulative_num_cases']['date'])
        ], className='mini_container secondRow'),
        html.Div([
            html.P(data['Newfoundland and Labrador']['cumulative_num_cases']['num_of_cases']),
            html.P(data['Newfoundland and Labrador']['cumulative_num_cases']['date'])
        ], className='mini_container secondRow'),
        html.Div([
            html.P(data['Northwest Territories']['cumulative_num_cases']['num_of_cases']),
            html.P(data['Northwest Territories']['cumulative_num_cases']['date'])
        ], className='mini_container secondRow'),
        html.Div([
            html.P(data['Nova Scotia']['cumulative_num_cases']['num_of_cases']),
            html.P(data['Nova Scotia']['cumulative_num_cases']['date'])
        ], className='mini_container secondRow'),
        html.Div([
            html.P(data['Ontario']['cumulative_num_cases']['num_of_cases']),
            html.P(data['Ontario']['cumulative_num_cases']['date'])
        ], className='mini_container secondRow'),
        html.Div([
            html.P(data['Prince Edward Island']['cumulative_num_cases']['num_of_cases']),
            html.P(data['Prince Edward Island']['cumulative_num_cases']['date'])
        ], className='mini_container secondRow'),
        html.Div([
            html.P(data['Saskatchewan']['cumulative_num_cases']['num_of_cases']),
            html.P(data['Saskatchewan']['cumulative_num_cases']['date'])
        ], className='mini_container secondRow'),
        html.Div([
            html.P(data['Yukon']['cumulative_num_cases']['num_of_cases']),
            html.P(data['Yukon']['cumulative_num_cases']['date'])
        ], className='mini_container secondRow')
    ], className="row flex-display"),

    html.Div([
        html.Div([html.P("New Cases")], className='mini_container thirdRow firstColumn'),
        html.Div([html.P(data['Alberta']['latest']['new_cases'])], className='mini_container thirdRow'),
        html.Div([html.P(data['British Columbia']['latest']['new_cases'])], className='mini_container thirdRow'),
        html.Div([html.P(data['Manitoba']['latest']['new_cases'])], className='mini_container thirdRow'),
        html.Div([html.P(data['New Brunswick']['latest']['new_cases'])], className='mini_container thirdRow'),
        html.Div([html.P(data['Newfoundland and Labrador']['latest']['new_cases'])],
                 className='mini_container thirdRow'),
        html.Div([html.P(data['Northwest Territories']['latest']['new_cases'])], className='mini_container thirdRow'),
        html.Div([html.P(data['Nova Scotia']['latest']['new_cases'])], className='mini_container thirdRow'),
        html.Div([html.P(data['Ontario']['latest']['new_cases'])], className='mini_container thirdRow'),
        html.Div([html.P(data['Prince Edward Island']['latest']['new_cases'])], className='mini_container thirdRow'),
        html.Div([html.P(data['Saskatchewan']['latest']['new_cases'])], className='mini_container thirdRow'),
        html.Div([html.P(data['Yukon']['latest']['new_cases'])], className='mini_container thirdRow')
    ], className="row flex-display"),

    html.Div([
        html.Div([html.P("Daily Record")], className='mini_container fourthRow firstColumn'),
        html.Div([
            html.P(data['Alberta']['most_daily_cases']['num_of_cases']),
            html.P(data['Alberta']['most_daily_cases']['date'])
        ], className='mini_container fourthRow'),
        html.Div([
            html.P(data['British Columbia']['most_daily_cases']['num_of_cases']),
            html.P(data['British Columbia']['most_daily_cases']['date'])
        ], className='mini_container fourthRow'),
        html.Div([
            html.P(data['Manitoba']['most_daily_cases']['num_of_cases']),
            html.P(data['Manitoba']['most_daily_cases']['date'])
        ], className='mini_container fourthRow'),
        html.Div([
            html.P(data['New Brunswick']['most_daily_cases']['num_of_cases']),
            html.P(data['New Brunswick']['most_daily_cases']['date'])
        ], className='mini_container fourthRow'),
        html.Div([
            html.P(data['Newfoundland and Labrador']['most_daily_cases']['num_of_cases']),
            html.P(data['Newfoundland and Labrador']['most_daily_cases']['date'])
        ], className='mini_container fourthRow'),
        html.Div([
            html.P(data['Northwest Territories']['most_daily_cases']['num_of_cases']),
            html.P(data['Northwest Territories']['most_daily_cases']['date'])
        ], className='mini_container fourthRow'),
        html.Div([
            html.P(data['Nova Scotia']['most_daily_cases']['num_of_cases']),
            html.P(data['Nova Scotia']['most_daily_cases']['date'])
        ], className='mini_container fourthRow'),
        html.Div([
            html.P(data['Ontario']['most_daily_cases']['num_of_cases']),
            html.P(data['Ontario']['most_daily_cases']['date'])
        ], className='mini_container fourthRow'),
        html.Div([
            html.P(data['Prince Edward Island']['most_daily_cases']['num_of_cases']),
            html.P(data['Prince Edward Island']['most_daily_cases']['date'])
        ], className='mini_container fourthRow'),
        html.Div([
            html.P(data['Saskatchewan']['most_daily_cases']['num_of_cases']),
            html.P(data['Saskatchewan']['most_daily_cases']['date'])
        ], className='mini_container fourthRow'),
        html.Div([
            html.P(data['Yukon']['most_daily_cases']['num_of_cases']),
            html.P(data['Yukon']['most_daily_cases']['date'])
        ], className='mini_container fourthRow')
    ], className="row flex-display"),
    html.Hr(),
    html.Div(children=[
        html.H6('Canada'),
        html.P('Select province(s) and incident outcome below.'),
        dcc.Dropdown(id='province_list',
                     # options=[{'label': province, 'value': province} for province in df['Province/State'].unique()],
                     options=[{'label': province, 'value': province} for province in df['Province/State'].unique()],
                     value=['Ontario'],
                     multi=True,
                     placeholder='Select a province(s)'
                     ),
        dcc.Dropdown(id='state',
                     options=[
                         {'label': 'Confirmed', 'value': 'Confirmed'},
                         {'label': 'Recovered', 'value': 'Recovered'},
                         {'label': 'Deaths', 'value': 'Deaths'},
                         {'label': 'Cases as a % of ppln', 'value': 'cases_as_percent_of_population'},
                         {'label': 'Recovered as a % of ppln', 'value': 'recovered_as_percent_of_population'},
                         {'label': 'Deaths as a % of ppln', 'value': 'deaths_as_percent_of_population'},
                         {'label': 'Cases per day', 'value': 'cases_per_day'},
                         {'label': 'Recovered per day', 'value': 'recovered_per_day'},
                         {'label': 'Deaths per day', 'value': 'deaths_per_day'},
                     ],
                     value=['Confirmed'],
                     multi=True,
                     placeholder='Select a state(s)'
                     ),
        dcc.Graph(id='dd-output-container')
    ]),
    html.Hr(),
    html.Div(children=[
        html.H6('Ontario'),
        html.P(
            'The graph below focuses on how COVID-19 in trending in Ontario. Select data category from the dropdown below to update graph.'),
        dcc.Dropdown(id='categories',
                     options=[{'label': i, 'value': i} for i in categories],
                     value=[
                         'Total Positive LTC Resident Cases',
                         'Total Positive LTC HCW Cases'
                     ],
                     multi=True,
                     placeholder='Select data category'
                     ),
        dcc.Graph(id='dd-output-container2')
    ])

])


@app.callback(
    dash.dependencies.Output('dd-output-container', component_property='figure'),
    [
        dash.dependencies.Input('province_list', 'value'),
        dash.dependencies.Input('state', 'value')
    ])
def update_output(provinces, states):
    figure = {
        'data': [
            dict(
                x=df[df['Province/State'] == i]['Date'],
                y=df[df['Province/State'] == i][j],
                text=df[df['Province/State'] == i]['Province/State'],
                mode='line',
                opacity=0.8,
                marker={
                    'size': 5,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i + ' (' + j + ')'
            ) for i in provinces for j in states
        ],
        'layout': dict(
            xaxis={'type': 'line', 'title': ''},
            yaxis={'title': ''}
        )
    }
    return figure


@app.callback(
    dash.dependencies.Output('dd-output-container2', component_property='figure'),
    [
        dash.dependencies.Input('categories', 'value')
    ])
def update_output(categories):
    figure = {
        'data': [
            dict(
                x=df1['Reported Date'],
                y=df1[i],
                text=i,
                mode='line',
                opacity=0.8,
                marker={
                    'size': 5,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in categories
        ],
        'layout': dict(
            xaxis={'type': 'line', 'title': ''},
            yaxis={'title': ''}
        )
    }
    return figure


# @app.callback(
#     dash.dependencies.Output('ontario', "children")
#     [
#         dash.dependencies.Input(most_daily_cases)
#     ])
# def update_output(value):
#     return most_daily_cases['Ontario']['num_of_cases']


if __name__ == '__main__':
    app.run_server(debug=True)
