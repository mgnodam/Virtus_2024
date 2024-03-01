from prototype import *
from simulator import *
from performance import *
import matplotlib.pyplot as plt
import time

"""
Este arquivo contém alguns testes que foram úteis para debugging durante o desenvolvimento do código.
"""

aviao1= Prototype (w_cr= 0.56562231, w_ct= 0.30305969, w_z= 0.10866631, w_inc= 0.09366175, eh_b= 1.3, eh_c= 0.29018557, eh_inc= -0.56474704, ev_b= 0.22687644, eh_x= 0.85862047, eh_z= 0.25888654, motor_x= -0.1, motor_z= 0.3, ge= False)
aviao1_ge= Prototype (w_cr= 0.56562231, w_ct= 0.30305969, w_z= 0.10866631, w_inc= 0.09366175, eh_b= 1.3, eh_c= 0.29018557, eh_inc= -0.56474704, ev_b= 0.22687644, eh_x= 0.85862047, eh_z= 0.25888654, motor_x= -0.1, motor_z= 0.3, ge= True)
aviao2= Prototype ( w_cr= 0.5550223752921603, w_ct= 0.32440387770404855, w_z= 0.21381808524016974, w_inc= 0.202664347310206, eh_b= 1.2, eh_c= 0.3, eh_inc= 3.0, ev_b= 0.20350832048754716, eh_x= 1.1162955896906936, eh_z= 0.21434295817757107, motor_x= -0.16789474310742902, motor_z= 0.3, ge= False)
aviao2_ge= Prototype ( w_cr= 0.5550223752921603, w_ct= 0.32440387770404855, w_z= 0.21381808524016974, w_inc= 0.202664347310206, eh_b= 1.2, eh_c= 0.3, eh_inc= 3.0, ev_b= 0.20350832048754716, eh_x= 1.1162955896906936, eh_z= 0.21434295817757107, motor_x= -0.16789474310742902, motor_z= 0.3, ge= True)
aviao3= Prototype ( w_cr= 0.57, w_ct= 0.33354097292827256, w_z= 0.21305598815840998, w_inc= -1, eh_b= 1.1546734224464779, eh_c= 0.3, eh_inc= 0, ev_b= 0.15, eh_x= 1.1363659972048326, eh_z= 0.2, motor_x= -0.18738468275339834, motor_z= 0.3, ge= False)
aviao3_ge= Prototype ( w_cr= 0.57, w_ct= 0.33354097292827256, w_z= 0.21305598815840998, w_inc= -1, eh_b= 1.1546734224464779, eh_c= 0.3, eh_inc= 0, ev_b= 0.15, eh_x= 1.1363659972048326, eh_z= 0.2, motor_x= -0.18738468275339834, motor_z= 0.3, ge= True)
#aviao4= Prototype ( w_cr= 0.50, w_ct= 0.44, w_z= 0.20, w_inc= 0, eh_b= 0.9, eh_c= 0.2, eh_inc= -1, ev_b= 0.2, eh_x= 1, eh_z= 0.4, motor_x= -0.3, motor_z= 0.24, ge= False)
#aviao4_ge= Prototype ( w_cr= 0.50, w_ct= 0.44, w_z= 0.20, w_inc= 0, eh_b= 0.9, eh_c= 0.2, eh_inc= -1, ev_b= 0.2, eh_x= 1, eh_z= 0.4, motor_x= -0.3, motor_z= 0.24, ge= True)
aviao5= Prototype ( w_cr= 0.50, w_ct= 0.44, w_z= 0.18, w_inc= 0, eh_b= 0.9, eh_c= 0.25, eh_inc= -3, ev_b= 0.2, eh_x= 1, eh_z= 0.25, motor_x= -0.1, motor_z= 0.24, ge= False)
aviao5_ge= Prototype ( w_cr= 0.50, w_ct= 0.44, w_z= 0.18, w_inc= 0, eh_b= 0.9, eh_c= 0.25, eh_inc= -3, ev_b= 0.2, eh_x= 1, eh_z= 0.25, motor_x= -0.1, motor_z= 0.24, ge= True)
aviao6= Prototype ( w_cr= 0.57, w_ct= 0.3790322580645161, w_z= 0.18, w_inc= -2.142857142857143, eh_b= 1.1746031746031744, eh_c= 0.26, eh_inc= -1.1904761904761907, ev_b= 0.24, eh_x= 1.0507936507936508, eh_z= 0.25, motor_x= -0.21774193548387094, ge= False)
aviao6_ge= Prototype ( w_cr= 0.57, w_ct= 0.3790322580645161, w_z= 0.18, w_inc= -2.142857142857143, eh_b= 1.1746031746031744, eh_c= 0.26, eh_inc= -1.1904761904761907, ev_b= 0.24, eh_x= 1.0507936507936508, eh_z= 0.25, motor_x= -0.21774193548387094, ge= True)


print('Peso vazio:', aviao6.pv, 
      'X_cg:',aviao6.x_cg, 
      'Z_cg:',aviao6.z_cg)

print('Comprimento do boom:', aviao6.boom_l)


simulation1= Simulator(aviao6,aviao6_ge)

simulation1.scorer()

#simulation1.run_a()
#simulation1.run_stall()
#simulation1.run_ge()
#print('CL=',simulation1.cl)
#print('CD=',simulation1.cd)
#print('CLmax=', simulation1.clmax)
#print('CL_GE=',simulation1.cl_ge)
#print('CD_GE=',simulation1.cd_ge)

alpha_cases=[]

for a in range(0,25):
    a_case= Case(name='a'+str(a), alpha=a, X_cg= aviao6.x_cg, Z_cg= aviao6.z_cg)
    alpha_cases.append(a_case)


a0 = Case(name='a0', alpha=0, X_cg= aviao6.x_cg, Z_cg= aviao6.z_cg)
a_trim = Case(name='a10', alpha=0, X_cg=aviao6.x_cg, Z_cg=aviao6.z_cg,  elevator=Parameter(name='elevator', constraint='Cm', value=0))
beta= Case(name='dutch_roll', beta=5, bank=5, X_cg=aviao6.x_cg, Z_cg=aviao6.z_cg)
#trimmed = Case(name='Trimmed', alpha=10, elevator=Parameter(name='elevator', constraint='Cm', value=0.0))
aviao6.show_geometry()

trimmed= Case(name='trimmed', X_cg=aviao6.x_cg, Z_cg=aviao6.z_cg, alpha=Parameter(name='a', constraint='Cm',value=0.0))

session=Session(geometry=aviao6.geometry,cases=[beta])

session._run_analysis


results= session.get_results()

with open('out6.json', 'w') as f:
        f.write(json.dumps(results))
#time.sleep(1000)

#mass= mtow(simulation1.p, simulation1.t, simulation1.v, simulation1.prototype.m, simulation1.prototype.s, simulation1.cl_ge[0], simulation1.clmax, simulation1.cd_ge[0], simulation1.cd[0], g= 9.81, mu= 0.03, n= 1.2, gamma= 0)
#print(mass)


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