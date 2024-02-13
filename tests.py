from prototype import *
from simulator import *
from performance import *
import matplotlib.pyplot as plt
import time

"""
Este arquivo contém alguns testes que foram úteis para debugging durante o desenvolvimento do código.
"""

aviao1= Prototype (w_cr= 0.56562231, w_ct= 0.30305969, w_z= 0.10866631, w_inc= 0.09366175, eh_b= 1.3, eh_c= 0.29018557, eh_inc= -0.56474704, ev_b= 0.22687644, eh_x= 0.85862047, eh_z= 0.25888654, motor_x= -0.1, motor_z= 0.3, fus_h= 0.15, ge= False)
aviao1_ge= Prototype (w_cr= 0.56562231, w_ct= 0.30305969, w_z= 0.10866631, w_inc= 0.09366175, eh_b= 1.3, eh_c= 0.29018557, eh_inc= -0.56474704, ev_b= 0.22687644, eh_x= 0.85862047, eh_z= 0.25888654, motor_x= -0.1, motor_z= 0.3, fus_h= 0.15, ge= True)
aviao2= Prototype ( w_cr= 0.5550223752921603, w_ct= 0.32440387770404855, w_z= 0.21381808524016974, w_inc= 0.202664347310206, eh_b= 1.2, eh_c= 0.3, eh_inc= 3.0, ev_b= 0.20350832048754716, eh_x= 1.1162955896906936, eh_z= 0.21434295817757107, motor_x= -0.16789474310742902, motor_z= 0.3, fus_h= 0.15, ge= False)
aviao2_ge= Prototype ( w_cr= 0.5550223752921603, w_ct= 0.32440387770404855, w_z= 0.21381808524016974, w_inc= 0.202664347310206, eh_b= 1.2, eh_c= 0.3, eh_inc= 3.0, ev_b= 0.20350832048754716, eh_x= 1.1162955896906936, eh_z= 0.21434295817757107, motor_x= -0.16789474310742902, motor_z= 0.3, fus_h= 0.15, ge= True)

#cg(w_s= 1.05269712, w_z= 0.265, w_cr= 0.5372, eh_s= 0.365085, eh_x= 1.2, eh_z= 0.433, eh_c= 0.285, ev_s=0.171, ev_x= 1.2, ev_z= 1.2, ev_c= 0.285, fus_z= 0.15, fus_w= 0.12, fus_h= 0.24, fus_l= 0.3, boom_l)

print('Peso vazio:', aviao2.pv, 
      'X_cg:',aviao2.x_cg, 
      'Z_cg:',aviao2.z_cg)

print('Comprimento do boom:', aviao2.boom_l)

#aviao1.show_geometry()

simulation1= Simulator(aviao2,aviao2_ge)

simulation1.scorer()

#simulation1.run_a()
#simulation1.run_stall()
#simulation1.run_ge()
#print('CL=',simulation1.cl)
#print('CD=',simulation1.cd)
#print('CLmax=', simulation1.clmax)
#print('CL_GE=',simulation1.cl_ge)
#print('CD_GE=',simulation1.cd_ge)

#a0 = Case(name='a0', alpha=10, X_cg= aviao1.x_cg, Z_cg= aviao1.z_cg)
a_trim = Case(name='Trimmed', alpha=10, X_cg=aviao2.x_cg, Z_cg=aviao2.z_cg,  elevator=Parameter(name='elevator', constraint='Cm', value=0.0))
#a_trim = Case(name='Trimmed', alpha=10, elevator=Parameter(name='elevator', constraint='Cm', value=0.0))
#trimmed= Case(name='trimmed', X_cg=aviao1.x_cg, Z_cg=aviao1.z_cg, alpha=Parameter(name='alpha', constraint='Cm',value=0.0))

session=Session(geometry=aviao2.geometry,cases=[a_trim])
results= session.get_results()
with open('out.json', 'w') as f:
        f.write(json.dumps(results))
#session.show_geometry()
aviao1.show_geometry()

#mass= mtow(simulation1.p, simulation1.t, simulation1.v, simulation1.prototype.m, simulation1.prototype.s, simulation1.cl_ge[0], simulation1.clmax, simulation1.cd_ge[0], simulation1.cd[0], g= 9.81, mu= 0.03, n= 1.2, gamma= 0)
#print(mass)

#time.sleep(0)
'''
fig, ax = plt.subplots(figsize=(10,6))
x = np.linspace(0,20, 200)
y= np.zeros(200)
for e in range(len(x)):
    i= x[e]
    y[e]= f_d_sol(i, simulation1.p, simulation1.t, simulation1.prototype.m, simulation1.prototype.s, simulation1.cl_ge[0], simulation1.clmax, simulation1.cd_ge[0])
ax.plot(x, y, 'r-', linewidth=2, alpha=0.6) 
plt.grid()
ax.set_xlabel('v') 
ax.set_ylabel('distsol')
#ax.set_xticks(np.arange(0, 21, 5))
#ax.set_yticks(np.arange(0, 2.5, 0.2))
plt.axhline(color='k', lw=0.8)
plt.axvline(color='k', lw=0.8)
ax.set_title('dist_sol x v')
plt.show()
'''