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
individual_inputs= ['w_baf', 'w_bt', 'w_cr', 'w_ct', 'w_z', 'w_inc', 'w_wo', 'eh_b', 'eh_c', 'eh_inc', 'ev_b', 'eh_x', 'eh_z', 'x_cg', 'z_cg']
individual_outputs= ['score', 'vht', 'vvt', 'cm0', 'cma', 'a_trim', 'me', 'g_const', 'ar', 'eh_ar', 'cg_con']

#Subsistema de avaliação
prob.model.add_subsystem('individual_scorer', Individual(), promotes_inputs= individual_inputs)

prob.model.set_input_defaults('w_baf', 0.25)
prob.model.set_input_defaults('w_bt', 2.3)
prob.model.set_input_defaults('w_cr', 0.55)
prob.model.set_input_defaults('w_ct', 0.75)
prob.model.set_input_defaults('w_z', 0.3)
prob.model.set_input_defaults('w_inc', 0.5)
prob.model.set_input_defaults('w_wo', -1.0)
prob.model.set_input_defaults('eh_b', 1.18)
prob.model.set_input_defaults('eh_c', 0.28)
prob.model.set_input_defaults('eh_inc', -2.0)
prob.model.set_input_defaults('ev_b', 0.20)
prob.model.set_input_defaults('eh_x', 1.1)
prob.model.set_input_defaults('eh_z', 0.15)
prob.model.set_input_defaults('x_cg', 0.28)
prob.model.set_input_defaults('z_cg', 0.25)

#Setup do driver
prob.driver = om.DifferentialEvolutionDriver()
prob.driver.options['debug_print']= ['desvars', 'nl_cons', 'totals']    # Apenas pra debug no log
prob.driver.options['pop_size']= 48                                     # Muito importante um número bom pra explorar todo o espaço de design. Quanto mais variável maior precisa ser a pop.
prob.driver.options['penalty_parameter']= 15.0                          # Necessário para controlar a violação das restrições
prob.driver.options['penalty_exponent']= 2.0
prob.driver.options['run_parallel']= False                            # Só funciona se conseguir fazer o programa rodar no mpi, fácil pelo wsl

#Adição de um recorder para guardar o histórico da otimização e possibilitar a visualização
prob.driver.add_recorder(om.SqliteRecorder("cases.db"))
prob.driver.recording_options['record_objectives'] = True
prob.driver.recording_options['record_constraints'] = True
prob.driver.recording_options['record_desvars'] = True

# Adicionando todas as variáveis de design
prob.model.add_design_var('w_bt', lower= 2.30, upper= 2.30)
prob.model.add_design_var('w_cr', lower= 0.50, upper= 0.57)
prob.model.add_design_var('w_ct', lower= 0.63, upper= 0.8)
prob.model.add_design_var('w_baf', lower=0.20, upper= 0.56)
prob.model.add_design_var('w_z', lower= 0.20, upper= 0.40)
prob.model.add_design_var('w_inc', lower= 0, upper= 3)
prob.model.add_design_var('w_wo', lower= -5, upper= 0)
prob.model.add_design_var('eh_b', lower= 1.0, upper= 1.3)
prob.model.add_design_var('eh_c', lower= 0.25, upper= 0.30)
prob.model.add_design_var('eh_inc', lower= -3.0, upper= 0.0)
prob.model.add_design_var('eh_x', lower= 0.8, upper= 1.2)
prob.model.add_design_var('eh_z', lower= 0.15, upper= 0.35)
prob.model.add_design_var('ev_b', lower= 0.15, upper= 0.3)
prob.model.add_design_var('x_cg', lower= 0.25, upper= 0.30)
prob.model.add_design_var('z_cg', lower= 0.25, upper= 0.30)

prob.model.add_objective('individual_scorer.score', scaler= -1)

# Adicionando as restrições e seus limites superiores e inferiores.
# Ele não zera as pontuações dos indivíduos que violam as restrições, apenas penaliza. As configurações de penalização influenciam bastante... Principalmente se ele encontrar -
# - alguma falha do avl (ex.: uma asa com a ponta entrando nela de novo dava um cl absurdamente alto e ele otimizava nessa direção nas primeiras versões)
# Sim, daria pra zerar a pontuação de qualquer indivíduo que violasse alguma dessas restrições, só que isso é bem ineficiente (testado)
prob.model.add_constraint('individual_scorer.g_const', upper=2.9, scaler= 2)
prob.model.add_constraint('individual_scorer.ar', lower=5.0)
prob.model.add_constraint('individual_scorer.eh_ar', upper=4.75)
prob.model.add_constraint('individual_scorer.vht', lower= vht_min, upper= vht_max, scaler= 0)
prob.model.add_constraint('individual_scorer.vvt', lower= vvt_min, upper= vvt_max, scaler= 100)
prob.model.add_constraint('individual_scorer.cm0', lower= cm0_min, scaler= 100)
prob.model.add_constraint('individual_scorer.cma', upper= cma_max, scaler= 5)
prob.model.add_constraint('individual_scorer.a_trim', lower= a_trim_min, upper= a_trim_max, scaler= 10)
prob.model.add_constraint('individual_scorer.me', lower= me_min, upper= me_max, scaler= 10)
prob.model.add_constraint('individual_scorer.cg_con', lower= 0, scaler= 10)

# Settando e rodando o driver
prob.setup()

prob.run_driver()

# Incluindo um report em html ao fim da otimização. Não parece tão útil não.
# Se parar o programa com um CTRL+C nem mostra
prob.driver.scaling_report()