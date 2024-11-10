import json
import re

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

    col = {
        "A": "#00FFFF",
        "B": "#EEDB95",
        "C": "#5E5E5E",
        "D": "#9437FF",
        "E": "#10D20F",
        "F": "#0096FF",
        # "G": "#0ff",
        "H": "#5B7F00",
        "I": "#FF40FF",
        "J": "#4C250D",
        # "K": "#0ff",
        "L": "#9B95BC",
        "M": "#FF8000",
        "N": "#0433FF",
        "O": "#021987",
        "P": "#008E00",
        # "Q": "#0ff",
        "R": "#FE2E9A",
        "S": "#FFFA28",
        "T": "#915001",
        "U": "#2B2C35",
        "V": "#FF8AD8",
        "W": "#FF0000",
        "X": "#000000",
        "XM": "#000000",
        # "Y": "#0ff",
        "Z": "#EEEEEE",
    }

    for line_i in company["lines"]:
        line = data[str(line_i)]
        colour = col.get(line["code"], "#888")
        n.add_line(
            Line(
                id=line_i,
                name="MRT " + line["code"],
                colour=Colour.solid(colour),
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

    col = {
        "1": "#c00",
        "2": "#ffa500",
        "3": "#fe0",
        "4": "#987654",
        "5": "#008000",
        "6": "#0c0",
        "7": "#0cc",
        "8": "#008b8b",
        "9": "#00c",
        "10": "",
        "11": "",
        "12": "",
        "13": "#555",
        "14": "#aaa",
        "15": "#000",
        "16": "#eee",
        "17": "#c2b280",
        "18": "#bb9955",
        "19": "#000080",
        "20": "#965f46",
        "21": "#8b3d2e",
        "22": "#a3501e",
        "23": "#bb8725",
        "24": "#3d291b",
        "N1": "#8c0",
        "N2": "#5cf",
        "N3": "#f5f",
        "N4": "#fc0",
        "AB": "",
    }

    lines = {}
    for line_i in company["lines"]:
        line = data[str(line_i)]
        name = line["name"]
        if name.startswith("N") or name == "AB":
            colour = Colour.solid(col[name])
        elif name.startswith("W"):
            colour = Colour(
                (
                    Stroke(dashes=col[name[1:]], thickness_multiplier=1.0),
                    Stroke(dashes="#fff", thickness_multiplier=0.5),
                )
            )
        else:
            match = re.search(r"^(.)(\d+)(.*)$", line["name"])
            colour = Colour.solid(col[match.group(2)])
        line = n.add_line(
            Line(id=line_i, name="nFLR " + line["code"], colour=colour)
        )
        lines[line.name] = line

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations, lines


def intra(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "IntraRail")

    col = {
        "6": ["#d16d8f"],
        "7": ["#d16d8f", "#4ebdb8", "#2f4bb3"],
        "15": ["#e6e630"],
        "17": ["#4ebdb8", "#00da37"],
        "29": ["#d98030", "#00da37", "#9a3030"],
        "32": ["#e6e630"],
        "34": ["#d98030", "#d3b2a2", "#9a3030"],
        "38": ["#00da37"],
        "40": ["#00da37"],
        "43": ["#2f4bb3"],
        "48": ["#d3b2a2"],
        "49": ["#b34bd9"],
        "50": ["#b34bd9", "#ff0000"],
        "51": ["#ff0000"],
        "52": ["#ff0000"],
        "63": ["#986d4c"],
        "64": ["#986d4c"],
    }

    lines = {}
    for line_i in company["lines"]:
        line = data[str(line_i)]
        colour = (
            Colour.solid("#3d6edd")
            if line["code"].startswith("MCR")
               or line["code"].startswith("LM")
               or line["code"].startswith("S")
            else Colour.stroke(
                Stroke(dash_length=8, dashes=tuple(col[line["code"]]))
            )
            if line["code"] in col
            else Colour.solid("#888")
        )
        line = n.add_line(
            Line(
                id=line_i,
                name="IR "
                     + line["code"].replace("<", "&lt;").replace(">", "&gt;"),
                colour=colour,
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
        colour = Colour.solid(
            "#c01c22"
            if line["code"].endswith("X") and line["code"][0].isdigit()
            else "#0a7ec3"
            if line["code"][-1].isdigit()
            else "#0c4a9e"
        )
        n.add_line(Line(id=line_i, name="Blu " + line["code"], colour=colour))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def rlq(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "RaiLinQ")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        colour = Colour.solid(
            "#ff5500" if line["code"].startswith("IC") else "#ffaa00"
        )
        n.add_line(Line(id=line_i, name="RLQ " + line["code"], colour=colour))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def wzr(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "West Zeta Rail")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        colour = Colour.solid(line["colour"] or "#aa0000")
        n.add_line(Line(id=line_i, name="WZR " + line["code"], colour=colour))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def mtc(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "MarbleRail")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        colour = Colour.solid(line["colour"] or "#cc00cc")
        n.add_line(Line(id=line_i, name="MTC " + line["code"], colour=colour))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def nsc(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "Network South Central")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        colour = Colour.solid(line["colour"] or "#cc0000")
        n.add_line(Line(id=line_i, name="NSC " + line["code"], colour=colour))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def redtrain(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "RedTrain")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        colour = Colour.solid(line["colour"] or "#ff0000")
        n.add_line(
            Line(id=line_i, name="RedTrain " + line["code"], colour=colour)
        )

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def rn(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "RailNorth")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        colour = Colour.solid(line["colour"] or "#000080")
        n.add_line(Line(id=line_i, name=line["code"], colour=colour))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def fr(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "RailCompany" and a['name'] == "Fred Rail")

    lines = {}
    for line_i in company["lines"]:
        line = data[str(line_i)]
        colour = Colour.solid(line["colour"] or "#000080")
        line = n.add_line(
            Line(id=line_i, name="FR " + line["code"], colour=colour)
        )
        lines[line.name] = line

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations, lines


def main():
    data = niquests.get(
        "https://raw.githubusercontent.com/MRT-Map/gatelogue/dist/data_no_sources.json"
    )  # noqa: S1131
    data = json.loads(data.text)['nodes']
    n = Network()
    mrt(n, data)
    s_nflr, l_nflr = nflr(n, data)
    intra(n, data)
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
    s_fr["New Haven"].adjacent_stations[l_fr["FR New Jerseyan"].id] = [
        [s_fr["Boston Clapham Junction"].id],
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

    for station_i in n.stations:
        station = data[str(station_i)]
        for shared_station_i in (a.v for a in station['shared_facility']):
            print("a")
            if shared_station_i not in n.stations:
                continue
            n.stations[shared_station_i].merge_into(n, n.stations[station_i])

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
