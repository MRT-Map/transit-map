import re

import requests
import vector
from autocarter.colour import Colour, Stroke
from autocarter.drawer import Drawer, Style
from autocarter.network import Connection, Line, Network, Station


def _station(n: Network, company_json, data):
    stations = {}
    for station_uuid in company_json["stations"]:
        station_json = data["station"][station_uuid]
        coordinates = station_json["coordinates"]
        if coordinates is None:
            print("No conns", station_json["name"])  # noqa: T201
            continue
        if station_json["name"] is None:
            continue
        station = n.add_station(
            Station(
                id=station_uuid,
                name=station_json["name"].replace("&", "&amp;"),
                coordinates=vector.obj(x=coordinates[0], y=coordinates[1]),
            )
        )
        stations[station.name] = station
    return stations


def _connect(n: Network, company_json, data):
    visited_stations = []
    for station_uuid in company_json["stations"]:
        if station_uuid not in n.stations:
            continue
        station_json = data["station"][station_uuid]
        if not station_json["connections"]:
            print("No conns", station_json["name"])  # noqa: T201
        for conn_station_uuid, connections in station_json["connections"].items():
            if (
                conn_station_uuid in visited_stations
                or conn_station_uuid not in n.stations
            ):
                continue
            for connection in connections:
                n.connect(
                    n.stations[station_uuid],
                    n.stations[conn_station_uuid],
                    n.lines[connection["line"]],
                )
        visited_stations.append(station_uuid)


def mrt(n: Network, data):
    data = data["rail"]
    company_uuid, company_json = next(
        (k, v) for k, v in data["company"].items() if v["name"] == "MRT"
    )

    col = {
        "A": "#00FFFF",
        "B": "#EEDB95",
        "C": "#5E5E5E",
        "D": "#9437FF",
        "E": "#10D20F",
        "F": "#0096FF",
        # "G": "#0ff",
        "H": "#5B7F00",
        "I": "#FF40FF",
        "J": "#4C250D",
        # "K": "#0ff",
        "L": "#9B95BC",
        "M": "#FF8000",
        "N": "#0433FF",
        "O": "#021987",
        "P": "#008E00",
        # "Q": "#0ff",
        "R": "#FE2E9A",
        "S": "#FFFA28",
        "T": "#915001",
        "U": "#2B2C35",
        "V": "#FF8AD8",
        "W": "#FF0000",
        "X": "#000000",
        "XM": "#000000",
        # "Y": "#0ff",
        "Z": "#EEEEEE",
    }

    for line_uuid in company_json["lines"]:
        line_json = data["line"][line_uuid]
        colour = col.get(line_json["code"], "#888")
        n.add_line(
            Line(
                id=line_uuid,
                name="MRT " + line_json["code"],
                colour=Colour.solid(colour),
            )
        )

    stations = {}
    for station_uuid in company_json["stations"]:
        station_json = data["station"][station_uuid]
        if station_json["world"] == "Old" or not station_json["connections"]:
            continue
        coordinates = station_json["coordinates"] or [0, 0]
        station = n.add_station(
            Station(
                id=station_uuid,
                name=(
                    " ".join(sorted(station_json["codes"]))
                    + " "
                    + (station_json["name"] or "")
                ).strip(),
                coordinates=vector.obj(x=coordinates[0], y=coordinates[1]),
            )
        )
        stations[station.name] = station

    _connect(n, company_json, data)

    return stations


