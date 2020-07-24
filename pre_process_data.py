# import pandas as pd

# df = pd.read_json('weather_subset.json', lines=True)

# df_city = df["city"].apply(pd.Series)
# df = df.drop(['city'], axis=1)
# df = pd.concat([df_city, df], axis=1)

# df_main = df["main"].apply(pd.Series)
# df = df.drop(['main'], axis=1)
# df = pd.concat([df, df_main], axis=1)

# df_wind = df.wind.apply(pd.Series)
# df_wind.columns = ["wind_speed", "wind_degrees"]
# df = df.drop(['wind'], axis=1)
# df = pd.concat([df, df_wind], axis=1)


##############################################################

# import pandas as pd
# import json

# result = None
# with open(r'./data/weather_subset.json',  encoding="utf8") as data_source:
#     for record in data_source:
#         js = json.loads(record)
#         result = pd.concat([result, pd.json_normalize(js)],  ignore_index=True)

# result.weather = result.weather.str[0]

# weather = result.weather.apply(pd.Series)
# weather.columns = ["weather.id", "weather.main", "weather.description", "weather.icon"]

# weather = result.weather.apply(pd.Series)

# result = pd.concat([result, weather], axis=1)
# result = result.drop("weather", axis=1)

# result.to_csv(r'./data/weather_subset.csv', index = False)

######################## rendering ###########################

# WIP

import pandas as pd

def expand_column(df, col_name):
    frame = df[col_name].apply(pd.Series)
    frame.columns = [f"{col_name}_{x}" for x in frame.columns]

    df.drop(col_name, axis=1, inplace=True)
    df = pd.concat([df, frame], axis=1)
    # Drop rows with any empty cells
    df.dropna(axis=0, how='any', thresh=None,subset=None, inplace=True)

    return df

def replace_in_column_names(df, old_value, new_value):
    return df.rename(columns={col_name : col_name.replace(old_value, new_value) for col_name in df.columns})

def cleanse_data(df):
    # empty city names
    df = df[df.city_name != "-"]
    df = df[df.city_name != ""]

    # remove continents
    df = df[df.country != ""]
    return df

if __name__ == "__main__":
    file_name = "weather"
    # file_name = "weather_subset"

    df = pd.read_json(f'./data/{file_name}.json', lines=True)

    df = expand_column(df, "city")
    df = df.drop("city_findname", axis=1)

    df = replace_in_column_names(df, "city_country", "country")
    df = replace_in_column_names(df, "city_zoom", "zoom")

    df = expand_column(df, "city_coord")
    df = replace_in_column_names(df, "city_coord_", "")

    df = expand_column(df, "clouds")
    df = replace_in_column_names(df, "clouds_all", "clouds")

    df = expand_column(df, "main")
    df = replace_in_column_names(df, "main_", "")

    df = expand_column(df, "wind")
    df.time = df.time.apply(lambda t : pd.to_datetime(t, unit='s'))

    df = cleanse_data(df)

    # df["time_rounded"] = df['time'].apply(lambda t : t.round('H')

    df.to_csv(fr'./data/{file_name}.csv', index = False)
