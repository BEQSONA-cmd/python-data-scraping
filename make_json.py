import json
import os
import csv
import random
from time import sleep

names = []

def get_names():
    file = "names.csv"
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f]

names = get_names()

class Airline:
    def __init__(self, name, country, id):
        self.name = name
        self.country = country
        self.id = id

    def __str__(self):
        return f'Name: {self.name}, Country: {self.country}'

def add_json(airline):
    filename = 'airline.json'
    if os.path.exists(filename):
        with open(filename, 'r+', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

            data.append({
                'name': airline.name,
                'country': airline.country,
                'logo': f'{airline.id}.png',
                'stars': round(random.uniform(3.5, 4.9), 1)
            })

            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
    else:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([{
                'name': airline.name,
                'country': airline.country
            }], f, indent=4, ensure_ascii=False)

def get_country_from_openflights(name):
    with open("airlines.dat", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == name or row[2] == name:
                return row[6]

    return "Unknown"

if __name__ == '__main__':
    iter = 1
    for name in names:
        country = get_country_from_openflights(name)
        airline = Airline(name, country, iter)

        add_json(airline)
        print(f"Added: {airline}")
        iter += 1

