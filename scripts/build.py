from __future__ import annotations

import json

import niquests
from bus import bus
from rail import rail
from sea import sea

if __name__ == "__main__":
    data = niquests.get(
        "https://raw.githubusercontent.com/MRT-Map/gatelogue/dist/data_no_sources.json"
    )
    data = json.loads(data.text)['nodes']

    rail(data)
    sea(data)
    bus(data)
