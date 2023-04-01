import openmdao.api as om
from prototype import *
from simulator import *
from avlwrapper import *	


class Individual(om.ExplicitComponent):
    '''
    Classe responsável por formatar e simular o score de um indivíduo da classe Simulator() em um componente para a otimização no openMDAO
    '''
    # Definição de todas as variáveis de design a serem otimizadas
    def setup(self):
        self.add_input('w_baf', val= 0.5)
        self.add_input('w_bt', val= 2.4)
        self.add_input('w_cr', val= 0.5)
        self.add_input('w_ct', val= 0.8)
        self.add_input('w_z', val=0.1)
        self.add_input('w_inc', val= 0.0)
        self.add_input('w_wo', val= 0.0)
        self.add_input('eh_b', val= 0.8)
        self.add_input('eh_c', val= 0.3)
        self.add_input('eh_inc', val= 0.0)
        self.add_input('ev_b', val= 0.2)
        self.add_input('ev_cr', val= 0.3)
        self.add_input('ev_ct', val= 0.8)
        self.add_input('eh_x', val= 1.0)
        self.add_input('eh_z', val= 0.4)
        self.add_input('ev_x', val= 0.8)
        self.add_input('x_cg', val=0.28)
        self.add_input('z_cg', val=0.1)

        # Os outputs incluem a pontuação e possíveis restrições calculadas internamente em outro código
        self.add_output('score', val= -10.0)
        self.add_output('vht', val= 0.45)
        self.add_output('vvt', val= 0.06)
        self.add_output('cm0', val= 0.05)
        self.add_output('cma', val= -0.05)
        self.add_output('a_trim', val= 3)
        self.add_output('me', val= 0.1)
        self.add_output('cnb', val= 0.1)
        self.add_output('g_const', val= 2.9)

    # Aqui definimos o que vamos rodar para cada indivíduo
    def compute(self,inputs,outputs):
        # Antes, precisamos converter os inputs do openmdao (arrays) em floats para as classes e funções dos outros módulos
        w_baf= float(inputs['w_baf'])
        w_bt= float(inputs['w_bt'])
        w_cr= float(inputs['w_cr'])
        w_ct= float(inputs['w_ct'])
        w_z= float(inputs['w_z'])
        w_inc= float(inputs['w_inc'])
        w_wo= float(inputs['w_wo'])
        eh_b= float(inputs['eh_b'])
        eh_c= float(inputs['eh_c'])
        eh_inc= float(inputs['eh_inc'])
        ev_b= float(inputs['ev_b'])
        ev_cr= float(inputs['ev_cr'])
        ev_ct= float(inputs['ev_ct'])
        eh_x= float(inputs['eh_x'])
        eh_z= float(inputs['eh_z'])
        ev_x= float(inputs['ev_x'])
        x_cg= float(inputs['x_cg'])
        z_cg= float(inputs['z_cg'])

        # Construção dos indivíduos. Para facilitar, está sendo construindo um indivíduo com e o outro sem efeito solo
        prototype= Prototype(w_baf, w_bt, w_cr, w_ct, w_z, w_inc, w_wo, eh_b, eh_c, eh_inc, ev_b, ev_cr, ev_ct, eh_x, eh_z, ev_x, x_cg, z_cg)
        prototype_ge= Prototype(w_baf, w_bt, w_cr, w_ct, w_z, w_inc, w_wo, eh_b, eh_c, eh_inc, ev_b, ev_cr, ev_ct, eh_x, eh_z, ev_x, x_cg, z_cg, ge=True)

        simulator= Simulator(prototype, prototype_ge)

        # Rodando a pontuação de cada indivíduo
        score= simulator.scorer()
        
        # Definindo os outputs dessa computação. Nesse caso, todos os outputs do indivíduo saem daqui mesmo
        outputs['score'] = score
        outputs['vht'] = prototype.vht
        outputs['vvt'] = prototype.vvt
        outputs['cm0'] = simulator.cm[0]
        outputs['cma'] = simulator.cma[0]
        outputs['a_trim'] = simulator.a_trim
        outputs['me'] = simulator.me
        outputs['cnb'] = simulator.cnb[0]
        outputs['g_const']= prototype.g_const
