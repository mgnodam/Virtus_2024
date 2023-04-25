from prototype import *
from simulator import *
from performance import *
import matplotlib.pyplot as plt
import time

aviao1= Prototype ( w_baf= 0.2, w_bt= 2.3, w_cr= 0.5371999324707349, w_ct= 0.63, w_z= 0.3355599220403599, w_inc= 0.0, w_wo= 0.0, eh_b= 1.3, eh_c= 0.2747593961304255, eh_inc= -0.948999247897511, ev_b= 0.20194664637788945, eh_x= 1.2, eh_z= 0.15888979890259508, x_cg= 0.3, z_cg= 0.2747023413120976,
ge=False)
aviao1_ge= Prototype( w_baf= 0.2, w_bt= 2.3, w_cr= 0.5371999324707349, w_ct= 0.63, w_z= 0.3355599220403599, w_inc= 0.0, w_wo= 0.0, eh_b= 1.3, eh_c= 0.2747593961304255, eh_inc= -0.948999247897511, ev_b= 0.20194664637788945, eh_x= 1.2, eh_z= 0.15888979890259508, x_cg= 0.3, z_cg= 0.2747023413120976,
ge=True)

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
a0 = Case(name='a0', alpha=0, X_cg= 0.3, Z_cg=0.27)
#trimmed= Case(name='trimmed', alpha=Parameter(name='alpha', constraint='Cm',value=0.0))
session=Session(geometry=aviao1.geometry,
        cases=[a0])
results= session.get_results()
#mass= mtow(simulation1.p, simulation1.t, simulation1.v, simulation1.prototype.m, simulation1.prototype.s, simulation1.cl_ge[0], simulation1.clmax, simulation1.cd_ge[0], simulation1.cd[0], g= 9.81, mu= 0.03, n= 1.2, gamma= 0)
#print(mass)
with open('out.json', 'w') as f:
        f.write(json.dumps(results))

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