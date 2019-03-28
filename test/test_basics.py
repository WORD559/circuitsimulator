## Tests of basic functions

import unittest
from circuits import ComponentManager
import Components

class BasicTests(unittest.TestCase):

    def test_make_resistor(self):
        mgr = ComponentManager()
        self.assertTrue(isinstance(mgr.new_resistor("r1"), Components.Resistor))

    def test_make_battery(self):
        mgr = ComponentManager()
        self.assertTrue(isinstance(mgr.new_battery("v1"), Components.Battery))

    def test_make_wire(self):
        mgr = ComponentManager()
        self.assertTrue(isinstance(mgr.new_wire("w1"), Components.Wire))

    def test_make_capacitor(self):
        mgr = ComponentManager()
        self.assertTrue(isinstance(mgr.new_capacitor("r1"), Components.Capacitor))

    def test_disallow_duplicates(self):
        mgr = ComponentManager()
        r1 = mgr.new_resistor("r1")
        with self.assertRaises(ValueError):
            r2 = mgr.new_resistor("r1")

    def test_cannot_connect_twice(self):
        mgr = ComponentManager()
        r1 = mgr.new_resistor("r1")
        r2 = mgr.new_resistor("r2")
        r1.connect_to(r2)
        with self.assertRaise(ValueError):
            r1.connect_to(r2)
