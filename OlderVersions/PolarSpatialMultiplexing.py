import numpy as np
import matplotlib.pyplot as plt

# Constants used
SPEED_OF_LIGHT  = 3e8
FREQUENCY       = 3e9 # 3GHz
THETA           = np.arange(0, 2 * np.pi, np.pi / 180) #Theta values from 0 to 2*pi

class MIMOConfig:
    def __init__(self, num_antennas, receiver_angle):
           
        self.num_antennas = num_antennas
        # Number of receivers determined from the number of angles 
        # self.num_receivers = len(receiver_angles)
    
        # self.receiver_angles = receiver_angles
        self.receiver_angle_rad = receiver_angle*(np.pi/180)    

        #self.distance = distance
        # Calculate antenna spacing ( wavelength/2 ) (C/F)/2
        self.wavelength = SPEED_OF_LIGHT / FREQUENCY
        self.antenna_spacing = self.wavelength / 2
        
        # self.leftmost_antenna = (self.antenna_spacing * (num_antennas - 1)) / 2

        # Calculate positions of antennas for receivers in (x, y)
        # Centering with leftmost_antenna - to have them centered over the - + sides of Y 
        #self.transmitter_antenna_positions = [
        #    ((self.antenna_spacing * antenna) - self.leftmost_antenna, 0) for antenna in range(num_antennas)
        #]

        # Calculate position of receivers in (x, y)
        #self.receiver_positions = [
        #    ( self.distance * np.cos(np.radians(angle)), self.distance * np.sin(np.radians(angle)))
        #    for angle in self.receiver_angles
        #]


        # Array indices
        n = np.arange(1, num_antennas + 1)
        print("_____n_____")
        print(n)

        # Reshape n to a column vector
        n = n.reshape(-1, 1)

        # Array response matrix
        X = np.exp(-1j * (n - 1) * 2 * np.pi * self.antenna_spacing * np.cos(THETA) / self.wavelength)
        print("_____X_____")
        print(X)


        # Weight vector for steering
        w = np.exp(1j * (n - 1) * 2 * np.pi * self.antenna_spacing * np.cos(self.receiver_angle_rad) / self.wavelength)
        print("_____W_____")
        print(w)
        #w = w.reshape(-1, 1)
        print("_____W -reshaped_____")
        print(w)

        # Array response with steering
        self.array_response = np.dot(w.T, X)

        print("_____r_____")
        print(self.array_response)

# Calculate the superposition of array_responses 
def superpose(*arrays):
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
    plt.legend()
    plt.show()




## Testing 

config1 = MIMOConfig(num_antennas=4, receiver_angle=135)
config2 = MIMOConfig(num_antennas=4, receiver_angle=90)
config3 = MIMOConfig(num_antennas=4, receiver_angle=45)
#config4 = MIMOConfig(num_antennas=8, receiver_angle=30)

sp = superpose(config1.array_response, config2.array_response, config3.array_response)


# Plot the gain in polar coordinates
polarPlot(config1.array_response)
polarPlot(sp)
#plt.polar(THETA, np.abs(sp.flatten()), 'g', label='Superposition')


