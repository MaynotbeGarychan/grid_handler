clear;close all;
addpath ../matlab_octave;

%======================================================
%
% GENERATION OF 2 SPHERES MOCROSTRUCTURE
%
%                 MATRIX  = 1
%                 SPHERES = 2
%
% test octave : OK
% test matlab : OK
%======================================================


%------------------------------------------------------ PARAMETERS
Filename="vtk/2spheres";

Dbox = 1.;
Nx = 128;
D1 = 0.3;
D2 = 0.2;
P1 = [0.3,0.3,0.3];
P2 = [0.6,0.6,0.6];

%-------------------------------------------------------GENERATION

%--- Coordinates grid X,Y,Z
P0 = [0,0,0];
D0 = [Dbox,Dbox,Dbox];
N0 = [Nx,Nx,Nx];
[X,Y,Z] = gen_grid(P0,D0,N0);

%--- Initialize image IM0
IM0 = ones(size(X),'int8');

%-------------------------------- SPHERE 1
%--- Distance to the center D
p0x = P1(1);p0y = P1(2);p0z = P1(3);
P0Mx = X - p0x;
P0My = Y - p0y;
P0Mz = Z - p0z;
D =  sqrt(P0Mx.*P0Mx + P0My.*P0My + P0Mz.*P0Mz);

%--- Threshold
IM0(D<D1/2.) = 2;

%-------------------------------- SPHERE 2
%--- Distance to the center D
p0x = P2(1);p0y = P2(2);p0z = P2(3);
P0Mx = X - p0x;
P0My = Y - p0y;
P0Mz = Z - p0z;
D =  sqrt(P0Mx.*P0Mx + P0My.*P0My + P0Mz.*P0Mz);

%--- Threshold
IM0(D<D2/2.) = 2;

%-------------------------------------------------------VTK OUTPUT
savefieldvtk(IM0,Dbox/Nx,Dbox/Nx,Dbox/Nx,strcat(Filename,".vtk"),"materialID",'int8');