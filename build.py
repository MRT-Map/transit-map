from __future__ import annotations

import json

import niquests
import vector
from autocarter.colour import Colour, Stroke
from autocarter.drawer import Drawer, Style
from autocarter.network import Connection, Line, Network, Station


def _station(n: Network, company: dict, data: dict[str, dict]):
    stations = {}
    for station_i in company["stations"]:
        station = data[str(station_i)]
        coordinates = station["coordinates"]
        if coordinates is None:
            print("No coords", company['name'], station["name"])  # noqa: T201
            continue
        if station["name"] is None:
            continue
        station = n.add_station(
            Station(
                id=station_i,
                name=station["name"].replace("&", "&amp;"),
                coordinates=vector.obj(x=coordinates[0], y=coordinates[1]),
            )
        )
        stations[station.name] = station
    return stations


def _connect(n: Network, company: dict, data: dict[str, dict]):
    visited_stations = []
    for station_i in company["stations"]:
        if station_i not in n.stations:
            continue
        station = data[str(station_i)]
        if not station["connections"]:
            print("No conns", company['name'], station["name"])  # noqa: T201
        for conn_station_i, connections in station["connections"].items():
            conn_station_i = int(conn_station_i)
            if (
                    conn_station_i in visited_stations
                    or conn_station_i not in n.stations
            ):
                continue
            for connection in connections:
                n.connect(
                    n.stations[station_i],
                    n.stations[conn_station_i],
                    n.lines[connection["line"]],
                )
        visited_stations.append(station)


def mrt(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "MRT")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        n.add_line(
            Line(
                id=line_i,
                name="MRT " + line["code"],
                colour=Colour.solid(line["colour"] or "#888"),
            )
        )

    stations = {}
    for station_i in company["stations"]:
        station = data[str(station_i)]
        if station["world"] == "Old" or not station["connections"]:
            continue
        coordinates = station["coordinates"] or [0, 0]
        station = n.add_station(
            Station(
                id=station_i,
                name=(
                        " ".join(sorted(station["codes"]))
                        + " "
                        + (station["name"] or "")
                ).strip(),
                coordinates=vector.obj(x=coordinates[0], y=coordinates[1]),
            )
        )
        stations[station.name] = station

    _connect(n, company, data)

    return stations


def nflr(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "nFLR")

    lines = {}
    for line_i in company["lines"]:
        line = data[str(line_i)]
        name = line["name"]
        if name.startswith("W"):
            colour = Colour(
                (
                    Stroke(dashes=line["colour"], thickness_multiplier=1.0),
                    Stroke(dashes="#fff", thickness_multiplier=0.5),
                )
            )
        else:
            colour = Colour.solid(line["colour"] or "#888")
        line = n.add_line(
            Line(id=line_i, name="nFLR " + line["code"], colour=colour)
        )
        lines[line.name] = line

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations, lines


def intra(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "IntraRail")

    lines = {}
    for line_i in company["lines"]:
        line = data[str(line_i)]
        line = n.add_line(
            Line(
                id=line_i,
                name="IR "
                     + line["code"].replace("<", "&lt;").replace(">", "&gt;"),
                colour=Colour.solid(line["colour"] or "#888"),
            )
        )
        lines[line.name] = line

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations, lines


