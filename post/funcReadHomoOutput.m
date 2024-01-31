function data = funcReadHomoOutput(file_dir,head_lines,num_var)
%   1ere colonne : le temps
%   2-7e colonne : la contrainte moyenne en xx,yy,zz,xy,xz,yz
%  8-13e colonne : la deformation moyenne en xx,yy,zz,xy,xz,yz
% 14-19e colonne : l'ecart type de la contrainte moyenne en xx,yy,zz,xy,xz,yz
% 20-25e colonne : l'ecart type de la deformation moyenne en xx,yy,zz,xy,xz,yz
%    26e colonne : nombre d'iterations necessaires pour ce pas de chargement
fid = fopen(file_dir, 'r');
for i = 1:head_lines
    fgetl(fid);
end
data = fscanf(fid, '%f', [num_var, Inf])';
fclose(fid);
end