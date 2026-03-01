from __future__ import annotations

from autocarter.colour import Colour
from autocarter.drawer import Drawer
from autocarter.network import Line, Network
from autocarter.style import Style
import gatelogue_types as gt
from utils import _connect, _station, handle_proximity, handle_shared_stations


def intra(n: Network, gd: gt.GD):
    company = next(a for a in gd.nodes(gt.SeaCompany) if a.name == "IntraSail")

    for line in company.lines:
        n.add_line(Line(id=line.i, name="IS " + line.code, colour=Colour.solid(line.colour or "#888")))

    stations = _station(n, company)
    _connect(n, company)
    return stations


def wzf(n: Network, gd: gt.GD):
    company = next(a for a in gd.nodes(gt.SeaCompany) if a.name == "West Zeta Ferry")

    for line in company.lines:
        n.add_line(Line(id=line.i, name="WZF " + line.code, colour=Colour.solid(line.colour or "#800")))

    stations = _station(n, company)
    _connect(n, company)
    return stations


def alq(n: Network, gd: gt.GD):
    company = next(a for a in gd.nodes(gt.SeaCompany) if a.name == "AquaLinQ")

    for line in company.lines:
        n.add_line(Line(id=line.i, name="ALQ " + line.code, colour=Colour.solid(line.colour or "#ffa500")))

    stations = _station(n, company)
    _connect(n, company)
    return stations


def cfc(n: Network, gd: gt.GD):
    company = next(a for a in gd.nodes(gt.SeaCompany) if a.name == "Caravacan Floaty Company")

    for line in company.lines:
        n.add_line(Line(id=line.i, name="CFC " + line.code, colour=Colour.solid(line.colour or "#800")))

    stations = _station(n, company)
    _connect(n, company)
    return stations


def erz(n: Network, gd: gt.GD):
    company = next(a for a in gd.nodes(gt.SeaCompany) if a.name == "ErzLink Ferry")

    for line in company.lines:
        n.add_line(Line(id=line.i, name=line.code, colour=Colour.solid(line.colour or "#0aa")))

    stations = _station(n, company)
    _connect(n, company)
    return stations


def windboat(n: Network, gd: gt.GD):
    company = next(a for a in gd.nodes(gt.SeaCompany) if a.name == "Windboat")

    for line in company.lines:
        n.add_line(Line(id=line.i, name=line.code, colour=Colour.solid(line.colour or "#aaa")))

    stations = _station(n, company)
    _connect(n, company)
    return stations


def sea(gd):
    n = Network()
    intra(n, gd)
    wzf(n, gd)
    alq(n, gd)
    cfc(n, gd)
    erz(n, gd)
    windboat(n, gd)

    handle_shared_stations(gd, n)
    handle_proximity(gd, n)
    n.finalise()

    s = Drawer(n, Style(scale=0.075, station_dots=True)).draw()
    with open("maps/sea.svg", "w") as f:
        f.write(str(s))


if __name__ == "__main__":
    gd = gt.GD.urllib_get()

    sea(gd)
