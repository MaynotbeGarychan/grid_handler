import os

import numpy as np
from src.grid import objGrid
from math import sqrt,acosh,asinh,atanh,cosh,sinh,pi
from src.shape import shape_unit_L1L2,shape_H
import shutil
from src.make_bash import make_batch_amitex_fftp_case, make_batch_amitex_fftp_project
from src.transformation import rotation_matrix_by_raxis_angle

resolution = 128
theta = pi/4
w1 = 1.0
alpha = 1.0
beta = 0.85
L1, L2 = shape_unit_L1L2(alpha)
foci = 0.601040764008565
R1 = 0.62
R2 = sqrt(pow(R1,2)-pow(foci,2))
R3 = R1*w1
x1 = R1/L1
e = foci/R1
# decision on H
H = shape_H(R3)
# ellipse
geom = f'ellipse_x1_{x1}_e_{e}_alpha_{alpha}_theta_{theta}_W1_{w1}_resolution_{resolution}'
size = np.array([L1 * 2, L2 * 2, H * 2], dtype=float)
cells = np.array(size * resolution, dtype=int)
origin = np.array([0, 0, 0], dtype=float)
grid = objGrid(cells, size, origin)
rot_mat = rotation_matrix_by_raxis_angle([0, 0, 1], theta)
grid.crop_rotated_ellipse(size / 2, [R1, R2, R3], rot_mat, 2)
os.mkdir(f'./{geom}')
grid.output(f'./{geom}/model.vtk', 'amitex_fftp')
shutil.copy('../../xml_files/onestep/mises.xml', f'./{geom}/material.xml')
shutil.copy('../../xml_files/onestep/onestep.xml', f'./{geom}/algorithm.xml')
shutil.copy('../../xml_files/onestep/tension.xml', f'./{geom}/load.xml')
print(f'finish {geom}\n')
make_batch_amitex_fftp_case(f'./{geom}', 32)
make_batch_amitex_fftp_project('./')