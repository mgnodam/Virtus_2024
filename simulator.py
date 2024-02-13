import json
from avlwrapper import *
from prototype import *
from performance import *
from stability import *
import numpy as np
import pandas as pd

class Simulator():

    '''
    Classe responsável por criar os cases e realizar as simulações no AVL, tipicamente recebe  geometria no formato Prototype().geometry. Também possui inputs de condições 
    atmosféricas e de parâmetros de casos. Que serão fixos ao longo de toda a otimização.
    Cada indivíduo dessa classe ainda corresponde a uma aeronave, porém a partir daqui inclui suas simulações e parâmetros de simulação.
    '''
    # Cada indivíduo no simulador possui uma geometria sem e com o efeito solo. Isso foi uma solução simples encontrada para incluir todos os coeficientes em um mesmo indivíduo -
    # - para a otimização. Se precisássemos de um caso de transição bastaria simular de novo o efeito solo, mas deslocando o plano de simetria em z para baixo com uma nova vari -
    # - ável da classe protótipo.
    def __init__(self, prototype, prototype_ge, p= 905.5, t= 25, v=10, mach=0.00):

        self.prototype= prototype
        self.prototype_ge= prototype_ge
        self.p= p
        self.t= t
        self.v= v
        self.rho = rho(p=p,t=t)
        self.mach = mach
        self.deflex= {}
        self.cl= {}
        self.cd= {}
        self.cm= {}
        self.cma= {}
        self.xnp= {}
        self.cnb= {}
        self.cl_ge= {}
        self.cd_ge= {}
        self.a_trim= -6; self.me= -0.2 # Caso não consiga calcular, a pontuação será zerada, mas não dará erro por não ter um valor de a_trim. Algumas simulações dão erro.
        
        # Cl e Cd são armazenados em dicionários com elementos [Ângulo de ataque: Coeficiente]

    # Função que verifica se o estol está ocorrendo ou não, retorna um booleano
    # O método utilizado é a verificação do Clmax para cada secção da asa. Copiando o Xf.
    def check_stall(self, results):

        stall= False
        b_stall=0

        for panel_n in range(int(len(results['a']['StripForces']['Wing']['Yle']))):             # Tinha um /2 aqui, acredito que era um erro
            if results['a']['StripForces']['Wing']['Yle'][panel_n] <= self.prototype.w_baf/2:
                clmax= self.prototype.w_root_clmax

                if results['a']['StripForces']['Wing']['cl'][panel_n] >= clmax:
                    stall= True
                    b_stall= results['a']['StripForces']['Wing']['Yle'][panel_n] / (self.prototype.w_bt/2) #b_stall é o ponto de estol em % da envergadura

                    return stall, b_stall

                else:
                    stall= False

            else:
                af_len= (self.prototype.w_bt - self.prototype.w_baf)/2
                af_len_perc= (results['a']['StripForces']['Wing']['Yle'][panel_n] - self.prototype.w_baf/2)/af_len
                clmax= (af_len_perc)*self.prototype.w_tip_clmax + (1-af_len_perc)*self.prototype.w_root_clmax           # Interpolando os clmáx na região afilada

                if results['a']['StripForces']['Wing']['cl'][panel_n] >= clmax:
                    stall= True
                    b_stall= results['a']['StripForces']['Wing']['Yle'][panel_n] / (self.prototype.w_bt/2) #b_stall é o ponto de estol em % da envergadura
                    
                    return stall, b_stall

                else:
                    stall= False

        return stall, b_stall

    # Cria e roda um caso de angulo de ataque definido e armazena os coeficientes desejados
    def run_a(self, a= 0):

        #a_case = Case(name='a', alpha=a, density= self.rho, Mach= self.mach, velocity= self.v, X_cg=self.prototype.x_cg, Z_cg=self.prototype.z_cg)

        #A definição de caso abaixo irá retornar as polares trimadas
        a_case = Case(name='a', alpha=a, density= self.rho, Mach= self.mach, velocity= self.v, X_cg=self.prototype.x_cg, Z_cg=self.prototype.z_cg, elevator=Parameter(name='elevator', constraint='Cm', value=0.0))

        #print(str.format('Calculando coeficientes em alfa = {}',a))

        session = Session(geometry=self.prototype.geometry, cases=[a_case])
        a_results = session.get_results()

        try:
            if not(self.check_stall(a_results)[0]):
                self.deflex[a]= a_results['a']['Totals']['elevator']
                self.cl[a]= a_results['a']['Totals']['CLtot']
                self.cd[a]= a_results['a']['Totals']['CDtot']
                self.cm[a]= a_results['a']['Totals']['Cmtot']
                self.cma[a]= a_results['a']['StabilityDerivatives']['Cma']
                self.xnp[a]= a_results['a']['StabilityDerivatives']['Xnp']
                self.cnb[a]= a_results['a']['StabilityDerivatives']['Cnb']

                return a_results
            
            else:
                raise

        except:
            #print('A asa se encontra estolada em alfa=', a, 'graus.')
            print('Estol em', self.check_stall(a_results)[1], '%', 'da envergadura')
            raise

    #LEMBRANDO... EFEITO SOLO NO VLM É CONHECIDO POR SUPERESTIMAÇÃO, PRINCIPALMENTE EM H/C < 0.7
    def run_ge(self):
        
        print('Calculando coeficientes em efeito solo')

        a_case = Case(name='a', alpha=0, density= self.rho, Mach= self.mach, velocity= self.v, X_cg=self.prototype.x_cg, Z_cg=self.prototype.z_cg)

        session = Session(geometry=self.prototype_ge.geometry, cases=[a_case])
        a_results = session.get_results()

        self.cl_ge[0]= a_results['a']['Totals']['CLtot']
        self.cd_ge[0]= a_results['a']['Totals']['CDtot']

        return a_results

    # Roda uma simulação para cada ângulo de ataque até o estol
    def run_stall(self):
    
         
        for a in np.arange(5,31,1):
            
            try:
                self.run_a(a)

            except:
                self.a_stall= a-1
                self.clmax= self.cl[a-1]
                print('Ângulo de estol entre=', a-1,'e', a, 'graus')
                break
    
    # Roda uma simulação com o avião trimmado com momento zerado, pra encontrar o ângulo de trimmagem e a margem estática
    def run_trim(self):

        trimmed= Case(name='trimmed', alpha=Parameter(name='alpha', constraint='Cm',value=0.0), X_cg=self.prototype.x_cg, Z_cg=self.prototype.z_cg)
        session=Session(geometry= self.prototype.geometry, cases=[trimmed])
        trim_results = session.get_results()

        self.a_trim= trim_results['trimmed']['Totals']['Alpha']
        self.me= me(self.xnp[0], self.prototype.x_cg, self.prototype.w_cr)

    # Método que escreve os resultados mais recentes em um arquivo json nomeado
    def write_results(self, filename):
        with open(filename+'.json', 'w') as f:
            f.write(json.dumps(self.results))
    
    # Método que imprime os coeficientes armazenados
    def print_coeffs(self):

        aero_coeffs= pd.DataFrame([self.cl, self.cd, self.cm, self.deflex], index= ['CL','CD','CM','Prof'])
        aero_coeffs= aero_coeffs.T

        print('Coeficientes aerodinâmicos:\n', aero_coeffs, sep='')
        print('CL_ge=', self.cl_ge[0])
        print('CD_ge=', self.cd_ge[0])
        print('Envergadura=', round(self.prototype.w_bt,3),'m')
        print('Transicao=', round(self.prototype.w_baf/self.prototype.w_bt,3)*100,'%','da envergadura')
        print('Área alar=', round(self.prototype.s_ref,3), 'm^2')
        print('AR=', round(self.prototype.ar,2))
        print('AR do EH=', round(self.prototype.eh_ar,2))
        print('M.A.C.=', round(self.prototype.mac,3), 'm')
        print('VHT=', round(self.prototype.vht,4))
        print('VVT=', round(self.prototype.vvt,4))
        print('X_CG=', round(self.prototype.x_cg/self.prototype.w_cr,3), '% ', 'da corda da asa')
        print('Z_CG', round(self.prototype.z_cg,3), 'm do chao')
        print('CG=', round(self.prototype.low_cg,3), 'm abaixo da asa')
        print('Ângulo de trimagem=', round(self.a_trim,2), 'graus')
        print('Margem Estatica=', round(self.me,3))
        #print('g_const=', round(self.prototype.g_const,3))
        
    # Método que realiza a simulação e pontuação da aeronave. No caso de qualquer erro, a pontuação do indivíduo é zerada
    def scorer(self):

        try:
            self.run_a(0)
            print('CASO ALFA 0 CONCLUIDO')
        except:
            print('FALHA NA SIMULACAO DE ALFA 0')
            self.score=0

        try:
            self.run_ge()
            print('CASO EFEITO SOLO CONCLUIDO')
        except:
            print('FALHA NA SIMULACAO EM EFEITO SOLO')
            self.score=0

        try:
            self.run_stall()   
            print('CASO ESTOL CONCLUIDO')  
        except:
            print('FALHA NA SIMULACAO ATE O ESTOL')
            self.score=0

        try:
            self.run_trim()   
            print('CASO TRIMADO CONCLUIDO')  
        except:
            print('FALHA NA SIMULACAO DE TRIMAGEM')
            self.score=0
            a_trim= 0
        
        try:
            #A otimização busca um mínimo, portanto a nossa pontuação é espelhada aqui
            self.mtow= mtow(self.p, self.t, self.v, self.prototype.pv, self.prototype.s_ref, self.cl_ge[0], self.clmax, self.cd_ge[0], self.cd[0], g= 9.81, mu= 0.03, n= 1.2, gamma= 0)
            print('MTOW CALCULADO COM SUCESSO')
            self.prototype.m= self.mtow

            self.score= self.mtow - self.prototype.pv

            self.print_coeffs()                                    # Printa os coeficientes desejados após a otimização
            
            print('########## MTOW=', round(self.mtow,3),'##########')
            print('########## Peso Vazio=', round(self.prototype.pv,3),'##########')
            print('########## Carga paga=', round(self.score,3),'##########')
            #print('v_decol=', round(1.2*v_estol(self.p, self.t, self.prototype.m, self.prototype.s_ref, self.clmax, g=9.81),3))
            
            
        except: 
            print('FALHA NA SIMULACAO DE MTOW')
            self.score=0
            

        '''
        ##### PENALIDADES MANUAIS #####

        vht_pen= 0
    
        if self.prototype.vht > vht_max:
            vht_pen= 2+ 5*(self.prototype.vht - vht_max)

        if self.prototype.vht < vht_min:
            vht_pen= 2+ 5*(vht_min - self.prototype.vht)

        pen= vht_pen

        self.score= self.score - pen
        '''

        return self.score