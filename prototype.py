from avlwrapper import *
from mass import *
from support import *

def h_const(ev_z,ev_b):
    '''
    Função que calcula o valor relacionado à restrição geométrica

    w_bt[m],ev_z[m],ev_b[m] -> g_const[m]
    '''
    return ev_z+ev_b

def s_ref(w_cr,w_baf,w_ct,w_bt):
    '''
    Função que calcula a área alar de uma asa trapezoidal

    w_cr[m],w_baf[m],w_ct[m],w_bt[m] -> s_ref[m^2]
    '''
    return (w_cr*w_baf + ((w_cr+w_ct)/2)*(w_bt-w_baf))

def c_med(s_ref,w_bt):
    '''
    Função que calcula a corda média de uma asa trapezoidal

    s_ref[m],w_bt[m] -> c_med[m]
    '''
    return s_ref/w_bt

def ref_span(w_baf,mac,w_cr,w_bt):
    '''
    Função que calcula a distância entre as cordas médias, envergadura de referência

    '''
    return w_baf+(mac/w_cr)*(w_bt-w_baf)

def lvt(ev_x, ev_c, x_cg):
    '''
    Função que calcula a distância entre o EV e o CG em uma empenagem em H
    '''
    # Entra a distância em y também
    return (ev_x + (ev_c/4))-x_cg

def svt(ev_c,ev_b):
    '''
    Função que calcula a área de ***DOIS*** EV retangulares
    '''
    return 2*(ev_c)*ev_b

def vvt(lvt,svt,w_bt,s_ref):
    '''
    Função que calcula o volume de cauda vertical de uma empenagem em H com EV retangular
    '''
    return ((lvt*svt)/(w_bt*s_ref))

def sht(eh_b,eh_c):
    '''
    Função que calcula a área de um EH retangular
    '''
    return eh_b*eh_c

def lht(eh_x, eh_c, x_cg):
    '''
    Função que calcula a distância entre o EH e o CG
    '''
    return (eh_x + (eh_c/4))-x_cg

def vht(lht,sht,mac,s_ref):
    '''
    Função que calcula o volume de cauda horizontal de uma empenagem com EH retangular
    '''
    return (lht*sht)/(mac*s_ref)

def ar(b,s):
    '''
    Função que calcula a razão de aspecto de uma superfície utilizando a envergadura e área
    '''
    return (b**2)/s

def l_boom(fus_l, eh_x):
    '''
    Função que calcula o comprimento do tailboom em função do comprimento da fuselagem, posição do eh e corda da raíz. Assumindo o início do boom na metade da fuselagem
    '''

    return eh_x-fus_l*0.5   # Boom começando no meio da fuselagem


