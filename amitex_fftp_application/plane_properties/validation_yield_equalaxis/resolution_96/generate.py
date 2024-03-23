import os

import numpy as np
from src.grid import objGrid
from math import sqrt,acosh,asinh
from src.shape import shape_unit_L1L2,shape_H
import shutil
from src.make_bash import make_batch_amitex_fftp_case, make_batch_amitex_fftp_project
from src.transformation import rotation_matrix_by_raxis_angle

resolution_list = [96]

theta = 0
alpha = 1
L1,L2 = shape_unit_L1L2(alpha)
e_list = [0.01, 0.3, 0.6, 0.8, 0.9]
x1_list = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
for k in range(len(resolution_list)):
    resolution = resolution_list[k]
    for i in range(len(e_list)):
        e = e_list[i]
        for j in range(len(x1_list)):
            x1 = x1_list[j]
            R1 = L1 * x1
            foci = R1 * e
            R2 = sqrt(pow(R1,2)-pow(foci,2))
            R3 = R2
            w1 = round(R3 / R1, 3)
            # decision on H
            H = shape_H(R3)
            # ellipse
            geom = f'eqaxellipse_x1_{x1}_e_{e}_alpha_{alpha}_theta_{theta}_W1_{w1}_resolution_{resolution}'
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
            # cylinder
            geom = f'eqaxcylinder_x1_{x1}_e_{e}_alpha_{alpha}_theta_{theta}_W1_{w1}_resolution_{resolution}'
            size = np.array([L1 * 2, L2 * 2, H * 2], dtype=float)
            cells = np.array(size * resolution, dtype=int)
            origin = np.array([0, 0, 0], dtype=float)
            grid = objGrid(cells, size, origin)
            rot_mat = rotation_matrix_by_raxis_angle([0, 0, 1], theta)
            grid.crop_rotated_cylinder(size / 2, [R1, R2], R3, rot_mat, 2, 'z')
            os.mkdir(f'./{geom}')
            grid.output(f'./{geom}/model.vtk', 'amitex_fftp')
            shutil.copy('../../xml_files/onestep/mises.xml', f'./{geom}/material.xml')
            shutil.copy('../../xml_files/onestep/onestep.xml', f'./{geom}/algorithm.xml')
            shutil.copy('../../xml_files/onestep/tension.xml', f'./{geom}/load.xml')
            print(f'finish {geom}\n')
            make_batch_amitex_fftp_case(f'./{geom}',32)

make_batch_amitex_fftp_project('./')