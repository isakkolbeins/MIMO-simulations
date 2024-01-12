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

config1 = MIMOConfig(num_antennas=12, receiver_angles_deg=[135,90,45])
sp = superpose(config1.array_responses)

# Plot the gain in polar coordinates
polarPlot(sp)

################################################################################################
#                                       DATA COLLECTION                                        #
################################################################################################

def iterateOverAnglesAndAntennas(separation_angles, antenna_counts, offset_angle=0):
    
    data = {"Antennas": [], "Separation_Angle": [], "Receiver1": [], "Receiver2": [], "Receiver3": []}
    for num_antennas in antenna_counts:
        for separation in separation_angles:
            centered_reciver_angle = 90-offset_angle

            config = MIMOConfig(num_antennas=num_antennas, receiver_angles_deg=[centered_reciver_angle+separation , centered_reciver_angle, centered_reciver_angle-separation])
            sp = superpose(config.array_responses)

            data["Antennas"].append(num_antennas)
            data["Separation_Angle"].append(separation)
            data["Receiver1"].append(angularGainInDBi(sp, centered_reciver_angle + separation ))
            data["Receiver2"].append(angularGainInDBi(sp, centered_reciver_angle ))
            data["Receiver3"].append(angularGainInDBi(sp, centered_reciver_angle - separation))
            
        
    return data

# First check for 3 receivers - the degree of separation effect [90-1 degree separation]
separation_angles = np.arange(90, 0, -1)  # Iterate from 90 to 1 degree of separation
antenna_counts = [12]  # Antenna configurations to test

separation_data = iterateOverAnglesAndAntennas(separation_angles, antenna_counts)
plt.figure(figsize=(12, 8))

plt.plot(separation_data["Separation_Angle"], separation_data["Receiver1"], label=f"Receiver1", color="green", linewidth=3)
plt.plot(separation_data["Separation_Angle"], separation_data["Receiver2"], label=f"Receiver2", color="red")
plt.plot(separation_data["Separation_Angle"], separation_data["Receiver3"], label=f"Receiver3", color="blue")

plt.title('Separation Angle effect on equally separated receivers')
plt.xlabel('Separation Angle (degrees)')
plt.ylabel('Transmitting Antenna Gain (dBi)')
plt.legend()
plt.grid(True)
plt.show()


config2 = MIMOConfig(num_antennas=12, receiver_angles_deg=[110,90,70])
sp2 = superpose(config2.array_responses)
polarPlot(sp2)

config3 = MIMOConfig(num_antennas=96, receiver_angles_deg=[110,90,70])
sp3 = superpose(config3.array_responses)
polarPlot(sp3)

# Repeating the same scenario but increacing the number of antennas plotting them all 
antenna_counts = [12, 24, 48, 96]  # Antenna configurations to test
separation_variable_antenna_data = iterateOverAnglesAndAntennas(separation_angles, antenna_counts)
plt.figure(figsize=(12, 8))

for num_antennas in antenna_counts:
    #Filter data for the current number of antennas
    filtered_data = {key: [val[i] for i, antennas in enumerate(separation_variable_antenna_data["Antennas"]) if antennas == num_antennas] for key, val in separation_variable_antenna_data.items()}

    plt.plot(filtered_data["Separation_Angle"], filtered_data["Receiver1"], label=f"{num_antennas} Antennas - R1", linewidth=3)
    plt.plot(filtered_data["Separation_Angle"], filtered_data["Receiver2"], label=f"{num_antennas} Antennas - R2")
    plt.plot(filtered_data["Separation_Angle"], filtered_data["Receiver3"], label=f"{num_antennas} Antennas - R3")

plt.title('Transmitting Antenna Gain vs. Separation Angle')
plt.xlabel('Separation Angle (degrees)')
plt.ylabel('Transmitting Antenna Gain (dBi)')
plt.legend(loc = 'lower right')
plt.grid(True)
plt.show()



def plotwithOffset(offset_angle):
    separation_angles = np.arange(90, 0, -1) # Central beam is at 45degrees (we can only explore explore separation up to 45degrees)
    antenna_counts = [12, 24, 48, 96]  # Antenna configurations to test
    offset_data = iterateOverAnglesAndAntennas(separation_angles, antenna_counts, offset_angle)
    plt.figure(figsize=(12, 8))
    for num_antennas in antenna_counts:
        #Filter data for the current number of antennas
        filtered_data = {key: [val[i] for i, antennas in enumerate(offset_data["Antennas"]) if antennas == num_antennas] for key, val in offset_data.items()}

        plt.plot(filtered_data["Separation_Angle"], filtered_data["Receiver1"], label=f"{num_antennas} Antennas - R1")
        plt.plot(filtered_data["Separation_Angle"], filtered_data["Receiver2"], label=f"{num_antennas} Antennas - R2")
        plt.plot(filtered_data["Separation_Angle"], filtered_data["Receiver3"], label=f"{num_antennas} Antennas - R3")

    plt.title(f'{offset_angle}degree offset')
    plt.xlabel('Separation Angle (degrees)')
    plt.ylabel('Transmitting Antenna Gain (dBi)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Now exploring the angular effect on the separation factor
plotwithOffset(30)
plotwithOffset(45)
config4 = MIMOConfig(num_antennas=96, receiver_angles_deg=[90,45,0])
sp4 = superpose(config4.array_responses)
polarPlot(sp4)


