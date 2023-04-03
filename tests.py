from prototype import *
from simulator import *
from performance import *
import matplotlib.pyplot as plt
import time

aviao1= Prototype( w_baf= 0.9, w_bt= 2.4886864070340415, w_cr= 0.5975868851952, w_ct= 0.5381150891133276, w_z= 0.07545691024680848, w_inc= -4.120454771745422, w_wo= 0.0, eh_b= 1.1983769793171646, eh_c= 0.39050050501385347, eh_inc= -2.221760712264008, ev_b= 0.16044966125505655, ev_c= 0.48207334453495154, eh_x= 1.9873489733060234, eh_z= 0.2874396071067858, x_cg= 0.35, z_cg= 0.1, ge=False)
aviao1_ge= Prototype( w_baf= 0.9, w_bt= 2.4886864070340415, w_cr= 0.5975868851952, w_ct= 0.5381150891133276, w_z= 0.07545691024680848, w_inc= -4.120454771745422, w_wo= 0.0, eh_b= 1.1983769793171646, eh_c= 0.39050050501385347, eh_inc= -2.221760712264008, ev_b= 0.16044966125505655, ev_c= 0.48207334453495154, eh_x= 1.9873489733060234, eh_z= 0.2874396071067858, x_cg= 0.35, z_cg= 0.1, ge=True)

aviao1.show_geometry()

simulation1= Simulator(aviao1,aviao1_ge)

simulation1.scorer()

#simulation1.run_a()
#simulation1.run_stall()
#simulation1.run_ge()
#print('CL=',simulation1.cl)
#print('CD=',simulation1.cd)
#print('CLmax=', simulation1.clmax)
#print('CL_GE=',simulation1.cl_ge)
#print('CD_GE=',simulation1.cd_ge)
#a0 = Case(name='a0', alpha=0, X_cg= 0.2, Z_cg=0.1)
#trimmed= Case(name='trimmed', alpha=Parameter(name='alpha', constraint='Cm',value=0.0))
#session=Session(geometry=aviao1.geometry,
#        cases=[a0])
#results= session.get_results()
#mass= mtow(simulation1.p, simulation1.t, simulation1.v, simulation1.prototype.m, simulation1.prototype.s, simulation1.cl_ge[0], simulation1.clmax, simulation1.cd_ge[0], simulation1.cd[0], g= 9.81, mu= 0.03, n= 1.2, gamma= 0)
#print(mass)
#with open('out.json', 'w') as f:
#        f.write(json.dumps(results))

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