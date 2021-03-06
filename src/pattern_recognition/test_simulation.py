__author__ = 'juancarlosfarah'

import unittest
import math

from pattern_recognition.simulation import Simulation
from pattern_recognition.sample import Sample
import numpy as np


class SimulationTests(unittest.TestCase):

    def setUp(self):
        """
        Creates a Simulation to test on.
        :return: None.
        """
        # Generate Simulation
        self.simulation = Simulation()

    def test_load_file(self):
        """
        Tests if Simulation loads a file containing sample spike trains.
        """
        sim = self.simulation
        sim.load_file("sample", folder="test/", extension=".npz")

        p = np.load("test/sample.npz")
        st = p['spike_trains']
        d = p['pattern_duration']

        # Test assertions.
        self.failUnless((sim.spike_trains == st).all())
        self.failUnless((sim.start_positions == p['start_positions']).all())
        self.failUnless(sim.pattern_duration == d)
        self.failUnless(sim.num_afferents == st.shape[0])
        self.failUnless(sim.duration == st.shape[1])
        self.failUnless(sim.sampling_interval == math.ceil(st.shape[1] / 5))

    def test_load(self):
        """
        Tests if Simulation loads a sample containing spike trains.
        """

        sim = self.simulation

        # Generate Sample
        sample_duration = 1000
        num_neurons = 500
        s = Sample(sample_duration, num_neurons=num_neurons)
        
        sim.load(s)

        # Test assertions.
        self.failUnless((sim.spike_trains == s.spike_trains).all())
        self.failUnless(sim.start_positions == s.start_positions)
        self.failUnless(sim.pattern_duration == s.pattern_duration)
        self.failUnless(sim.num_afferents == s.spike_trains.shape[0])
        self.failUnless(sim.duration == s.spike_trains.shape[1])
        self.failUnless(sim.sampling_interval == math.ceil(sim.duration / 5))

    def test_general_test(self):
        """
        One mothafacka test to rule them all.

        :return:
        """

        sim = Simulation()
        sim.load_file("sample")
        n1 = sim.add_neuron(0.03125, .95, 300)
        sim.run()
        sim.plot_weight_distributions()
        sim.plot_membrane_potential()

    def tearDown(self):
        """
        Resets the sample for the tests.
        :return:
        """
        self.simulation = None


def main():
    unittest.main()

if __name__ == '__main__':
    main()
