from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from autocarter.network import Connection, Network, Station
from autocarter.vector import Vector
import gatelogue_types as gt


def handle_shared_stations(gd: gt.GD, n: Network):
    def get_shared_stations(station: gt.RailStation | gt.BusStop | gt.SeaStop, s=None):
        s = s or {station.i}
        for shared in station.shared_facilities:
            if shared.i in s or shared.i not in n.station_id2index:
                continue
            s.add(shared.i)
            yield shared
            yield from get_shared_stations(shared, s)

    merged = []
    for station_i in list(a.id for a in n.g.nodes()):
        if station_i in merged:
            continue
        station: gt.RailStation | gt.BusStop | gt.SeaStop = gd.get_node(station_i)
        for shared_station in list(get_shared_stations(station)):
            n.station(shared_station.i).merge_into(n, n.station(station_i))
            merged.append(shared_station.i)


def handle_proximity(gd: gt.GD, n: Network):
    for station_i in list(a.id for a in n.g.nodes()):
        station: gt.RailStation | gt.BusStop | gt.SeaStop = gd.get_node(station_i)
        for prox_station, prox in station.nodes_in_proximity:
            prox_station: gt.RailStation | gt.BusStop | gt.SeaStop
            if prox_station.i not in n.station_id2index:
                continue
            if (
                not prox.explicit
                and hasattr(station, "lines")
                and any(line.local for line in station.lines)
                and hasattr(prox_station, "lines")
                and any(line.local for line in prox_station.lines)
            ):
                continue

            n.connect(
                n.station(station_i),
                n.station(prox_station.i),
                Connection(),
            )


def _station(n: Network, company: gt.RailCompany | gt.BusCompany | gt.SeaCompany):
    for station in company.stations if hasattr(company, "stations") else company.stops:
        station: gt.RailStation | gt.BusStop | gt.SeaStop
        if station.world is None or station.world != "New":
            continue
        coordinates = station.coordinates
        if coordinates is None:
            print("No coords", company.name, station.name)
            continue
        if station.name is None:
            continue
        n.add_station(
            Station(
                id=station.i,
                name=station.name.replace("&", "&amp;"),
                coordinates=Vector(*coordinates),
            )
        )


def _connect(n: Network, company: gt.RailCompany | gt.BusCompany | gt.SeaCompany):
    visited_connections: list[tuple[int, int, int]] = []
    prefix = type(company).__name__.removesuffix("Company")
    for (connection_i,) in company.conn.execute(
        f"SELECT C.i FROM {prefix}Connection C LEFT JOIN {prefix}Line L ON C.line = L.i WHERE L.company = ?",
        (company.i,),
    ).fetchall():
        connection = (
            gt.BusConnection if prefix == "Bus" else gt.RailConnection if prefix == "Rail" else gt.SeaConnection
        )(company.conn, connection_i)
        pt1, pt2 = connection.from_, connection.to
        st1, st2 = (pt1.station, pt2.station) if prefix == "Rail" else (pt1.stop, pt2.stop)
        if st1.i > st2.i:
            st1, st2 = st2, st1
        if st1.i not in n.station_id2index or st2.i not in n.station_id2index:
            continue
        if (st1.i, st2.i, connection.line.i) in visited_connections:
            continue

        n.connect(n.station(st1.i), n.station(st2.i), n.line(connection.line.i))
        visited_connections.append((st1.i, st2.i, connection.line.i))


def adjacent_stations(
    n: Network,
    gd: gt.GD,
    company_name: str,
    station_name: str,
    line_code: str,
    *adjacent_station_names: list[str],
    company_type: type[gt.Node] = gt.RailCompany,
):
    company = next(a for a in gd.nodes(company_type) if a.name == company_name)
    company_stations = list(company.stations if company_type == gt.RailCompany else company.stops)
    station = next(a for a in company_stations if a.name == station_name).i
    line = next(a for a in company.lines if a.code == line_code).i
    n.station(station).adjacent_stations[line] = [
        [next(a for a in company_stations if a.name == name).i for name in ls] for ls in adjacent_station_names
    ]
