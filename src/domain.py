from numpy import power, sum, where, abs, where
from src.transformation import rotate_point_clouds,origin_point_clouds

def chk_sphere_domain(x_arr, y_arr, z_arr, center, radius):
    dist_array_2 = power(x_arr - center[0], 2) + power(y_arr - center[1], 2) + power(z_arr - center[2], 2)
    thres = radius ** 2
    condition_array = dist_array_2 < thres
    return condition_array

def chk_ellipse_domain(x_arr, y_arr, z_arr, center, radius, rot_bool = False, rot = None):
    a2, b2, c2 = radius[0] ** 2, radius[1] ** 2, radius[2] ** 2
    if rot_bool == True:
        x_arr_rot, y_arr_rot, z_arr_rot = rotate_point_clouds(x_arr - center[0], y_arr - center[1], z_arr - center[2],
                                                              rot)
        dist_array_2 = (x_arr_rot - center[0]) ** 2 / a2 + (y_arr_rot - center[1]) ** 2 / b2 + (
                    z_arr_rot - center[2]) ** 2 / c2
    else:
        dist_array_2 = (x_arr - center[0]) ** 2 / a2 + (y_arr - center[1]) ** 2 / b2 + (z_arr - center[2]) ** 2 / c2
    condition_array = dist_array_2 < 1
    return condition_array

def chk_cylinder_domain(x_arr, y_arr, z_arr, center, radius, height, rot_bool = False, rot = None):
    height_array = abs(z_arr - center[2])
    if rot_bool == True:
        x_array_origin_rot, y_array_origin_rot, z_array_origin_rot = (
            rotate_point_clouds(x_arr - center[0], y_arr - center[1], z_arr - center[2], rot))
        dist_array_2 = x_array_origin_rot ** 2 / (radius[0] ** 2) + y_array_origin_rot ** 2 / (radius[1] ** 2)
    else:
        dist_array_2 = (x_arr - center[0]) ** 2 / (radius[0] ** 2) + (y_arr - center[1]) ** 2 / (
                radius[1] ** 2)
    condition_array = (height_array < height) & (dist_array_2 < 1)
    return condition_array