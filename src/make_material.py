import damask
import numpy as np
import xml.dom.minidom as md
from src.xml_processor import make_one_info_amitex_fftp

def make_material_porous_damask(matrix_euler,material_matrix_dir,material_void_dir,save_dir):
    config_material = damask.ConfigMaterial()
    config_material['homogenization']['dummy'] = {'N_constituents': 1, 'mechanical': {'type': 'pass'}}
    config_material['phase']['A'] = damask.ConfigMaterial.load(material_matrix_dir)
    config_material['phase']['B'] = damask.ConfigMaterial.load(material_void_dir)
    O_A = damask.Rotation.from_Euler_angles(matrix_euler, degrees=True)
    O_B = damask.Rotation.from_Euler_angles(np.array([0, 0, 0]), degrees=True)
    config_material = config_material.material_add(homogenization='dummy', phase='A', O=O_A)
    config_material = config_material.material_add(homogenization='dummy', phase='B', O=O_B)
    config_material.save(save_dir)

def make_material_porous_amitex_fftp(save_dir,umat_lib_dir,laws_list,coeff_form,var_form):
    root = md.Document()
    materials = root.createElement("Materials")
    root.appendChild(materials)
    # reference material
    item_list = [("Lambda0", "2.02e+10"),
             ("Mu0", "1.35e+10")]
    reference_material = make_one_info_amitex_fftp(root,"Reference_Material",item_list)
    materials.appendChild(reference_material)
    num = len(laws_list)
    # material matrix
    for i in range(num):
        # base
        item_list = [("numM", f"{i+1}"),
                     ("Lib", umat_lib_dir),
                     ("Law", laws_list[i])]
        one_material = make_one_info_amitex_fftp(root, "Material", item_list)
        materials.appendChild(one_material)
        # coeff
        coeff_list = coeff_form[i]
        for j in range(len(coeff_list)):
            item_list = []
            item_list.append(("Index", f"{j+1}"))
            item_list.append(("Type", "Constant"))
            item_list.append(("Value", f"{coeff_list[j]}"))
            one_info = make_one_info_amitex_fftp(root, "Coeff", item_list)
            one_material.appendChild(one_info)
        # IntVar
        var_list = var_form[i]
        for j in range(len(var_list)):
            item_list = []
            item_list.append(("Index", f"{j+1}"))
            item_list.append(("Type", "Constant"))
            item_list.append(("Value", f"{var_list[j]}"))
            one_info = make_one_info_amitex_fftp(root, "IntVar", item_list)
            one_material.appendChild(one_info)
    # Save the formatted XML to a file
    xml_str = root.toprettyxml(indent="  ")
    with open(save_dir, "w", encoding="utf-8") as f:
        f.write(xml_str)
        f.close()

