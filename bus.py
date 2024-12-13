from __future__ import annotations
import vector
from autocarter.colour import Colour, Stroke
from autocarter.drawer import Drawer
from autocarter.network import Network, Line, Station
from autocarter.style import Style

from utils import _connect, _station, handle_shared_stations, handle_proximity

def intra(n: Network, data: dict[str, dict]):
    company = next(a for a in data.values() if a['type'] == "BusCompany" and a['name'] == "IntraBus")

    for line_i in company["lines"]:
        line = data[str(line_i)]
        n.add_line(Line(id=line_i, name="IB " + line["code"], colour=Colour.solid(line["colour"] or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def bus(data):
    n = Network()
    intra(n, data)

    handle_shared_stations(data, n)
    handle_proximity(data, n)
    n.finalise()

    s = Drawer(n, Style(scale=0.075, station_dots=True)).draw()
    with open("./bus.svg", "w") as f:
        f.write(str(s))
