import json
from avlwrapper import *
from prototype import *
from performance import *
from stability import *
import numpy as np

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
        self.cl= {}
        self.cd= {}
        self.cm= {}
        self.cma= {}
        self.xnp= {}
        self.cnb= {}
        self.cl_ge= {}
        self.cd_ge= {}
        self.a_trim= -6; self.me= -0.2 # Caso não consiga calcular, a pontuação será zerada, mas não dará erro por não ter um valor de a_trim
        
        # Cl e Cd são armazenados em dicionários com elementos [Ângulo de ataque: Coeficiente]

    # Função que verifica se o estol está ocorrendo ou não, retorna um booleano
    # O método utilizado é a verificação do Clmax para cada secção da asa. Copiando o Xf.
    # Provavelmente será (v03 atualmente) necessário fazer uma espécie de ponderação na transição de perfis
    def check_stall(self, results):

        stall= False

        for panel_n in range(int(len(results['a']['StripForces']['Wing']['Yle'])/2)):
            if results['a']['StripForces']['Wing']['Yle'][panel_n] <= self.prototype.w_baf:
                clmax= self.prototype.w_root_clmax

            else:
                clmax= self.prototype.w_tip_clmax

            if results['a']['StripForces']['Wing']['cl'][panel_n] >= clmax:
                stall= True
                print('Asa em estol')
                return stall

            else:
                stall= False

            return stall

    # Cria e roda um caso de angulo de ataque definido e armazena cl e cd
    def run_a(self, a= 0):

        a_case = Case(name='a', alpha=a, density= self.rho, Mach= self.mach, velocity= self.v)

        print(str.format('Calculando coeficientes em alfa = {}',a))

        session = Session(geometry=self.prototype.geometry, cases=[a_case])
        a_results = session.get_results()

        try:
            if not(self.check_stall(a_results)):
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
            print('A asa ja se encontra estolada em alfa=', a, 'graus.', 'Os coeficientes nao foram escritos')
            raise

    #LEMBRANDO... EFEITO SOLO NO VLM É CONHECIDO POR SUPERESTIMAÇÃO, PRINCIPALMENTE EM H/C < 0.7
    def run_ge(self):
        
        print('Calculando coeficientes em efeito solo')

        a_case = Case(name='a', alpha=0, density= self.rho, Mach= self.mach, velocity= self.v)

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

    def run_trim(self):

        trimmed= Case(name='trimmed', alpha=Parameter(name='alpha', constraint='Cm',value=0.0))
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
        #print('CL=', self.cl)
        #print('CD=', self.cd)
        #print('CL_ge=', self.cl_ge)
        #print('CD_ge=', self.cd_ge)
        print('Cm=', self.cm)
        print('Cma=', self.cma)
        print('Xnp=', self.xnp)
        print('X_CG=', self.prototype.x_cg)
        print('ME=', self.me)
        #print('cnb=', self.cnb)
        print('vht=', self.prototype.vht)
        #print('vvt=', self.prototype.vvt)
        print('a_trim=', self.a_trim)

    # Método que checa se o protótipo é estável ou não.
    def check_stab(self):

        stab_check(self.prototype.vht, self.cm[0], self.cma[0], self.a_trim, self.xnp[0], self.prototype.x_cg, self.prototype.w_cr, self.prototype.vvt, self.cnb[0])

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

            #É possível descomentar alguns elementos abaixo para debugging
            
            #print('CL=', self.cl)
            #print('CD=', self.cd)
            #print('CLmax=', self.clmax)
            #print('No solo: CL=', self.cl_ge[0], 'CD=', self.cd_ge[0])
            #print('p=',self.p)
            #print('t=',self.t)
            #print('v=',self.v)
            #print('massa=',self.prototype.m)
            #print('s=',self.prototype.s)
            #print('cl_ge=',self.cl_ge[0])
            #print('clmax=', self.clmax)
            #print('cd_ge=',self.cd_ge[0])
            #print('cd=',self.cd[0])
        
        try:
            #A otimização busca um mínimo, portanto a nossa pontuação é espelhada aqui
            self.score= -mtow(self.p, self.t, self.v, self.prototype.m, self.prototype.s, self.cl_ge[0], self.clmax, self.cd_ge[0], self.cd[0], g= 9.81, mu= 0.03, n= 1.2, gamma= 0)
            print('MTOW CALCULADO COM SUCESSO')
            self.prototype.m= -self.score
            self.print_coeffs()   
            print('########## MTOW=', -self.score,'##########')

        except:
            print('FALHA NA SIMULACAO DE MTOW')
            self.score=0

        '''
        try:
            if not self.check_stab():
                print('XXXXXXXXXX PROTOTIPO INSTAVEL, PONTUACAO ZERADA XXXXXXXXXX')
                self.score=0
        
        except:
            print('FALHA NA ANALISE DE ESTABILIDADE')
            self.score= 0
        '''

        return self.score