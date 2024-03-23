import matplotlib.pyplot as plt
import numpy as np
from math import pi
from src.grid import objGrid
import os
from shutil import copytree
from src.make_bash import make_batch_amitex_fftp_case, make_batch_amitex_fftp_case_multi,make_batch_win2unix

if __name__ == "__main__":
    # void fraction calculation
    vol_void = 0.04
    ratio_void0 = 0.1
    ratio_band = 0.1
    l = 0.5

    # crop
    resolution = 100
    size = np.array([l*2, l*2, l*2], dtype=float)
    cells = np.array(size * resolution, dtype=int)
    origin = np.array([0, 0, 0], dtype=float)
    grid = objGrid(cells, size, origin)
    grid.crop_porous_band(vol_void, ratio_void0, ratio_band, 2)

    geom = f'distribution_vol_{vol_void}_r_{ratio_void0}_band_{ratio_band}_resolution_{resolution}'
    os.mkdir(f'./{geom}')
    grid.output(f'./{geom}/model.vtk', 'amitex_fftp')
    copytree('../../../xml_files/onestep/material', f'./{geom}/material')
    copytree('../../../xml_files/onestep/algorithm', f'./{geom}/algorithm')
    copytree('../../../xml_files/onestep/load', f'./{geom}/load')
    make_batch_amitex_fftp_case_multi(f'./{geom}',8)
    print(f'finish {geom}\n')