class Prototype():

    '''
    Classe responsável por construir a geometria no formato do AVL a partir dos parâmetros de interesse
    w= referente à asa, eh= referente ao eh, ev= referente ao ev, b= envergadura, c= corda, r=raíz, t=ponta, af= afilamento, x e z = pontos do bordo de ataque.
    m= massa, x e z cg = localização do CG. 
    ge liga ou desliga o efeito solo.
    O número de painéis no AVL é ajustado diretamente no código desta classe.
    '''

    def __init__(self, w_cr, w_ct, w_z, w_inc, eh_b, eh_c, eh_inc, ev_b, eh_x, eh_z, motor_x, motor_z= 0.24, w_wo= 0, ge= False):
        
        #w_ct são frações (0 a 1) de outra quantidade. Para facilitar a restrição na otimização

        #Asa:
        w_bt= 2.9- (eh_z+ev_b/2)               ####### Função exclusiva para a restrição de 2023 ###########
        w_ct= w_ct* w_cr            # O input de w_ct é porcentagem da corda da raíz (w_cr), convertendo para [m]
        w_baf= w_baf_opt(w_ct, w_bt, w_cr)  # O input de w_baf é porcentagem do ponto de transição (w_bt), otimizando para asa eliptica, convertendo para [m] 
        self.w_baf= w_baf           # Ponto de transição da envergadura
        self.w_bt= w_bt             # Envergadura total
        self.w_cr= w_cr             # Corda da raíz
        self.w_ct= w_ct             # Corda da ponta
        self.w_inc= w_inc           # Ângulo de incidência da asa
        self.w_wo= w_wo             # Washout na ponta da asa
        self.w_z= w_z               # Altura da asa em relação ao chão

        # EH           
        self.eh_b= eh_b             # Envergadura do EH
        self.eh_c= eh_c             # Corda do EH
        self.eh_inc= eh_inc         # Ângulo de incidência do EH
        self.eh_x= eh_x             # Distância horizontal do bordo de atque do EH, em relação ao bordo de ataque da asa
        self.eh_z= eh_z             # Distância vertical do bordo de atque do EH, em relação ao solo

        # EV
        ev_c= eh_c                  # Na configuração de empenagem em H a corda do ev é igual à do eh
        ev_x= eh_x                  # EV fixado com o EH
        ev_y= eh_b/2                # Fixando ev_y na ponta do eh
        ev_z= eh_z-ev_b/2           # Ajuste da altura do EV, para ficar sobre o tailboom
        self.ev_b= ev_b             # Envergadura do EV
        self.ev_c= ev_c             # Corda do EV
        self.ev_x= ev_x             # Distância horizontal do bordo de atque dos EV's, em relação ao bordo de ataque da asa
        self.ev_y= ev_y             # Distância no eixo Y dos EV's até o plano de simetria do avião
        self.ev_z= ev_z             # Distância vertical do bordo de atque dos EV's, em relação ao bordo de ataque da asa

        # MOTOR
        self.motor_x= motor_x       # Posição horizontal do motor. Vai ser negativa em uma configuração convencional
        self.motor_z= motor_z       # Posição vertical do motor

        # FUSELAGEM E TAILBOOM
        fus_h= self.w_cr*0.12       # Modelando as placas da fuselagem como retângulos de altura = 12% da corda da raíz
        self.fus_z= self.w_z - fus_h*0.5           # Posicionando o centro da fuselagem coincidente com a asa
        self.fus_l= 1.1*self.w_cr           # Comprimento da fuselagem
        self.fus_h= fus_h           # Altura da fuselagem
        #self.x0_boom= self.fus_l-self.motor_x
        self.boom_l= l_boom(self.fus_l, self.eh_x)

        #VALORES DE REFERÊNCIA (ficar atento à implementação do cg aqui)
        self.s_ref= s_ref(self.w_cr,self.w_baf,self.w_ct,self.w_bt)
        self.c_med= c_med(self.s_ref,self.w_bt)
        self.mac= mac(0, self.w_bt, self.w_baf, self.w_cr, self.w_ct)
        self.ref_span= ref_span(self.w_baf,self.mac,self.w_cr,self.w_bt)
        #Para o volume de cauda vertical
        self.svt= svt(self.ev_c,self.ev_b)
        #Para o volume horizontal    
        self.sht= sht(self.eh_b,self.eh_c)
        #Para a asa
        self.ar= ar(self.w_bt,self.s_ref)
        self.eh_ar= ar(self.eh_b,self.sht)

        # RESTRIÇÕES GEOMÉTRICAS
        self.h_const = h_const(ev_z,ev_b) # Restrição geométrica de altura
        self.eh_z_const= self.eh_z - self.w_z # Restrição geométrica para eh acima da asa
        
        #Dividindo as envergaduras pela metade devido à simetria. CUIDADO NA HORA DE CALCULAR A ÁREA E OUTRAS PROPRIEDADES MAIS TARDE!!!
        w_baf_h= self.w_baf/2
        w_bt_h= self.w_bt/2
        eh_b_h= self.eh_b/2
 
 ################################################### DEFINIÇÕES DE MASSA E ESTABILIDADE ###################################################
        # ESTABILIDADE
        self.pv= total_m(self.s_ref, self.sht, self.svt, self.fus_h, self.fus_l, self.boom_l)
        self.x_cg= cg(self.s_ref, self.w_z, self.w_cr, self.sht, self.eh_x, self.eh_z, self.eh_c, self.svt, self.ev_x, self.ev_z, self.ev_c, self.fus_z, self.fus_h, self.fus_l, self.boom_l, self.motor_x, self.motor_z)[0]
        self.z_cg= cg(self.s_ref, self.w_z, self.w_cr, self.sht, self.eh_x, self.eh_z, self.eh_c, self.svt, self.ev_x, self.ev_z, self.ev_c, self.fus_z, self.fus_h, self.fus_l, self.boom_l, self.motor_x, self.motor_z)[1]
        self.x_cg_p= self.x_cg/self.w_cr    # Posição do CG como fração da corda

        self.lvt= lvt(self.ev_x, self.ev_c, self.x_cg)
        self.vvt= vvt(self.lvt,self.svt,self.w_bt,self.s_ref)

        self.lht= lht(self.eh_x, self.eh_c, self.x_cg)
        self.vht= vht(self.lht,self.sht,self.mac,self.s_ref)

        self.low_cg= self.w_z - self.z_cg

################################################### DEFINIÇÃO DOS PERFIS ###################################################
        #Clmax dos perfis para detecção do estol
        e50s201550_clmax= 2.195 # Peril da raíz
        e30s201570_clmax= 2.243 # Perfil da ponta
        
        #Definindo as polares para contabilização do arrasto parasita em cada perfil. Também vindo do xf

        e50s201550_profile_drag= ProfileDrag(cl=[-0.245,1.15,2.195],cd=[0.1896,0.015,0.0485])
        e30s201570_profile_drag= ProfileDrag(cl=[-0.26,1.15,2.243],cd=[0.192,0.015,0.048])

        naca0012_profile_drag= ProfileDrag(cl=[-1.128,0.0,1.128],cd=[0.038,0.0077,0.038])

        # O arquivo .dat deve estar junto com o arquivo deste código, colocar os perfis em uma pasta separada, em primeira análise, gera erros
        root_foil='e50s201550_MIN002_R.dat'
        tip_foil='e30s201570_MIN002_T.dat'

        root_profile_drag= e50s201550_profile_drag
        tip_profile_drag= e30s201570_profile_drag

        self.w_root_clmax= e50s201550_clmax
        self.w_tip_clmax= e30s201570_clmax
        
