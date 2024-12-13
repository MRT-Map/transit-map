from __future__ import annotations
import vector
from autocarter.colour import Colour, Stroke
from autocarter.drawer import Drawer
from autocarter.network import Network, Line, Station
from autocarter.style import Style

from utils import _connect, _station, handle_shared_stations, handle_proximity

def intra(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "SeaCompany" and a['name'] == "IntraSail")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        n.add_line(Line(id=line_i, name="IS " + line["code"], colour=Colour.solid(line["colour"] or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations

def wzf(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "SeaCompany" and a['name'] == "West Zeta Ferry")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        n.add_line(Line(id=line_i, name="WZF " + line["code"], colour=Colour.solid(line["colour"] or "#800")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations

def alq(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "SeaCompany" and a['name'] == "AquaLinQ")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        n.add_line(Line(id=line_i, name="ALQ " + line["code"], colour=Colour.solid(line["colour"] or "#ffa500")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def sea(data):
    n = Network()
    intra(n, data)
    wzf(n, data)
    alq(n, data)

    handle_shared_stations(data, n)
    handle_proximity(data, n)
    n.finalise()

    s = Drawer(n, Style(scale=0.075, station_dots=True)).draw()
    with open("./sea.svg", "w") as f:
        f.write(str(s))
