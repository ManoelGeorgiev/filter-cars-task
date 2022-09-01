import json
from datetime import datetime


def valid_date(date):
    """
    Validates argument format is dd/mm/yyyy.
    Returns boolean.
    """
    try:
        datetime.strptime(date, '%d/%m/%Y')
        return True
    except ValueError:
        return False


def valid_string(spec):
    """
    Validates that the argument is not an empty or blank string.
    Returns boolean.
    """
    return True if spec.strip() else False


def remove_invalid_manufacturers(manufacturers):
    """
    Removes manufacturers with invalid names or without cars.
    Returns new list.
    """
    valid_manufacturers = list()

    for manufacturer in manufacturers:
        if valid_string(manufacturer['Manufacturer']) and manufacturer['Models']:
            valid_manufacturers.append(manufacturer)

    return valid_manufacturers


def remove_invalid_cars(cars):
    """
    Removes cars with invalid power, torque or year.
    Returns new list.
    """
    valid_cars = list()

    for car in cars:
        if valid_string(car['Power']) and valid_string(car['Torque']) and valid_date(car['Year']):
            valid_cars.append(car)

    return valid_cars


def filter_cars(cars, year, power, weight, fuel):
    """
    Filter cars based on year, power, weight and fuel type.
    Returns new list.
    """
    filtered_cars = list()

    for car in cars:
        car_year = int(car['Year'].split('/')[2])
        car_power = int(car['Power'].split(' ')[0])
        car_weight = int(car['WeightKg'])
        car_fuel = car['FuelType']
        if car_year >= year and car_fuel != fuel and car_power > power and car_weight >= weight:
            filtered_cars.append(car)

    return filtered_cars


def read_file(file_path, encoding):
    """
    Reads file content.
    Returns JSON object.
    """
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return json.load(file)
    except FileNotFoundError:
        print('File not found!')


def write_file(data, file_path, encoding):
    """
    Writes JSON object to file.
    """
    try:
        with open(file_path, 'w', encoding=encoding) as file:
            json.dump(data, file, indent=2)
    except FileNotFoundError:
        print('Directory not found!')


def main():
    input_file_path = 'cars.json'
    output_file_path = 'carsResult.json'
    file_encoding = 'utf-8-sig'
    min_year = 2018
    min_power = 200
    min_weight = 1500
    unwanted_fuel_type = 'Diesel'
    cars_data = read_file(input_file_path, file_encoding)

    for manufacturer in cars_data:
        validated_cars = remove_invalid_cars(manufacturer['Models'])
        manufacturer['Models'] = filter_cars(validated_cars, min_year, min_power, min_weight, unwanted_fuel_type)

    validated_manufacturers = remove_invalid_manufacturers(cars_data)
    write_file(validated_manufacturers, output_file_path, file_encoding)


if __name__ == '__main__':
    main()
