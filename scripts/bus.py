from __future__ import annotations

from autocarter.colour import Colour
from autocarter.drawer import Drawer
from autocarter.network import Line, Network
from autocarter.style import Style
import gatelogue_types as gt
from utils import _connect, _station, handle_proximity, handle_shared_stations


def intra(n: Network, gd: gt.GD):
    company = next(a for a in gd.nodes(gt.BusCompany) if a.name == "IntraBus")

    for line in company.lines:
        n.add_line(Line(id=line.i, name="IB " + line.code, colour=Colour.solid(line.colour or "#888")))

    stations = _station(n, company)
    _connect(n, company)
    return stations


def ccc(n: Network, gd: gt.GD):
    company = next(a for a in gd.nodes(gt.BusCompany) if a.name == "Caravacan Caravan Company")

    for line in company.lines:
        n.add_line(Line(id=line.i, name="CCC " + line.code, colour=Colour.solid(line.colour or "#800")))

    stations = _station(n, company)
    _connect(n, company)
    return stations


def sb(n: Network, gd: gt.GD):
    company = next(a for a in gd.nodes(gt.BusCompany) if a.name == "Seabeast Buses")

    for line in company.lines:
        n.add_line(Line(id=line.i, name="SeaBeast " + line.code, colour=Colour.solid(line.colour or "#333")))

    stations = _station(n, company)
    _connect(n, company)
    return stations


def bus(gd):
    n = Network()
    intra(n, gd)
    ccc(n, gd)
    sb(n, gd)

    handle_shared_stations(gd, n)
    handle_proximity(gd, n)
    n.finalise()

    s = Drawer(n, Style(scale=0.075, station_dots=True)).draw()
    with open("maps/bus.svg", "w") as f:
        f.write(str(s))


if __name__ == "__main__":
    gd = gt.GD.urllib_get()

    bus(gd)
