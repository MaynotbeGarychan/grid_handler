import multiprocessing

import numpy as np
import struct
# import damask
from src.transformation import rotation_matrix_by_euler_angle
from src.transformation import rotate_point_clouds
from src.domain import chk_sphere_domain, chk_ellipse_domain, chk_cylinder_domain
from math import pi

class objGrid(object):
    x_array = np.array(0)
    y_array = np.array(0)
    z_array = np.array(0)
    phase_id_array = np.array(0)
    origin = np.array(0)
    cells = np.array(0)
    size = np.array(0)
    spacing = np.array(0)
    num_points = 0
    unit_dist = 0
    periodic = False
    x_array_periodic = np.array(0)
    y_array_periodic = np.array(0)
    z_array_periodic = np.array(0)
    phase_id_array_periodic = np.array(0)

    def __init__(self,cells,size,origin):
        self.origin = np.zeros(shape=3, dtype=float)
        self.cells = np.zeros(shape=3, dtype=int)
        self.size = np.zeros(shape=3, dtype=float)
        self.spacing = np.zeros(shape=3, dtype=float)
        self.origin = origin
        self.size = size
        self.cells = cells
        self.num_points = cells[0] * cells[1] * cells[2]
        self.phase_id_array = np.ones(shape=self.num_points, dtype=int)
        self.spacing[0] = size[0] / cells[0]
        self.spacing[1] = size[1] / cells[1]
        self.spacing[2] = size[2] / cells[2]

        self.x_array = np.zeros(shape=self.num_points, dtype=float)
        self.y_array = np.zeros(shape=self.num_points, dtype=float)
        self.z_array = np.zeros(shape=self.num_points, dtype=float)
        pos = 0
        for k in range(cells[2]):
            for j in range(cells[1]):
                for i in range(cells[0]):
                    self.x_array[pos] = i * self.spacing[0]
                    self.y_array[pos] = j * self.spacing[1]
                    self.z_array[pos] = k * self.spacing[2]
                    pos = pos + 1

#   periodic
    def init_periodic(self):
        self.periodic = True
        # x
        self.x_array_periodic = np.concatenate((self.x_array, self.x_array + self.size[0]))
        self.y_array_periodic = np.concatenate((self.y_array, self.y_array))
        self.z_array_periodic = np.concatenate((self.z_array, self.z_array))
        self.x_array_periodic = np.concatenate((self.x_array_periodic, self.x_array - self.size[0]))
        self.y_array_periodic = np.concatenate((self.y_array_periodic, self.y_array))
        self.z_array_periodic = np.concatenate((self.z_array_periodic, self.z_array))
        # y
        self.x_array_periodic = np.concatenate((self.x_array_periodic, self.x_array))
        self.y_array_periodic = np.concatenate((self.y_array_periodic, self.y_array + self.size[1]))
        self.z_array_periodic = np.concatenate((self.z_array_periodic, self.z_array))
        self.x_array_periodic = np.concatenate((self.x_array_periodic, self.x_array))
        self.y_array_periodic = np.concatenate((self.y_array_periodic, self.y_array - self.size[1]))
        self.z_array_periodic = np.concatenate((self.z_array_periodic, self.z_array))
        # z
        self.x_array_periodic = np.concatenate((self.x_array_periodic, self.x_array))
        self.y_array_periodic = np.concatenate((self.y_array_periodic, self.y_array))
        self.z_array_periodic = np.concatenate((self.z_array_periodic, self.z_array + self.size[2]))
        self.x_array_periodic = np.concatenate((self.x_array_periodic, self.x_array))
        self.y_array_periodic = np.concatenate((self.y_array_periodic, self.y_array))
        self.z_array_periodic = np.concatenate((self.z_array_periodic, self.z_array - self.size[2]))
        # phase_id
        self.phase_id_array_periodic = np.ones(shape=self.num_points*7, dtype=int)

    def crop_periodic_phase(self, condition_array_total, damage_id):
        temp_arr = condition_array_total.reshape((7, self.num_points))
        summed_array = np.sum(temp_arr, axis=0)
        self.phase_id_array = np.where(summed_array != 0, damage_id, self.phase_id_array)

#   crop single damage
    def crop_sphere(self,center,radius,sphere_id):
        condition_array = chk_sphere_domain(self.x_array,self.y_array,self.z_array,center,radius)
        self.phase_id_array = np.where(condition_array, sphere_id, self.phase_id_array)

    def crop_ellipse(self,center,radius,in_ellipse_id):
        condition_array = chk_ellipse_domain(self.x_array,self.y_array,self.z_array, center, radius)
        self.phase_id_array = np.where(condition_array, in_ellipse_id, self.phase_id_array)

    def crop_rotated_ellipse(self,center,radius,rot,in_ellipse_id):
        condition_array = chk_ellipse_domain(self.x_array,self.y_array,self.z_array, center, radius, True, rot)
        self.phase_id_array = np.where(condition_array, in_ellipse_id, self.phase_id_array)

    def crop_cylinder(self,center,radius,height,in_cylinder_id, axis_option = 'x'):
        condition_array = chk_cylinder_domain(self.x_array, self.y_array, self.z_array, center, radius, height)
        self.phase_id_array = np.where(condition_array, in_cylinder_id, self.phase_id_array)

    # def crop_cylinder_outside_frictive(self,center,radius,out_cylinder_id):
    #     x_array_origin = self.x_array - center[0]
    #     y_array_origin = self.y_array - center[1]
    #     z_array_origin = self.z_array - center[2]
    #     dist_array_2 = np.power(x_array_origin,2) / (radius[0] ** 2) + np.power(y_array_origin,2) / (radius[1] ** 2)
    #     idx_list = np.where(dist_array_2 > 1)
    #     self.phase_id_array[idx_list] = out_cylinder_id

    def crop_rotated_cylinder(self,center,radius,height,rot,in_cylinder_id):
        condition_array = (self.x_array, self.y_array, self.z_array, center, radius, height, True, rot)
        self.phase_id_array = np.where(condition_array, in_cylinder_id, self.phase_id_array)

