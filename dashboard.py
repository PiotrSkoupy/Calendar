import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go 
import pycountry
import dash_bootstrap_components as dbc
import pycountry_convert as pc
import dash_table
from dash import Dash, dcc, html, Input, Output 

DATABASE = 'sqlite:///calendar_holidays.sqlite'
TABLE = 'holidays'

df = pd.read_sql(TABLE, DATABASE)
df1 = df.copy()
df['Amount'] = 1
df = df.groupby(['Country Name','Month','Year']).sum()
df.reset_index(inplace=True)
df = df[['Country Name', 'Month', 'Year', 'Amount']]

countries_name = []
countries_iso = []
continent =[]


def country_to_continent(country_name):
    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name

for country in pycountry.countries:
    countries_name.append(country.name)
    countries_iso.append(country.alpha_3)
    try:
        continent.append(country_to_continent((country.name)))
    except KeyError:
        continent.append(('Antarctica'))

d = {'Country Name':countries_name, 'iso_alpha': countries_iso, 'Continent':continent}
countries_frame = pd.DataFrame(d)

df = pd.merge(df, countries_frame, on='Country Name')
df1 = pd.merge(df1, countries_frame, on='Country Name')
GIT_LOGO = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"

# App layout
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])


page_1_layout = html.Div([
dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=GIT_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("My GitHub", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://github.com/PiotrSkoupy",
        ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Table Site", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="/page-2",
        ),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
    ],
    color="dark",
    dark=True,
    ),

    html.H1("Amount of Holidays in each country per month", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_month",
                 options=[
                     {"label": "January", "value": 1},
                     {"label": "February", "value": 2},
                     {"label": "March", "value": 3},
                     {"label": "April", "value": 4},
                     {"label": "May", "value": 5},
                     {"label": "June", "value": 6},
                     {"label": "July", "value": 7},
                     {"label": "August", "value": 8},
                     {"label": "September", "value": 9},
                     {"label": "October", "value": 10},
                     {"label": "November", "value": 11},
                     {"label": "December", "value": 12}],
                 multi=False,
                 value=1,
                 style={'width': "40%"}
                 ),
   html.Br(),
dcc.Dropdown(id="slct_continent",
                 options=[
                     {"label": "All continents", "value": 'world'},
                     {"label": "Europe", "value": 'Europe'},
                     {"label": "Asia", "value": 'Asia'},
                     {"label": "North America", "value": 'North America'},
                     {"label": "South America", "value": 'South America'},
                     {"label": "Africa", "value": 'Africa'},
                     {"label": "Australia", "value": 'Australia'}],
                 multi=False,
                 value=1,
                 style={'width': "40%"},
                 placeholder='Please choose a continent'
                 ),
    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='my_holidays_map', figure={})

])

''' Funkcja która pozwala na aktualizowanie naszego dashboardu'''
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_holidays_map', component_property='figure')],
    Input(component_id='slct_month', component_property='value'),
    Input(component_id='slct_continent', component_property='value')
)
def update_graph(slct_month, slct_contintent):
    container = ""
    dff = df.copy()
    dff = dff[dff["Month"] == slct_month]
    if slct_contintent == 1 or slct_contintent is None:
        scope = 'world'
    else:
        scope = slct_contintent.lower()

    fig = px.choropleth(
    data_frame=dff,
    locations="iso_alpha",
    color='Amount',
    hover_data=['Country Name', 'Amount'],
    color_continuous_scale=px.colors.sequential.YlOrRd,
    labels={'Amount': 'Amount of holidays during this month'},
    scope = scope)
    return container, fig


page_2_layout = html.Div([
dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=GIT_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("My GitHub", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://github.com/PiotrSkoupy",
        ),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Map Site", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="/page-1",
        ),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)
    ],
    color="dark",
    dark=True,
    ),
html.Div(
    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df1.columns],
    filter_action="native",
    data=df1.to_dict('records'),
    page_action="native",
        page_current= 0,
        page_size= 10,
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
    },
        )),
    html.Div(id='output_container1', children=[]),
    html.Div(id='page-2-content'),
])


@app.callback(Output(component_id='output_container1', component_property='component'),
              Input(component_id='slct_month', component_property='value'),
              Input(component_id='slct_continent', component_property='value')
              )
def page_2_radios(container):
    container = ""
    return  container

'''Funkcja pozwalająca na przełączanie się między stronami'''
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-2':
        return page_2_layout
    else:
        return page_1_layout

if __name__ == '__main__':
    app.run_server(debug=True)
