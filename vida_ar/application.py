# TODO:
# - edit labels
# - add titles

from imp import IMP_HOOK
from dash import Dash,html,dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

from data_preprocessing import physical_df,fruits_df, soda_vegs_df,alcohol_df

physical_bar = go.Figure(data=[go.Bar(x=physical_df['Sport per week'], y=physical_df['count'], 
            marker_color=['limegreen', 'mediumseagreen', 'red', 'tomato', 'limegreen', 'yellowgreen', 'springgreen', 'limegreen'])])


physical_bar.update_layout(height=600, title='How much sport did you do in the last week?')

fruits_pie = px.pie(fruits_df, values='count', names='fruit',
                    labels={
                        'count': 'Number of teenagers',
                        'fruit': 'Amount of fruit you ate in the last week'
                    }, title='How many fruit did you eat in the last week?',
                    color_discrete_sequence=px.colors.sequential.RdBu, height=600)
soda_vegs_bar = px.bar(soda_vegs_df, x='Soda', y='count', color='Vegs',
                labels={
                    'count': 'Number of teenagers',
                    'Soda': 'Amount of soda you drank in the last week'
                }, title='How much soda did you drink in the last week?',
                color_discrete_sequence=px.colors.sequential.RdPu_r, height=800, width=900)
soda_vegs_bar.update_layout(legend=dict(yanchor='top', xanchor='right'))


alcohol_tree = px.treemap(alcohol_df, path=['alcohol', 'sex'], values='count', color='alcohol',
                        color_discrete_map={
                            'all':'white',
                            'Between 12 and 15 years old': 'darkblue',
                            'I never drank more than a few sips': 'cornflowerblue',
                            '10 or 11 years old': 'darkslateblue',
                            '8 or 9 years old': 'midnightblue',
                            '7 years old or less': 'navy',
                            '16 or 17 years old': 'dodgerblue'
                        }, title='When did you first try alcohol?',
                        height=650, width=650)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
application = app.server

app.layout = html.Div([
    html.H1('This is VidAR. An insight into argentinian teenagers lifestyle.'),
    dbc.Row(
        [
            dbc.Col([
                html.H2('A lot of teenagers have a sedentary lifestyle.'),
                dcc.Graph(id='physical-pie', figure=physical_bar)], md=6),
            dbc.Col(
                [html.H2('Fruit is barely consumed by teenagers.'),
                dcc.Graph(id='fruits-pie', figure=fruits_pie)], md=6)
        ]
    ),
    dbc.Row(
        [
            dbc.Col([
                html.H2('Most teenagers have already consumed alcohol before age 15.',style={'textAlign': 'center'}),
                dcc.Graph(id='alcohol-tree', figure=alcohol_tree)
            ], md=5), 
            dbc.Col([
                html.H2('Soda beverages are frequently consumed.',style={'textAlign': 'center'}),
                html.H3('On the other hand, vegetable consumption is really low.',style={'textAlign': 'center'}),
                dcc.Graph(id='soda_vegs-bar', figure=soda_vegs_bar)
            ], md=6)
        ]
    ),
    html.P('Source: Encuesta Mundial de Salud Escolar, Argentina 2018'),
    html.P('Find the dataset in: https://datos.gob.ar/dataset/salud-base-datos-3deg-encuesta-mundial-salud-escolar-emse-con-resultados-nacionales-argentina/archivo/salud_9888b372-8094-45e2-8b62-40630838c5dc')
])

if __name__ == '__main__':
    application.run(debug=True, port=8080)