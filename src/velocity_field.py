import numpy as np
import numpy.linalg

from src.grid import objGrid
from src.transformation import (cartesian_to_cylinder,cartesian_to_ellipse_cylinder, rotation_matrix_by_raxis_angle,
                                origin_point_clouds, rotate_point_clouds, cartesian_to_cylinder_bpo)
from math import acosh,cosh,sqrt,asinh
from src.shape import cal_miub
from src.vtk_processor import write_vtk_vector_field,write_vtk_scalar_field
from math import pi

def cal_velocity_field_ricetracey(x_array, y_array, z_array, phase_id_array, center, c, h, D33, L):
    r_array, theta_array, cyl_z_array = cartesian_to_cylinder(x_array, y_array, z_array, center)
    # init
    vr_array = np.zeros_like(x_array)
    vz_array = np.zeros_like(x_array)
    vx_array = np.zeros_like(x_array)
    vy_array = np.zeros_like(x_array)
    deq  = np.zeros_like(x_array)
    # conduct calculation if phase_id is 1
    mask = np.where((phase_id_array == 1) & (np.abs(cyl_z_array) < h) & (r_array<L))
    # mask = np.where(phase_id_array == 1)
    # Calculate vr and vz only for the filtered points
    vr_array[mask] = (1 / (2 * c)) * D33 * (pow(L, 2) / r_array[mask] - r_array[mask])
    vz_array[mask] = (1 / c) * D33 * cyl_z_array[mask]
    # Calculate vx and vy from vr
    vx_array[mask] = vr_array[mask] * np.cos(theta_array[mask])
    vy_array[mask] = vr_array[mask] * np.sin(theta_array[mask])
    deq[mask] = D33 / sqrt(3) / c * np.sqrt(3 + pow(L, 4) / np.power(r_array[mask], 4))
    return vx_array, vy_array, vz_array, deq

def cal_strain_rate_field_ricetracey(x_array, y_array, z_array, phase_id_array, center, c, h, D33, L):
    r_array, theta_array, cyl_x_array = cartesian_to_cylinder(x_array, y_array, z_array, center)
    # init
    # drr_array = np.zeros_like(y_array)
    # conduct calculation if phase_id is 1
    mask = np.where((phase_id_array == 1) & (np.abs(cyl_x_array) < h))
    # calculation the strain rate field
    dyy_array = np.zeros_like(y_array)
    dzz_array = np.zeros_like(y_array)
    dxx_array = np.zeros_like(x_array)
    r2_array = r_array * r_array
    dyy_array[mask] = D33/(2*c)*(-pow(L,2)/r2_array[mask]-1)
    dzz_array[mask] = D33/(2*c)*(-pow(L,2)/r2_array[mask]-1)
    dxx_array[mask] = D33/c
    return dxx_array,dyy_array,dzz_array

def cal_velocity_field_barriozpo(x_array, y_array, z_array, phase_id_array, center, alpha, c, h, D33, L1):
    cyl_x_array = x_array - center[0]
    cyl_y_array = y_array - center[1]
    cyl_z_array = z_array - center[2]
    #
    vz_array = np.zeros_like(z_array)
    vx_array = np.zeros_like(x_array)
    vy_array = np.zeros_like(y_array)
    # conduct calculation if phase_id is 1
    mask = np.where((phase_id_array == 1) & (np.abs(cyl_x_array) < h))
    #
    cyl_y2_array = cyl_y_array * cyl_y_array
    cyl_z2_array = cyl_z_array * cyl_z_array
    var_array = pow(L1,2)/(cyl_y2_array + pow(alpha,2) * cyl_z2_array)
    vy_array[mask] = D33 / 2 / c * (var_array[mask] - 1) * cyl_y_array[mask]
    vz_array[mask] = D33 / 2 / c * (var_array[mask] - 1) * cyl_z_array[mask]
    vx_array[mask] = D33 / c * cyl_x_array[mask]
    return vx_array, vy_array, vz_array

def cal_velocity_field_elliptic(x_array,y_array,z_array,phase_id_array,center, foci, c, h, D33, L):
    eta, miu, z = cartesian_to_ellipse_cylinder(x_array, y_array, z_array, center, foci)
    # init
    vx = np.zeros_like(x_array)
    vy = np.zeros_like(y_array)
    vz = np.zeros_like(z_array)
    veta = np.zeros_like(x_array)
    # conduct calculation if phase_id is 1
    idx = np.where((phase_id_array == 1) & (np.abs(z) < h))
    L2 = pow(acosh(L/foci),2)
    veta[idx] = D33 / 2 / c * (L2 / eta[idx] - eta[idx])
    vx[idx] = foci * np.cosh(veta[idx]) * np.cos(miu[idx])
    vy[idx] = foci * np.sinh(veta[idx]) * np.sin(miu[idx])
    vz[idx] = D33 / c * z[idx]
    return vx,vy,vz,veta

