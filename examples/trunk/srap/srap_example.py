import os
from GridCalEngine.api import FileOpen
from GridCalEngine.Simulations.ContingencyAnalysis.contingency_analysis_driver import (ContingencyAnalysisOptions,
                                                                                       ContingencyAnalysisDriver)
from GridCalEngine.enumerations import EngineType, ContingencyEngine

path = "/home/santi/Escritorio/Redes/15_Caso_2026.gridcal"

print('Loading grical circuit... ', sep=' ')
grid = FileOpen(path).open()

print("Running contingency analysis...")
con_options = ContingencyAnalysisOptions()
con_options.use_srap = True
con_options.engine = ContingencyEngine.PTDF

con_drv = ContingencyAnalysisDriver(grid=grid,
                                    options=con_options,
                                    engine=EngineType.GridCal)

con_drv.run()

print(f"Elapsed: {con_drv.elapsed} s")

print(con_drv.results.report.get_data())

print('Done!')
