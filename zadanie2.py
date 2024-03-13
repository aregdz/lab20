#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os.path

import click


@click.group()
@click.version_option(version="0.1.0")
def flights():
    """
    Manage flight data.
    """
    pass


@flights.command()
@click.option(
    "-f", "--filename", default="flights.json", help="The data file name"
)
@click.option(
    "-d",
    "--destination",
    prompt="Destination",
    help="Destination of the flight",
)
@click.option(
    "-dd",
    "--departure_date",
    prompt="Departure Date",
    help="Departure date of the flight",
)
@click.option(
    "-at",
    "--aircraft_type",
    prompt="Aircraft Type",
    help="Aircraft type of the flight",
)
def add(filename, destination, departure_date, aircraft_type):
    """
    Add a new flight.
    """
    flights = load_flights(filename)
    flights.append(
        {
            "destination": destination,
            "departure_date": departure_date,
            "aircraft_type": aircraft_type,
        }
    )
    save_flights(filename, flights)


@flights.command()
@click.option(
    "-f", "--filename", default="flights.json", help="The data file name"
)
def display(filename):
    """
    Display all flights.
    """
    flights = load_flights(filename)
    display_flights(flights)


@flights.command()
@click.option(
    "-f", "--filename", default="flights.json", help="The data file name"
)
@click.option(
    "-at",
    "--aircraft_type",
    prompt="Aircraft Type",
    help="Aircraft type to select flights",
)
def select(filename, aircraft_type):
    """
    Select flights by aircraft type.
    """
    flights = load_flights(filename)
    selected = select_flights(flights, aircraft_type)
    display_flights(selected)


def add_flight(flights, destination, departure_date, aircraft_type):
    """
    Add flight data.
    """
    flights.append(
        {
            "destination": destination,
            "departure_date": departure_date,
            "aircraft_type": aircraft_type,
        }
    )
    return flights


def display_flights(flights):
    """
    Display list of flights.
    """
    if flights:
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 20, "-" * 8
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^20} | {:^8} |".format(
                "No", "Destination", "Departure Date", "Aircraft Type"
            )
        )
        print(line)
        for idx, flight in enumerate(flights, 1):
            print(
                "| {:>4} | {:<30} | {:<20} | {:>8} |".format(
                    idx,
                    flight.get("destination", ""),
                    flight.get("departure_date", ""),
                    flight.get("aircraft_type", ""),
                )
            )
            print(line)
    else:
        print("List of flights is empty.")


def select_flights(flights, aircraft_type):
    """
    Select flights by aircraft type.
    """
    result = []
    for flight in flights:
        if flight.get("aircraft_type") == aircraft_type:
            result.append(flight)
    return result


def save_flights(file_name, flights):
    """
    Save all flights to a JSON file.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(flights, fout, ensure_ascii=False, indent=4)


def load_flights(file_name):
    """
    Load all flights from a JSON file.
    """
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as fin:
            return json.load(fin)
    else:
        return []


if __name__ == "__main__":
    flights()