def vtk_eqstrain_rate_field_elliptic(resolution, L1, L2, h, H, R1, R2, D33, mub, rot_angle,
                                     save_dir_grid, save_dir_velo, save_dir_deq, periodic = 'off'):
    # init some parameter
    foci = sqrt(pow(R1,2)-pow(R2,2))
    c = h/H
    # sphere_w_resolution_32_m_0.1 grid and output
    size = np.array([2 * L1, 2 * L2, 2 * H], dtype=float)
    cells = np.array(size * resolution, dtype=int)
    grid = objGrid(cells, size, [0, 0, 0])
    rot_mat = rotation_matrix_by_raxis_angle([0,0,1],rot_angle)
    grid.crop_rotated_cylinder(size/2,[R1, R2], h,rot_mat,2, 'z')
    mat_id = np.zeros_like(grid.x_array)
    void_idx = np.where(grid.phase_id_array == 2)
    mat_id[void_idx] = 1.0
    write_vtk_scalar_field(save_dir_grid, cells, mat_id)
    # sphere_w_resolution_32_m_0.1 field and vector
    x, y, z = origin_point_clouds(grid.x_array, grid.y_array, grid.z_array, size / 2)
    # xr, yr, zr = rotate_point_clouds(x, y, z, rot_mat)
    vx,vy,vz,deq = cal_eqstrain_rate_field_elliptic(x, y, z, grid.phase_id_array, foci, c, h, D33, mub, rot_mat, L1, L2,
                                                    periodic)
    rot_mat_inv = numpy.linalg.inv(rot_mat)
    vxr, vyr, vzr = rotate_point_clouds(vx, vy, vz, rot_mat_inv)
    write_vtk_vector_field(save_dir_velo, cells, vxr, vyr, vzr)
    write_vtk_scalar_field(save_dir_deq, cells, deq)

def cal_eqstrain_rate_field_elliptic(x_array, y_array, z_array, phase_id_array, foci, c, h, D33, miub, rot_mat, L1, L2,
                                     periodic = 'off'):
    xr, yr, zr = rotate_point_clouds(x_array, y_array, z_array, rot_mat)
    # obtain elliptic cylindrical coordinates system
    miu, v, z = cartesian_to_ellipse_cylinder(xr, yr, zr, foci)
    # init
    vx = np.zeros_like(x_array)
    vy = np.zeros_like(y_array)
    vz = np.zeros_like(z_array)
    vmiu = np.zeros_like(x_array)
    deq = np.zeros_like(x_array)
    # select the ligament index
    idx = np.where((phase_id_array == 1) & (np.abs(z) < h) & (miu < miub))
    # calculate field and vector
    vmiu[idx] = D33 / 2 / c * (pow(miub,2) / miu[idx] - miu[idx])
    vx[idx] = foci * np.cos(v[idx]) * np.sinh(miu[idx]) * vmiu[idx]
    vy[idx] = foci * np.sin(v[idx]) * np.cosh(miu[idx]) * vmiu[idx]
    vz[idx] = D33 / c * z[idx]
    deq[idx] = D33 / sqrt(3) / c * np.sqrt(3 + pow(miub, 4) / np.power(miu[idx], 4))
    # exterior region
    if periodic == 'on':
        # 1
        x = np.array(x_array)
        y = np.array(y_array)
        x = x + 2 * L1
        xr, yr, zr = rotate_point_clouds(x, y, z, rot_mat)
        miu, v, z = cartesian_to_ellipse_cylinder(xr, yr, zr, foci)
        idx = np.where((phase_id_array == 1) & (np.abs(z) < h) & (miu < miub))
        deq[idx] = D33 / sqrt(3) / c * np.sqrt(3 + pow(miub, 4) / np.power(miu[idx], 4))

        x = np.array(x_array)
        y = np.array(y_array)
        x = x - 2 * L1
        xr, yr, zr = rotate_point_clouds(x, y, z, rot_mat)
        miu, v, z = cartesian_to_ellipse_cylinder(xr, yr, zr, foci)
        idx = np.where((phase_id_array == 1) & (np.abs(z) < h) & (miu < miub))
        deq[idx] = D33 / sqrt(3) / c * np.sqrt(3 + pow(miub, 4) / np.power(miu[idx], 4))

        x = np.array(x_array)
        y = np.array(y_array)
        y = y + 2 * L2
        xr, yr, zr = rotate_point_clouds(x, y, z, rot_mat)
        miu, v, z = cartesian_to_ellipse_cylinder(xr, yr, zr, foci)
        idx = np.where((phase_id_array == 1) & (np.abs(z) < h) & (miu < miub))
        deq[idx] = D33 / sqrt(3) / c * np.sqrt(3 + pow(miub, 4) / np.power(miu[idx], 4))

        x = np.array(x_array)
        y = np.array(y_array)
        y = y - 2 * L2
        xr, yr, zr = rotate_point_clouds(x, y, z, rot_mat)
        miu, v, z = cartesian_to_ellipse_cylinder(xr, yr, zr, foci)
        idx = np.where((phase_id_array == 1) & (np.abs(z) < h) & (miu < miub))
        deq[idx] = D33 / sqrt(3) / c * np.sqrt(3 + pow(miub, 4) / np.power(miu[idx], 4))
    return vx,vy,vz,deq


