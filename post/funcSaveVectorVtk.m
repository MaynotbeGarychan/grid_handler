function funcSaveVectorVtk(vx,vy,vz,dx,dy,dz,ficname)
[nx, ny, nz] = size(vx);
fid = fopen(ficname, 'w');
fprintf(fid, '# vtk DataFile Version 4.5\n');
fprintf(fid, 'Materiau\n');
fprintf(fid, 'BINARY\n');
fprintf(fid, 'DATASET STRUCTURED_POINTS\n');
fprintf(fid, 'DIMENSIONS    %d   %d   %d\n', nx+1, ny+1, nz+1);
fprintf(fid, 'ORIGIN    0.000   0.000   0.000\n');
fprintf(fid, 'SPACING    %f    %f   %f\n', dx, dy, dz);
fprintf(fid, 'CELL_DATA   %lu\n', nx*ny*nz);
fprintf(fid, 'VECTORS vectors float\n');

for k=1:nz
    for j =1:ny
        for i=1:nx
            fprintf(fid, '%f %f %f ',vx(i,j,k),vy(i,j,k),vz(i,j,k));
        end
    end
    fprintf(fid, '\n');
end

end

