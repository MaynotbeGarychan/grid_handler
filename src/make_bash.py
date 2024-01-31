import os


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

    write_io = open(batch_dir, 'w')
    write_io.writelines(lines)
    write_io.close()

def make_batch_amitex_fftp_case(case_folder_dir,num_core):
    lines = []
    lines.append(f"NUM_THREADS={num_core}\n")
    lines.append(f"mkdir ./result\n")
    lines.append(
        f"mpirun -np $NUM_THREADS amitex_fftp -nm ./model.vtk -m ./material.xml -c ./load.xml -a ./algorithm.xml -s ./result/output_file\n")
    sh_dir = os.path.join(case_folder_dir,'run.sh')
    write_io = open(sh_dir, 'w')
    write_io.writelines(lines)
    write_io.close()

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
    write_io = open(os.path.join(project_dir,'run_all.sh'), 'w')
    write_io.writelines(lines)
    write_io.close()




