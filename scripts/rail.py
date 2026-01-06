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
                name=(
                    " ".join(sorted(station.codes)) + " " + (station.name or "")
                ).strip(),
                coordinates=Vector(*coordinates),
            )
        )
        stations[station.name] = station

    _connect(n, company, data)

    return stations


def the_rest(n: Network, data: GatelogueDataNS):
    companies = sorted((a for a in data if isinstance(a, RailCompanyNS) and a.name != "MRT"), key=lambda a: a.name)

    lines_all = {}
    stations_all = {}
    for company in companies:
        prefix = {
            "BluRail": "Blu",
            "IntraRail": "IR",
            "RaiLinQ": "RLQ",
            "West Zeta Rail": "WZR",
            "MarbleRail": "MTC",
            "Network South Central": "NSC",
            "RailNorth": "",
            "Seabeast Rail": "Seabeast",
            "Fred Rail": "FR",
            "Pacifica": "Pac",
            "Nobody's Rail Network": "NRN",
            "ErzLink Intercity": "Erz",
            "Lava Rail": "Lava",
            "CVCExpress": "CVC",
        }.get(company.name, company.name) or ""
        lines = {}
        for line_i in company.lines:
            line: RailLineNS = data[line_i]

            name = (
                (line.code if company.local else prefix + " " + line.code)
                .strip()
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            thickness = 0.5 if company.local else 1.0
            colour = (
                Colour(
                    (
                        Stroke(dashes=line.colour or "#888", thickness_multiplier=thickness),
                        Stroke(dashes="#fff", thickness_multiplier=thickness / 2),
                    )
                )
                if (
                    company.name == "nFLR"
                    and (line.code.startswith("W") or line.code.endswith("Rapid"))
                ) or (company.name == "ErzLink Trams" and line.code.startswith("X"))
                or (company.name == "ErzLink Metro" and line.code.endswith("Express"))
                else Colour.solid(line.colour or "#888", thickness)
            )

            line2 = n.add_line(Line(id=line_i, name=name, colour=colour))
            lines[line2.name] = line2

        stations = _station(n, company, data)
        _connect(n, company, data)
        lines_all[company.name] = lines
        stations_all[company.name] = stations
    return stations_all, lines_all


def rail(data):
    n = Network()
    mrt(n, data)
    s, l = the_rest(n, data)  # noqa: E741

    s_nflr, l_nflr = s["nFLR"], l["nFLR"]
    s_intra, l_intra = s["IntraRail"], l["IntraRail"]
    s_fr, l_fr = s["Fred Rail"], l["Fred Rail"]
    s_blu = s["BluRail"]

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

    s_fr["New Haven"].adjacent_stations[l_fr["FR New Jerseyan"].id] = [
        [s_fr["Boston Clapham Junction"].id],
        [s_fr["Tung Wan Transfer"].id, s_fr["Palo Alto"].id],
    ]
    s_fr["Palo Alto"].adjacent_stations[l_fr["FR New Jerseyan"].id] = [
        [s_fr["Concord"].id],
        [s_fr["Tung Wan Transfer"].id, s_fr["New Haven"].id],
    ]

    s_intra["Laclede Airport Plaza"].adjacent_stations[l_intra["IR 202"].id] = [
        [s_blu["Laclede Central"].id],
        [
            s_intra["Amestris Cummins Highway"].id,
            s_intra["Amestris Washington Street"].id,
        ],
    ]
    s_intra["Formosa Northern"].adjacent_stations[l_intra["IR 2X"].id] = [
        [s_intra["Kenthurst Aerodrome"].id],
        [
            s_intra["UCWT International Airport East"].id,
            s_intra["Danielston Paisley Place Transportation Center"].id,
        ],
    ]
    s_intra["UCWT International Airport East"].adjacent_stations[
        l_intra["IR 2X"].id
    ] = [
        [
            s_intra["Formosa Northern"].id,
            s_intra["Danielston Paisley Place Transportation Center"].id,
        ],
        [s_blu["Sealane Central"].id],
    ]
    s_intra["Central City Warp Rail Terminal"].adjacent_stations[
        l_intra["IR 2X"].id
    ] = [
        [s_fr["Central City Beltway Terminal North"].id],
        [
            s_intra["Rochshire"].id,
            s_intra["Achowalogen Takachsin-Covina International Airport"].id,
        ],
    ]
    s_intra["Achowalogen Takachsin-Covina International Airport"].adjacent_stations[
        l_intra["IR 2X"].id
    ] = [
        [s_blu["Central City Warp Rail Terminal"].id, s_intra["Sienos"].id],
        [s_intra["Woodsbane"].id, s_intra["Siletz Salvador Station"].id],
    ]
    s_intra["Siletz Salvador Station"].adjacent_stations[l_intra["IR 2X"].id] = [
        [
            s_intra["Woodsbane"].id,
            s_intra["Achowalogen Takachsin-Covina International Airport"].id,
        ],
        [],
    ]

    s_flrk = s["FLR Kazeshima/Shui Chau"]
    l_flrk = l["FLR Kazeshima/Shui Chau"]
    s_flrk["Ho Kok"].adjacent_stations[l_flrk["C1"].id] = [
        [s_flrk["Ho Kok West"].id, s_flrk["Sha Tsui"].id],
        [],
    ]

    s_nps = s["New Prubourne Subway"]
    l_nps = l["New Prubourne Subway"]
    s_nps["Evergreen Parkway"].adjacent_stations[l_nps["B"].id] = [
        [s_nps["Wuster Drive"].id, s_nps["Penn Island-Zoo"].id],
        [],
    ]

    s_erzt = s["ErzLink Trams"]
    l_erzt = l["ErzLink Trams"]
    s_erzt["Atrium North"].adjacent_stations[l_erzt["3"].id] = [
        [s_erzt["Atrium West"].id, s_erzt["Atrium East"].id],
        [s_erzt["Almono"].id],
    ]
    s_erzt["Atrium South"].adjacent_stations[l_erzt["3"].id] = [
        [s_erzt["Atrium West"].id, s_erzt["Atrium East"].id],
        [s_erzt["Spire of New Domain"].id],
    ]

    s_ref = s["Refuge Streetcar"]
    l_ref = l["Refuge Streetcar"]
    s_ref["West Train Station"].adjacent_stations[l_ref["North/South Loop"].id] = [
        [s_ref["Cranberry Green"].id, s_ref["Downtown North"].id],
        [s_ref["Hilltop"].id],
    ]
    s_ref["South Hill"].adjacent_stations[l_ref["North/South Loop"].id] = [
        [s_ref["Refuge Airfield North"].id, s_ref["University South"].id],
        [s_ref["Hilltop"].id],
    ]

    handle_shared_stations(data, n)
    handle_proximity(data, n)
    n.finalise()

    s = Drawer(n, Style(scale=0.1, station_dots=True)).draw()
    with open("maps/rail.svg", "w") as f:
        f.write(str(s))
