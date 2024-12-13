# transit-map

![GitHub Pages Status](https://img.shields.io/github/actions/workflow/status/MRT-Map/transit-map/.github%2Fworkflows%2Fbuild.yaml)
![GitHub repo size](https://img.shields.io/github/repo-size/MRT-Map/transit-map)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/mrt-map/transit-map?label=last%20update)

Map of rail lines (MRT, warp rail, traincart rail, etc) on the Minecart Rapid Transit server

## Building the map
* (Optional: Start a virtual environment: `python -m venv env && source ./env/bin/activate.sh`)
* Install dependencies: `pip install -Ur requirements.txt`
* Run the build script: `python scripts/build.py`
* The map is located in `maps`
