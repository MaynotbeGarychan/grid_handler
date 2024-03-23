import os

# damask batch
def make_batch_damask(load_dir,model_dir,material_dir,num_threads:int,batch_dir):
    lines = []
    lines.append(f"export OMP_NUM_THREADS={num_threads} && \\\n")
    geom_list = os.listdir(model_dir)
    load_list = os.listdir(load_dir)
    material_list = os.listdir(material_dir)
    for i in range(len(geom_list)):
        geom = geom_list[i].replace('.vti','')
        for j in range(len(load_list)):
            load = load_list[j].replace('.yaml', '')
            for k in range(len(material_list)):
                material = material_list[k].replace('.yaml','')
                job_name = f'{geom}_{load}'
                lines.append(f"mkdir {job_name} && \\\n")
                lines.append(f"cp ./material/{material}.yaml ./{job_name} && \\\n")
                lines.append(f"cp ./load/{load}.yaml ./{job_name} && \\\n")
                lines.append(f"cp ./model/{geom}.vti ./{job_name} && \\\n")
                lines.append(f"DAMASK_grid -w ./{job_name} -l {load}.yaml -g {geom}.vti && \\\n")
    lines[-1] = lines[-1][:-6]

    write_io = open(batch_dir,'w')
    write_io.writelines(lines)
    write_io.close()

# amitex batch
def make_batch_amitex_fftp(load_dir,model_dir,material_dir,algorithm_dir,batch_dir,num_core):
    lines = []
    geom_list = os.listdir(model_dir)
    load_list = os.listdir(load_dir)
    material_list = os.listdir(material_dir)
    algorithm_list = os.listdir(algorithm_dir)

    lines.append(f"NUM_THREADS={num_core}\n")

    for i in range(len(geom_list)):
        geom = geom_list[i].replace('.vtk', '')
        for j in range(len(load_list)):
            load = load_list[j].replace('.xml', '')
            for k in range(len(material_list)):
                material = material_list[k].replace('.xml', '')
                for l in range(len(algorithm_list)):
                    algorithm = algorithm_list[l].replace('.xml', '')
                    # job_name = f'{geom}_{load}_{material}_{algorithm}'
                    job_name = f'{geom}'
                    lines.append(f"mkdir {job_name} && \\\n")
                    lines.append(f"cp ./material/{material}.xml ./{job_name} && \\\n")
                    lines.append(f"cp ./load/{load}.xml ./{job_name} && \\\n")
                    lines.append(f"cp ./model/{geom}.vtk ./{job_name} && \\\n")
                    lines.append(f"cp ./algorithm/{algorithm}.xml ./{job_name} && \\\n")
                    lines.append(f"mkdir ./{job_name}/result && \\\n")
                    lines.append(f"mpirun -np $NUM_THREADS amitex_fftp -nm ./{job_name}/{geom}.vtk -m ./{job_name}/{material}.xml -c ./{job_name}/{load}.xml -a ./{job_name}/{algorithm}.xml -s ./{job_name}/result/output_file\n")
    #lines[-1] = lines[-1][:-6]
    write_lines(batch_dir, lines)

def make_batch_amitex_fftp_case(case_folder_dir,num_core):
    lines = []
    lines.append(f"NUM_THREADS={num_core}\n")
    lines.append(f"mkdir ./result\n")
    lines.append(
        f"mpirun -np $NUM_THREADS amitex_fftp -nm ./model.vtk -m ./material.xml -c ./load.xml -a ./algorithm.xml -s ./result/output_file\n")
    write_lines(os.path.join(case_folder_dir,'run.sh'), lines)

def make_batch_amitex_fftp_case_multi(folder_dir,num_core):
    # xml list
    load_list = ret_xml_list(os.path.join(folder_dir,'load'), False)
    material_list = ret_xml_list(os.path.join(folder_dir,'material'), False)
    algorithm_list = ret_xml_list(os.path.join(folder_dir,'algorithm'), False)
    # make lines
    case_list = []
    multi_case_lines = []
    for algorithm in algorithm_list:
        for material in material_list:
            for load in load_list:
                case = f'{algorithm}_{material}_{load}'
                case_list.append(case)
                case_lines = []
                case_lines.append(f"NUM_THREADS={num_core}\n")
                case_lines.append(f"mkdir ./result_{case}\n")
                case_lines.append(
                    f"mpirun -np $NUM_THREADS amitex_fftp -nm ./model.vtk -m ./material/{material}.xml -c ./load/{load}.xml -a ./algorithm/{algorithm}.xml -s ./result_{case}/output_file\n")
                write_lines(os.path.join(folder_dir, f'run_{case}.sh'), case_lines)
                multi_case_lines.append(f'./run_{case}.sh\n')
    write_lines(os.path.join(folder_dir, 'run_all.sh'), multi_case_lines)

def make_batch_amitex_fftp_project(project_dir):
    lines = []
    dir_list = os.listdir(project_dir)
    for dir in dir_list:
        sh_dir = os.path.join(dir,'run.sh')
        if os.path.exists(sh_dir):
            lines.append(f"cd ./{dir} && \\\n")
            lines.append(f"./run.sh\n")
            lines.append(f"cd .. && \\\n")
    lines[-1] = lines[-1][:-5]
    write_lines(os.path.join(project_dir,'run_all.sh'), lines)

def make_batch_win2unix(file_path):
    # replacement strings
    WINDOWS_LINE_ENDING = b'\r\n'
    UNIX_LINE_ENDING = b'\n'
    # relative or absolute file path, e.g.:
    with open(file_path, 'rb') as open_file:
        content = open_file.read()
    # Windows ➡ Unix
    content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
    with open(file_path, 'wb') as open_file:
        open_file.write(content)

# others
def write_lines(file_dir,lines):
    write_io = open(file_dir, 'w', encoding="utf-8")
    write_io.writelines(lines)
    write_io.close()
    make_batch_win2unix(file_dir) # for windows

def ret_xml_list(folder_dir, with_ending = True):
    xml_list = []
    for xml in os.listdir(folder_dir):
        if with_ending == False:
            xml_list.append(xml.split('.')[0])
        else:
            xml_list.append(xml)
    return xml_list




