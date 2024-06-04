from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

app = Dash(__name__)

spacex_df = pd.read_csv('spacex_launch_dash.csv')

site_list = list(spacex_df['Launch Site'].unique())
site_list = ['ALL'] + site_list

options=[{'label': s, 'value': s} for s in site_list]
min_value = spacex_df['Payload Mass (kg)'].min()
max_value = spacex_df['Payload Mass (kg)'].max()

app.layout = html.Div([
                dcc.Dropdown(id='site-dropdown',
                            options=options,
                            value='ALL',
                            placeholder="Select a Launch Site here",
                            searchable=True
                            ),
                dcc.Graph(id='success-pie-chart'),
                html.P('Payload Mass (kg)'),
                dcc.RangeSlider(id='payload-slider',
                            min=0, max=10000, step=1000,
                            marks={0: '0',
                                2500: '2500',
                                5000:'5000',
                                7500:'7500',
                                10000:'10000'},
                            value=[min_value, max_value]),
                dcc.Graph('success-payload-scatter-chart')
])

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['class'] == 1]
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total success by launches')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df['c'] = 1
        fig = px.pie(filtered_df, values='c', 
        names='class', 
        title=f'Total success launches for site {entered_site}')
        # return the outcomes piechart for a selected site
    return fig


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value"))
def get_chart(entered_site, play_load):
    if entered_site == 'ALL':
        filtered_df = spacex_df.copy()
        fig = px.scatter(filtered_df, x='Payload Mass (kg)',
        y='class', color='Launch Site',
        title='Correlation between Playload and Sucsess for all Sites')
    else:
        max = play_load[1]
        min = play_load[0]
        filtered_df = spacex_df[(spacex_df['Launch Site']==entered_site) & (spacex_df['Payload Mass (kg)'] <=  max) & (spacex_df['Payload Mass (kg)'] >=  min)]
        print(filtered_df.info())
        fig = px.scatter(filtered_df, x='Payload Mass (kg)',
        y='class', color='Booster Version Category',
        title=f'Correlation between Playload and Sucsess in {entered_site} by Booster versinon category')

    return fig


if __name__ == '__main__':
    app.run(debug=True)