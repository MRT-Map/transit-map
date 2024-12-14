from __future__ import annotations

import vector
from autocarter.network import Connection, Network, Station


def handle_shared_stations(data, n: Network):
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


def handle_proximity(data, n: Network):
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


def _station(n: Network, company: dict, data: dict[str, dict]):
    stations = {}
    for station_i in (company["stations" if "stations" in company else "stops"]):
        station = data[str(station_i)]
        if station["world"] is None or station["world"] != "New":
            continue
        coordinates = station["coordinates"]
        if coordinates is None:
            print("No coords", company['name'], station["name"])
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
    for station_i in (company["stations" if "stations" in company else "stops"]):
        if station_i not in n.stations:
            continue
        station = data[str(station_i)]
        if not station["connections"]:
            print("No conns", company['name'], station["name"])
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
