NUM_THREADS=8
mkdir ./result_onestep_mises_tension
mpirun -np $NUM_THREADS amitex_fftp -nm ./model.vtk -m ./material/mises.xml -c ./load/tension.xml -a ./algorithm/onestep.xml -s ./result_onestep_mises_tension/output_file
