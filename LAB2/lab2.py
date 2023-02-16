import pandas as pd
import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output

types = ['Very interested', 'Somewhat interested', 'Not interested']
#import data:
df = pd.read_csv('lab2 Topic_Survey_Assignment.csv', encoding= 'ISO-8859-1')
df.rename(columns={'Unnamed: 0': 'Topic'}, inplace=True)

#Calculating percentage to analyze
df_per = df[['Topic']]
df_per = round(df[types]/2233*100, 2)
df_per.insert(0, 'Topic', df['Topic'], True)

#Create histogram
fig_bar = px.histogram(df_per, x='Topic', y=types, barmode='group', text_auto=True)

#Define the options
options = [
    {'label': 'Full Histogram', 'value': 'Full Histogram'},
    {'label': 'Big Data (Spark / Hadoop)', 'value': 'Big Data (Spark / Hadoop)'},
    {'label': 'Data Analysis / Statistics', 'value': 'Data Analysis / Statistics'},
    {'label': 'Data Journalism', 'value': 'Data Journalism'},
    {'label': 'Data Visualization', 'value': 'Data Visualization'},
    {'label': 'Deep Learning', 'value': 'Deep Learning'},
    {'label': 'Machine Learning', 'value': 'Machine Learning'}
]


app = dash.Dash(__name__)
app.layout = html.Div([html.H1("Percentage of Respondents' Interest in Data Science Topics",
                        style={'text-align': 'center', 'color': '#FFB6C1', 'font-size': 50}),
                        html.Br(),
                        dcc.Graph(id='bar-plot', figure=fig_bar),
                        html.Div([
                                dcc.Dropdown(id='topic-dropdown', options=options, value='Full Histogram',
                                style={'width': '50%', 'margin': 'auto'})
                                ], style={'text-align': 'center'})
                                ])


@app.callback(
    Output('bar-plot', 'figure'),
    [Input('topic-dropdown', 'value')]
)

def update_plot(topics):
    if topics == "Full Histogram" or topics is None:
        fig_bar = px.histogram(df_per, x='Topic', y=types, barmode='group', text_auto=True)
        fig_bar.update_layout(title_text="Percentage of Respondents' Interest in Data Science Topics")
    else:
        filtered_df = df_per[df_per['Topic'] == topics]
        fig_bar = px.histogram(filtered_df, x='Topic', y=types, barmode='group', text_auto=True)
        fig_bar.update_layout(title_text=f"Percentage of Respondents' Interest in {topics}")
    return fig_bar

if __name__ =='__main__':
    app.run_server(port=8002, host='192.168.2.10', debug=True)