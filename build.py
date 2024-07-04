import re

import requests
import vector
from autocarter.drawer import Drawer, Style
from autocarter.network import Line, Network, Station, Connection


def _station(n: Network, company_json, data):
    for station_uuid in company_json["stations"]:
        station_json = data["station"][station_uuid]
        coordinates = station_json["coordinates"] or [0, 0]
        n.add_station(
            Station(
                id=station_uuid,
                name=station_json["name"].replace("&", "&amp;"),
                coordinates=vector.obj(x=coordinates[0], y=coordinates[1]),
            )
        )


def _connect(n: Network, company_json, data):
    visited_stations = []
    for station_uuid in company_json["stations"]:
        if station_uuid not in n.stations:
            continue
        station_json = data["station"][station_uuid]
        if not station_json["connections"]:
            print("No conns", station_json["name"])
        for conn_station_uuid, connections in station_json["connections"].items():
            if conn_station_uuid in visited_stations:
                continue
            for connection in connections:
                n.connect(
                    n.stations[station_uuid],
                    n.stations[conn_station_uuid],
                    n.lines[connection["line"]],
                )
        visited_stations.append(station_uuid)


def mrt(n: Network, data):
    data = data["rail"]
    company_uuid, company_json = next((k, v) for k, v in data["company"].items() if v["name"] == "MRT")

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

    for line_uuid in company_json["lines"]:
        line_json = data["line"][line_uuid]
        colour = col.get(line_json["code"], "#888")
        n.add_line(Line(id=line_uuid, name="MRT " + line_json["code"], colour=colour))

    for station_uuid in company_json["stations"]:
        station_json = data["station"][station_uuid]
        if station_json["world"] == "Old" or not station_json["connections"]:
            continue
        coordinates = station_json["coordinates"] or [0, 0]
        n.add_station(
            Station(
                id=station_uuid,
                name=(" ".join(station_json["codes"]) + " " + (station_json["name"] or "")),
                coordinates=vector.obj(x=coordinates[0], y=coordinates[1]),
            )
        )

    _connect(n, company_json, data)


def nflr(n: Network, data):
    data = data["rail"]
    company_uuid, company_json = next((k, v) for k, v in data["company"].items() if v["name"] == "nFLR")

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

    for line_uuid in company_json["lines"]:
        line_json = data["line"][line_uuid]
        name = line_json["name"]
        if name.startswith("N") or name == "AB":
            colour = col[name]
        elif name.startswith("W"):
            colour = (col[name[1:]], "#0000")
        else:
            match = re.search(r"^(.)(\d+)(.*)$", line_json["name"])
            colour = col[match.group(2)]
        n.add_line(Line(id=line_uuid, name="nFLR " + line_json["code"], colour=colour))

    _station(n, company_json, data)
    _connect(n, company_json, data)


def intra(n: Network, data):
    data = data["rail"]
    company_uuid, company_json = next((k, v) for k, v in data["company"].items() if v["name"] == "IntraRail")

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

    for line_uuid in company_json["lines"]:
        line_json = data["line"][line_uuid]
        colour = (
            "#3d6edd"
            if line_json["code"].startswith("MCR") or line_json["code"].startswith("LM") or line_json["code"].startswith("S")
            else tuple(col[line_json["code"]])
            if line_json["code"] in col
            else "#888"
        )
        n.add_line(
            Line(id=line_uuid, name="IR " + line_json["code"].replace("<", "&lt;").replace(">", "&gt;"), colour=colour))

    _station(n, company_json, data)
    _connect(n, company_json, data)


def blu(n: Network, data):
    data = data["rail"]
    company_uuid, company_json = next((k, v) for k, v in data["company"].items() if v["name"] == "BluRail")

    for line_uuid in company_json["lines"]:
        line_json = data["line"][line_uuid]
        colour = (
            "#c01c22" if line_json["code"].endswith("X") else "#0a7ec3" if line_json["code"][
                -1].isdigit() else "#0c4a9e"
        )
        n.add_line(Line(id=line_uuid, name="Blu " + line_json["code"], colour=colour))

    _station(n, company_json, data)
    _connect(n, company_json, data)


def main():
    data = requests.get("https://raw.githubusercontent.com/MRT-Map/gatelogue/dist/data_no_sources.json").json()
    n = Network()
    mrt(n, data)
    nflr(n, data)
    intra(n, data)
    blu(n, data)

    for station_uuid, station in n.stations.items():
        station_json = data['rail']["station"][station_uuid]
        for prox_station_uuid in station_json['proximity'].get("railstation", {}):
            if prox_station_uuid not in n.stations:
                continue
            n.connect(
                n.stations[station_uuid],
                n.stations[prox_station_uuid],
                Connection(),
            )

    n.finalise()

    s = Drawer(n, Style(scale=0.1, station_dots=True)).draw()
    with open("./out.svg", "w") as f:
        f.write(str(s))


if __name__ == "__main__":
    main()
