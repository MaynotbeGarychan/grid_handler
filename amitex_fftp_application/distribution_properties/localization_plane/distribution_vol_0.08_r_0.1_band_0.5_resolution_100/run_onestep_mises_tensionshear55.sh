NUM_THREADS=8
mkdir ./result_onestep_mises_tensionshear55
mpirun -np $NUM_THREADS amitex_fftp -nm ./model.vtk -m ./material/mises.xml -c ./load/tensionshear55.xml -a ./algorithm/onestep.xml -s ./result_onestep_mises_tensionshear55/output_file
