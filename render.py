import os
import pathlib

import gmaps
import numpy as np
import pandas as pd
import plotly.express as px


def get_api_key():
    api_key = os.environ.get("GOOGLE_API_KEY") or pathlib.Path("secret.txt").read_text().strip()

    if not api_key:
        msg = "Could not find gmaps api key.\n"
        msg += "Please declare it in 'GOOGLE_API_KEY' env variable or place into secret.txt"
        raise RuntimeError(msg)

    return api_key


def get_data_points_figure(data):
    gmaps.configure(api_key=get_api_key())
    figure_layout = {'height' : '500px', 'margin': '0 auto 0 auto'}
    fig = gmaps.figure(map_type="ROADMAP", zoom_level=2, center=(30, 31), layout=figure_layout)
    heatmap_layer = gmaps.heatmap_layer(data)
    heatmap_layer.max_intensity = 100
    heatmap_layer.point_radius = 1
    heatmap_layer.dissipating = False

    # ToDo: consider using gmaps.symbol_layer with small markers

    fig.add_layer(heatmap_layer)
    return fig


if __name__ == "__main__":
    # df = pd.read_csv(r"./data/weather.csv")

    # ==== temperatures by city and time ====

    # fig = px.scatter(df, x="city_name", y="time", color="temp")

    # fig.show()

    # ==== avg temperature by country and time ====

    # temp_by_country_and_time = df.groupby(['country', 'time'],  as_index=False)['temp'].agg('mean')
    # temp_by_country_and_time.columns = ["country", "time", "avg_temp"]

    # fig = px.scatter(
    #     temp_by_country_and_time,
    #     x="country",
    #     y="time",
    #     color="avg_temp",
    #     title='Avg temperature by country and time (rounded to h)'
    # )

    # fig.show()

    # ----------------------------------------------------------------------

    # temp_by_country_and_time.plot(x='date', y='payout_value',kind="bar")
    # temp_by_country_and_time.show()

    # gmaps.configure(api_key=os.environ["GOOGLE_API_KEY"])

    # heatmap_layer = gmaps.heatmap_layer(coords)
    # heatmap_layer.max_intensity = 100
    # heatmap_layer.point_radius = 5

    # fig.add_layer(heatmap_layer)
    # fig

    print(get_api_key())
