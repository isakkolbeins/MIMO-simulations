import numpy as np
import matplotlib.pyplot as plt

SPEED_OF_LIGHT = 3e8



class MIMOConfig:
    def __init__(self, num_antennas, receiver_angles, distance, frequency):
        
        # Initialize the MIMO config setting.
            # num_antennas (int): Number of transmitting antennas.
            # receiver_angles (list [degrees]): List of angles (in degrees) of receiver direction.
            # distance float: Distance between the transmitter and receivers.
            # frequency (float): The frequency of the signal
           
        self.num_antennas = num_antennas
        # Number of receivers determined from the number of angles 
        self.num_receivers = len(receiver_angles)
        self.receiver_angles = receiver_angles
        self.distance = distance
        self.frequency = frequency

        # Calculate antenna spacing ( wavelength/2 ) 
        self.wavelength = SPEED_OF_LIGHT / frequency
        self.antenna_spacing = self.wavelength / 2
        self.leftmost_antenna = (self.antenna_spacing * (num_antennas - 1)) / 2

        # Calculate positions of antennas for receivers in (x, y)
        # Centering with leftmost_antenna - to have them centered over the - + sides of Y 
        self.transmitter_antenna_positions = [
            ((self.antenna_spacing * antenna) - self.leftmost_antenna, 0) for antenna in range(num_antennas)
        ]

        # Calculate position of receivers in (x, y)
        self.receiver_positions = [
            ( self.distance * np.cos(np.radians(angle)), self.distance * np.sin(np.radians(angle)))
            for angle in self.receiver_angles
        ]



def plot_mimo_config(config, x_range=(-130, 130), y_range=(-30, 130)):
    # Show a plot of the MIMO configuration in 2D with positions of antennas and receivers.

    # Make it bigger
    plt.figure(figsize=(10, 6))
   
    # Plot receivers
    plt.scatter(*zip(*config.receiver_positions), marker='o', label='Receivers', color='green')
    
    # Plot antennas centered at (0,0)
    plt.scatter(*zip(*config.transmitter_antenna_positions), marker='^', label='Antennas', color='blue')
    
    # Plot the "transmitter"
    plt.scatter(0, 0, marker='s', color='red', label='Transmitter')
    
    # Labeling the recivers 
    for i, (x, y) in enumerate(config.receiver_positions):
        plt.text(x, y+10, f'Receiver {i + 1}\n({config.receiver_angles[i]}°)', ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

    # Finalize plot 
    plt.title(f'MIMO Configuration - { config.num_antennas } Antennas, { config.num_receivers } Receivers, Frequency: { config.frequency } Hz')
    plt.xlabel('X Distance (meters)')
    plt.ylabel('Y Distance (meters)')
    plt.xlim(x_range)
    plt.ylim(y_range)
    # plt.legend()
    plt.grid(True)
    plt.show()


### Testing 

config = MIMOConfig(num_antennas=12, receiver_angles=[120, 90, 60], distance=100, frequency=3e9)
plot_mimo_config(config)

config = MIMOConfig(num_antennas=6, receiver_angles=[90], distance=100, frequency=3e9)
plot_mimo_config(config)
