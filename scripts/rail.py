from __future__ import annotations

from autocarter.colour import Colour, Stroke
from autocarter.drawer import Drawer
from autocarter.network import Line, Network, Station
from autocarter.style import Style
from autocarter.vector import Vector
from gatelogue_types import GatelogueDataNS, RailCompanyNS, RailLineNS
from utils import _connect, _station, handle_proximity, handle_shared_stations


def mrt(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, RailCompanyNS) and a.name == "MRT")

    for line_i in company.lines:
        line: RailLineNS = data[line_i]
        n.add_line(
            Line(
                id=line_i,
                name="MRT " + line.code,
                colour=Colour.solid(line.colour or "#888"),
            )
        )

    stations = {}
    for station_i in company.stations:
        station = data[station_i]
        if station.world == "Old" or not station.connections:
            continue
        coordinates = station.coordinates or [0, 0]
        station = n.add_station(
            Station(
                id=station_i,
                name=(" ".join(sorted(station.codes)) + " " + (station.name or "")).strip(),
                coordinates=Vector(*coordinates),
            )
        )
        stations[station.name] = station

    _connect(n, company, data)

    return stations


def nflr(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, RailCompanyNS) and a.name == "nFLR")

    lines = {}
    for line_i in company.lines:
        line: RailLineNS = data[line_i]
        name = line.name
        if name.startswith("W") or name.endswith("Rapid"):
            colour = Colour(
                (
                    Stroke(dashes=line.colour, thickness_multiplier=1.0),
                    Stroke(dashes="#fff", thickness_multiplier=0.5),
                )
            )
        else:
            colour = Colour.solid(line.colour or "#888")
        line2 = n.add_line(Line(id=line_i, name="nFLR " + line.code, colour=colour))
        lines[line2.name] = line2

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations, lines


def intra(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, RailCompanyNS) and a.name == "IntraRail")

    lines = {}
    for line_i in company.lines:
        line: RailLineNS = data[line_i]
        line2 = n.add_line(
            Line(
                id=line_i,
                name="IR " + line.code.replace("<", "&lt;").replace(">", "&gt;"),
                colour=Colour.solid(line.colour or "#888"),
            )
        )
        lines[line2.name] = line2

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations, lines


