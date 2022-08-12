from GridCal.Engine import *
from GridCal.Engine.IO.file_handler import FileOpen
from GridCal.Engine.Devices.enumerations import FaultType

# grid = FileOpen('IEEE30.xlsx').open()
grid = FileOpen('5bus_Saadat.xlsx').open()

pf_options = PowerFlowOptions(solver_type=SolverType.NR,  # Base method to use
                          verbose=False,  # Verbose option where available
                          tolerance=1e-6,  # power error in p.u.
                          max_iter=25,  # maximum iteration number
                          )
pf = PowerFlowDriver(grid, pf_options)
pf.run()

sc_options = ShortCircuitOptions(bus_index=[2], fault_type=FaultType.LG)
sc = ShortCircuitDriver(grid, options=sc_options, pf_options=pf_options, pf_results=pf.results)
sc.run()

print('V0: ')
print(abs(sc.results.voltage0))
print('V1: ')
print(abs(sc.results.voltage1))
print('V2: ')
print(abs(sc.results.voltage2))

print('Finished!')