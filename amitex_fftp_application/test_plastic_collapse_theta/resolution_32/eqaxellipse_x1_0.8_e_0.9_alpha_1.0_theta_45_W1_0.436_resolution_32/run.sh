NUM_THREADS=16
mkdir ./result
mpirun -np $NUM_THREADS amitex_fftp -nm ./model.vtk -m ./material.xml -c ./load.xml -a ./algorithm.xml -s ./result/output_file
