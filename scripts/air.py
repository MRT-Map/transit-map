from __future__ import annotations

import vector
from autocarter.colour import Colour
from autocarter.drawer import Drawer
from autocarter.network import Line, Network, Station
from autocarter.style import Style
from gatelogue_types import AirAirlineNS, AirAirportNS, AirFlightNS, GatelogueDataNS
from utils import handle_proximity, handle_shared_stations


def air(data: GatelogueDataNS):
    n = Network()

    for airport in (a for a in data if isinstance(a, AirAirportNS)):
        if airport.coordinates is None:
            continue
        if airport.world == "Old":
            x, y = airport.coordinates
            airport.coordinates = (x+30000-3200, y-30000-3200-1000)

        n.add_station(
            Station(
                id=airport.i,
                name=airport.code + " " + airport.name,
                coordinates=vector.obj(
                    x=airport.coordinates[0], y=airport.coordinates[1]
                ),
            )
        )

    for company in (a for a in data if isinstance(a, AirAirlineNS)):
        for flight_id in company.flights:
            flight: AirFlightNS = data[flight_id]

            line = n.add_line(
                Line(
                    id=flight_id,
                    name=company.name + " " + "/".join(flight.codes),
                    colour=Colour.solid("#888"),
                )
            )

            prev_airport_id = None
            for gate_id in flight.gates:
                airport_id = data[gate_id].airport
                if (
                    prev_airport_id is not None
                    and prev_airport_id not in n.stations
                    or airport_id not in n.stations
                ):
                    continue
                if prev_airport_id is not None:
                    n.connect(n.stations[prev_airport_id], n.stations[airport_id], line)
                prev_airport_id = airport_id

    handle_shared_stations(data, n)
    handle_proximity(data, n)
    n.finalise()

    s = Drawer(n, Style(scale=0.075, station_dots=True, stiffness=0.001)).draw()
    with open("maps/air.svg", "w") as f:
        f.write(str(s))
