import sympy

from Components import *

class ComponentManager(object):
    def __init__(self, sig_figs=8):
        self.components = {}
        self.SF = sig_figs

    def _add_component(self, component):
        if component.id not in self.components:
            self.components[component.id] = component
        else:
            raise ValueError("Component with id {id} already exists!".format(id=component.id))

    def solve_all(self, start_component, t=0):
        sols = solve(start_component)
        sols[sympy.symbols("t")] = t
                
        vals = {}
        for component in self.components.values():
            vals.update({component.id: component.subs(sols)})
        return vals

    def new_resistor(self, id, R=0):
        r = Resistor(id, self, R)
        self._add_component(r)
        return r

    def new_battery(self, id, V=0):
        v = Battery(id, self, V)
        self._add_component(v)
        return v

    def new_wire(self, id):
        w = Wire(id, self)
        self._add_component(w)
        return w

    def new_capacitor(self, id, C=0):
        c = Capacitor(id, self, C)
        self._add_component(c)
        return c


        
def _loop(component, traversed, start, loops):
    for node in component.outputs:
        if node == start: # made full loop
            loops.append(traversed+[component])
        if node in traversed: # already been here
            continue
        _loop(node, traversed+[component], start, loops)

def loop_law(start_component):
    """Takes start component and finds all the loops from it."""
    loops = []
    for node in start_component.outputs:
        _loop(node, [start_component], start_component, loops)
    # now convert loops to sympy equations
    loop_eqns = []
    for loop in loops:
        eqn = 0
        for node in loop:
            eqn += node.V
        loop_eqns.append(sympy.Eq(eqn))
    return loop_eqns

def _node_sum(nodes, opposite):
    s = 0
    for node in nodes:
        if len(opposite) == 1:
            s += node.I
    return s
    
def node_law(manager):
    node_eqns = []
    for component in manager.components.values():
        if not component.inputs or not component.outputs:
            node_eqns.append(component.I)
            continue
        into = _node_sum(component.inputs, component.outputs)
        outof = _node_sum(component.outputs, component.inputs)

        if into != 0:
            node_eqns.append(sympy.Eq(into, component.I))
        if outof != 0:
            node_eqns.append(sympy.Eq(component.I, outof))

    # remove duplicates
##    non_dupes = [node_eqns[0]]
##    for i in range(1, len(node_eqns)):
##        unique = True
##        for eqn in non_dupes:
##            if node_eqns[i] == eqn:
##                unique = False
##                break
##        if unique:
##            non_dupes.append(node_eqns[i])
##    return non_dupes
    return node_eqns

def _get_to_find(manager):
    to_find = []
    for component in manager.components.values():
        try:
            for item in component.solve_for:
                to_find.append(item)
        except TypeError: # not iterable
            to_find.append(component.solve_for)
    return to_find

def _get_ics(manager):
    ics = {}
    for component in manager.components.values():
        ics.update(component.initial_conditions)
    return ics

def solve(start_component):
    manager = start_component.parent
    loops = loop_law(start_component)
    nodes = node_law(manager)
    to_find = _get_to_find(manager)
    
##    print (loops+nodes)
##    print (to_find)
    sols = sympy.solve(loops+nodes, to_find)
    if not sols:
        raise ValueError("Could not find solutions. Check circuit is connected.")
    all_sols = sols.copy()
    var_sols = {}
    for key, val in list(sols.items()):
        if not isinstance(key, sympy.Function):
            var_sols[key] = sols.pop(key)
    if sols:
        ics = _get_ics(manager)
        dsols = {}
        for loop in loops:
            dsol = sympy.dsolve(loop.subs(var_sols), ics=ics)
            dsols[dsol.lhs] = dsol.rhs

        for key, val in all_sols.items():
            all_sols[key] = val.subs(dsols).doit()

    else:
        for key, val in all_sols.items():
            all_sols[key] = val.doit()
    
    return all_sols
