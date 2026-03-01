from __future__ import annotations

from autocarter.colour import Colour
from autocarter.drawer import Drawer
from autocarter.network import Line, Network, Station
from autocarter.style import Style
from autocarter.vector import Vector
import gatelogue_types as gt
from utils import handle_proximity, handle_shared_stations


def air(gd: gt.GD):
    n = Network()

    for airport in gd.nodes(gt.AirAirport):
        if airport.coordinates is None:
            continue
        x, y = airport.coordinates
        if airport.world == "Old":
            x, y = x + 30000 - 3200, y - 30000 - 3200 - 1000

        n.add_station(
            Station(
                id=airport.i,
                name=airport.code + " " + "/".join(airport.names),
                coordinates=Vector(x, y),
            )
        )

    for company in gd.nodes(gt.AirAirline):
        for flight in company.flights:
            line = n.add_line(
                Line(
                    id=flight.i,
                    name=company.name + " " + "/".join(flight.code),
                    colour=Colour.solid("#888"),
                )
            )

            prev_airport_id = None
            for gate in (flight.from_, flight.to):
                airport = gate.airport
                if (
                    prev_airport_id is not None
                    and prev_airport_id not in n.station_id2index
                    or airport.i not in n.station_id2index
                ):
                    continue
                if prev_airport_id is not None:
                    n.connect(n.station(prev_airport_id), n.station(airport.i), line)
                prev_airport_id = airport.i

    handle_shared_stations(gd, n)
    handle_proximity(gd, n)
    n.finalise()

    s = Drawer(n, Style(scale=0.075, station_dots=True, stiffness=0.001)).draw()
    with open("maps/air.svg", "w") as f:
        f.write(str(s))


if __name__ == "__main__":
    gd = gt.GD.urllib_get()

    air(gd)