#   crop multiple damage
    def crop_multi_spheres(self, center_list, radius_list, damage_id):
        self.init_periodic()
        num = len(center_list)
        condition_array = np.zeros(len(self.x_array_periodic),dtype=int)
        for i in range(num):
            print(f"Cropping multiple sphere: {i + 1}/{num}")
            condition_array += chk_sphere_domain(self.x_array_periodic, self.y_array_periodic, self.z_array_periodic,
                                                center_list[i], radius_list[i])
        print(f"Analyzing multiple sphere")
        self.crop_periodic_phase(condition_array, damage_id)

    def crop_porous_band(self, vol_void, ratio_void0, ratio_band, in_damage_id, supplement_bool = True):
        l = self.size[0]/2
        radius_void0 = l * ratio_void0
        vol_void0 = 4 / 3 * pi * pow(radius_void0, 3)
        num_void = round(vol_void / vol_void0)
        band_width = l * ratio_band
        # generate random point
        center_list = _generate_random_seeds_in_band(l, num_void, band_width)
        radius_list = [radius_void0] * num_void
        # crop
        self.crop_multi_spheres(center_list, radius_list, in_damage_id)
        # checking damage
        if supplement_bool is True:
            vol_void_model = self.ret_damage_fraction(in_damage_id)
            vol_void_add = vol_void - vol_void_model
            num_void_add = int(vol_void_add/vol_void0)
            while num_void_add > 1:
                print('begin to add additional voids')
                center_list = _generate_random_seeds_in_band(l, num_void_add, band_width)
                radius_list = [radius_void0] * num_void_add
                self.crop_multi_spheres(center_list, radius_list, in_damage_id)
                vol_void_model = self.ret_damage_fraction(in_damage_id)
                vol_void_add = vol_void - vol_void_model
                num_void_add = int(vol_void_add / vol_void0)

# analyze damage
    def ret_damage_fraction(self, in_damage_id):
        num_dmg = np.count_nonzero(self.phase_id_array == in_damage_id)
        return num_dmg/len(self.phase_id_array)

# output function
    def output(self,dir,solver):
        if solver == 'amitex_fftp':
            self.output_amitxfftp(dir)
        elif solver == 'damask':
            self.output_damask(dir)
        else:
            RuntimeError('Grid: Please select a right solver for outputting format!')

    def output_damask(self,dir):
        comments = ['by script']
        header = [f'{len(comments) + 4} header'] + comments
        header = header + [f'grid   a {self.cells[0]} b {self.cells[1]} c {self.cells[2]}',
                           f'size   x {self.size[0]} y {self.size[1]} z {self.size[2]}',
                           f'origin x {self.origin[0]} y {self.origin[1]} z {self.origin[2]}',
                           'homogenization 1',
                           ]
        format_string = '%g' if self.phase_id_array.dtype in np.sctypes['float'] else \
            '%{}i'.format(1 + int(np.floor(np.log10(np.nanmax(self.phase_id_array)))))
        np.savetxt('temp.vtk',
                   self.phase_id_array.reshape([self.cells[0], np.prod(self.cells[1:])]),
                   header='\n'.join(header), fmt=format_string, comments='')
        grid_temp = damask.Grid.load_ASCII('temp.vtk')
        grid_temp.save(dir)

    def output_amitxfftp(self,dir):
        header = ['# vtk DataFile Version 4.5\n',
                  'Materiau\n',
                  'BINARY\n',
                  'DATASET STRUCTURED_POINTS\n',
                  f'DIMENSIONS    {self.cells[0]+1}   {self.cells[1]+1}   {self.cells[2]+1}\n',
                  f'ORIGIN    0.000   0.000   0.000\n',
                  f'SPACING    {self.spacing[0]}    {self.spacing[1]}   {self.spacing[2]}\n',
                  f'CELL_DATA   {self.num_points}\n',
                  'SCALARS materialId unsigned_int\n',
                  'LOOKUP_TABLE default\n']
        fio = open(dir,'w')
        fio.writelines(header)
        fio.close()
        fio = open(dir,'ab')
        binary_data = struct.pack('>' + 'i'*len(self.phase_id_array), *self.phase_id_array )
        fio.write(binary_data)
        fio.close()

# others
def _generate_random_seeds_in_band(l, num, width):
    rng = np.random.default_rng(12345)
    x_arr = rng.uniform(0, l * 2, num)
    y_arr = rng.uniform(0, l * 2, num)
    z_arr = rng.uniform(l - width, l + width, num)
    center_list = np.stack((x_arr, y_arr, z_arr), axis=-1)
    return center_list