def nflr(n: Network, data):
    data = data["rail"]
    company_uuid, company_json = next(
        (k, v) for k, v in data["company"].items() if v["name"] == "nFLR"
    )

    col = {
        "1": "#c00",
        "2": "#ffa500",
        "3": "#fe0",
        "4": "#987654",
        "5": "#008000",
        "6": "#0c0",
        "7": "#0cc",
        "8": "#008b8b",
        "9": "#00c",
        "10": "",
        "11": "",
        "12": "",
        "13": "#555",
        "14": "#aaa",
        "15": "#000",
        "16": "#eee",
        "17": "#c2b280",
        "18": "#bb9955",
        "19": "#000080",
        "20": "#965f46",
        "21": "#8b3d2e",
        "22": "#a3501e",
        "23": "#bb8725",
        "24": "#3d291b",
        "N1": "#8c0",
        "N2": "#5cf",
        "N3": "#f5f",
        "N4": "#fc0",
        "AB": "",
    }

    lines = {}
    for line_uuid in company_json["lines"]:
        line_json = data["line"][line_uuid]
        name = line_json["name"]
        if name.startswith("N") or name == "AB":
            colour = Colour.solid(col[name])
        elif name.startswith("W"):
            colour = Colour(
                (
                    Stroke(dashes=col[name[1:]], thickness_multiplier=1.0),
                    Stroke(dashes="#fff", thickness_multiplier=0.5),
                )
            )
        else:
            match = re.search(r"^(.)(\d+)(.*)$", line_json["name"])
            colour = Colour.solid(col[match.group(2)])
        line = n.add_line(
            Line(id=line_uuid, name="nFLR " + line_json["code"], colour=colour)
        )
        lines[line.name] = line

    stations = _station(n, company_json, data)
    _connect(n, company_json, data)
    return stations, lines


def intra(n: Network, data):
    data = data["rail"]
    company_uuid, company_json = next(
        (k, v) for k, v in data["company"].items() if v["name"] == "IntraRail"
    )

    col = {
        "6": ["#d16d8f"],
        "7": ["#d16d8f", "#4ebdb8", "#2f4bb3"],
        "15": ["#e6e630"],
        "17": ["#4ebdb8", "#00da37"],
        "29": ["#d98030", "#00da37", "#9a3030"],
        "32": ["#e6e630"],
        "34": ["#d98030", "#d3b2a2", "#9a3030"],
        "38": ["#00da37"],
        "40": ["#00da37"],
        "43": ["#2f4bb3"],
        "48": ["#d3b2a2"],
        "49": ["#b34bd9"],
        "50": ["#b34bd9", "#ff0000"],
        "51": ["#ff0000"],
        "52": ["#ff0000"],
        "63": ["#986d4c"],
        "64": ["#986d4c"],
    }

    for line_uuid in company_json["lines"]:
        line_json = data["line"][line_uuid]
        colour = (
            Colour.solid("#3d6edd")
            if line_json["code"].startswith("MCR")
            or line_json["code"].startswith("LM")
            or line_json["code"].startswith("S")
            else Colour.stroke(
                Stroke(dash_length=8, dashes=tuple(col[line_json["code"]]))
            )
            if line_json["code"] in col
            else Colour.solid("#888")
        )
        n.add_line(
            Line(
                id=line_uuid,
                name="IR "
                + line_json["code"].replace("<", "&lt;").replace(">", "&gt;"),
                colour=colour,
            )
        )

    stations = _station(n, company_json, data)
    _connect(n, company_json, data)
    return stations


def blu(n: Network, data):
    data = data["rail"]
    company_uuid, company_json = next(
        (k, v) for k, v in data["company"].items() if v["name"] == "BluRail"
    )

    for line_uuid in company_json["lines"]:
        line_json = data["line"][line_uuid]
        colour = Colour.solid(
            "#c01c22"
            if line_json["code"].endswith("X") and line_json["code"][0].isdigit()
            else "#0a7ec3"
            if line_json["code"][-1].isdigit()
            else "#0c4a9e"
        )
        n.add_line(Line(id=line_uuid, name="Blu " + line_json["code"], colour=colour))

    stations = _station(n, company_json, data)
    _connect(n, company_json, data)
    return stations


def rlq(n: Network, data):
    data = data["rail"]
    company_uuid, company_json = next(
        (k, v) for k, v in data["company"].items() if v["name"] == "RaiLinQ"
    )

    for line_uuid in company_json["lines"]:
        line_json = data["line"][line_uuid]
        colour = Colour.solid(
            "#ff5500" if line_json["code"].startswith("IC") else "#ffaa00"
        )
        n.add_line(Line(id=line_uuid, name="RLQ " + line_json["code"], colour=colour))

    stations = _station(n, company_json, data)
    _connect(n, company_json, data)
    return stations


