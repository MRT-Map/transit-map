from __future__ import annotations

from autocarter.colour import Colour, Stroke
from autocarter.drawer import Drawer
from autocarter.network import Line, Network, Station
from autocarter.style import Style
from autocarter.vector import Vector
import gatelogue_types as gt

from utils import adjacent_stations
from utils import _connect, _station, handle_proximity, handle_shared_stations


def mrt(n: Network, gd: gt.GD):
    company = next(a for a in gd.nodes(gt.RailCompany) if a.name == "MRT")

    for line in company.lines:
        n.add_line(
            Line(
                id=line.i,
                name="MRT " + line.code,
                colour=Colour.solid(line.colour or "#888"),
            )
        )

    for station in company.stations:
        if (
            station.world == "Old"
            or len(list(station.connections_to_here)) == 0
            or len(list(station.connections_from_here)) == 0
        ):
            continue
        coordinates = station.coordinates or [0, 0]
        n.add_station(
            Station(
                id=station.i,
                name=(" ".join(sorted(station.codes)) + " " + (station.name or "")).strip(),
                coordinates=Vector(*coordinates),
            )
        )

    _connect(n, company)


def the_rest(n: Network, gd: gt.GD):
    companies = sorted((a for a in gd.nodes(gt.RailCompany) if a.name != "MRT"), key=lambda a: a.name)

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
        for line in company.lines:
            name = (
                (line.code if line.local else prefix + " " + line.code)
                .strip()
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            thickness = 0.5 if line.local else 1.0
            colour = (
                Colour(
                    (
                        Stroke(dashes=line.colour or "#888", thickness_multiplier=thickness),
                        Stroke(dashes="#fff", thickness_multiplier=thickness / 2),
                    )
                )
                if (company.name == "nFLR" and (line.code.startswith("W") or line.code.endswith("Rapid")))
                or (company.name == "ErzLink Trams" and line.code.startswith("X"))
                or (company.name == "ErzLink Metro" and line.code.endswith("Express"))
                else Colour.solid(line.colour or "#888", thickness)
            )

            line2 = n.add_line(Line(id=line.i, name=name, colour=colour))

        _station(n, company)
        _connect(n, company)


def rail(gd):
    n = Network()
    mrt(n, gd)
    the_rest(n, gd)  # noqa: E741

    adjacent_stations(n, gd, "nFLR", "Deadbush Karaj Expo", "R5A", ["Deadbush Works"], ["Deadbush New Euphorial"])
    adjacent_stations(
        n, gd, "nFLR", "Sansvikk Kamprad Airfield", "R23", ["Sansvikk Karlstad"], ["Glacierton", "Port Dupont"]
    )
    adjacent_stations(n, gd, "nFLR", "Glacierton", "R23", ["Snowydale"], ["Sansvikk Kamprad Airfield", "Port Dupont"])
    adjacent_stations(
        n, gd, "nFLR", "Port Dupont", "R23", ["Light Society Villeside"], ["Sansvikk Kamprad Airfield", "Glacierton"]
    )

    adjacent_stations(
        n, gd, "Fred Rail", "New Haven", "New Jerseyan", ["Boston Clapham Junction"], ["Tung Wan Transfer", "Palo Alto"]
    )
    adjacent_stations(n, gd, "Fred Rail", "Palo Alto", "New Jerseyan", ["Concord"], ["Tung Wan Transfer", "New Haven"])

    adjacent_stations(
        n,
        gd,
        "IntraRail",
        "Laclede Airport Plaza",
        "202",
        ["Laclede Central"],
        ["Amestris Cummins Highway", "Amestris Washington Street"],
    )
    adjacent_stations(
        n,
        gd,
        "IntraRail",
        "Formosa Northern",
        "2X",
        ["Kenthurst Aerodrome"],
        ["UCWT International Airport East", "Danielston Paisley Place Transportation Center"],
    )
    adjacent_stations(
        n,
        gd,
        "IntraRail",
        "UCWT International Airport East",
        "2X",
        ["Sealane Central"],
        ["Formosa Northern", "Danielston Paisley Place Transportation Center"],
    )
    adjacent_stations(
        n,
        gd,
        "IntraRail",
        "Central City Warp Rail Terminal",
        "2X",
        ["Central City Beltway Terminal North"],
        ["Rochshire", "Achowalogen Takachsin-Covina International Airport"],
    )
    adjacent_stations(
        n,
        gd,
        "IntraRail",
        "Achowalogen Takachsin-Covina International Airport",
        "2X",
        ["Central City Warp Rail Terminal", "Sienos"],
        ["Woodsbane", "Siletz Salvador Station"],
    )
    adjacent_stations(
        n,
        gd,
        "IntraRail",
        "Siletz Salvador Station",
        "2X",
        ["Woodsbane", "Achowalogen Takachsin-Covina International Airport"],
    )

    adjacent_stations(n, gd, "FLR Kazeshima/Shui Chau", "Ho Kok", "C1", ["Ho Kok West", "Sha Tsui"])

    adjacent_stations(n, gd, "New Prubourne Subway", "Evergreen Parkway", "B", ["Wuster Drive", "Penn Island-Zoo"])

    adjacent_stations(n, gd, "ErzLink Trams", "Atrium North", "3", ["Atrium West", "Atrium East"], ["Almono"])
    adjacent_stations(
        n, gd, "ErzLink Trams", "Atrium South", "3", ["Atrium West", "Atrium East"], ["Spire of New Domain"]
    )

    adjacent_stations(
        n,
        gd,
        "Refuge Streetcar",
        "West Train Station",
        "North/South Loop",
        ["Cranberry Green", "Downtown North"],
        ["Hilltop"],
    )
    adjacent_stations(
        n,
        gd,
        "Refuge Streetcar",
        "South Hill",
        "North/South Loop",
        ["Refuge Airfield North", "University South"],
        ["Hilltop"],
    )

    handle_shared_stations(gd, n)
    handle_proximity(gd, n)
    n.finalise()

    s = Drawer(n, Style(scale=0.1, station_dots=True)).draw()
    with open("maps/rail.svg", "w") as f:
        f.write(str(s))


if __name__ == "__main__":
    gd = gt.GD.urllib_get()

    rail(gd)
