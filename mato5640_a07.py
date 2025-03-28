#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px

data = [
    {"Year": 1930, "Winner": "Uruguay", "RunnerUp": "Argentina"},
    {"Year": 1934, "Winner": "Italy", "RunnerUp": "Czechoslovakia"},
    {"Year": 1938, "Winner": "Italy", "RunnerUp": "Hungary"},
    {"Year": 1950, "Winner": "Uruguay", "RunnerUp": "Brazil"},
    {"Year": 1954, "Winner": "Germany", "RunnerUp": "Hungary"},
    {"Year": 1958, "Winner": "Brazil", "RunnerUp": "Sweden"},
    {"Year": 1962, "Winner": "Brazil", "RunnerUp": "Czechoslovakia"},
    {"Year": 1966, "Winner": "England", "RunnerUp": "Germany"},
    {"Year": 1970, "Winner": "Brazil", "RunnerUp": "Italy"},
    {"Year": 1974, "Winner": "Germany", "RunnerUp": "Netherlands"},
    {"Year": 1978, "Winner": "Argentina", "RunnerUp": "Netherlands"},
    {"Year": 1982, "Winner": "Italy", "RunnerUp": "Germany"},
    {"Year": 1986, "Winner": "Argentina", "RunnerUp": "Germany"},
    {"Year": 1990, "Winner": "Germany", "RunnerUp": "Argentina"},
    {"Year": 1994, "Winner": "Brazil", "RunnerUp": "Italy"},
    {"Year": 1998, "Winner": "France", "RunnerUp": "Brazil"},
    {"Year": 2002, "Winner": "Brazil", "RunnerUp": "Germany"},
    {"Year": 2006, "Winner": "Italy", "RunnerUp": "France"},
    {"Year": 2010, "Winner": "Spain", "RunnerUp": "Netherlands"},
    {"Year": 2014, "Winner": "Germany", "RunnerUp": "Argentina"},
    {"Year": 2018, "Winner": "France", "RunnerUp": "Croatia"}
]

df = pd.DataFrame(data)

wins_df = df.groupby("Winner").size().reset_index(name="Wins")
wins_df.rename(columns={"Winner": "Country"}, inplace=True)

iso_codes = {
    "Uruguay": "URY",
    "Italy": "ITA",
    "Germany": "DEU",
    "Brazil": "BRA",
    "England": "GBR",
    "Argentina": "ARG",
    "France": "FRA",
    "Spain": "ESP"
}
wins_df['iso_alpha'] = wins_df['Country'].map(iso_codes)

fig = px.choropleth(
    wins_df,
    locations="iso_alpha",
    color="Wins",
    hover_name="Country",
    color_continuous_scale=px.colors.sequential.Plasma,
    title="FIFA World Cup Wins by Country"
)
fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

app = dash.Dash(__name__)
server = app.server
app.title = "FIFA World Cup Dashboard"

app.layout = html.Div([
    html.H1("FIFA World Cup Finals Dashboard", style={'textAlign': 'center'}),
    
    html.Div([
        dcc.Graph(figure=fig)
    ]),
    
    html.Hr(),
    
    html.Div([
        html.H2("Countries That Have Won the World Cup"),
        html.Ul([html.Li(country) for country in wins_df["Country"].sort_values()])
    ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    
    html.Div([
        html.H2("View Wins by Country"),
        html.Label("Select a Country:"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in sorted(wins_df["Country"].unique())],
            placeholder="Select a country"
        ),
        html.Div(id='country-output', style={'marginTop': 20})
    ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '5%'}),
    
    html.Hr(),
    
    html.Div([
        html.H2("View Final Result by Year"),
        html.Label("Select a Year:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in sorted(df["Year"].unique())],
            placeholder="Select a year"
        ),
        html.Div(id='year-output', style={'marginTop': 20})
    ], style={'width': '50%', 'margin': 'auto'})
])

@app.callback(
    Output('country-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_output(selected_country):
    if selected_country is None:
        return "Please select a country to view the number of World Cup wins."
    wins = wins_df[wins_df["Country"] == selected_country]["Wins"].values[0]
    return html.Div([
        html.P(f"{selected_country} has won the FIFA World Cup {wins} time{'s' if wins > 1 else ''}.")
    ])

@app.callback(
    Output('year-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_year_output(selected_year):
    if selected_year is None:
        return "Please select a year to view the final match details."
    row = df[df["Year"] == selected_year].iloc[0]
    return html.Div([
        html.P(f"In {selected_year}, the winner was {row['Winner']} and the runner-up was {row['RunnerUp']}.")
    ])

if __name__ == '__main__':
    app.run(debug=True)

