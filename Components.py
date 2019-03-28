import sympy

def symround(x, sf=1):
    return sympy.N(x, sf)
##    if isinstance(x, (int, float)):
##        return round(x, dp)
##    else:
##        try:
##            if x.free_symbols:
##                return x
##        except AttributeError:
##            try:
##                return round(x, dp)
##            except TypeError:
##                return x

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
    def __init__(self, id, parent, R=0):
        super().__init__(id, parent)

        self._R = sympy.symbols("R_{"+self.id+"}")
        self._I = sympy.symbols("I_{"+self.id+"}")
        self._V = self._I*self._R
        self.R = R

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
        return {"V": symround(self.V.subs(solutions), self.parent.SF),
                "I": symround(self._I.subs(solutions), self.parent.SF),
                "R": symround(self.R, self.parent.SF)}

    def __repr__(self):
        return "<"+__name__+".Resistor(id='"+str(self.id)+"',R="+str(self.R)+")>"

class Battery(Component):
    def __init__(self, id, parent, V):
        super().__init__(id, parent)

        self.R = 0
        self._I = sympy.symbols("I_{"+self.id+"}")
        self._V = V

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
        return {"V":symround(self.V*(-1), self.parent.SF),
                "I":symround(self._I.subs(solutions), self.parent.SF),
                "R":symround(self.R, self.parent.SF),}

    def __repr__(self):
        direction = "normal" if self.direction == 1 else "reversed"
        return "<"+__name__+".Battery(id='"+str(self.id)+"',V="+str(self.V)+","+direction+")>"

class Wire(Resistor):
    def __repr__(self):
        return "<"+__name__+".Wire(id='"+str(self.id)+"')>"

class Capacitor(Component):
    def __init__(self, id, parent, C):
        super().__init__(id, parent)

        self.C = C
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
        return {"V":symround(self.V.subs(solutions).doit(), self.parent.SF),
                "I":symround(self.I.subs(solutions).doit(), self.parent.SF),
                "R":symround(self.R, self.parent.SF),
                "Q":symround(self.Q, self.parent.SF)}

    def __repr__(self):
        return "<"+__name__+".Capacitor(id='"+str(self.id)+"',C="+str(self.C)+",V_0="+str(self.V_0)+")>"
