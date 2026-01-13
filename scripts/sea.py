from __future__ import annotations

from autocarter.colour import Colour
from autocarter.drawer import Drawer
from autocarter.network import Line, Network
from autocarter.style import Style
from gatelogue_types import GatelogueDataNS, SeaCompanyNS, SeaLineNS
from utils import _connect, _station, handle_proximity, handle_shared_stations


def intra(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, SeaCompanyNS) and a.name == "IntraSail")

    for line_i in company.lines:
        line: SeaLineNS = data[line_i]
        n.add_line(Line(id=line_i, name="IS " + line.code, colour=Colour.solid(line.colour or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def wzf(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, SeaCompanyNS) and a.name == "West Zeta Ferry")

    for line_i in company.lines:
        line: SeaLineNS = data[line_i]
        n.add_line(Line(id=line_i, name="WZF " + line.code, colour=Colour.solid(line.colour or "#800")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def alq(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, SeaCompanyNS) and a.name == "AquaLinQ")

    for line_i in company.lines:
        line: SeaLineNS = data[line_i]
        n.add_line(Line(id=line_i, name="ALQ " + line.code, colour=Colour.solid(line.colour or "#ffa500")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations

def cfc(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, SeaCompanyNS) and a.name == "Caravacan Floaty Company")

    for line_i in company.lines:
        line: SeaLineNS = data[line_i]
        n.add_line(Line(id=line_i, name="CFC " + line.code, colour=Colour.solid(line.colour or "#800")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def erz(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, SeaCompanyNS) and a.name == "ErzLink Ferry")

    for line_i in company.lines:
        line: SeaLineNS = data[line_i]
        n.add_line(Line(id=line_i, name=line.code, colour=Colour.solid(line.colour or "#0aa")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations

def windboat(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, SeaCompanyNS) and a.name == "Windboat")

    for line_i in company.lines:
        line: SeaLineNS = data[line_i]
        n.add_line(Line(id=line_i, name=line.code, colour=Colour.solid(line.colour or "#aaa")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations

def sea(data):
    n = Network()
    intra(n, data)
    wzf(n, data)
    alq(n, data)
    cfc(n, data)
    erz(n, data)
    windboat(n, data)

    handle_shared_stations(data, n)
    handle_proximity(data, n)
    n.finalise()

    s = Drawer(n, Style(scale=0.075, station_dots=True)).draw()
    with open("maps/sea.svg", "w") as f:
        f.write(str(s))
