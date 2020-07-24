import json
import datetime


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
    results = []
    for record in records:
        lon, lat = record["city"]["coord"].values()
        results.append((lat, lon,))
    return results


def get_time_interval_from_records(records):
    times = {x["time"] for x in records}
    start = datetime.datetime.fromtimestamp(min(times))
    end = datetime.datetime.fromtimestamp(max(times))
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
