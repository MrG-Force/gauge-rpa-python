# Mainframe and Windows App Automation with RPA and Gauge

## Pre-requisites
- [Python 3.9](https://www.python.org/downloads/)
- [Gauge](https://docs.gauge.org/getting_started/installing-gauge.html)

## Quick Start
- To run the Mainframe terminal emulator specs you'll need access to [IBM Z Xplore](https://www.ibm.com/z/resources/zxplore). There you can obtain the host, port, user and password to connect to the mainframe.
- Add a `.env` file in the root directory as follows:
```shell
MAINFRAME_HOST=your-mainframe-host
MAINFRAME_PORT=your-mainframe-port
MAINFRAME_USER=your-mainframe-user
MAINFRAME_PASS=your-mainframe-pass
```
- Create a virtual environment, run:
```shell
python -m venv venv
```

- Install pip dependencies, run:
```shell
pip install -r requirements.txt
```

