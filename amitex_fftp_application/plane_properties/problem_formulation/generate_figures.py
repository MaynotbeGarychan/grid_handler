import os
import numpy as np
from src.grid import objGrid
from src.make_grid import make_grid_with_sphere_in_center,make_grid_with_ellipse_in_center, make_grid_with_cylinder_inside
from src.transformation import rotation_matrix_by_vector,rotation_matrix_by_raxis_angle
from math import pi,sqrt,pow
from src.make_bash import make_batch_amitex_fftp
from src.init import init_directory
from src.shape import shape_unit_L1L2Foci
import shutil


if __name__ == '__main__':
    init_directory(['./case_size'])

    resolution = 200
    # Size
    h = 0.25
    H = 0.5
    L1 = 0.5
    L2 = 0.5
    e = 0.8
    R1_list = [0.25,0.3,0.4]
    for i in range(len(R1_list)):
        R1 = R1_list[i]
        foci = R1*e
        R2 = sqrt(pow(R1,2)-pow(foci,2))
        R3 = R2

        geom = f'case_{i+1}'
        size = np.array([L1 * 2, L2 * 2, H * 2], dtype=float)
        cells = np.array(size * resolution, dtype=int)
        origin = np.array([0, 0, 0], dtype=float)
        grid = objGrid(cells, size, origin)
        grid.crop_ellipse(size/2,[R1,R2,R3],2)
        grid.output(f'./case_size/{geom}.vtk', 'amitex_fftp')