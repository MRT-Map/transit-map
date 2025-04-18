from __future__ import annotations

from air import air
from bus import bus
from gatelogue_types import GatelogueDataNS
from rail import rail
from sea import sea

if __name__ == "__main__":
    data = GatelogueDataNS.get()

    air(data)
    rail(data)
    sea(data)
    bus(data)

