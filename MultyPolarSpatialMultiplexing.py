import numpy as np
import matplotlib.pyplot as plt

# Constants used
SPEED_OF_LIGHT  = 3e8
FREQUENCY       = 3e9 # 3GHz
THETA           = np.arange(0, 2 * np.pi, np.pi / 180) #Theta values from 0 to 2*pi

class MIMOConfig:
    def __init__(self, num_antennas, receiver_angles_deg):

        # Number of receivers determined from the number of angles 
        self.num_receivers = len(receiver_angles_deg)

        self.num_antennas = num_antennas // self.num_receivers

        self.receiver_angles_deg = receiver_angles_deg
        self.receiver_angles_rad = [
            angle*(np.pi/180) for angle in receiver_angles_deg
        ]    

        # Calculate antenna spacing ( wavelength/2 ) (C/F)/2
        self.wavelength = SPEED_OF_LIGHT / FREQUENCY
        self.antenna_spacing = self.wavelength / 2
        
        print(self.antenna_spacing)
        self.array_responses = [
            self.getArrayResponse(angle_rad) for angle_rad in self.receiver_angles_rad
        ]

    def getArrayResponse(self, angle_rad):

        # Array indices
        n = np.arange(1,self.num_antennas + 1)
       
        # Reshape n to a column vector
        n = n.reshape(-1, 1)

        # Array response matrix
        X = np.exp(-1j * (n - 1) * 2 * np.pi * self.antenna_spacing * np.cos(THETA) / self.wavelength)
       
        # Weight vector for steering
        w = np.exp(1j * (n - 1) * 2 * np.pi * self.antenna_spacing * np.cos(angle_rad) / self.wavelength)
        w = w.reshape(-1, 1)
        # Array response with steering
        #self.array_responses = np.dot(w.T, X)
        return np.dot(w.T, X)



def angularGainInDBi(superpossition, angle_deg):
        
        # The number of THETA's used = 360 - one per deg (so angle_deg can be the index)
        array_response_at_angle = np.abs(superpossition[0][angle_deg])

        # Calculate the gain of the transmitting antenna based on the array response
        Gt_dB = 10 * np.log10(array_response_at_angle)

        return Gt_dB


# Calculate the superposition of array_responses 
def superpose(arrays):
    num_arrays = len(arrays)
    weights = np.ones(num_arrays) / num_arrays  # Even weights
    result = np.zeros_like(arrays[0])
    for i in range(num_arrays):
        result += weights[i] * arrays[i]
    return result

def polarPlot(array):
    plt.figure(figsize=(10, 6))

    plt.polar(THETA, np.abs(array.flatten()), 'b')
    #plt.title()
    #plt.legend()
    plt.show()


################################################################################################
#                                           TESTING                                            #
################################################################################################

config1 = MIMOConfig(num_antennas=6, receiver_angles_deg=[90])
#config2 = MIMOConfig(num_antennas=4, receiver_angle=90)
#config3 = MIMOConfig(num_antennas=4, receiver_angle=45)
#config4 = MIMOConfig(num_antennas=8, receiver_angle=30)

sp = superpose(config1.array_responses)

# Plot the gain in polar coordinates
polarPlot(sp)
#plt.polar(THETA, np.abs(sp.flatten()), 'g', label='Superposition')
# Example of how to use estimateReceivedGain
distance = 100  # Example distance in meters
Pt_dB = 30  # Example transmit power in dB
Gr_dB = 1  # Example receive antenna gain in dB

# Example of how to use calculateTransmittingAntennaGain
angle_rad = np.radians(90)  # Example angle in radians
Gt_dB_at_angle = angularGainInDBi(sp, 90)
print(f"Transmitting antenna gain at {np.degrees(angle_rad)} degrees: {Gt_dB_at_angle} dB")

Gt_dB_at_angle = angularGainInDBi(sp, 30)
print(f"Transmitting antenna gain at {30} degrees: {Gt_dB_at_angle} dB")