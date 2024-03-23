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
    init_directory(['./load', './material', './model', './algorithm'])
    shutil.copy('../xml_files/load_tensionx_finite_strain.xml', './load')
    shutil.copy('../xml_files/material_porous_finite_strain_flab20ex.xml', './material')
    shutil.copy('../xml_files/algorithm_finite_strain.xml', './algorithm')

    # calculation
    resolution = 200
    alpha = 1.5
    beta = 0.4
    L1,L2,foci = shape_unit_L1L2Foci(alpha, beta)
    rot = pi/4
    H = 0.5
    h = 0.25
    R1 = 0.35
    R2 = sqrt(pow(R1,2)-pow(foci,2))
    R3 = R2

    geom = 'case'
    size = np.array([L1*2, L2*2, H*2], dtype=float)
    cells = np.array(size*resolution, dtype=int)
    origin = np.array([0, 0, 0], dtype=float)
    grid = objGrid(cells, size, origin)
    rot_mat = rotation_matrix_by_raxis_angle([0,0,1],rot)
    grid.crop_rotated_ellipse(size/2, [R1,R2,R3],rot_mat,2)
    grid.output(f'./model/{geom}.vtk', 'amitex_fftp')

    make_batch_amitex_fftp('./load', './model', './material',
                           './algorithm', 'run.sh', 32)