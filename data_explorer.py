import json


def get_records_by_city_name(city_name, file_path):
    results = []
    with open(file_path, encoding='utf-8') as input_file:
        for record in input_file:
            item = json.loads(record.strip())
            if item['city']['name'] == city_name:
                results.append(item)
    return results


def get_temperatures_from_records(records):
    return [(x['main']['temp_min'], x['main']['temp'], x['main']['temp_min']) for x in records]
