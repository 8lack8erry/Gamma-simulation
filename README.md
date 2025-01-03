# Gamma Scattering Simulation

This repository contains a comprehensive simulation framework for modeling and analyzing Compton scattering experiments involving gamma rays. The project implements several key classes and functionalities that allow users to simulate photon interactions with matter, visualize results, and perform advanced data analysis.

## Table of Contents
- [Overview](#overview)
- [Implemented Classes](#implemented-classes)
- [Simulation Experiments](#simulation-experiments)
- [Visualization](#visualization)

## Overview
This simulation models the interaction of gamma rays using key principles of Compton scattering. It provides tools to simulate different experimental setups, including spectroscopy, coincidence measurements, and detailed scattering experiments, allowing for visualization and deeper insights into gamma-ray behavior.

## Implemented Classes
The core of the simulation consists of several modular classes:

### 1. `Photon`
- Represents a gamma-ray photon.
- Tracks energy, position, and direction.

### 2. `Electron`
- Models an electron that interacts with the photon during scattering.

### 3. `Detector`
- Simulates a detector that records the energy and direction of photons.

### 4. `Source`
- Represents a gamma-ray source, such as Na-22, used in spectroscopy and scattering experiments.

### 5. `Target`
- Models the material where Compton scattering occurs.

### 6. `Interaction`
- Implements the physics of Compton scattering and other relevant photon interactions.

## Simulation Experiments
Three main types of experiments are implemented:

### 1. **Spectroscopy of Na-22 Spectrum**
- Simulates the energy spectrum emitted by a Na-22 gamma-ray source.
- Models the detection of characteristic energy peaks.

### 2. **Coincidence Measurement**
- Simulates a coincidence experiment where two detectors simultaneously measure photons resulting from pair production or other correlated processes.

### 3. **Compton Scattering on a Target**
- Models photons scattering off a target material.
- Analyzes energy and angular distribution of scattered photons.

## Visualization
The project includes a 3D visualization feature that allows users to:
- Display the gamma-ray source and photon trajectories.
- Visualize detectors and the target in a 3D environment.
- Understand the spatial distribution of interactions.

