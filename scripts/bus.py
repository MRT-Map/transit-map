from __future__ import annotations

from autocarter.colour import Colour
from autocarter.drawer import Drawer
from autocarter.network import Line, Network
from autocarter.style import Style
from gatelogue_types import GatelogueData, BusCompany, BusCompanyNS, GatelogueDataNS, RailLineNS, BusLineNS

from utils import _connect, _station, handle_proximity, handle_shared_stations


def intra(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, BusCompanyNS) and a.name == "IntraBus")

    for line_i in company.lines:
        line: BusLineNS =data[line_i]
        n.add_line(Line(id=line_i, name="IB " + line.code, colour=Colour.solid(line.colour or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def ccc(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, BusCompanyNS) and a.name == "Caravacan Caravan Company")

    for line_i in company.lines:
        line: BusLineNS =data[line_i]
        n.add_line(Line(id=line_i, name="CCC " + line.code, colour=Colour.solid(line.colour or "#800")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def sb(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, BusCompanyNS) and a.name == "Seabeast Buses")

    for line_i in company.lines:
        line: BusLineNS =data[line_i]
        n.add_line(Line(id=line_i, name="SeaBeast " + line.code, colour=Colour.solid(line.colour or "#333")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def bus(data):
    n = Network()
    intra(n, data)
    ccc(n, data)
    sb(n, data)

    handle_shared_stations(data, n)
    handle_proximity(data, n)
    n.finalise()

    s = Drawer(n, Style(scale=0.075, station_dots=True)).draw()
    with open("maps/bus.svg", "w") as f:
        f.write(str(s))
