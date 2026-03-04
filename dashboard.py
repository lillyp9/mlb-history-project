import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import sqlite3
import pandas as pd
from pathlib import Path

#have the absolute path to the SQlite database file
DB_PATH = Path(__file__).resolve().parent / "db" / "mlb_history.db"
print(DB_PATH)

#Function to load data 
def get_data(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df
#-------DROPDOWN DATA LOADING -------
#Load year options for dropdowns
years_df = get_data("SELECT DISTINCT year FROM team_standings ORDER BY year")
year_options = [{'label': str(year), 'value': year} for year in years_df['year']]

#load team options for dropdowns
teams_df = get_data("SELECT DISTINCT team FROM team_standings ORDER BY team")
team_options = [{'label': team, 'value': team} for team in teams_df['team']]

#Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # Expose the server variable for deployments

#App layout
app.layout = html.Div([
    html.H1("MLB History Dashboard", style={'textAlign': 'center', 'color': '#003366' ,'marginBottom': '20px'}),

# ====== Visualization 1: Top Team by Wins ======
#Bar chart showing each teams win for a selected year
    html.Div([
        html.H2("Top Team by Wins"),
        html.P("Select a year to see how each team performed in terms of wins."),
        dcc.Dropdown(
            id='year-dropdown-wins',
            options=year_options,
            value=1990, #default value
            clearable=False,
            style={'width': '200px', 'marginBottom': '10px'}
        ),
        dcc.Graph(id='wins-bar-chart')
    ], style={'marginBottom': '50px', 'padding': '20px', 'backgroundColor': '#f0f8ff', 'borderRadius': '10px'}),                     
    
# ====== Visualization 2: Hitting Leaders ======
#Bar chart showing top players for a selected statistic and year
    html.Div([
        html.H2("Hitting Leaders"),
        html.P("Select a year and statistic to see the top players."),
        #Year dropdown - will trigger the update of the stat dropdown options and default value
        dcc.Dropdown(
            id='year-dropdown-hitting',
            options=year_options,
            value=1990, #default value
            clearable=False,
            style={'width': '200px', 'marginBottom': '10px'}
        ),
        #stat selector - options will be populated by callback based on the selected year
        dcc.Dropdown(
            id='stat-dropdown',
            options=[], #options will be populated by callback
            value=None, #default value will be set by callback
            clearable=False,
            style={'width': '300px', 'marginBottom': '10px'}
        ),
        
        dcc.Graph(id='hitting-bar-chart')
    ], style={'marginBottom': '50px', 'padding': '20px', 'backgroundColor': '#f0f8ff', 'borderRadius': '10px'}),
    
# ====== Visualization 3: Team Performance Comparison ======
#line chart showing slected teams wins over time
    html.Div([
        html.H2("Team Wins Over Time (1990-2020)"),
        html.P("Select teams to compare their wins over time."),
        dcc.Dropdown(
            id='team-dropdown',
            options=team_options,
            value='New York Yankees',  #default value
            clearable=False,
            style={'width': '300px'}
        ),
            dcc.Graph(id='wins-line-chart')
        ], style={'marginBottom': '50px'}),
    ])

#----Callback 1: Wins Bar Chart ----
#Trigger when user selects different year
#Queries team standings and renders a bar chart sorted by wins 
@app.callback(
    Output('wins-bar-chart', 'figure'),
    Input('year-dropdown-wins', 'value')
)

def update_wins_chart(year):
    df = get_data(
        "SELECT team, wins, losses FROM team_standings WHERE year = ? ORDER BY wins DESC",
        params=(year,)
    )
    fig = px.bar(df, x='team', y='wins',
                 title=f"Team Wins in {year}",
                 labels={'team': 'Team', 'wins': 'Wins'},
                 color='wins',
                 color_continuous_scale='Blues')
    fig.update_layout(xaxis_tickangle=-45)
    return fig

#----Callback Dropdown : Populate stat dropdown
#When year changes reload avaible hitting stats for that year and set default value to the first stat in the list   

@app.callback(
    Output('stat-dropdown', 'options'),
    Output('stat-dropdown', 'value'),
    Input('year-dropdown-hitting', 'value')
)
def update_stat_dropdown(year):
    df = get_data(
        "SELECT DISTINCT statistic FROM hitting_leaders WHERE year = ?",
        params=(year,)
    )
    options = [{'label': stat, 'value': stat} for stat in df['statistic']]
    value = options[0]['value'] if options else None
    return options, value

#-----Calback for hitting bar chart ----
#Tiggered when either the year statistic dropdown changes 
#Queries hitting leaders and render a bar chart showing top players 
@app.callback(
    Output('hitting-bar-chart', 'figure'),
    Input('year-dropdown-hitting', 'value'),
    Input('stat-dropdown', 'value')
)
def update_hitting_chart(year, statistic):
    #Clause against empty statistic to avoid querying with None value which would return all records for the year and cause an error when trying to plot
    if not statistic:
        return {}
    
    df = get_data(
        "SELECT player_name, team, value FROM hitting_leaders WHERE year = ? AND statistic = ? ORDER BY value DESC",
        params=(year, statistic)
    )
    
    fig = px.bar(df, x='player_name', y='value',
                 title=f"{statistic} Leaders in {year}",
                 labels={'player_name': 'Player', 'value': statistic},
                 color='team')
    fig.update_layout(xaxis_tickangle=-45)
    return fig

#----Callback3 for wins line chart ----
#Tiggered when user selects different team from dropdown
#Queries all year of wins for that team and renders a line chart showing wins over time from 1990-2020
@app.callback(
    Output('wins-line-chart', 'figure'),
    Input('team-dropdown', 'value')
)
def update_line_chart(team):
    df = get_data(
        "SELECT year, wins FROM team_standings WHERE team = ? ORDER BY year",
        params=(team,)
    )
    df['year'] = df['year'].astype(str) # convert year to string so plotly treats it as a category not a number 
    #then line chart
    fig = px.line(df, x='year', y='wins',
              title=f"{team} Wins Over Time (1990-2020)",
              labels={'year': 'Year', 'wins': 'Wins'},
              markers=True
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)

    