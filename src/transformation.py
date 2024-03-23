import numpy as np
from math import cos,sin, atan2

def rotation_matrix_by_euler_angle(euler_angles):
    rotation_matrix = np.zeros(shape=(3,3),dtype=float)
    phi1,lphi,phi2 = euler_angles[0],euler_angles[1],euler_angles[2]
    c1 = cos(phi1)
    s1 = sin(phi1)
    c2 = cos(lphi)
    s2 = sin(lphi)
    c3 = cos(phi2)
    s3 = sin(phi2)
    rotation_matrix[0, 0] = c1 * c3- s1 * c2 * s3
    rotation_matrix[0, 1] = -c1 * s3- s1 * c2 * c3
    rotation_matrix[0, 2] = s1 * s2
    rotation_matrix[1, 0] = s1 * c3+ c1 * c2 * s3
    rotation_matrix[1, 1] = -s1 * s3+ c1 * c2 * c3
    rotation_matrix[1, 2] = -c1 * s2
    rotation_matrix[2, 0] = s2 * s3
    rotation_matrix[2, 1] = s2 * c3
    rotation_matrix[2, 2] = c2
    return rotation_matrix

def rotation_matrix_by_raxis_angle(axis,angle):
    c = np.cos(angle)
    s = np.sin(angle)
    t = 1 - c
    rotation_matrix = np.array([
        [t * axis[0] ** 2 + c, t * axis[0] * axis[1] - s * axis[2], t * axis[0] * axis[2] + s * axis[1]],
        [t * axis[0] * axis[1] + s * axis[2], t * axis[1] ** 2 + c, t * axis[1] * axis[2] - s * axis[0]],
        [t * axis[0] * axis[2] - s * axis[1], t * axis[1] * axis[2] + s * axis[0], t * axis[2] ** 2 + c]
    ])
    return rotation_matrix

def rotation_matrix_by_vector(vector):
    vector_norm = np.linalg.norm(vector)
    unit_vector = vector / vector_norm
    base_vector = np.array([1,0,0], dtype=float)
    axis = np.cross(base_vector, unit_vector)
    angle = np.arccos(np.dot(base_vector, unit_vector))
    rotation_matrix = rotation_matrix_by_raxis_angle(axis,angle)
    return rotation_matrix

def origin_point_clouds(x,y,z,center):
    x_t = x - center[0]
    y_t = y - center[1]
    z_t = z - center[2]
    return  x_t, y_t, z_t

def rotate_point_clouds(x_array,y_array,z_array,rot):
    x_array_rot = x_array * rot[0, 0] + y_array * rot[1, 0] + z_array * rot[2, 0]
    y_array_rot = x_array * rot[0, 1] + y_array * rot[1, 1] + z_array * rot[2, 1]
    z_array_rot = x_array * rot[0, 2] + y_array * rot[1, 2] + z_array * rot[2, 2]
    return x_array_rot,y_array_rot,z_array_rot

def cartesian_to_cylinder(x_array, y_array, z_array, center):
    dx = x_array - center[0]
    dy = y_array - center[1]
    r_array = np.sqrt(dx**2 + dy**2)
    theta_array = np.arctan2(dy, dx)
    cyl_z_array = z_array - center[2]
    return r_array, theta_array, cyl_z_array

def cartesian_to_cylinder_bpo(x_array, y_array, z_array, center,alpha):
    dx = x_array - center[0]
    dy = y_array - center[1]
    dy = dy * alpha
    r_array = np.sqrt(dx ** 2 + dy ** 2)
    theta_array = np.arctan2(dy, dx)
    cyl_z_array = z_array - center[2]
    return r_array, theta_array, cyl_z_array

def cartesian_to_ellipse_cylinder(x, y, z, foci):
    B = np.power(x,2) + np.power(y,2) - pow(foci,2)
    B2 = np.power(B,2)
    foci2 = pow(foci,2)
    y2 = np.power(y, 2)
    val = np.sqrt(B2 + 4 * foci2 * y2)
    p = (-B + val) / (2 * foci2)
    q = (-B - val) / (2 * foci2)
    #
    miu0 = np.arcsin(np.sqrt(p))
    miu = np.full(len(x),miu0)
    idx_list = np.where((x < 0) & (y >= 0))
    miu[idx_list] = np.pi - miu0[idx_list]
    idx_list = np.where((x <= 0) & (y < 0))
    miu[idx_list] = np.pi + miu0[idx_list]
    idx_list = np.where((x > 0) & (y < 0))
    miu[idx_list] = 2*np.pi - miu0[idx_list]
    eta = 0.5 * np.log(1 - 2 * q + 2 * np.sqrt(np.power(q, 2) - q))
    return eta, miu, z

def ellipse_to_cartersian(mu,v,foci):
    x = foci * np.cosh(mu)*np.cos(v)
    y = foci * np.sinh(mu)*np.sin(v)
    return x,y
