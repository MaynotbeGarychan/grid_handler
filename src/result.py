import damask
import numpy as np


def getBCFP(result: damask.Result):
    data_F = result.get(['F'])
    data_P = result.get(['P'])

    num_step = len(result.increments)
    num_phase = len(result.phases)
    F_homo = np.zeros((num_step,3,3),dtype=float)
    P_homo = np.zeros((num_step,3,3),dtype=float)
    for i in range(num_step):
        for j in range(num_phase):
            F_homo[i, 0, 0] = F_homo[i, 0, 0] + sum(data_F[result.increments[i]][result.phases[j]][:, 0, 0])
            F_homo[i, 0, 1] = F_homo[i, 0, 1] + sum(data_F[result.increments[i]][result.phases[j]][:, 0, 1])
            F_homo[i, 0, 2] = F_homo[i, 0, 2] + sum(data_F[result.increments[i]][result.phases[j]][:, 0, 2])
            F_homo[i, 1, 0] = F_homo[i, 1, 0] + sum(data_F[result.increments[i]][result.phases[j]][:, 1, 0])
            F_homo[i, 1, 1] = F_homo[i, 1, 1] + sum(data_F[result.increments[i]][result.phases[j]][:, 1, 1])
            F_homo[i, 1, 2] = F_homo[i, 1, 2] + sum(data_F[result.increments[i]][result.phases[j]][:, 1, 2])
            F_homo[i, 2, 0] = F_homo[i, 2, 0] + sum(data_F[result.increments[i]][result.phases[j]][:, 2, 0])
            F_homo[i, 2, 1] = F_homo[i, 2, 1] + sum(data_F[result.increments[i]][result.phases[j]][:, 2, 1])
            F_homo[i, 2, 2] = F_homo[i, 2, 2] + sum(data_F[result.increments[i]][result.phases[j]][:, 2, 2])

            P_homo[i, 0, 0] = P_homo[i, 0, 0] + sum(data_P[result.increments[i]][result.phases[j]][:, 0, 0])
            P_homo[i, 0, 1] = P_homo[i, 0, 1] + sum(data_P[result.increments[i]][result.phases[j]][:, 0, 1])
            P_homo[i, 0, 2] = P_homo[i, 0, 2] + sum(data_P[result.increments[i]][result.phases[j]][:, 0, 2])
            P_homo[i, 1, 0] = P_homo[i, 1, 0] + sum(data_P[result.increments[i]][result.phases[j]][:, 1, 0])
            P_homo[i, 1, 1] = P_homo[i, 1, 1] + sum(data_P[result.increments[i]][result.phases[j]][:, 1, 1])
            P_homo[i, 1, 2] = P_homo[i, 1, 2] + sum(data_P[result.increments[i]][result.phases[j]][:, 1, 2])
            P_homo[i, 2, 0] = P_homo[i, 2, 0] + sum(data_P[result.increments[i]][result.phases[j]][:, 2, 0])
            P_homo[i, 2, 1] = P_homo[i, 2, 1] + sum(data_P[result.increments[i]][result.phases[j]][:, 2, 1])
            P_homo[i, 2, 2] = P_homo[i, 2, 2] + sum(data_P[result.increments[i]][result.phases[j]][:, 2, 2])

    F_homo = F_homo / result.N_materialpoints
    P_homo = P_homo / result.N_materialpoints

    return F_homo,P_homo

def getPhaseFraction(result: damask.Result,phase_name):
    count = np.count_nonzero(result.phase == phase_name)
    return count/result.N_materialpoints




