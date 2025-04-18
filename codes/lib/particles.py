import numpy as np
from scipy.integrate import quad

# Physical constants
bn = 1e-28  # Barn in m^2, unit of cross-section
r_e = 2.817e-15  # Classical electron radius in meters
m_e = 511  # Rest mass energy of the electron in keV
alpha = 1 / 137  # Fine-structure constant (dimensionless)

class Particle:
    def __init__(self, energy: float, direction: list[float], position: list[float] = [0, 0, 0]):
        """
        Initializes a Particle object with energy and direction.
        
        :param energy: Particle energy in keV.
        :param direction: Direction of the particle as a 3D unit vector.
        """
        self.energy = energy
        self.direction = np.array(direction)
        self.position = np.array(position)


    def __repr__(self):
        """
        Return a string representation of the Particle object for easy printing.
        """
        return f"Particle(energy={self.energy} keV, direction={self.direction}, position={self.position})"


    def propagation(self, distance: float):
        """
        Calculate the new position of the particle after traveling a given distance.
        
        :param distance: The distance traveled by the particle.
        :return: The new position as a 3D vector.
        """
        self.position = self.position + np.array(self.direction) * distance


# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
# SUBCLASS PHOTON
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-


class Photon(Particle):
    def __init__(self, energy: float, direction: list[float], position: list[float] = [0, 0, 0]):
        """
        Initializes a Photon object with energy and direction.
        
        :param energy: Photon energy in keV.
        :param direction: Direction of the photon as a 3D unit vector.
        """
        super().__init__(energy, direction, position)


    def __repr__(self):
        """
        Return a string representation of the Photon object for easy printing.
        """
        return f"Photon(energy={self.energy} keV, direction={self.direction}, position={self.position})"
    

    def info(self):
        """
        Print the energy and direction of the photon.
        """
        print(f"Energy: {self.energy}")
        print(f"Direction: {self.direction}")
        print(f"Position: {self.position}")

    
    def compton_scattering(self, angle: float) -> float:
        """
        Calculate the energy of the photon after Compton scattering.
        
        :param angle: Scattering angle in radians.
        :return: Scattered photon energy.
        """
        return self.energy / (1 + (self.energy / m_e) * (1 - np.cos(angle)))
    

    def klein_nishina(self, angle: float) -> float:
        """
        Calculate the Klein-Nishina differential cross-section for Compton scattering.
        
        :param angle: Scattering angle in radians.
        :return: Differential cross-section value.
        """
        r = self.compton_scattering(angle) / self.energy
        c = alpha ** 2 / (2 * m_e ** 2)
        return c * r ** 2 * (r + 1 / r - np.sin(angle) ** 2)
    

    def compton_angle(self) -> float:
        """
        Generate random angles for Compton scattering using rejection sampling.

        :return: Scattering angle in radians.
        """
        # Normalize the Klein-Nishina distribution by integrating over all angles
        normalization, _ = quad(self.klein_nishina, 0, np.pi)

        max_pdf = 0.9  # Max value of the probability distribution for rejection sampling
        
        while True:
            theta = np.random.uniform(0, np.pi)  # Random angle between 0 and pi
            u = np.random.uniform(0, max_pdf)  # Random uniform value for rejection sampling

            pdf_compton = self.klein_nishina(theta) / normalization  # Probability density function for Compton scattering

            # Accept or reject based on the probability density
            if u <= pdf_compton:
                return theta  # Return the accepted angle
            

# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
# SUBCLASS ELECTRON
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-


class Electron(Particle):
    def __init__(self, energy: float, direction: list[float], position: list[float] = [0, 0, 0]):
        """
        Initializes a Electron object with energy and direction.

        :param energy: Electron energy in keV.
        """
        super().__init__(energy, direction, position)


    def __repr__(self):
        """
        Return a string representation of the Electron object for easy printing.
        """
        return f"Electron(energy={self.energy} keV, direction={self.direction}, position={self.position})"


    def info(self):
        """
        Print the energy and the direction of the electron.
        """
        print(f"Energy: {self.energy}")
        print(f"Direction: {self.direction}")
        print(f"Position: {self.position}")

   
    def compton_scattering(self, angle: float, photon: Photon) -> float:
        """
        Calculate the energy of the electron after Compton scattering.

        :param angle: Scattering angle in radians.
        :param photon: Incident photon.
        :return: Scattered photon energy.
        """
        return photon.energy - photon.compton_scattering(angle)

