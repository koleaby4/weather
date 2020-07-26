import json
import datetime
import pandas as pd
import urllib.request
from pathlib import Path
import gzip


def get_data():
    data_folder = Path('./data')
    gzip_data_file = data_folder / 'weatherjson.gz'

    if not data_folder.exists():
        data_folder.mkdir()

    if not gzip_data_file.exists():
        url = r'https://www.whiteswandata.com/s/weatherjson.gz'
        urllib.request.urlretrieve(url, gzip_data_file)

    destination_data_file = data_folder / "weather.json"
    if not destination_data_file.exists():
        compressed_file_content = gzip_data_file.read_bytes()
        decompressed_content = gzip.decompress(compressed_file_content)
        destination_data_file.write_bytes(decompressed_content)


def get_records(file_path):
    records = []
    with open(file_path, encoding="utf-8") as input_file:
        for record in input_file:
            records.append(json.loads(record.strip()))
    return records


def get_records_by_city_name(city_name, file_path):
    for record in get_records(file_path):
        item = json.loads(record.strip())
        if item["city"]["name"] == city_name:
            yield item


def get_temperatures_from_records(records):
    return [(x["main"]["temp_min"], x["main"]["temp"], x["main"]["temp_min"]) for x in records]


def get_coords(records):
    for record in records:
        lon, lat = record["city"]["coord"].values()
        yield (lat, lon,)


def get_time_interval_from_records(records):
    time_series = pd.Series([x["time"] for x in records])
    start = datetime.datetime.fromtimestamp(pd.Series.min(time_series))
    end = datetime.datetime.fromtimestamp(pd.Series.max(time_series))
    return (start, end)

def get_pressure_to_humidity_pairs(records):
    zipped = [(x["main"]["pressure"], x["main"]["humidity"]) for x in records]
    return list(zip(*zipped))


def get_temperature_to_pressure_pairs(records):
    zipped = [(x["main"]["temp"], x["main"]["pressure"]) for x in records]
    return list(zip(*zipped))

def get_pressure_to_wind_speed_pairs(records):
    zipped = [(x["main"]["pressure"], x["wind"]["speed"]) for x in records]
    return list(zip(*zipped))


def get_temperature_to_lat_pairs(records):
    zipped = [(x["main"]["temp"], x["city"]["coord"]["lat"]) for x in records]
    return list(zip(*zipped))


def get_temperature_to_distance_triplets(records):
    zipped = [(x["main"]["temp"], x["distance"], x["city"]["country"]) for x in records]
    return list(zip(*zipped))


def get_distance_between(a, b):
    """
    source: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    """
    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0

    lat_a = radians(a["lat"])
    lon_a = radians(a["lon"])
    lat_b = radians(b["lat"])
    lon_b = radians(b["lon"])

    lon_delta = lon_b - lon_a
    lat_delta = lat_b - lat_a

    A = sin(lat_delta / 2)**2 + cos(lat_a) * cos(lat_b) * sin(lon_delta / 2)**2
    c = 2 * atan2(sqrt(A), sqrt(1 - A))

    return R * c

def get_points_within_distance(center, max_distance_km, records):

    # we can optimise this for performance
    results = []
    for x in records:
        distance = get_distance_between(center, x["city"]["coord"])
        if distance < max_distance_km:
            x["distance"] = distance
            results.append(x)

    return results

def report_correlation(lhs, rhs):
    correlation = pd.Series(lhs).corr(pd.Series(rhs))

    if correlation > 0:
        direction = "uphill"
    elif correlation < 0:
        direction = "downhill"
    else:
        direction = ""

    abs_correlation = abs(correlation)

    if abs_correlation < 0.1:
        strength = "negligible"
    elif abs_correlation < 0.3:
        strength = "very weak"
    elif abs_correlation < 0.5:
        strength = "weak"
    elif abs_correlation < 0.6:
        strength = "moderate"
    elif 0.7 < abs_correlation < 1:
        strength = "strong"
    elif abs_correlation == 1:
        strength = "perfect"

    return f"{correlation} # {strength} {direction} correlation"
