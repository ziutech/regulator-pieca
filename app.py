#!/usr/bin/env python3
from dash.dependencies import State
import pandas as pd
import plotly.express as px
import oven
from dash import Dash, html, dcc, Output, Input
import layout


app = Dash(__name__)
app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        layout.num_input(
                            id="goal_temp",
                            label="oczekiwana temperatura",
                            min=150,
                            max=220,
                        ),
                        # df = run(k_p=0.022, T_i=200, T_d=5)
                        layout.num_input(
                            id="k_p",
                            label="wzmocnienie regulatora",
                            min=0.01,
                            max=0.05,
                            default=0.022,
                            step=0.001,
                        ),
                        layout.num_input(
                            id="T_i",
                            label="stała zdwojenia",
                            min=1,
                            max=400,
                            default=200,
                            step=1,
                        ),
                        layout.num_input(
                            id="T_d",
                            label="stała wyprzedzenia",
                            min=0,
                            max=10,
                            default=5,
                            step=0.1,
                        ),
                    ],
                    id="sliders",
                    className="list",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div("""Oś X:"""),
                                dcc.Dropdown(value="", options=[], id="choice_x"),
                            ],
                        ),
                        html.Div(
                            [
                                html.Div("""Oś Y:"""),
                                dcc.Dropdown(value="", options=[], id="choice_y"),
                            ],
                        ),
                    ],
                    id="options",
                    className="list",
                ),
            ],
            id="settings",
        ),
        dcc.Store(id="data"),
        dcc.Graph(id="graph"),
    ]
)


@app.callback(
    output=dict(
        data=Output("data", "data"),
        dropdowns={
            "x": (Output("choice_x", "value"), Output("choice_x", "options")),
            "y": (Output("choice_y", "value"), Output("choice_y", "options")),
        },
    ),
    inputs={
        "inputs": dict(
            zip(layout.fields(), [Input(input, "value") for input in layout.fields()])
        ),
        "dropdowns": {
            "x": State("choice_x", "value"),
            "y": State("choice_y", "value"),
        },
    },
)
def simulate(inputs, dropdowns):
    df = oven.simulate(**inputs)

    x = dropdowns["x"]
    y = dropdowns["y"]
    columns = list(df.columns)

    return dict(
        data=df.to_json(orient="split"),
        dropdowns={
            "x": (x if x else columns[0], columns),
            "y": (y if y else columns[1], columns),
        },
    )


@app.callback(
    Output("graph", "figure"),
    inputs=[
        Input("data", "data"),
        Input("choice_x", "value"),
        Input("choice_y", "value"),
    ],
)
def update_graph(data, x, y):
    # TODO previous graph
    return px.line(
        pd.read_json(data, orient="split"),
        range_y=[-20, 240],
        x=x,
        y=y,
    )


app.run_server(debug=True)
#
