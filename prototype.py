from avlwrapper import *

class Prototype():
    '''
    Classe responsável por construir a geometria no formato do AVL a partir dos parâmetros de interesse
    w= referente à asa, eh= referente ao eh, ev= referente ao ev, b= envergadura, c= corda, r=raíz, t=ponta, af= afilamento, x e z = pontos do bordo de ataque.
    m= massa, x e z cg = localização do CG. 
    ge liga ou desliga o efeito solo.
    O número de painéis no AVL é ajustado diretamente no código desta classe.
    '''

    def __init__(self, w_baf, w_bt, w_cr, w_ct, w_z, w_inc, w_wo, eh_b, eh_c, ev_b, ev_c, eh_x, eh_z, x_cg, z_cg, m= 10, ge= False):
        
        #w_baf, w_ct, ev_ct e ev_x são frações (0 a 1) de outra quantidade. Para facilitar a restrição na otimização

        #Asa:
        w_baf= w_baf* w_bt          # O input de w_baf é porcentagem do ponto de transição (w_bt)
        w_ct= w_ct* w_cr            # O input de w_ct é porcentagem da corda da raíz (w_cr)
        self.w_baf= w_baf           # Ponto de transição da envergadura
        self.w_bt= w_bt             # Envergadura total
        self.w_cr= w_cr             # Corda da raíz
        self.w_ct= w_ct             # Corda da ponta
        self.w_inc= w_inc           # Ângulo de incidência da asa
        self.w_wo= w_wo             # Washout na ponta da asa
        self.w_z= w_z               # Altura da asa em relação ao chão

        # EH
        eh_z= eh_z + w_z            # eh_z é a altura do EH em relação à asa
        self.eh_b= eh_b             # Envergadura do EH
        self.eh_c= eh_c             # Corda do EH
        self.eh_x= eh_x             # Distância horizontal do bordo de atque do EH, em relação ao bordo de ataque da asa
        self.eh_z= eh_z             # Distância vertical do bordo de atque do EH, em relação ao bordo de ataque da asa

        # EV
        ev_ct= ev_c                 # O input de ev_ct é porcentagem da corda da raíz (ev_cr)
        ev_x= eh_x                  # EV fixado com o EH
        ev_y= eh_b/2                # Fixando ev_y na ponta do eh
        ev_z= eh_z-ev_b/2           # Ajuste da altura do EV, para ficar sobre o tailboom
        self.ev_b= ev_b             # Envergadura do EV
        self.ev_cr= ev_c            # Corda da raíz do EV
        self.ev_ct= ev_ct           # Corda da ponta do EV
        self.ev_x= ev_x             # Distância horizontal do bordo de atque dos EV's, em relação ao bordo de ataque da asa
        self.ev_y= ev_y             # Distância no eixo Y dos EV's até o plano de simetria do avião
        self.ev_z= ev_z             # Distância vertical do bordo de atque dos EV's, em relação ao bordo de ataque da asa

        # Estabilidade
        x_cg= x_cg * w_cr           # x_cg é input em porcentagem
        self.m= m                   # Massa total do avião (Não altera os momentos, já que o ponto de referência é o próprio CG)
        self.x_cg= x_cg             # Distância horizontal do CG, em relação ao bordo de ataque da asa
        self.z_cg= z_cg             # Distância vertical do CG, em relação ao bordo de ataque da asa

        # Efeito solo e restrição geométrica
        self.ge= ge
        self.g_const= max(w_bt+ev_z+ev_b , w_bt+eh_z) # Restrição geométrica
        
        #Dividindo as envergaduras pela metade devido à simetria. CUIDADO NA HORA DE CALCULAR A ÁREA E OUTRAS PROPRIEDADES MAIS TARDE!!!
        w_baf_h= w_baf/2
        w_bt_h= w_bt/2
        eh_b_h= eh_b/2

        ################################################### FIM DAS DEFINIÇÕES GEOMÉTRICAS ###################################################

        ################################################### DEFINIÇÃO DOS PERFIS ###################################################
        #Clmax dos perfis
        s1223_clmax= 2.27
        e75s25_clmax= 2.168 # Peril da raíz
        e25s75_clmax= 2.22  # Perfil da ponta
        
        #Definindo as polares para contabilização do arrasto parasita em cada perfil. Também vindo do xf
        s1223_profile_drag= ProfileDrag(cl=[0.53,1.58,2.27],cd=[0.039,0.019,0.044])
        e75s25_profile_drag= ProfileDrag(cl=[0.557,1.485,2.168],cd=[0.05,0.0145,0.045])
        e25s75_profile_drag= ProfileDrag(cl=[0.411,1.536,2.22],cd=[0.06,0.018,0.052])
        s1223_profile_drag= ProfileDrag(cl=[0.53,1.58,2.27],cd=[0.039,0.019,0.044])
        naca0012_profile_drag= ProfileDrag(cl=[-1.128,0.0,1.128],cd=[0.038,0.0077,0.038])

        # O arquivo .dat deve estar junto com o arquivo deste código, colocar os perfis em uma pasta separada aparentemente gera erros
        root_foil='e75s25_MIN003.dat'
        tip_foil='e25s75_MIN003.dat'
        #root_foil='s1223.dat'
        #tip_foil='s1223.dat'

        root_profile_drag= e75s25_profile_drag
        tip_profile_drag= e25s75_profile_drag
        #root_profile_drag= s1223_profile_drag
        #tip_profile_drag= s1223_profile_drag

        self.w_root_clmax= e75s25_clmax
        self.w_tip_clmax= e25s75_clmax
        #self.w_root_clmax= s1223_clmax
        #self.w_tip_clmax= s1223_clmax

        ########################################## Cálculos de valores de referência (ficar atento à implementação do cg aqui) ##########################################
        self.s_ref= (w_cr*w_baf + ((w_cr+w_ct)/2)*(w_bt-w_baf))
        self.c_med= self.s_ref/self.w_bt
        self.ref_span= w_baf+(self.c_med/w_cr)*(w_bt-w_baf)
        
        #Para o volume de cauda vertical
        self.lvt= ((ev_x-(self.x_cg))**2+(ev_z)**2)**0.5
        self.svt= (ev_c)*ev_b
        self.vvt= (self.lvt*self.svt)/(w_bt*self.s_ref)

        #Para o volume horizontal    
        self.sht= eh_b*eh_c
        self.lht= ((eh_x-(self.x_cg))**2+(eh_z)**2)**0.5
        self.vht= (self.lht*self.sht)/(self.c_med*self.s_ref)

        #Para a asa
        self.ar= (self.w_bt**2)/self.s_ref
        self.eh_ar= (self.eh_b/self.eh_c)
        
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
                                    angle= w_wo
                                    )

        self.eh_root_section = Section(leading_edge_point=Point(eh_x, 0, eh_z),
                                        chord=eh_c,
                                        airfoil=NacaAirfoil(naca='0012'),
                                        profile_drag= naca0012_profile_drag
                                        )
        
        self.eh_tip_section = Section(leading_edge_point=Point(eh_x, eh_b_h, eh_z),
                                        chord=eh_c,
                                        airfoil=NacaAirfoil(naca='0012'),
                                        profile_drag= naca0012_profile_drag
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
                                    n_spanwise=25,
                                    span_spacing=Spacing.neg_sine,
                                    #y_duplicate=0.0,
                                    sections=[self.w_root_section,self.w_trans_section, self.w_tip_section],
                                    angle= self.w_inc
                                    )
        
        self.eh_surface = Surface(name="Horizontal_Stabilizer",
                                    n_chordwise=6,
                                    chord_spacing=Spacing.cosine,
                                    n_spanwise=15,
                                    span_spacing=Spacing.equal,
                                    #y_duplicate=0.0,
                                    sections=[self.eh_root_section, self.eh_tip_section],
                                    angle= 0
                                    )
        
        self.ev_surface = Surface(name="Vertical_Stabilizer",
                                    n_chordwise=6,
                                    chord_spacing=Spacing.cosine,
                                    n_spanwise=15,
                                    span_spacing=Spacing.equal,
                                    #y_duplicate=0.0,
                                    sections=[self.ev_root_section, self.ev_tip_section]
                                    )

        ############################################# Definição da geometria com e sem o efeito solo (método das imagens) #############################################
        if ge:
            #Todas as dimensões de referência são calculadas diretamente, mas podem ser implementadas funções mais acima
            self.geometry = Geometry(name="Prototype",
                                    reference_area= self.s_ref,
                                    reference_chord= self.c_med,
                                    reference_span= self.ref_span,
                                    reference_point=Point(self.x_cg, 0, z_cg),
                                    surfaces=[self.wing_surface, self.eh_surface, self.ev_surface],
                                    y_symmetry=Symmetry.symmetric,
                                    z_symmetry=Symmetry.symmetric,
                                    z_symmetry_plane= 0.00
                                    )

        else:

            self.geometry = Geometry(name="Prototype",
                                    reference_area= self.s_ref,
                                    reference_chord= self.c_med,
                                    reference_span= self.ref_span,
                                    reference_point= Point(self.x_cg, 0, z_cg),
                                    surfaces=[self.wing_surface, self.eh_surface, self.ev_surface],
                                    y_symmetry=Symmetry.symmetric
                                    )

        

    #Método utilizado para mostrar em interface gráfica a geometria do protótipo
    def show_geometry(self):

        geometry_session= Session(geometry= self.geometry, cases=[])
        geometry_session.show_geometry()