def blu(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "BluRail")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        n.add_line(Line(id=line_i, name="Blu " + line["code"], colour=Colour.solid(
            line["colour"] or "#888"
        )))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def rlq(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "RaiLinQ")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        n.add_line(Line(id=line_i, name="RLQ " + line["code"], colour=Colour.solid(line["colour"] or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def wzr(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "West Zeta Rail")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        n.add_line(Line(id=line_i, name="WZR " + line["code"], colour=Colour.solid(line["colour"] or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def mtc(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "MarbleRail")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        n.add_line(Line(id=line_i, name="MTC " + line["code"], colour=Colour.solid(line["colour"] or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def nsc(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "Network South Central")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        n.add_line(Line(id=line_i, name="NSC " + line["code"], colour=Colour.solid(line["colour"] or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def redtrain(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "RedTrain")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        n.add_line(
            Line(id=line_i, name="RedTrain " + line["code"], colour=Colour.solid(line["colour"] or "#888"))
        )

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def rn(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "RailNorth")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        n.add_line(Line(id=line_i, name=line["code"], colour=Colour.solid(line["colour"] or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def fr(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "Fred Rail")

    lines = {}
    for line_i in company["lines"]:
        line = data[str(line_i)]
        line = n.add_line(
            Line(id=line_i, name="FR " + line["code"], colour=Colour.solid(line["colour"] or "#888"))
        )
        lines[line.name] = line

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations, lines


def main():
    data = niquests.get(
        "https://raw.githubusercontent.com/MRT-Map/gatelogue/dist/data_no_sources.json"
    )
    data = json.loads(data.text)['nodes']
    n = Network()
    mrt(n, data)
    s_nflr, l_nflr = nflr(n, data)
    s_intra, l_intra = intra(n, data)
    blu(n, data)
    rlq(n, data)
    wzr(n, data)
    mtc(n, data)
    nsc(n, data)
    rn(n, data)
    s_fr, l_fr = fr(n, data)
    redtrain(n, data)

    s_nflr["Deadbush Karaj Expo"].adjacent_stations[l_nflr["nFLR R5A"].id] = [
        [s_nflr["Deadbush Works"].id],
        [s_nflr["Deadbush Valletta"].id, s_nflr["Deadbush New Euphorial"].id],
    ]
    s_nflr["Sansvikk Kamprad Airfield"].adjacent_stations[l_nflr["nFLR R23"].id] = [
        [s_nflr["Sansvikk Karlstad"].id],
        [s_nflr["Glacierton"].id, s_nflr["Port Dupont"].id],
    ]
    s_nflr["Glacierton"].adjacent_stations[l_nflr["nFLR R23"].id] = [
        [s_nflr["Snowydale"].id],
        [s_nflr["Sansvikk Kamprad Airfield"].id, s_nflr["Port Dupont"].id],
    ]
    s_nflr["Port Dupont"].adjacent_stations[l_nflr["nFLR R23"].id] = [
        [s_nflr["Light Society Villeside"].id],
        [s_nflr["Sansvikk Kamprad Airfield"].id, s_nflr["Glacierton"].id],
    ]
    s_intra["Laclede Airport Plaza"].adjacent_stations[l_intra["IR 202"].id] = [
        [s_intra["Laclede Central"].id],
        [s_intra["Amestris Cummins Highway"].id, s_intra["Amestris Washington Street"].id],
    ]
    s_fr["New Haven"].adjacent_stations[l_fr["FR New Jerseyan"].id] = [
        [s_intra["Boston Clapham Junction"].id],
        [s_fr["Tung Wan Transfer"].id, s_fr["Palo Alto"].id],
    ]
    s_fr["Palo Alto"].adjacent_stations[l_fr["FR New Jerseyan"].id] = [
        [s_fr["Concord"].id],
        [s_fr["Tung Wan Transfer"].id, s_fr["New Haven"].id],
    ]
    # s_intra["Shadowpoint Capitol Union Station"].adjacent_stations[l_intra["IR 54"].id] = [
    #     [s_intra["Shadowpoint Old Town"].id],
    #     [s_intra["Geneva Bay Hendon Road"].id, s_intra["Hendon"].id],
    # ]
    # s_intra["Creeperville Sakura Park"].adjacent_stations[l_intra["IR 54"].id] = [
    #     [s_intra["Creeperville Shimoko"].id],
    #     [s_intra["New Cainport Riverside Stadium"].id, s_intra["Creeperville Haneda Airport"].id],
    # ]

    def get_shared_stations(station, s=None):
        s = s or {station['i']}

        for shared_station_i in station['shared_facility']:
            if shared_station_i in s or shared_station_i not in n.stations:
                continue
            s.add(shared_station_i)
            yield shared_station_i
            yield from get_shared_stations(data[str(shared_station_i)], s)

    merged = []
    for station_i in list(n.stations.keys()):
        if station_i in merged:
            continue
        station = data[str(station_i)]
        for shared_station_i in list(get_shared_stations(station)):
            n.stations[shared_station_i].merge_into(n, n.stations[station_i])
            merged.append(shared_station_i)

    for station_i in n.stations:
        station = data[str(station_i)]
        for prox_station_i in station["proximity"]:
            prox_station_i = int(prox_station_i)
            if prox_station_i not in n.stations:
                continue
            n.connect(
                n.stations[station_i],
                n.stations[prox_station_i],
                Connection(),
            )

    n.finalise()

    s = Drawer(n, Style(scale=0.1, station_dots=True)).draw()
    with open("./out.svg", "w") as f:
        f.write(str(s))


if __name__ == "__main__":
    main()
