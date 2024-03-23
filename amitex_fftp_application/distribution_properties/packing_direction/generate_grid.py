import os
import numpy as np
from src.grid import objGrid
import shutil
from src.make_bash import make_batch_amitex_fftp_case, make_batch_amitex_fftp_project
from src.make_bash import make_batch_win2unix
# make grid
resolution = 50
num = 3
l = 0.5
L1 = l*num
L2 = l*num
L3 = l*num
size = np.array([L1 * 2, L2 * 2, L3 * 2], dtype=float)
cells = np.array(size * resolution, dtype=int)
origin = np.array([0, 0, 0], dtype=float)
grid = objGrid(cells, size, origin)

# crop damage
center_list = [[0.5,0.5,1.5],[0.5,1.5,1.5],[0.5,2.5,1.5],
               [1.5,0.5,1.5],[1.5,1.5,1.5],[1.5,2.5,1.5],
               [2.5,0.5,1.5],[2.5,1.5,1.5],[2.5,2.5,1.5]]
v_radius = 0.3
radius_list = [v_radius]*9
grid.crop_multi_spheres(center_list,radius_list,2)

geom = f'distribution_r_{v_radius}_resolution_{resolution}'
os.mkdir(f'./{geom}')
grid.output(f'./{geom}/model.vtk', 'amitex_fftp')
shutil.copy('../../../xml_files/onestep/material/mises.xml', f'./{geom}/material.xml')
shutil.copy('../../../xml_files/onestep/algorithm_onestep.xml', f'./{geom}/algorithm.xml')
shutil.copy('../../../xml_files/onestep/load_onestep_tension.xml', f'./{geom}/load.xml')
print(f'finish {geom}\n')
make_batch_amitex_fftp_case(f'./{geom}', 32)
make_batch_win2unix(f'./{geom}/run.sh')
make_batch_amitex_fftp_project('./')
make_batch_win2unix(f'./run_all.sh')