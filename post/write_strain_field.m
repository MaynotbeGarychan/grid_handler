filein = '/home/chen/Desktop/remmina_share_folder/cylinder_rot_0.0_load_tensionx_finite_strain_material_porous_finite_strain_flab20ex_algorithm_finite_strain/result/output_file_sig1_200.vtk'; 
[X,dx,dy,dz,nx,ny,nz,S,datatype] = readfieldvtk(filein);

filein = '/home/chen/Desktop/remmina_share_folder/cylinder_rot_0.0_load_tensionx_finite_strain_material_porous_finite_strain_flab20ex_algorithm_finite_strain/result/output_file_sig2_200.vtk'; 
[Y,dx,dy,dz,nx,ny,nz,S,datatype] = readfieldvtk(filein);

filein = '/home/chen/Desktop/remmina_share_folder/cylinder_rot_0.0_load_tensionx_finite_strain_material_porous_finite_strain_flab20ex_algorithm_finite_strain/result/output_file_sig3_200.vtk'; 
[Z,dx,dy,dz,nx,ny,nz,S,datatype] = readfieldvtk(filein);
%%

funcSaveVectorVtk(X,Y,Z,dx,dy,dz,'vt.vtk');