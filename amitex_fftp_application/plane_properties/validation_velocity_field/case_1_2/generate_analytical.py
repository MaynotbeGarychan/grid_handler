from src.velocity_field import vtk_eqstrain_rate_field_elliptic,vtk_eqstrain_rate_field_elliptic_BarriozPO
from src.shape import shape_unit_L1L2,shape_H
from math import sqrt,acosh,asinh,atanh,cosh,sinh

resolution = 128
theta = 0
w1 = 1.0
alpha = 1.7
beta = 0.3
L1, L2 = shape_unit_L1L2(alpha)
foci = 0.226903711114753
R1 = 0.3
R2 = sqrt(pow(R1,2)-pow(foci,2))
R3 = R1*w1
x1 = R1/L1
e = foci/R1
H = shape_H(R3)
D33 = 1.0
mub = 1.295773283916334
rot_angle = 0

vtk_eqstrain_rate_field_elliptic(resolution, L1, L2, R3, H, R1, R2, D33, mub, rot_angle,
                                     'analytical_grid.vtk', 'analytical_velo.vtk', 'analytical_deq.vtk', rve = 'off')
vtk_eqstrain_rate_field_elliptic_BarriozPO(resolution, L1, L2, R3, H, R1, R2, D33,
                                               'analytical_grid_bpo.vtk', 'analytical_velo_bpo.vtk', 'analytical_deq_bpo.vtk')