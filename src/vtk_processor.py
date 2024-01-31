import vtk
from vtkmodules.numpy_interface import dataset_adapter as dsa
import numpy as np
from pyvtk import *

def read_vtk_field(file_dir):
    # file_dir = '/home/chen/Desktop/remmina_share_folder/cylinder_rot_0.7853981633974483_load_tensionx_finite_strain_material_porous_finite_strain_flab20ex_algorithm_finite_strain/result/output_file_M1_varInt8_200.vtk'
    reader = vtk.vtkStructuredPointsReader()
    reader.SetFileName(file_dir)
    reader.Update()
    data_set = dsa.WrapDataObject(reader.GetOutput())
    key = data_set.CellData.keys()[0]
    data = data_set.CellData[key]
    return data

def write_vtk_vector_field(save_dir,cells,x_list,y_list,z_list):
    vector_list = np.empty(len(x_list), dtype=tuple)
    for i in range(len(x_list)):
        vector_list[i] = (x_list[i], y_list[i], z_list[i])
    vtk = VtkData(StructuredPoints(cells), PointData(Vectors(vector_list)))
    vtk.tofile(save_dir,'binary')

def write_vtk_scalar_field(save_dir,cells,val_list):
    vtk = VtkData(StructuredPoints(cells), PointData(Scalars(val_list)))
    vtk.tofile(save_dir,'binary')


if __name__ == "__main__":

    file_dir = '/home/chen/Desktop/remmina_share_folder/test_Barrioz2019_h0.2/cylinder_x1_0.8_x2_0.6_W1_1_alpha_1_load_tensionx_finite_strain_material_porous_finite_strain_flab20ex_algorithm_finite_strain/result/output_file_M1_varInt8_258.vtk'
    x_data = read_vtk_field(file_dir)

    file_dir = '/home/chen/Desktop/remmina_share_folder/test_Barrioz2019_h0.2/cylinder_x1_0.8_x2_0.6_W1_1_alpha_1_load_tensionx_finite_strain_material_porous_finite_strain_flab20ex_algorithm_finite_strain/result/output_file_M1_varInt9_258.vtk'
    y_data = read_vtk_field(file_dir)

    file_dir = '/home/chen/Desktop/remmina_share_folder/test_Barrioz2019_h0.2/cylinder_x1_0.8_x2_0.6_W1_1_alpha_1_load_tensionx_finite_strain_material_porous_finite_strain_flab20ex_algorithm_finite_strain/result/output_file_M1_varInt10_258.vtk'
    z_data = read_vtk_field(file_dir)

    save_dir = '/home/chen/Desktop/grid_solver/velocity_field/test_output.vtk'
    write_vtk_vector_field(save_dir, [102,64,64], x_data, y_data, z_data)
