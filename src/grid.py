import numpy as np
import damask
from src.transformation import rotation_matrix_by_euler_angle
import struct
from src.transformation import rotate_point_clouds

class objGrid(object):
    x_array = np.array(0)
    y_array = np.array(0)
    z_array = np.array(0)
    phase_id_array = np.array(0)
    origin =  np.array(0)
    cells =  np.array(0)
    size =  np.array(0)
    spacing = np.array(0)
    num_points = 0
    unit_dist = 0

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

    def crop_sphere(self,center,radius,sphere_id):
        distx = self.x_array - center[0]
        disty = self.y_array - center[1]
        distz = self.z_array - center[2]
        distx2 = np.power(distx,2)
        disty2 = np.power(disty, 2)
        distz2 = np.power(distz, 2)
        dist_array_2 = distx2 + disty2 + distz2
        thres = radius ** 2
        condition_array = dist_array_2 < thres
        self.phase_id_array = np.where(condition_array, sphere_id, self.phase_id_array)

    def crop_ellipse(self,center,radius,in_ellipse_id):
        a2,b2,c2 = radius[0]**2,radius[1]**2,radius[2]**2
        dist_array_2 = (self.x_array - center[0])**2/a2 + (self.y_array - center[1])**2/b2 +(self.z_array - center[2])**2/c2
        condition_array = dist_array_2 < 1
        self.phase_id_array = np.where(condition_array, in_ellipse_id, self.phase_id_array)

    def crop_rotated_ellipse(self,center,radius,rot,in_ellipse_id):
        # rot = rotation_matrix_by_euler_angle(euler_angle)
        x_array_origin = self.x_array - center[0]
        y_array_origin = self.y_array - center[1]
        z_array_origin = self.z_array - center[2]
        x_array_origin_rot = x_array_origin * rot[0, 0] + y_array_origin * rot[1, 0] + z_array_origin * rot[2, 0]
        y_array_origin_rot = x_array_origin * rot[0, 1] + y_array_origin * rot[1, 1] + z_array_origin * rot[2, 1]
        z_array_origin_rot = x_array_origin * rot[0, 2] + y_array_origin * rot[1, 2] + z_array_origin * rot[2, 2]
        a2, b2, c2 = radius[0] ** 2, radius[1] ** 2, radius[2] ** 2
        dist_array_2 = x_array_origin_rot ** 2 / a2 + y_array_origin_rot ** 2 / b2 + z_array_origin_rot ** 2 / c2
        condition_array = dist_array_2 < 1
        self.phase_id_array = np.where(condition_array, in_ellipse_id, self.phase_id_array)

    def crop_cylinder(self,center,radius,height,in_cylinder_id, axis_option = 'x'):
        if axis_option == 'z':
            height_array = np.abs(self.z_array - center[2])
            dist_array_2 = (self.x_array - center[0]) ** 2 / (radius[0] ** 2) + (self.y_array - center[1]) ** 2 / (
                        radius[1] ** 2)
            condition_array = (height_array < height) & (dist_array_2 < 1)
            idx_list = np.where(condition_array)
            self.phase_id_array[idx_list] = in_cylinder_id
        else:
            height_array = np.abs(self.x_array - center[0])
            dist_array_2 = (self.y_array - center[1])**2/(radius[0]**2) +(self.z_array - center[2])**2/(radius[1]**2)
            condition_array = (height_array<height) & (dist_array_2 < 1)
            idx_list = np.where(condition_array)
            self.phase_id_array[idx_list] = in_cylinder_id

    def crop_cylinder_outside_frictive(self,center,radius,out_cylinder_id):
        x_array_origin = self.x_array - center[0]
        y_array_origin = self.y_array - center[1]
        z_array_origin = self.z_array - center[2]
        dist_array_2 = np.power(x_array_origin,2) / (radius[0] ** 2) + np.power(y_array_origin,2) / (radius[1] ** 2)
        idx_list = np.where(dist_array_2 > 1)
        self.phase_id_array[idx_list] = out_cylinder_id

    def crop_rotated_cylinder(self,center,radius,height,rotation,in_cylinder_id, axis_option = 'x'):
        x_array_origin = self.x_array - center[0]
        y_array_origin = self.y_array - center[1]
        z_array_origin = self.z_array - center[2]
        x_array_origin_rot, y_array_origin_rot, z_array_origin_rot = rotate_point_clouds(x_array_origin, y_array_origin,
                                                                                         z_array_origin, rotation)
        if axis_option == 'z':
            height_array = np.abs(z_array_origin_rot)
            dist_array_2 = x_array_origin_rot ** 2 / (radius[0] ** 2) + y_array_origin_rot ** 2 / (radius[1] ** 2)
        else:
            height_array = np.abs(x_array_origin_rot)
            dist_array_2 = y_array_origin_rot**2/(radius[0]**2) + z_array_origin_rot**2/(radius[1]**2)
        condition_array = (height_array<height) & (dist_array_2 < 1)
        self.phase_id_array = np.where(condition_array, in_cylinder_id, self.phase_id_array)

    def crop_oblique_cylinder_with_various_direction(self,center,radius,h,plane_direction,z_axis_direction,in_cylinder_id):

        plane_direction /= np.linalg.norm(plane_direction)
        z_axis_direction /= np.linalg.norm(z_axis_direction)

        point_vector_x_array = self.x_array - center[0]
        point_vector_y_array = self.y_array - center[1]
        point_vector_z_array = self.z_array - center[2]
        vertical_distance_array = (point_vector_x_array * plane_direction[0] + point_vector_y_array * plane_direction[1]
                                + point_vector_z_array * plane_direction[2])

        real_distance_array_2 = point_vector_x_array**2 + point_vector_y_array**2 + point_vector_z_array**2

        horizonal_distance_array_2 = real_distance_array_2 - vertical_distance_array**2

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
