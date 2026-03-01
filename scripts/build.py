from __future__ import annotations

from air import air
from bus import bus
import gatelogue_types as gt
from rail import rail
from sea import sea

if __name__ == "__main__":
    gd = gt.GD.urllib_get()

    air(gd)
    rail(gd)
    sea(gd)
    bus(gd)