def vtk_eqstrain_rate_field_elliptic_BarriozPO(resolution, L1, L2, h, H, R1, R2, D33,
                                               save_dir_grid, save_dir_velo, save_dir_deq):
    # sphere_w_resolution_32_m_0.1 grid1
    size = np.array([2 * L1, 2 * L2, 2 * H], dtype=float)
    cells = np.array(size * resolution, dtype=int)
    grid = objGrid(cells, size, [0, 0, 0])
    grid.crop_cylinder(size / 2, [R1, R2], h, 2, 'z')
    mat_id = np.zeros_like(grid.x_array)
    void_idx = np.where(grid.phase_id_array == 2)
    mat_id[void_idx] = 1.0
    write_vtk_scalar_field(save_dir_grid, cells, mat_id)
    # init
    center = size/2
    alpha = L1/L2
    r,theta,z = cartesian_to_cylinder_bpo(grid.x_array, grid.y_array, grid.z_array, center, alpha)
    dist2_ref = pow(L1,2) * np.power(np.cos(theta),2) + pow(L2,2) * np.power(np.sin(theta),2)
    x = grid.x_array - center[0]
    y = grid.y_array - center[1]
    z = grid.z_array - center[2]
    vx = np.zeros_like(grid.x_array)
    vy = np.zeros_like(grid.y_array)
    vz = np.zeros_like(grid.z_array)
    deq = np.zeros_like(grid.x_array)
    temp = np.zeros_like(grid.x_array)
    temp2 = np.zeros_like(grid.x_array)
    temp3 = np.zeros_like(grid.x_array)
    # geometric parameters
    c = h/H
    alpha = L1/L2
    const = D33/2/c
    # velocity field
    x2 = np.power(x, 2)
    y2 = np.power(y, 2)
    dist2 = x2 + y2
    idx = np.where((grid.phase_id_array == 1) & (np.abs(z) < h) & (dist2 < dist2_ref))
    vx[idx] = const * (pow(L1, 2) / (x2[idx] + pow(alpha, 2) * y2[idx]) - 1) * x[idx]
    vy[idx] = const * (pow(L1, 2) / (x2[idx] + pow(alpha, 2) * y2[idx]) - 1) * y[idx]
    vz[idx] = const * 2 * z[idx]
    write_vtk_vector_field(save_dir_velo, cells, vx,vy,vz)
    # equivalent strain rate field
    temp[idx] = (pow(alpha,2)-1)/(2*alpha) * np.sin(2*theta[idx])
    temp2[idx] = 1+np.power(temp[idx],2)
    temp3[idx] = 1+pow(L1,4)/(3*pow(r[idx],4))*temp2[idx]
    deq[idx] = abs(D33)/c * np.sqrt(temp3[idx])
    write_vtk_scalar_field(save_dir_deq, cells, deq)


if __name__ == "__main__":
    save_grid = '/home/chen/Desktop/research_progress/project_1/velocity_field/bpo_grid.vtk'
    save_velo = '/home/chen/Desktop/research_progress/project_1/velocity_field/bpo_velo.vtk'
    save_deq = '/home/chen/Desktop/research_progress/project_1/velocity_field/bpo_deq.vtk'
    # vtk_eqstrain_rate_field_elliptic(200, 0.5, 0.5, 0.25, 0.5, 0.4, 0.2, 1, 1.2156,
    #                                  pi/4, save_grid, save_velo, save_deq)
    vtk_eqstrain_rate_field_elliptic(100, 0.5, 0.5, 0.25, 0.5, 0.4, 0.1, 1, 0.902061969321513,
                                     pi/6, save_grid, save_velo, save_deq)
    # vtk_eqstrain_rate_field_elliptic_BarriozPO(100, 0.5,0.5,0.25,0.5,0.4,0.2,1,
    #                                            save_grid,save_velo,save_deq)