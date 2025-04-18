from __future__ import annotations

import json

import niquests
from gatelogue_types import GatelogueData, GatelogueDataNS

from bus import bus
from rail import rail
from air import air
from sea import sea

if __name__ == "__main__":
    data = GatelogueDataNS.get()

    air(data)
    rail(data)
    sea(data)
    bus(data)

