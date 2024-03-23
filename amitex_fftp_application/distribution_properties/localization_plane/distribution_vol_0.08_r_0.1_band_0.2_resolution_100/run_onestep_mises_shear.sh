NUM_THREADS=8
mkdir ./result_onestep_mises_shear
mpirun -np $NUM_THREADS amitex_fftp -nm ./model.vtk -m ./material/mises.xml -c ./load/shear.xml -a ./algorithm/onestep.xml -s ./result_onestep_mises_shear/output_file
