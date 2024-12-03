# Na-22 Gamma Emission Simulation

This repository contains code to simulate the gamma-ray emission from a sodium-22 (Na-22) source. The simulation includes key physical processes such as:

- Pair annihilation and the production of 511 keV photons.
- Gamma emission at 1274 keV.
- Effects of Compton scattering and the photoelectric effect.
- Detector resolution and electronics background.

The code is written in Python and is suitable for analyzing gamma-ray spectra and studying energy deposition mechanisms.

## Features

- **Spectrum Simulation**: Simulates the energy spectrum of gamma rays emitted from a Na-22 source.
- **Physics Processes**: Includes Compton scattering, photoelectric effects, and annihilation photons.
- **Detector Response**: Models detector resolution and electronic noise.
- **Visualization**: Generates spectra and marks key energy lines for visualization.

## Example Output

Below is an example of the simulated gamma-ray spectrum from a Na-22 source:

![Simulated Gamma Spectrum](simulazione_realistica.png)

The red dashed lines indicate the primary gamma emissions at **511 keV** and **1274 keV**.

## Requirements

- Python 3.7+
- Required libraries: `numpy`, `matplotlib`

## Installation

Clone this repository to your local machine:
```bash
git clone https://github.com/yourusername/Na22-Gamma-Simulation.git
cd Na22-Gamma-Simulation