def wzr(n: Network, data):
    data = data["rail"]
    company_uuid, company_json = next(
        (k, v) for k, v in data["company"].items() if v["name"] == "West Zeta Rail"
    )

    for line_uuid in company_json["lines"]:
        line_json = data["line"][line_uuid]
        colour = Colour.solid(line_json["colour"] or "#aa0000")
        n.add_line(Line(id=line_uuid, name="WZR " + line_json["code"], colour=colour))

    stations = _station(n, company_json, data)
    _connect(n, company_json, data)
    return stations


def mtc(n: Network, data):
    data = data["rail"]
    company_uuid, company_json = next(
        (k, v) for k, v in data["company"].items() if v["name"] == "MarbleRail"
    )

    for line_uuid in company_json["lines"]:
        line_json = data["line"][line_uuid]
        colour = Colour.solid(line_json["colour"] or "#cc00cc")
        n.add_line(Line(id=line_uuid, name="MTC " + line_json["code"], colour=colour))

    stations = _station(n, company_json, data)
    _connect(n, company_json, data)
    return stations


def nsc(n: Network, data):
    data = data["rail"]
    company_uuid, company_json = next(
        (k, v)
        for k, v in data["company"].items()
        if v["name"] == "Network South Central"
    )

    for line_uuid in company_json["lines"]:
        line_json = data["line"][line_uuid]
        colour = Colour.solid(line_json["colour"] or "#cc0000")
        n.add_line(Line(id=line_uuid, name="NSC " + line_json["code"], colour=colour))

    stations = _station(n, company_json, data)
    _connect(n, company_json, data)
    return stations


def redtrain(n: Network, data):
    data = data["rail"]
    company_uuid, company_json = next(
        (k, v) for k, v in data["company"].items() if v["name"] == "RedTrain"
    )

    for line_uuid in company_json["lines"]:
        line_json = data["line"][line_uuid]
        colour = Colour.solid(line_json["colour"] or "#ff0000")
        n.add_line(
            Line(id=line_uuid, name="RedTrain " + line_json["code"], colour=colour)
        )

    stations = _station(n, company_json, data)
    _connect(n, company_json, data)
    return stations


def rn(n: Network, data):
    data = data["rail"]
    company_uuid, company_json = next(
        (k, v) for k, v in data["company"].items() if v["name"] == "RailNorth"
    )

    for line_uuid in company_json["lines"]:
        line_json = data["line"][line_uuid]
        colour = Colour.solid(line_json["colour"] or "#000080")
        n.add_line(Line(id=line_uuid, name=line_json["code"], colour=colour))

    stations = _station(n, company_json, data)
    _connect(n, company_json, data)
    return stations


def fr(n: Network, data):
    data = data["rail"]
    company_uuid, company_json = next(
        (k, v) for k, v in data["company"].items() if v["name"] == "Fred Rail"
    )

    lines = {}
    for line_uuid in company_json["lines"]:
        line_json = data["line"][line_uuid]
        colour = Colour.solid(line_json["colour"] or "#000080")
        line = n.add_line(
            Line(id=line_uuid, name="FR " + line_json["code"], colour=colour)
        )
        lines[line.name] = line

    stations = _station(n, company_json, data)
    _connect(n, company_json, data)
    return stations, lines


