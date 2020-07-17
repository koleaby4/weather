import pandas as pd
import plotly.express as px
import gmaps
import os

if __name__ == "__main__":
    df = pd.read_csv(r"./data/weather.csv")

    # ==== temprerature by city and time ====

    # fig = px.scatter(
    #     df,
    #     x="city_name",
    #     y="time",
    #     color="temp"
    # )

    # fig.show()


    # ==== avg temperature by country and time ====

    temp_by_country_and_time = df.groupby(['country', 'time'],  as_index=False)['temp'].agg('mean')
    temp_by_country_and_time.columns = ["country", "time", "avg_temp"]

    fig = px.scatter(
        temp_by_country_and_time,
        x="country",
        y="time",
        color="avg_temp",
        title='Avg temperature by country and time (rounded to h)'
    )

    fig.show()

    # ----------------------------------------------------------------------

    # temp_by_country_and_time.plot(x='date', y='payout_value',kind="bar")
    # temp_by_country_and_time.show()

    # gmaps.configure(api_key=os.environ["GOOGLE_API_KEY"])
