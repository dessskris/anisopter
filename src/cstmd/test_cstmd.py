"""
Unit tests for module CSTMD.
"""
from subprocess import call
import unittest
import pickle

from cstmd import cstmd
import numpy as np
import os
import matplotlib


class TestCSTMD(unittest.TestCase):
    """
    This class represents sequence of tests for class CSTMD.
    """
    # Create an array of zeros
    frames = []
    for i in range(10) :
        frame_list.append(np.zeros([32,32]))

    # Set up initial value for the CSTMD object
    num_neurons = 2
    num_electrodes=2
    num_synapses=500
    synaptic_distance=30
    duration_per_frame=10
    description="Test"


    # Initiate the CSTMD object
    cstmd = Cstmd(num_neurons=num_neurons,
              num_synapses=num_synapses,
              synaptic_distance=synaptic_distance,
              num_electrodes=num_electrodes,
              duration=duration_per_frame,
              description=description,
              input=frames)


    # Run simulation for the empty arrray
    times, cstmd.spike_trains = cstmd.run()


    def setUp(self):
        """
        Method that runs at start of each test.
        """
        self.perc_change_acceptable=50.0

    def real_firing_rates(self,data) :
        """
        Method that calculates the firing rate of the CSTMD neurons.
        """
        fr = []
        for i in range(len(data)-4) :
            fr.append(4000.0 / (data[i+4] - data[i]))
        return fr

    def test_compFireRate(self):
        """
        Method which compares the firing rate of the CSTMD with and without
        input.
        """

        # Runs the simulation with no input
        call(["python", "example.py", "-file", "64x64_no_input_200.pkl", "-K", str(self.K), "-Na", str(self.Na)])
        with open("data.pkl", 'rb') as my_file :
            data_no_input = pickle.load(my_file)

        # Runs the simulation with some input
        call(["python", "example.py", "-file", "64x64_strong_200.pkl", "-K", str(self.K), "-Na", str(self.Na)])
        with open("data.pkl", 'rb') as my_file :
            data_input = pickle.load(my_file)

        # Gets the firing rate for each of the 2 simulations
        real_fr_no_input = self.real_firing_rates(data_no_input)
        real_fr_input = self.real_firing_rates(data_input)


        # Gets the percentage change of the firing rate range while having an input
        without_input_rng=max(real_fr_no_input)-min(real_fr_no_input)
        with_input_rng=max(real_fr_input)-min(real_fr_input)
        perc_change=100*(with_input_rng-without_input_rng)/without_input_rng

        # If the percentage change of the firing rate is greater than the
        # predicted rate then the test succeeds
        self.failUnless(perc_change>=self.perc_change_acceptable)



    def test_plot(self):
        """
        Method which checks whether the expected plots are produced.
        """
        # Retrieve scatter plot
        fig = self.dr.plot(return_fig=True)

        # If the correct type of plot is return, then the test succeeds
        self.failUnless(type(fig) is matplotlib.collections.PathCollection)


if __name__ == '__main__':
    unittest.main()


