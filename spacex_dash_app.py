# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()
launch_sites_df = spacex_df.groupby(["Launch Site"], as_index=False).first()
options_site = [
    {"label": site, "value": site} for site in launch_sites_df["Launch Site"]
]
opt = []
for i in range(len(launch_sites_df) + 1):
    if i == 0:
        opt.append({"label": "All Sites", "value": "ALL"})
    else:
        opt.append(options_site[i - 1])

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        dcc.Dropdown(
            id="site-dropdown",
            options=opt,
            value="ALL",
            placeholder="Select a Launch Site here",
            searchable=True,
        ),
        html.Br(),
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            marks={0: "0", 2500: "2500", 5000: "5000", 7500: "7500", 10000: "10000"},
            value=[min_payload, max_payload],
        ),
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == "ALL":
        fig = px.pie(
            filtered_df,
            values="class",
            names="Launch Site",
            title="Total Success Launches by Site",
        )
        return fig
    else:
        filtered_df = filtered_df[filtered_df["Launch Site"] == entered_site]
        fig = px.pie(
            filtered_df,
            names="class",
            title="Total Success Launches for Site {}".format(entered_site),
        )
        return fig


@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
    Input(component_id="payload-slider", component_property="value"),
)
def get_scatter_chart(entered_site, entered_payload):
    filtered_df = spacex_df
    if entered_site == "ALL":
        fig = px.scatter(
            filtered_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Correlation between Payload and Success for all Sites"
        )
        fig.update_layout(xaxis_title='Payload Mass (kg)', yaxis_title='Success Rate')
        fig.update_xaxes(range=entered_payload)
        return fig
    else:
        filtered_df = filtered_df[filtered_df["Launch Site"] == entered_site]
        fig = px.scatter(
            filtered_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Correlation between Payload and Success for Site {}".format(
                entered_site
            )
        )
        fig.update_layout(xaxis_title='Payload Mass (kg)', yaxis_title='Success Rate')
        fig.update_xaxes(range=entered_payload)
        return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
