import sympy

class Component(object):
    def __init__(self, id, parent):
        self.id = id
        self.parent = parent
        
        self.inputs = []
        self.outputs = []

    def connect_to(self, component):
        """Connects "out" side of this component to the "in" side of other component"""
        if component not in self.outputs:
            self.outputs.append(component)
            component._be_connected(self)
        else:
            raise ValueError("Components already connected")

    def _be_connected(self, by):
        if by not in self.inputs:
            self.inputs.append(by)
        else:
            raise ValueError("Component already feeds into this component")

    @property
    def solve_for(self):
        return []

    @property
    def initial_conditions(self):
        return {}

class Resistor(Component):
    def __init__(self, id, parent):
        super().__init__(id, parent)

        self._R = sympy.symbols("R_{"+self.id+"}")
        self._I = sympy.symbols("I_{"+self.id+"}")
        self._V = self._I*self._R
        self.R = 0

    @property
    def V(self):
        return self._V.subs({self._R:self.R})

    @property
    def I(self):
        return self._I

    @property
    def solve_for(self):
        return self._I

    def subs(self, solutions):
        return {"V": round(self.V.subs(solutions), self.parent.DP),
                "I": round(self._I.subs(solutions), self.parent.DP),
                "R": round(self.R, self.parent.DP)}

    def __repr__(self):
        return __name__+".Resistor(id="+str(self.id)+",R="+str(self.R)+")"

class Battery(Component):
    def __init__(self, id, parent):
        super().__init__(id, parent)

        self.R = 0
        self._I = sympy.symbols("I_{"+self.id+"}")
        self._V = 0

        # direction determines voltage sign
        # 1:  input = -ve, output = +ve
        # -1: input = +ve, output = -ve
        self.direction = 1

    def reverse_battery(self):
        self.direction *= -1

    def set_voltage(self, V):
        self._V = V

    @property
    def I(self):
        return self._I

    @property
    def V(self):
        return self._V*(self.direction*-1)

    @property
    def solve_for(self):
        return self._I

    def subs(self, solutions):
        return {"V":round(self.V*(-1), self.parent.DP),
                "I":round(self._I.subs(solutions), self.parent.DP),
                "R":round(self.R, self.parent.DP),}

class Wire(Resistor):
    pass

class Capacitor(Component):
    def __init__(self, id, parent):
        super().__init__(id, parent)

        self.C = 0
        self.V_0 = 0
        self._t = sympy.symbols("t")
        self._C = sympy.symbols("C_{"+self.id+"}")
        self._V = sympy.Function("V_{"+self.id+"}")(self._t)
        self._I = self._C*self._V.diff(self._t)
        self._Q = self._C*self._V

    @property
    def R(self):
        return 0

    @property
    def I(self):
        return self._I.subs({self._C: self.C})

    @property
    def V(self):
        return self._V

    @property
    def Q(self):
        return self._Q.subs({self._C: self.C})

    @property
    def solve_for(self):
        return self.V

    @property
    def initial_conditions(self):
        return {self.V.subs({self._t:0}): self.V_0}

    def subs(self, solutions):
        return {"V":round(self.V.subs(solutions).doit(), self.parent.DP),
                "I":round(self.I.subs(solutions).doit(), self.parent.DP),
                "R":round(self.R, self.parent.DP),}
