import os

import numpy as np
from src.grid import objGrid
from math import sqrt,acosh,asinh
from src.shape import shape_unit_L1L2,shape_H
import shutil
from src.make_bash import make_batch_amitex_fftp_case, make_batch_amitex_fftp_project
from src.transformation import rotation_matrix_by_raxis_angle
from src.make_load import make_load_amitexfftp

m = 0.1
resolution_list = [64]

theta = 0
alpha = 1
L1,L2 = shape_unit_L1L2(alpha)
e_list = [0.6]
w1_list = [0.2, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0]
x1 = 0.3
strain_list = [[1.5, 1.2, 1.0, 1.0 ,0.8, 0.8, 0.6]]
for k in range(len(resolution_list)):
    resolution = resolution_list[k]
    for i in range(len(e_list)):
        e = e_list[i]
        for j in range(len(w1_list)):
            w1 = w1_list[j]
            R1 = L1 * x1
            foci = R1 * e
            R2 = sqrt(pow(R1,2)-pow(foci,2))
            R3 = w1 * R1
            # decision on H
            H = 1.0
            # H = shape_H(R3)
            # ellipse
            geom = f'ellipse_x1_{x1}_e_{e}_alpha_{alpha}_theta_{theta}_w1_{w1}_resolution_{resolution}'
            size = np.array([L1 * 2, L2 * 2, H * 2], dtype=float)
            cells = np.array(size * resolution, dtype=int)
            origin = np.array([0, 0, 0], dtype=float)
            grid = objGrid(cells, size, origin)
            rot_mat = rotation_matrix_by_raxis_angle([0, 0, 1], theta)
            grid.crop_rotated_ellipse(size / 2, [R1, R2, R3], rot_mat, 2)
            os.mkdir(f'./{geom}')
            grid.output(f'./{geom}/model.vtk', 'amitex_fftp')
            shutil.copy(f'../../xml_files/coalescence/material_coalescence_m_{m}.xml', f'./{geom}/material.xml')
            shutil.copy('../../xml_files/coalescence/algorithm_coalescence.xml', f'./{geom}/algorithm.xml')
            # shutil.copy('../../xml_files/coalescence/load_coalescence_tension.xml', f'./{geom}/load.xml')
            strain = strain_list[i][j]
            make_load_amitexfftp(f'./{geom}/load.xml',[1],[[7,8]],['Linear',1000, strain*10000],
                                 [500, 1000], [0.0, 0.0, strain, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],[0.4, 0.4, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            print(f'finish {geom}\n')
            make_batch_amitex_fftp_case(f'./{geom}', 32)

make_batch_amitex_fftp_project('./')