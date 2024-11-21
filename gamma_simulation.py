#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
# SIMULATION OF THE GAMMA EMISSION FOR Na22
#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.integrate import quad

#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

# Detector parameters
Len = 10  # cm (Length of the detector)
Height = 5  # cm (Height of the detector)
d_source = 30  # cm (Distance from source to detector)
resolution = 0.07  # Detector resolution
density = 3.67  # g/cm^3 (Density of NaI, detector material)
Z = 47  # Atomic number of NaI (detector material), it is a sort of mean between Z = 11 (Na) and Z = 53 (I)

# Physical constants
r_e = 2.817e-15  # Classical electron radius in cm
pi_r_e2 = 2.53 # barn ---> 1 barn = 10^(-28) m^2
m_e = 511  # Rest mass energy of the electron in keV
alpha = 1 / 137  # Fine-structure constant

#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

# Function to simulate detector resolution by applying Gaussian smearing
def detector_resolution(energy, resolution=resolution):
    return np.random.normal(energy, energy * resolution)

# Function to simulate gamma emission from Na22 with energy and type (511 keV or 1274 keV)
def gamma_emission():
    gamma_type = random.uniform(0, 100)  
    if gamma_type <= 90.3:  
        return 511
    else:  
        return 1274

# Function to calculate the distance traveled by the gamma ray in the detector based on the emission angle
def distance_in_detector(angle, Len_detector=Len, Height_detector=Height, Distance_source=d_source):
    theta_lim1 = np.arctan(Height_detector / (2 * Distance_source))
    theta_lim2 = np.arctan(Height_detector / (2 * (Distance_source + Len_detector)))

    if angle < theta_lim2:
        return Len_detector / np.cos(angle)
    if theta_lim2 <= angle < theta_lim1:
        return ((Height_detector / 2) - Distance_source * np.tan(angle)) / np.sin(angle)
    else:
        return None  # If outside detector boundaries, return None    

# Function to calculate the energy of the electron after Compton scattering
def compton_scattering(energy, angle):
    return energy - energy / (1 + (energy / m_e) * (1 - np.cos(np.radians(angle))))

#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
# CROSS SECTION
#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

# Function to calculate the energy of the gamma ray after Compton scattering
def cross_section_photoelectron(energy, detector_Z=Z):
    cross_section = (5 * 10 ** (11)) * (detector_Z ** 5) / ((energy * 10 ** (3)) ** 3.5) # energy conversion from keV to eV
    return cross_section

# Function to calculate the photoelectric cross-section for a given energy in the detector
def cross_section_compton(energy):
    # Klein-Nishina differential cross-section formula
    def differential_cross_section(angle):
        lamlam1 = 1 / (1 + (energy / m_e) * (1 - np.cos(angle)))
        d_cross_section = (pi_r_e2) * (lamlam1 ** 2) * (lamlam1 + 1/lamlam1 - np.sin(angle) ** 2)
        return d_cross_section * np.sin(angle)  # Include 2 pi * sin(angle) for solid angle integration
                                                # Il fattore 2 pi è già stato considerato nel calcolo di d_cross_section
    
    cross_section, _ = quad(differential_cross_section, 0, np.pi)
    return cross_section

# Con queste costanti le sezioni d'urto del 511 escono (in barn): 
# sigma_photo = 1.2022260761757484
# sigma_compton = 2.905977173453491 
# sigma_photo/sigma_compton = 0.41370802467350815
# Dovrebbero essere: 
# sigma_photo ~ 1.5
# sigma_compton ~ 3
# sigma_photo/sigma_compton ~ 0.5

#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
# GAMMA DETECTION
#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

# Function to calculate the interaction probability in NaI
def interaction_probability(x, energy):
    mu = 0
    if energy == 511:
        mu = 0.2 # cm^-1
    if energy == 1274:
        mu = 0.1 # cm^-1
    return (1 - np.exp(-x * mu))

def gamma_detection(step=0.1, resolution=resolution, Len_detector=Len, Height_detector=Height, Distance_source=d_source, detector_Z=Z): 
    energy = gamma_emission()

    angle = random.uniform(-180 if energy == 1274 else -90, 180 if energy == 1274 else 90)
    d_detector = distance_in_detector(angle, Len_detector, Height_detector, Distance_source)
    if d_detector == None: 
        return None

    sigma_photo = cross_section_photoelectron(energy, detector_Z)
    sigma_compton = cross_section_compton(energy)
    total_sigma = sigma_photo + sigma_compton

    # Calculate probabilities based on relative cross-sections
    photo_prob = sigma_photo / total_sigma
    compton_prob = sigma_compton / total_sigma

    detected_energy = []

    for r1 in np.arange(0, d_detector, step):
        ip = random.uniform(0, 1)
        if ip < interaction_probability(r1, energy):
            eff = random.uniform(0, 1)

            if eff < photo_prob: # Photoelectric effect
                detected_energy.append(detector_resolution(energy, resolution))
            else:  # Compton scattering
                scattering_angle = random.uniform(0, 180)
                compton_energy = compton_scattering(energy, scattering_angle)
                detected_energy.append(detector_resolution(compton_energy, resolution))
                energy -= compton_energy

                # Multi-Compton (only 2)
                x = r1 * np.cos(angle)
                y = r1 * np.sin(angle)

                d_detector2 = 0

                if scattering_angle < np.arctan(y / (Len - x)):
                    d_detector2 = (Len - x) / np.cos(scattering_angle)
                elif 180 - scattering_angle < np.arctan(y / x):
                    d_detector2 = x / np.cos(180 - scattering_angle)
                else:
                    if scattering_angle < 90:
                        d_detector2 = y / np.cos(90 - scattering_angle)
                    else:
                        d_detector2 = y / np.cos(scattering_angle - 90)
                
                for r2 in np.arange(0, d_detector2, step): 
                    ip = random.uniform(0, 1)
                    if ip < interaction_probability(r2, energy):
                        eff = random.uniform(0, 1)

                        if eff < photo_prob: # Photoelectric effect
                            detected_energy.append(detector_resolution(energy, resolution))
                        else:  # Compton scattering
                            scattering_angle2 = random.uniform(0, 180)
                            compton_energy = compton_scattering(energy, scattering_angle2)
                            detected_energy.append(detector_resolution(compton_energy, resolution))

    return detected_energy
