## Simple series tests

import unittest
from circuits import ComponentManager

class SeriesTests(unittest.TestCase):

    def test_one_resistor_voltage(self):
        mgr = ComponentManager()
        v1 = mgr.new_battery("v1")
        v1.set_voltage(12)
        r1 = mgr.new_resistor("r1")
        r1.R = 10
        v1.connect_to(r1)
        r1.connect_to(v1)
        sols = mgr.solve_all(v1)

        self.assertEqual(sols["v1"]["V"], 12)
        self.assertEqual(sols["r1"]["V"], 12)

    def test_one_resistor_current(self):
        mgr = ComponentManager()
        v1 = mgr.new_battery("v1")
        v1.set_voltage(12)
        r1 = mgr.new_resistor("r1")
        r1.R = 10
        v1.connect_to(r1)
        r1.connect_to(v1)
        sols = mgr.solve_all(v1)

        self.assertEqual(sols["v1"]["I"], 1.2)
        self.assertEqual(sols["r1"]["I"], 1.2)

    def test_three_resistor_voltage(self):
        mgr = ComponentManager()
        v1 = mgr.new_battery("v1", 12)
        r1 = mgr.new_resistor("r1", 10)
        r2 = mgr.new_resistor("r2", 20)
        r3 = mgr.new_resistor("r3", 30)
        v1.connect_to(r1)
        r1.connect_to(r2)
        r2.connect_to(r3)
        r3.connect_to(v1)
        sols = mgr.solve_all(v1)

        self.assertEqual(sols["v1"]["V"], 12)
        self.assertEqual(sols["r1"]["V"], 2)
        self.assertEqual(sols["r2"]["V"], 4)
        self.assertEqual(sols["r3"]["V"], 6)

    def test_three_resistor_current(self):
        mgr = ComponentManager()
        v1 = mgr.new_battery("v1", 12)
        r1 = mgr.new_resistor("r1", 10)
        r2 = mgr.new_resistor("r2", 20)
        r3 = mgr.new_resistor("r3", 30)
        v1.connect_to(r1)
        r1.connect_to(r2)
        r2.connect_to(r3)
        r3.connect_to(v1)
        sols = mgr.solve_all(v1)

        self.assertEqual(sols["v1"]["I"], 0.2)
        self.assertEqual(sols["r1"]["I"], 0.2)
        self.assertEqual(sols["r2"]["I"], 0.2)
        self.assertEqual(sols["r3"]["I"], 0.2)
        
