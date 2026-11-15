# Satellite Overhead Tracker

A lightweight Python utility that fetches live orbital data from CelesTrak, calculates current satellite positions, and alerts you if any satellites are passing near a specified latitude and longitude within a user-defined variance.

## Features

* **Live Orbital Data:** Automatically pulls up-to-date Two-Line Element (TLE) sets directly from CelesTrak.
* **Custom Coordinates:** Check for overhead satellites at any location on Earth.
* **Adjustable Search Radius:** Define your own latitude/longitude variance to widen or narrow the detection zone.
* **Built-in Space Bases:** Comes with the locations of various space bases built-in, so you don't have to look up their coordinates.
* **Instant Reporting:** Clearly outputs the names and current positions of any satellites detected within your target area.

## Prerequisites

Before running the project, make sure you have Python 3.7+ installed, along with the required libraries for fetching data and propagating orbits:

```bash
pip install sgp4 skyfield numpy pyqt6
```

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/andre-sidarous/mecearth.git
   cd mecearth
   ```

2. Install the dependencies:
   ```bash
   pip install -r REQUIREMENTS.txt
   ```

## Usage

Run the main script from your terminal:

```bash
python main.py
```

A window should appear.
Enter your target coordinates and the allowable variance (in degrees) on the left side. The result will appear on the right.

## How It Works

1. **Data Retrieval:** Queries CelesTrak's public GP JSON data set to get current orbital data.
2. **Orbit Propagation:** Computes the sub-satellite point (current latitude and longitude directly beneath the satellite) for each satellite.
3. **Bounding Box Check:** Compares each satellite's coordinates against your target coordinates $\pm$ the user-provided variance, and gives the names of the satellites.

## Acknowledgments

* Orbital data provided by CelesTrak.