## Simple parallel tests

import unittest
from circuits import ComponentManager

class ParallelTests(unittest.TestCase):

    def test_two_same_R_voltage(self):
        mgr = ComponentManager()
        v1 = mgr.new_battery("v1")
        v1.set_voltage(12)
        r1 = mgr.new_resistor("r1")
        r1.R = 12
        r2 = mgr.new_resistor("r2")
        r2.R = 12
        v1.connect_to(r1)
        v1.connect_to(r2)
        r1.connect_to(v1)
        r2.connect_to(v1)
        sols = mgr.solve_all(v1)

        self.assertEqual(sols["v1"]["V"], 12)
        self.assertEqual(sols["r1"]["V"], 12)
        self.assertEqual(sols["r2"]["V"], 12)

    def test_two_same_R_current(self):
        mgr = ComponentManager()
        v1 = mgr.new_battery("v1")
        v1.set_voltage(12)
        r1 = mgr.new_resistor("r1")
        r1.R = 12
        r2 = mgr.new_resistor("r2")
        r2.R = 12
        v1.connect_to(r1)
        v1.connect_to(r2)
        r1.connect_to(v1)
        r2.connect_to(v1)
        sols = mgr.solve_all(v1)
        print(sols)

        self.assertEqual(sols["v1"]["I"], 2)
        self.assertEqual(sols["r1"]["I"], 1)
        self.assertEqual(sols["r2"]["I"], 1)
        
        
