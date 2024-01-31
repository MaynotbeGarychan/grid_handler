import xml.dom.minidom as md
from src.xml_processor import make_one_info_amitex_fftp
def inversion(l,fill=0):
    return [inversion(i,fill) if isinstance(i,list) else\
            fill if i == 'x' else 'x' for i in l]
def makeLoadDotF(df11,df22,df33,file_dir):
    write_io = open(file_dir,'w')
    write_io.write(f'---\n')
    write_io.write(f'\n')
    write_io.write(f'solver:\n')
    write_io.write(f'  mechanical: spectral_basic\n')
    write_io.write(f'\n')
    write_io.write(f'loadstep:\n')
    write_io.write(f'  - boundary_conditions:\n')
    write_io.write(f'      mechanical:\n')
    write_io.write(f'        dot_F: [ [{df11}, 0, 0], [0, {df22}, 0], [0, 0, {df33}] ]\n')
    write_io.write(f'    discretization:\n')
    write_io.write(f'      t: 10\n')
    write_io.write(f'      N: 10\n')
    write_io.write(f'    f_out: 2\n')
    write_io.close()

def makeLoadF(f,t,N,f_out,file_dir):
    p = inversion(f)
    write_io = open(file_dir, 'w')
    write_io.write(f'---\n')
    write_io.write(f'\n')
    write_io.write(f'solver:\n')
    write_io.write(f'  mechanical: spectral_basic\n')
    write_io.write(f'\n')
    write_io.write(f'loadstep:\n')
    write_io.write(f'  - boundary_conditions:\n')
    write_io.write(f'      mechanical:\n')
    write_io.write(f'        F:\n')
    write_io.write(f'            - [{f[0][0]}, {f[0][1]}, {f[0][2]}]\n')
    write_io.write(f'            - [{f[1][0]}, {f[1][1]}, {f[1][2]}]\n')
    write_io.write(f'            - [{f[2][0]}, {f[2][1]}, {f[2][2]}]\n')
    write_io.write(f'        P:\n')
    write_io.write(f'            - [{p[0][0]}, {p[0][1]}, {p[0][2]}]\n')
    write_io.write(f'            - [{p[1][0]}, {p[1][1]}, {p[1][2]}]\n')
    write_io.write(f'            - [{p[2][0]}, {p[2][1]}, {p[2][2]}]\n')
    write_io.write(f'    discretization: {{t: {t}, N: {N}}}\n')
    write_io.write(f'    f_out: {f_out}\n')
    write_io.close()

def make_load_amitexfftp(save_dir,
                         output_ss_list, output_Intvar_form,
                         time_discretization_info_form, output_time_list, bc_list, dir_stress_list):
    root = md.Document()
    Loading_Output = root.createElement("Loading_Output")
    root.appendChild(Loading_Output)
    # Output
    Output = _make_load_amitexfftp_output(root, output_ss_list, output_Intvar_form)
    Loading_Output.appendChild(Output)
    # Loading
    Loading = _make_load_amitexfftp_loading(root,
                                            time_discretization_info_form, output_time_list,
                                            bc_list, dir_stress_list)
    Loading_Output.appendChild(Loading)
    # write
    xml_str = root.toprettyxml()
    with open(save_dir, "w", encoding="utf-8") as f:
        f.write(xml_str)
        f.close()

def _make_load_amitexfftp_output(root, output_ss_list, output_Intvar_form):
    Output = root.createElement("Output")
    for i in range(len(output_ss_list)):
        vtk_StressStrain = root.createElement("vtk_StressStrain")
        vtk_StressStrain.setAttribute("Strain", f"{output_ss_list[i]}")
        vtk_StressStrain.setAttribute("Stress", f"{output_ss_list[i]}")
        Output.appendChild(vtk_StressStrain)
    for i in range(len(output_Intvar_form)):
        output_Intvar_list = output_Intvar_form[i]
        vtk_IntVarList = root.createElement("vtk_IntVarList")
        vtk_IntVarList.setAttribute("numM", f"{i + 1}")
        aString = ' '.join(map(str, output_Intvar_list))
        vtk_IntVarList.appendChild(root.createTextNode(aString))
        Output.appendChild(vtk_IntVarList)
    return Output

def _make_load_amitexfftp_loading(root, time_discretization_info_list, output_time_list,
                                  bc_list, dir_stress_list):
    Loading = root.createElement("Loading")
    Loading.setAttribute("Tag", f"1")
    # time discretization
    Time_Discretization = root.createElement("Time_Discretization")
    Time_Discretization.setAttribute("Discretization", time_discretization_info_list[0])
    Time_Discretization.setAttribute("Nincr", f'{int(time_discretization_info_list[1])}')
    Time_Discretization.setAttribute("Tfinal", f'{int(time_discretization_info_list[2])}')
    Loading.appendChild(Time_Discretization)
    # output vtk list
    if len(output_time_list) > 0:
        Output_vtkList = root.createElement("Output_vtkList")
        aString = ' '.join(map(str, output_time_list))
        Output_vtkList.appendChild(root.createTextNode(aString))
        Loading.appendChild(Output_vtkList)
    # loading
    if len(dir_stress_list) > 0:
        bc_dir_str_list = ["xx", "yy", "zz", "xy", "xz", "yz", "yx", "zx", "zy"]
        for j in range(len(bc_list)):
            bc_value = bc_list[j]
            bc = root.createElement(bc_dir_str_list[j])
            if bc_value == 0.0:
                bc.setAttribute("Driving", "Stress")
                bc.setAttribute("DirStress", f"{dir_stress_list[j]}")
            else:
                bc.setAttribute("Driving", "Strain")
                bc.setAttribute("Evolution", "Linear")
                bc.setAttribute("Value", f"{bc_value}")
                bc.setAttribute("DirStress", f"{dir_stress_list[j]}")
            Loading.appendChild(bc)
        DirStress = root.createElement("DirStress")
        DirStress.setAttribute("Type", f"cauchy")
        Loading.appendChild(DirStress)
    else:
        bc_dir_str_list = ["xx", "yy", "zz", "xy", "xz", "yz"]
        for j in range(len(bc_list)):
            bc_value = bc_list[j]
            bc = root.createElement(bc_dir_str_list[j])
            if bc_value == 0.0:
                bc.setAttribute("Driving", "Stress")
            else:
                bc.setAttribute("Driving", "Strain")
            bc.setAttribute("Evolution", "Linear")
            bc.setAttribute("Value", f"{bc_value}")
            Loading.appendChild(bc)
    return Loading

