from math import sqrt,acosh,asinh,cosh,sinh

def cal_shape_parameter(x1,x2,W1,W2):
    R1 = 0.5*x1
    R2 = 0.5*x2
    h = W1*R1
    return h,R1,R2

def cylinder_shape_parameters_to_model_parameters(alpha,x1,x2,W1):
    L2 = sqrt(1/alpha)/2
    L1 = alpha*L2
    R1 = x1*L1
    R2 = x2*L2
    h = W1*R1
    return L1,L2,R1,R2,h

def shape_cylinder_x2(x1,W1,W2,alpha):
    x2 = alpha*W1*x1/W2
    return x2

def cal_miub(alpha,beta):
    val1 = acosh(1/beta)
    val2 = asinh(alpha/beta)
    return min(val1,val2)

def shape_muv_to_rv(muv,foci):
    rv = [0]*2
    rv[0] = foci * cosh(muv)
    rv[1] = foci * sinh(muv)
    return rv

def shape_unit_L1L2Foci(alpha,beta):
    L1 = 0.5 * sqrt(alpha)
    L2 = 0.5 * sqrt(1 / alpha)
    foci = beta * sqrt(pow(L1,2) + pow(L2,2))
    return L1,L2,foci

def shape_unit_L1L2(alpha):
    L1 = 0.5 * sqrt(alpha)
    L2 = 0.5 * sqrt(1 / alpha)
    return L1, L2

def shape_H(R3):
    H = 2*R3
    if H<0.5:
        H = 0.5
    return H



