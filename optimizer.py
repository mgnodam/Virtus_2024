import openmdao.api as om
from prototype import *
from simulator import *
from individual import *
from performance import *

'''
Programa de otimização, que cria e avalia indivíduos da classe Individual(), otimizando-os a partir do driver escolhido, futuramente pode haver a implementação de outros módulos
e a necessidade da inclusão de ciclos
'''
#Criação do problema
prob= om.Problem()

#Definição dos subsistemas
individual_inputs= ['w_baf', 'w_bt', 'w_cr', 'w_ct', 'w_z', 'w_inc', 'w_wo', 'eh_b', 'eh_c', 'ev_b', 'ev_c', 'eh_x', 'eh_z', 'x_cg', 'z_cg']
individual_outputs= ['score', 'vht', 'vvt', 'cm0', 'cma', 'a_trim', 'me', 'cnb', 'g_const', 'ar', 'eh_ar']

#Subsistema de avaliação
prob.model.add_subsystem('individual_scorer', Individual(), promotes_inputs= individual_inputs)

prob.model.set_input_defaults('w_baf', 0.54)
prob.model.set_input_defaults('w_bt', 2.48)
prob.model.set_input_defaults('w_cr', 0.59)
prob.model.set_input_defaults('w_ct', 0.72)
prob.model.set_input_defaults('w_z', 0.07)
prob.model.set_input_defaults('w_inc', -1.0)
prob.model.set_input_defaults('w_wo', -1.0)
prob.model.set_input_defaults('eh_b', 1.18)
prob.model.set_input_defaults('eh_c', 0.38)
#prob.model.set_input_defaults('eh_inc', -4.5)
prob.model.set_input_defaults('ev_b', 0.25)
prob.model.set_input_defaults('ev_c', 0.48)
prob.model.set_input_defaults('eh_x', 1.4)
prob.model.set_input_defaults('eh_z', 0.15)
prob.model.set_input_defaults('x_cg', 0.32)
prob.model.set_input_defaults('z_cg', 0.12)

#Setup do driver
prob.driver = om.DifferentialEvolutionDriver()
prob.driver.options['debug_print']= ['desvars', 'nl_cons', 'totals']    # Apenas pra debug no log
prob.driver.options['pop_size']= 48                                     # Muito importante um número bom pra explorar todo o espaço de design. Quanto mais variável maior a pop.
prob.driver.options['penalty_parameter']= 15                            # Parâmetros de penalidade ajudam bastante, é bom ajustar se ele estiver violando-as
prob.driver.options['penalty_exponent']= 1.0
prob.driver.options['run_parallel']= True                              # Só funciona se conseguir fazer o programa rodar no mpi, fácil pelo wsl

#Adição de um recorder para guardar o histórico da otimização e possibilitar a visualização
prob.driver.add_recorder(om.SqliteRecorder("cases.db"))
prob.driver.recording_options['record_objectives'] = True
prob.driver.recording_options['record_constraints'] = True
prob.driver.recording_options['record_desvars'] = True

# Adicionando todas as variáveis de design
prob.model.add_design_var('w_baf', lower=0.2, upper= 0.9)
prob.model.add_design_var('w_bt', lower= 2.0, upper= 2.5)
prob.model.add_design_var('w_cr', lower= 0.2, upper= 0.6)
prob.model.add_design_var('w_ct', lower= 0.2, upper= 1.0)
prob.model.add_design_var('w_z', lower= 0.05, upper= 0.3)
prob.model.add_design_var('w_inc', lower= -5, upper= 5)
prob.model.add_design_var('w_wo', lower= -5, upper= 0)
prob.model.add_design_var('eh_b', lower= 0.5, upper= 1.2)
prob.model.add_design_var('eh_c', lower= 0.2, upper= 0.4)
#prob.model.add_design_var('eh_inc', lower= -0.1, upper= 0.1)
prob.model.add_design_var('ev_b', lower= 0.1, upper= 0.3)
prob.model.add_design_var('ev_c', lower= 0.2, upper= 0.5)
prob.model.add_design_var('eh_x', lower= 1.0, upper= 1.5)
prob.model.add_design_var('eh_z', lower= 0.05, upper= 0.3)
prob.model.add_design_var('x_cg', lower= 0.2, upper= 0.35)
prob.model.add_design_var('z_cg', lower= 0.1, upper= 0.3)

# Adicionando o único objetivo atualmente (27/03)
prob.model.add_objective('individual_scorer.score')

# Adicionando as restrições e seus limites superiores e inferiores.
# Ele não zera as pontuações dos indivíduos que violam as restrições, apenas penaliza. As configurações de penalização influenciam bastante... Principalmente se ele encontrar -
# - alguma falha do avl (ex.: uma asa com a ponta entrando nela de novo dava um cl absurdamente alto e ele otimizava nessa direção nas primeiras versões)
# Sim, daria pra zerar a pontuação de qualquer indivíduo que violasse alguma dessas restrições, só que isso é bem ineficiente (testado)
prob.model.add_constraint('individual_scorer.g_const', upper=2.9)
prob.model.add_constraint('individual_scorer.ar', lower=4.0)
prob.model.add_constraint('individual_scorer.eh_ar', upper=4.0)
prob.model.add_constraint('individual_scorer.vht', lower= vht_min, upper= vht_max)
prob.model.add_constraint('individual_scorer.vvt', lower= vvt_min)
prob.model.add_constraint('individual_scorer.cm0', lower= cm0_min)
prob.model.add_constraint('individual_scorer.cma', upper= cma_max)
prob.model.add_constraint('individual_scorer.a_trim', lower= a_trim_min, upper= a_trim_max)
prob.model.add_constraint('individual_scorer.me', lower= me_min, upper= me_max)
prob.model.add_constraint('individual_scorer.cnb', lower= cnb_min)

# Settando e rodando o driver
prob.setup()

prob.run_driver()

# Incluindo um report em html ao fim da otimização. Não parece tão útil não.
# Se parar o programa com um CTRL+C nem mostra
prob.driver.scaling_report()