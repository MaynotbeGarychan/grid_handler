import damask
import numpy as np
from src.grid import objGrid

def combine(geom_dir,material_dir,save_dir):
    material_config = material_dir  # path for material.yaml
    v = damask.VTK.load(geom_dir)
    material_ID = v.get('material').flatten()
    ma = damask.ConfigMaterial.load(material_config)
    phases = list(ma['phase'].keys())
    info = []
    for m in ma['material']:
        c = m['constituents'][0]
        phase = c['phase']
        info.append({'phase': phase,
                     'phaseID': phases.index(phase),
                     'lattice': ma['phase'][phase]['lattice'],
                     'O': c['O'],
                     })
    l = np.array([0, 0, 1])  # lab frame direction for IPF
    IPF = np.ones((len(material_ID), 3), np.uint8)
    for i, data in enumerate(info):
        IPF[np.where(material_ID == i)] = \
            np.uint8(damask.Orientation(data['O'], lattice=data['lattice']).IPF_color(l) * 255)
    v = v.set(f'IPF_{l}', IPF)
    p = np.array([d['phase'] for d in info])
    pid = np.array([d['phaseID'] for d in info])
    v = v.set('phase', p[material_ID], 'phase')
    v = v.set('phaseID', pid[material_ID], 'phaseID')
    v.save(save_dir)

def make_grid_with_sphere_in_center(cells, size, origin,radius,geom_dir,solver):
    # cells = np.array([32, 32, 32], dtype=int)
    # size = np.array([1, 1, 1], dtype=float)
    # origin = np.array([0, 0, 0], dtype=float)
    grid = objGrid(cells, size, origin)
    grid.crop_sphere(size / 2, radius, 2)
    grid.output(geom_dir,solver)

def make_grid_with_ellipse_in_center(cell,size,origin,radius_couple,rotation_matrix,geom_dir,solver):
    grid = objGrid(cell,size,origin)
    grid.crop_rotated_ellipse(size/2, radius_couple, rotation_matrix, 2)
    grid.output(geom_dir,solver)

# def make_grid_with_oblique_cylinder_in_center():

def make_grid_with_many_sphere(cell, size, origin, position_list, radius_list, geom_dir,solver):
    grid = objGrid(cell, size, origin)
    num_sphere = len(position_list)
    for i in range(num_sphere):
        grid.crop_sphere(position_list[i], radius_list[i], 2)
    grid.output(geom_dir,solver)

def make_grid_with_many_rotated_ellipses(cell, size, origin, position_list,
                                         radius_couple_list, rotation_matrix, geom_dir,solver):
    grid = objGrid(cell, size, origin)
    num_ellipses = len(position_list)
    for i in range(num_ellipses):
        grid.crop_rotated_ellipse(position_list[i], radius_couple_list[i], rotation_matrix, 2)
    grid.output(geom_dir,solver)

def make_grid_with_cylinder_inside(cell,size,origin,r,h,geom_dir,solver):
    grid = objGrid(cell, size, origin)
    grid.crop_cylinder(size / 2, r, h, 2)
    grid.output(geom_dir, solver)

def make_grid_with_many_cylinder_inside(cell,size,origin,position_list,radius_couple,height,rotation_matrix,geom_dir,solver):
    grid = objGrid(cell, size, origin)
    num = len(position_list)
    for i in range(num):
        grid.crop_rotated_cylinder(position_list[i],radius_couple,height,rotation_matrix,2)
    grid.output(geom_dir, solver)