################################################### Definindo as secções de cada superfície ###################################################
        self.w_root_section = Section(leading_edge_point=Point(0, 0, w_z),
                                    chord=w_cr,
                                    airfoil=FileAirfoil(root_foil),
                                    profile_drag= root_profile_drag
                                    )
        
        self.w_trans_section = Section(leading_edge_point=Point(0, w_baf_h, w_z),
                                    chord=w_cr,
                                    airfoil=FileAirfoil(root_foil),
                                    profile_drag= root_profile_drag
                                    )
        
        self.w_tip_section = Section(leading_edge_point=Point((w_cr-w_ct)/4, w_bt_h, w_z),
                                    chord=w_ct,
                                    airfoil=FileAirfoil(tip_foil),
                                    profile_drag= tip_profile_drag,
                                    angle= self.w_wo
                                    )
        
        self.elevator = Control(name="elevator",
                                gain=1.0,
                                x_hinge=0.4,
                                duplicate_sign=1.0)

        self.eh_root_section = Section(leading_edge_point=Point(eh_x, 0, eh_z),
                                        chord=eh_c,
                                        airfoil=NacaAirfoil(naca='0012'),
                                        profile_drag= naca0012_profile_drag,
                                        controls= [self.elevator]
                                        )
        
        self.eh_tip_section = Section(leading_edge_point=Point(eh_x, eh_b_h, eh_z),
                                        chord=eh_c,
                                        airfoil=NacaAirfoil(naca='0012'),
                                        profile_drag= naca0012_profile_drag,
                                        controls= [self.elevator]
                                        )
        
        self.ev_root_section = Section(leading_edge_point=Point(ev_x, eh_b_h, ev_z),
                                        chord=ev_c,
                                        airfoil=NacaAirfoil(naca='0012'),
                                        profile_drag= naca0012_profile_drag
                                        )
        
        self.ev_tip_section = Section(leading_edge_point=Point(ev_x, eh_b_h, ev_z+ev_b),
                                        chord=ev_c,
                                        airfoil=NacaAirfoil(naca='0012'),
                                        profile_drag= naca0012_profile_drag
                                        )
        
######################################################## Definindo as superfícies com base nas secções ########################################################
        self.wing_surface = Surface(name="Wing",
                                    n_chordwise=12,
                                    chord_spacing=Spacing.cosine,
                                    n_spanwise=22,
                                    span_spacing=Spacing.neg_sine,
                                    #y_duplicate=0.0,
                                    sections=[self.w_root_section,self.w_trans_section, self.w_tip_section],
                                    angle= self.w_inc
                                    )
        
        self.eh_surface = Surface(name="Horizontal_Stabilizer",
                                    n_chordwise=8,
                                    chord_spacing=Spacing.cosine,
                                    n_spanwise=10,
                                    span_spacing=Spacing.equal,
                                    #y_duplicate=0.0,
                                    sections=[self.eh_root_section, self.eh_tip_section],
                                    angle= self.eh_inc
                                    )
        
        self.ev_surface = Surface(name="Vertical_Stabilizer",
                                    n_chordwise=8,
                                    chord_spacing=Spacing.cosine,
                                    n_spanwise=8,
                                    span_spacing=Spacing.equal,
                                    #y_duplicate=0.0,
                                    sections=[self.ev_root_section, self.ev_tip_section]
                                    )

############################################# Definição da geometria com e sem o efeito solo (método das imagens) #############################################
        if ge:
            #Todas as dimensões de referência são calculadas diretamente, mas podem ser implementadas funções mais acima
            self.geometry = Geometry(name="Prototype",
                                    reference_area= self.s_ref,
                                    reference_chord= self.mac,
                                    reference_span= self.ref_span,
                                    reference_point=Point(self.x_cg, 0, self.z_cg),
                                    surfaces=[self.wing_surface, self.eh_surface, self.ev_surface],
                                    y_symmetry=Symmetry.symmetric,
                                    z_symmetry=Symmetry.symmetric,
                                    z_symmetry_plane= 0.00
                                    )

        else:

            self.geometry = Geometry(name="Prototype",
                                    reference_area= self.s_ref,
                                    reference_chord= self.mac,
                                    reference_span= self.ref_span,
                                    reference_point= Point(self.x_cg, 0, self.z_cg),
                                    surfaces=[self.wing_surface, self.eh_surface, self.ev_surface],
                                    y_symmetry=Symmetry.symmetric
                                    )

        

    #Método utilizado para mostrar em interface gráfica a geometria do protótipo
    def show_geometry(self):

        geometry_session= Session(geometry= self.geometry, cases=[])
        geometry_session.show_geometry()

    if __name__ == '__main__':

        print(s_ref(0.566,0.421152*2,0.172,1.09675*2))