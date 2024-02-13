from scipy import *
from scipy.integrate import quad
from scipy.optimize import root_scalar
from math import *

'''
Módulo que inclui todos os cálculos de desempenho necessários à otimização do modelo
'''

c_pista= 55
h_decol= 0.7

def alt(p, t):
    
    alti= (288.15/0.0065)*(1-((p/1013.25)/((t+273.15)/288.15))**0.234959)
    return alti
    
def rho(p, t):
    #alti=1500
    alti= alt(p,t)
    rho= 1.2250177777777773-0.00011760273526795266*alti+4.359717577108174e-9*(alti)**2-9.65009064952006e-14*alti**3
    return rho

def tracd(p, t, v):

    tracd= (28.709955+0.07366009766*v-0.03187744135*v**2-0.0013809470336*v**3+7.82035332027e-5*v**4-1.160949504525e-6*v**5)*(rho(p,t)/rho(p=1013.25, t=15))
    return tracd

def tracr(cld ,cdd , m):

    tracr= m*9.81*(cdd/cld)
    return tracr

def q(p, t, v):

    dens= rho(p,t)
    q= (dens*v**2)/2
    return q

def lift(p, t, v, s, cl):

    qp= q(p, t, v)
    lift= qp*s*cl
    return lift

def drag(p, t, v, s, cd):

    qp= q(p, t, v)
    drag= qp*s*cd
    return drag

def v_estol(p, t, m, s, clmax, g=9.81):

    dens= rho(p,t)
    v_estol= sqrt(abs((2*m*g)/(dens*s*clmax)))
    return v_estol 

def fric(p, t, m, s, clc, clmax, v, g= 9.81, mu= 0.03):

    if v <= 1.2*v_estol(p, t, m, s, clmax, g=9.81):
        lift_c= lift(p, t, v, s, clc)
        fric= mu*(m*g-lift_c)
    
    else:
        fric= 0
    
    return fric

def acel_dec(p, t, v, m, s, clc, clmax, cdc, g= 9.81, mu= 0.03):
    
    tracdisp= tracd(p,t,v)
    atrito= fric(p, t, m, s, clc, clmax, v, g= 9.81, mu= 0.03)
    dragc= drag(p, t, v, s, cdc)

    acel_dec= (tracdisp-dragc-atrito)/m

    return acel_dec

def f_d_sol(v, p, t, m, s, clc, clmax, cdc, g= 9.81, mu= 0.03):
    f= v/acel_dec(p, t, v, m, s, clc, clmax, cdc, g, mu)
    return f

def d_sol(p, t, v, m, s, clc, clmax, cdc, g= 9.81, mu= 0.03):

    v_est= v_estol(p, t, m, s, clmax, g)
    v_decol= 1.2*v_est

    d_sol, d_sol_res= quad(f_d_sol, 0, v_decol, args=(p, t, m, s, clc, clmax, cdc, g, mu), limit= 100)

    return d_sol

def d_rot(p, t, m, s, clmax, g= 9.81):

    v_est= v_estol(p, t, m, s, clmax, g)
    d_rot= 1.2*v_est/3

    return d_rot

def r_trans(p, t, m, s, clmax, g= 9.81, n= 1.2):

    v_est= v_estol(p, t, m, s, clmax, g)
    r_trans= (1.15*v_est)**2/(g*(n-1))

    return r_trans

def g_cl(p, t, m, s, clmax, cdt, g=9.81):

    v_est= v_estol(p, t, m, s, clmax, g)
    tracdisp= tracd(p, t, v_est)
    drag_t= drag(p, t, v_est, s, cdt)

    g_cl= (tracdisp-drag_t)/(m*g) #em rad

    return g_cl

def h_trans(p, t, m, s, clmax, cdt, g= 9.81, n= 1.2):

    r_t= r_trans(p, t, m, s, clmax, g, n)
    g_cl_rad= g_cl(p, t, m, s, clmax, cdt, g)

    ht= r_t*(1-cos(g_cl_rad))

    return ht

def f_g_tr(gamma, p, t, m, s, clmax, g= 9.81, n= 1.2):

    r_t= r_trans(p, t, m, s, clmax, g, n)

    f= h_decol- (r_t*(1-cos(gamma)))

    return f

def g_tr(gamma, p, t, m, s, clmax, g= 9.81, n= 1.2):

    g_tr= root_scalar(f_g_tr, args= (p, t, m, s, clmax, g, n), method='bisect', bracket=[0,pi/4])
    
    if g_tr.flag == 'converged':
        return g_tr.root #em radianos
    
    else:
        print('g_tr não convergiu, continuando assim mesmo')
        return g_tr.root
    
def d_trans(p, t, m, s, clmax, cdt, g= 9.81, n= 1.2, gamma=0):

    h_t= h_trans(p, t, m, s, clmax, cdt, g, n)
    r_t= r_trans(p, t, m, s, clmax, g, n)

    if h_t < h_decol:
        gamma_cl= g_cl(p, t, m, s, clmax, cdt, g)

        d_t= r_t*sin(gamma_cl)
    
    else:
        gamma_tr= g_tr(gamma, p, t, m, s, clmax, g, n)

        d_t= r_t*sin(gamma_tr)

    return d_t

def d_sub(p, t, m, s, clmax, cdt, g= 9.81, n= 1.2 ):

    h_t= h_trans(p, t, m, s, clmax, cdt, g, n)
    gamma_cl= g_cl(p, t, m, s, clmax, cdt, g)

    if h_t < h_decol:

        d_sub= (h_decol-h_t)/tan(gamma_cl)

    else:
        d_sub= 0

    return d_sub

def d_decol(p, t, v, m, s, clc, clmax, cdc, cdt, g= 9.81, mu= 0.03, n= 1.2, gamma= 0):

    dist_solo= d_sol(p, t, v, m, s, clc, clmax, cdc, g, mu)

    dist_rot= d_rot(p, t, m, s, clmax, g)

    dist_trans= d_trans(p, t, m, s, clmax, cdt, g, n, gamma)

    dist_sub= d_sub(p, t, m, s, clmax, cdt, g, n)

    dist_decol= dist_solo + dist_rot + dist_trans + dist_sub

    return dist_decol

def f_mtow(m, p, t, v, s, clc, clmax, cdc, cdt, g= 9.81, mu= 0.03, n= 1.2, gamma= 0):

    f= c_pista - d_decol(p, t, v, m, s, clc, clmax, cdc, cdt, g, mu, n, gamma)

    return f

def mtow(p, t, v, m, s, clc, clmax, cdc, cdt, g= 9.81, mu= 0.03, n= 1.2, gamma= 0):

    mtow= root_scalar(f_mtow, args= (p, t, v, s, clc, clmax, cdc, cdt, g, mu, n, gamma), method='bisect', bracket=[5,20])

    return mtow.root


#def mtow():






if __name__ == '__main__':
    print(alt(905,25))
    print(rho(1013,26))
    #print(tracd(8,1013,26))
    #print(v_estol(10,1013,26,0.8,2.04,9.81))
    print(d_sol(1013,26,10,10,0.8,1.2,2.04,0.2))
    print(g_tr(0,1013,26,10,0.8,2.04,9.81,1.2))
    print(d_trans(1013, 26, 10, 0.8, 2.04, 0.2))
    print(d_sub(1013, 26, 10, 0.8, 2.04, 0.2))
    print(d_decol(1013, 26, 10, 10.6, 0.8, 1.2, 2.04, 0.2, 0.3))
    print(mtow(1013, 26, 10, 20, 0.8, 1.2, 2.04, 0.2, 0.3))