def blu(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, RailCompanyNS) and a.name == "BluRail")

    for line_i in company.lines:
        line: RailLineNS = data[line_i]
        n.add_line(Line(id=line_i, name="Blu " + line.code, colour=Colour.solid(line.colour or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def rlq(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, RailCompanyNS) and a.name == "RaiLinQ")

    for line_i in company.lines:
        line: RailLineNS = data[line_i]
        n.add_line(Line(id=line_i, name="RLQ " + line.code, colour=Colour.solid(line.colour or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def wzr(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, RailCompanyNS) and a.name == "West Zeta Rail")

    for line_i in company.lines:
        line: RailLineNS = data[line_i]
        n.add_line(Line(id=line_i, name="WZR " + line.code, colour=Colour.solid(line.colour or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def mtc(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, RailCompanyNS) and a.name == "MarbleRail")

    for line_i in company.lines:
        line: RailLineNS = data[line_i]
        n.add_line(Line(id=line_i, name="MTC " + line.code, colour=Colour.solid(line.colour or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def nsc(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, RailCompanyNS) and a.name == "Network South Central")

    for line_i in company.lines:
        line: RailLineNS = data[line_i]
        n.add_line(Line(id=line_i, name="NSC " + line.code, colour=Colour.solid(line.colour or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def redtrain(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, RailCompanyNS) and a.name == "RedTrain")

    for line_i in company.lines:
        line: RailLineNS = data[line_i]
        n.add_line(Line(id=line_i, name="RedTrain " + line.code, colour=Colour.solid(line.colour or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def rn(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, RailCompanyNS) and a.name == "RailNorth")

    for line_i in company.lines:
        line: RailLineNS = data[line_i]
        n.add_line(Line(id=line_i, name=line.code, colour=Colour.solid(line.colour or "#888")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def sb(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, RailCompanyNS) and a.name == "Seabeast Rail")

    for line_i in company.lines:
        line: RailLineNS = data[line_i]
        n.add_line(Line(id=line_i, name="Seabeast" + line.code, colour=Colour.solid(line.colour or "#333")))

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations


def fr(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, RailCompanyNS) and a.name == "Fred Rail")

    lines = {}
    for line_i in company.lines:
        line: RailLineNS = data[line_i]
        line2 = n.add_line(Line(id=line_i, name="FR " + line.code, colour=Colour.solid(line.colour or "#888")))
        lines[line2.name] = line2

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations, lines


def seat(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, RailCompanyNS) and a.name == "SEAT")

    lines = {}
    for line_i in company.lines:
        line: RailLineNS = data[line_i]
        line2 = n.add_line(Line(id=line_i, name="SEAT " + line.code, colour=Colour.solid(line.colour or "#888")))
        lines[line2.name] = line2

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations, lines


def pac(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, RailCompanyNS) and a.name == "Pacifica")

    lines = {}
    for line_i in company.lines:
        line: RailLineNS = data[line_i]
        line2 = n.add_line(Line(id=line_i, name="Pac " + line.code, colour=Colour.solid(line.colour or "#888")))
        lines[line2.name] = line2

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations, lines


def nrn(n: Network, data: GatelogueDataNS):
    company = next(a for a in data if isinstance(a, RailCompanyNS) and a.name == "Nobody's Rail Network")

    lines = {}
    for line_i in company.lines:
        line: RailLineNS = data[line_i]
        line2 = n.add_line(Line(id=line_i, name="NRN " + line.code, colour=Colour.solid(line.colour or "#888")))
        lines[line2.name] = line2

    stations = _station(n, company, data)
    _connect(n, company, data)
    return stations, lines


def metros(n: Network, data: GatelogueDataNS):
    companies = (a for a in data if isinstance(a, RailCompanyNS) and a.local)

    lines_all = {}
    stations_all = {}
    for company in companies:
        lines = {}
        for line_i in company.lines:
            line: RailLineNS = data[line_i]
            line2 = n.add_line(Line(id=line_i, name=line.code, colour=Colour.solid(line.colour or "#888", 0.5)))
            lines[line2.name] = line2

        stations = _station(n, company, data)
        _connect(n, company, data)
        lines_all[company.name] = lines
        stations_all[company.name] = stations
    return stations_all, lines_all


def rail(data):
    n = Network()
    mrt(n, data)
    s_nflr, l_nflr = nflr(n, data)
    s_intra, l_intra = intra(n, data)
    blu(n, data)
    rlq(n, data)
    wzr(n, data)
    mtc(n, data)
    nsc(n, data)
    rn(n, data)
    s_fr, l_fr = fr(n, data)
    redtrain(n, data)
    sb(n, data)
    seat(n, data)
    pac(n, data)
    nrn(n, data)
    sm, lm = metros(n, data)

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
    s_intra["Laclede Airport Plaza"].adjacent_stations[l_intra["IR 202"].id] = [
        [s_intra["Laclede Central"].id],
        [s_intra["Amestris Cummins Highway"].id, s_intra["Amestris Washington Street"].id],
    ]
    s_fr["New Haven"].adjacent_stations[l_fr["FR New Jerseyan"].id] = [
        [s_intra["Boston Clapham Junction"].id],
        [s_fr["Tung Wan Transfer"].id, s_fr["Palo Alto"].id],
    ]
    s_fr["Palo Alto"].adjacent_stations[l_fr["FR New Jerseyan"].id] = [
        [s_fr["Concord"].id],
        [s_fr["Tung Wan Transfer"].id, s_fr["New Haven"].id],
    ]
    s_intra["Formosa Northern"].adjacent_stations[l_intra["IR 2X"].id] = [
        [s_intra["Kenthurst Aerodrome"].id],
        [s_intra["UCWT International Airport East"].id, s_intra["Danielston Paisley Place Transportation Center"].id],
    ]
    s_intra["UCWT International Airport East"].adjacent_stations[l_intra["IR 2X"].id] = [
        [s_intra["Formosa Northern"].id, s_intra["Danielston Paisley Place Transportation Center"].id],
        [s_intra["Sealane Central"].id],
    ]
    s_intra["Central City Warp Rail Terminal"].adjacent_stations[l_intra["IR 2X"].id] = [
        [s_intra["Central City Beltway Terminal North"].id],
        [s_intra["Rochshire"].id, s_intra["Achowalogen Takachsin-Covina International Airport"].id],
    ]
    s_intra["Achowalogen Takachsin-Covina International Airport"].adjacent_stations[l_intra["IR 2X"].id] = [
        [s_intra["Central City Warp Rail Terminal"].id, s_intra["Rochshire"].id],
        [s_intra["Woodsbane"].id, s_intra["Siletz Salvador Station"].id],
    ]
    s_intra["Siletz Salvador Station"].adjacent_stations[l_intra["IR 2X"].id] = [
        [s_intra["Woodsbane"].id, s_intra["Achowalogen Takachsin-Covina International Airport"].id],
        [],
    ]
    s_flrk = sm["FLR Kazeshima/Shui Chau"]
    l_flrk = lm["FLR Kazeshima/Shui Chau"]
    s_flrk["Ho Kok"].adjacent_stations[l_flrk["C1"].id] = [[s_flrk["Ho Kok West"].id, s_flrk["Sha Tsui"].id], []]
    s_nps = sm["New Prubourne Subway"]
    l_nps = lm["New Prubourne Subway"]
    s_nps["Evergreen Parkway"].adjacent_stations[l_nps["B"].id] = [
        [s_nps["Wuster Drive"].id, s_nps["Penn Island-Zoo"]],
        [],
    ]

    handle_shared_stations(data, n)
    handle_proximity(data, n)
    n.finalise()

    s = Drawer(n, Style(scale=0.1, station_dots=True)).draw()
    with open("maps/rail.svg", "w") as f:
        f.write(str(s))
