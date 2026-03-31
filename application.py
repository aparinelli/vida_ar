# TODO:
# - edit labels
# - add titles

from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from data_preprocessing import physical_df, fruits_df, soda_vegs_df, alcohol_df


# ---------- FIGURE BUILDERS ----------

def create_physical_bar(df):
    fig = go.Figure(data=[
        go.Bar(
            x=df['Sport per week'],
            y=df['count'],
            marker_color=[
                'limegreen', 'mediumseagreen', 'red', 'tomato',
                'limegreen', 'yellowgreen', 'springgreen', 'limegreen'
            ]
        )
    ])
    fig.update_layout(
        height=600,
        title='How much sport did you do in the last week?'
    )
    return fig


def create_fruits_pie(df):
    return px.pie(
        df,
        values='count',
        names='fruit',
        labels={
            'count': 'Number of teenagers',
            'fruit': 'Amount of fruit you ate in the last week'
        },
        title='How many fruit did you eat in the last week?',
        color_discrete_sequence=px.colors.sequential.RdBu,
        height=600
    )


def create_soda_vegs_bar(df):
    fig = px.bar(
        df,
        x='Soda',
        y='count',
        color='Vegs',
        labels={
            'count': 'Number of teenagers',
            'Soda': 'Amount of soda you drank in the last week'
        },
        title='How much soda did you drink in the last week?',
        color_discrete_sequence=px.colors.sequential.RdPu_r,
        height=800,
        width=900
    )
    fig.update_layout(legend=dict(yanchor='top', xanchor='right'))
    return fig


def create_alcohol_tree(df):
    return px.treemap(
        df,
        path=['alcohol', 'sex'],
        values='count',
        color='alcohol',
        color_discrete_map={
            'all': 'white',
            'Between 12 and 15 years old': 'darkblue',
            'I never drank more than a few sips': 'cornflowerblue',
            '10 or 11 years old': 'darkslateblue',
            '8 or 9 years old': 'midnightblue',
            '7 years old or less': 'navy',
            '16 or 17 years old': 'dodgerblue'
        },
        title='When did you first try alcohol?',
        height=650,
        width=650
    )


# ---------- LAYOUT ----------

def create_layout(figs):
    return html.Div([
        html.H1('This is VidAR. An insight into argentinian teenagers lifestyle.'),

        dbc.Row([
            dbc.Col([
                html.H2('A lot of teenagers have a sedentary lifestyle.'),
                dcc.Graph(figure=figs['physical'])
            ], md=6),

            dbc.Col([
                html.H2('Fruit is barely consumed by teenagers.'),
                dcc.Graph(figure=figs['fruits'])
            ], md=6)
        ]),

        dbc.Row([
            dbc.Col([
                html.H2(
                    'Most teenagers have already consumed alcohol before age 15.',
                    style={'textAlign': 'center'}
                ),
                dcc.Graph(figure=figs['alcohol'])
            ], md=5),

            dbc.Col([
                html.H2(
                    'Soda beverages are frequently consumed.',
                    style={'textAlign': 'center'}
                ),
                html.H3(
                    'On the other hand, vegetable consumption is really low.',
                    style={'textAlign': 'center'}
                ),
                dcc.Graph(figure=figs['soda_vegs'])
            ], md=6)
        ]),

        html.P('Source: Encuesta Mundial de Salud Escolar, Argentina 2018'),
        html.P('Find the dataset in: https://datos.gob.ar/dataset/salud-base-datos-3deg-encuesta-mundial-salud-escolar-emse-con-resultados-nacionales-argentina/archivo/salud_9888b372-8094-45e2-8b62-40630838c5dc')
    ])


# ---------- APP FACTORY ----------

def create_app():
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    figs = {
        'physical': create_physical_bar(physical_df),
        'fruits': create_fruits_pie(fruits_df),
        'soda_vegs': create_soda_vegs_bar(soda_vegs_df),
        'alcohol': create_alcohol_tree(alcohol_df)
    }

    app.layout = create_layout(figs)
    return app


# ---------- ENTRY POINT ----------

app = create_app()
application = app.server

if __name__ == '__main__':
    app.run(debug=True, port=8080)