def main():
    data = requests.get(
        "https://raw.githubusercontent.com/MRT-Map/gatelogue/dist/data_no_sources.json"
    ).json()  # noqa: S113
    n = Network()
    s_mrt = mrt(n, data)
    s_nflr, l_nflr = nflr(n, data)
    s_intra = intra(n, data)
    s_blu = blu(n, data)
    s_rlq = rlq(n, data)
    s_wzr = wzr(n, data)
    s_mtc = mtc(n, data)
    nsc(n, data)
    rn(n, data)
    s_fr, l_fr = fr(n, data)
    s_redtrain = redtrain(n, data)

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

    s_nflr["Dand Grand Central"].merge_into(n, s_intra["Dand Grand Central"])
    s_blu["Dand Central"].merge_into(n, s_intra["Dand Grand Central"])
    s_intra["Foresne Liveray"].merge_into(n, s_nflr["Foresne Liveray"])
    s_intra["Liveray"].merge_into(n, s_nflr["Foresne Liveray"])
    s_intra["Tembok Railway Station"].merge_into(n, s_nflr["Tembok"])
    s_wzr["Tembok"].merge_into(n, s_nflr["Tembok"])
    s_nflr["Tembok"].merge_into(n, s_mrt["M54 WS24 Tembok"])
    s_blu["Heampstead Kings Cross"].merge_into(
        n, s_intra["Deadbush Heampstead Kings Cross Railway Terminal"]
    )
    s_fr["Kings Cross Railway Terminal"].merge_into(
        n, s_intra["Deadbush Heampstead Kings Cross Railway Terminal"]
    )
    s_blu["Schillerton Maple Street"].merge_into(n, s_intra["Schillerton Maple Street"])
    s_blu["Boston Waterloo"].merge_into(n, s_intra["Boston Waterloo Station"])
    s_mtc["Boston Waterloo"].merge_into(n, s_intra["Boston Waterloo Station"])
    s_fr["Boston Waterloo"].merge_into(n, s_intra["Boston Waterloo Station"])
    s_mtc["Boston Clapham Junction"].merge_into(n, s_fr["Boston Clapham Junction"])
    s_intra["Boston Clapham Junction"].merge_into(n, s_fr["Boston Clapham Junction"])
    s_blu["Zaquar Tanzanite Station"].merge_into(n, s_intra["Zaquar Tanzanite Station"])
    s_blu["Tranquil Forest Central"].merge_into(n, s_intra["Tranquil Forest Central"])
    s_intra["MCR HQ"].merge_into(n, s_intra["Scarborough MCR HQ"])
    s_blu["San Dzobiak Union Station"].merge_into(
        n, s_intra["San Dzobiak Union Square"]
    )
    s_redtrain["San Dzobiak Union Square"].merge_into(
        n, s_intra["San Dzobiak Union Square"]
    )
    s_fr["San Dzobiak"].merge_into(n, s_intra["San Dzobiak Union Square"])
    s_blu["Siletz Salvador Station"].merge_into(n, s_intra["Siletz Salvador Station"])
    s_fr["Siletz"].merge_into(n, s_intra["Siletz Salvador Station"])
    s_redtrain["Siletz Salvador Station"].merge_into(
        n, s_intra["Siletz Salvador Station"]
    )
    s_fr["Lodminechead"].merge_into(n, s_intra["Lochminehead Trijunction"])
    s_blu["Los Angeles-Farwater Union Station"].merge_into(
        n, s_intra["Los Angeles-Farwater Union Station"]
    )
    s_blu["Valemount"].merge_into(n, s_intra["Valemount"])
    s_blu["Ravenna Union Station"].merge_into(n, s_intra["Ravenna Union Station"])
    s_blu["Rank Resort Central"].merge_into(n, s_intra["Rank Resort Central"])
    s_blu["Whitecliff Central"].merge_into(n, s_intra["Whitecliff Central"])
    s_rlq["Whitecliff Central"].merge_into(n, s_intra["Whitecliff Central"])
    s_blu["Segav Sal"].merge_into(n, s_intra["Segav Sal"])
    s_blu["Northlend"].merge_into(n, s_intra["Northlend Union Station"])
    s_rlq["Northlend Union"].merge_into(n, s_intra["Northlend Union Station"])
    s_rlq["Vegeta Junction"].merge_into(n, s_intra["Vegeta Junction"])
    s_blu["Broxbourne"].merge_into(n, s_intra["Broxbourne"])
    s_blu["Ilirea Transit Center"].merge_into(n, s_intra["Ilirea Transit Center"])
    s_rlq["Ilirea ITC"].merge_into(n, s_intra["Ilirea Transit Center"])
    s_intra["Ilirea Airport Station"].merge_into(n, s_blu["Ilirea Midcity Airport"])
    s_rlq["Ilirea Airport"].merge_into(n, s_blu["Ilirea Midcity Airport"])
    s_blu["Waverly"].merge_into(n, s_intra["Waverly Edinburgh Station"])
    s_blu["UCWT International Airport West"].merge_into(
        n, s_intra["Formosa-Sealane-Danielston UCWT International Airport West"]
    )
    s_fr["UCWTIA"].merge_into(
        n, s_intra["Formosa-Sealane-Danielston UCWT International Airport West"]
    )
    s_blu["Sealane Central"].merge_into(n, s_intra["Sealane Central"])
    s_rlq["Sealane Central"].merge_into(n, s_intra["Sealane Central"])
    s_blu["Central City Warp Rail Terminal"].merge_into(
        n, s_intra["Central City Warp Rail Terminal"]
    )
    s_rlq["Central City"].merge_into(n, s_intra["Central City Warp Rail Terminal"])
    s_fr["Central City"].merge_into(n, s_intra["Central City Warp Rail Terminal"])
    s_redtrain["Central City Warp Rail Terminal"].merge_into(
        n, s_intra["Central City Warp Rail Terminal"]
    )
    s_fr["Sealane New Forest Station"].merge_into(
        n, s_intra["Sealane New Forest Terminal"]
    )
    s_fr["Central City Beltway Terminal North"].merge_into(
        n, s_intra["Central City Beltway Terminal North"]
    )
    s_blu["Utopia - AFK"].merge_into(n, s_intra["Utopia Anthony Fokker Transit Hub"])
    s_fr["Utopia AFK"].merge_into(n, s_intra["Utopia Anthony Fokker Transit Hub"])
    s_blu["Venceslo"].merge_into(n, s_intra["Venceslo Union Station"])
    s_redtrain["Venceslo"].merge_into(n, s_intra["Venceslo Union Station"])
    s_blu["Laclede Central"].merge_into(n, s_intra["Laclede Central"])
    s_rlq["Laclede Central"].merge_into(n, s_intra["Laclede Central"])
    s_blu["Vermilion"].merge_into(n, s_intra["Vermilion Victory Square"])
    s_blu["Bakersville Grand Central"].merge_into(
        n, s_intra["Bakersville Grand Central"]
    )
    s_fr["Bakersville Grand Central"].merge_into(
        n, s_intra["Bakersville Grand Central"]
    )
    s_fr["Westchester Junction"].merge_into(
        n, s_intra["Bakersville Westchester Junction - Canal Works"]
    )
    s_intra["Laclede Theater District"].merge_into(
        n, s_intra["Laclede Theater District - Xavier Airport"]
    )  # TODO: gatelogue
    s_blu["Whitechapel Border"].merge_into(n, s_intra["Whitechapel Border"])
    s_blu["Waterville Union Station"].merge_into(n, s_intra["Waterville Union Station"])
    s_blu["Fort Yaxier Central"].merge_into(n, s_intra["Fort Yaxier Central"])
    s_blu["Sunshine Coast Máspalmas Terminal"].merge_into(
        n, s_intra["Sunshine Coast Máspalmas Terminal"]
    )
    s_blu["Murrville Central"].merge_into(n, s_intra["Murrville Central"])
    s_blu["BirchView Central"].merge_into(n, s_intra["BirchView Central"])
    s_rlq["Birchview Central"].merge_into(n, s_intra["BirchView Central"])
    s_rlq["Titsensaki"].merge_into(n, s_blu["Titsensaki North City"])
    s_rlq["East Mesa"].merge_into(n, s_intra["East Mesa M. Bubbles Station"])
    s_rlq["Mons Pratus"].merge_into(n, s_intra["Mons Pratus Transportation Hub"])
    s_rlq["Segville International"].merge_into(
        n, s_intra["Segville International Airport"]
    )
    s_blu["Segville International"].merge_into(
        n, s_intra["Segville International Airport"]
    )
    s_fr["Segville International Airport"].merge_into(
        n, s_intra["Segville International Airport"]
    )
    s_rlq["Utopia Central"].merge_into(n, s_blu["Utopia Central"])
    s_rlq["Utopia Stephenson"].merge_into(n, s_blu["Utopia Stephenson"])
    s_rlq["Utopia IKEA"].merge_into(n, s_blu["Utopia - IKEA"])
    s_blu["Saint Roux"].merge_into(n, s_intra["Saint Roux Gare Orsay"])
    s_rlq["Saint Roux Gare Orsay"].merge_into(n, s_intra["Saint Roux Gare Orsay"])
    s_nflr["Port of Porton"].merge_into(n, s_mrt["M83 U138 Porton"])
    s_nflr["Uacam Beach"].merge_into(n, s_mrt["M87 Uacam Beach East"])
    s_nflr["M90 Theme Park"].merge_into(n, s_mrt["M90"])
    s_nflr["Castlehill"].merge_into(n, s_mrt["U126"])
    s_nflr["Lilygrove Union"].merge_into(
        n, s_mrt["ZS52 Lilygrove Union Station/Heliport"]
    )
    s_nflr["Dewford City Lometa"].merge_into(n, s_wzr["Dewford City Lometa Station"])
    s_mtc["Cape Cambridge John Glenn"].merge_into(
        n, s_nflr["Cape Cambridge John Glenn Transit Centre"]
    )
    s_mtc["Port Sonder"].merge_into(n, s_nflr["Port Sonder"])
    s_mtc["Sandfield"].merge_into(n, s_nflr["Sandfield"])
    s_mtc["Seolho Midwest"].merge_into(n, s_nflr["Seolho Midwest"])
    s_mtc["Oceanside Bayfront"].merge_into(n, s_nflr["Oceanside Bayfront"])
    s_mtc["Tung Wan"].merge_into(n, s_nflr["Tung Wan"])
    s_mtc["Edwardsburg"].merge_into(n, s_nflr["Edwardsburg"])
    s_blu["Musique"].merge_into(n, s_mrt["D11 Musique"])
    s_blu["Elecna Bay North"].merge_into(n, s_intra["Elecna Bay North"])
    s_rlq["Elecna Bay North"].merge_into(n, s_intra["Elecna Bay North"])
    s_rlq["Outer Solarion"].merge_into(
        n, s_intra["Achowalogen Takachsin Outer Solarion"]
    )
    s_rlq["Downtown Solarion"].merge_into(
        n, s_intra["Achowalogen Takachsin Downtown Solarion"]
    )
    s_rlq["Achowalogen Takachsin Suburb"].merge_into(
        n, s_intra["Achowalogen Takachsin Suburb"]
    )
    s_rlq["Downtown Achowalogen Takachsin/Covina"].merge_into(
        n, s_intra["Achowalogen Takachsin-Covina Downtown"]
    )
    s_rlq["Achowalogen Takachsin Western Transportation Hub"].merge_into(
        n, s_intra["Achowalogen Takachsin West"]
    )
    s_blu["Chalxior Femtoprism Airfield"].merge_into(
        n, s_intra["Chalxior Femtoprism Airfield"]
    )
    s_blu["Pilmont"].merge_into(n, s_intra["Pilmont"])
    s_blu["New Acreadium - Central District"].merge_into(
        n, s_intra["New Acreadium Central District"]
    )
    s_blu["New Acreadium - Schiphol International"].merge_into(
        n, s_intra["New Acreadium Schiphol Airport"]
    )
    s_blu["Antioch Union Station"].merge_into(n, s_intra["Antioch Union Station"])
    s_rlq["Antioch"].merge_into(n, s_intra["Antioch Union Station"])
    s_rlq["Moramoa Wyndham Street"].merge_into(n, s_blu["Moramoa Wyndham Street"])
    s_rlq["Moramoa Central"].merge_into(n, s_blu["Moramoa Central"])
    s_intra["Seuland"].merge_into(n, s_blu["Seuland"])
    s_intra["Whiteley Turing Square"].merge_into(n, s_rlq["Whiteley Turing Square"])
    s_fr["Whiteley Turing Square"].merge_into(n, s_rlq["Whiteley Turing Square"])
    s_blu["Whiteley College Park"].merge_into(n, s_rlq["Whiteley College Park"])

    for station_uuid in n.stations:
        station_json = data["rail"]["station"][station_uuid]
        for prox_station_uuid in station_json["proximity"].get("railstation", {}):
            if prox_station_uuid not in n.stations:
                continue
            n.connect(
                n.stations[station_uuid],
                n.stations[prox_station_uuid],
                Connection(),
            )

    n.finalise()

    s = Drawer(n, Style(scale=0.1, station_dots=True)).draw()
    with open("./out.svg", "w") as f:
        f.write(str(s))


if __name__ == "__main__":
    main()
