from avlwrapper import *

class Prototype():
    '''
    Classe responsável por construir a geometria no formato do AVL a partir dos parâmetros de interesse
    w= referente à asa, eh= referente ao eh, ev= referente ao ev, b= envergadura, c= corda, r=raíz, t=ponta, af= afilamento, x e z = pontos do bordo de ataque.
    m= massa, x e z cg = localização do CG. ge liga ou desliga o efeito solo.
    Atualmente (v03) o CG ainda não é utilizado em cálculo.
    O número de painéis no AVL é ajustado diretamente no código desta classe.
    '''

    def __init__(self, w_baf, w_bt, w_cr, w_ct, w_z, w_inc, eh_b, eh_c, eh_inc, ev_b, ev_cr, ev_ct, eh_x, eh_z, ev_x, ev_z, x_cg, z_cg, m= 10, ge= False):
        
        #w_baf, w_ct, ev_ct e ev_x são frações (0 a 1) de outra quantidade. Para facilitar a restrição na otimização
        w_baf= w_baf* w_bt
        self.w_baf= w_baf # w_baf é porcentagem do ponto de transição (w_bt)
        self.w_bt= w_bt
        self.w_cr= w_cr
        w_ct= w_ct* w_cr
        self.w_ct= w_ct #w_ct é porcentagem da corda da raíz (w_cr)
        self.w_inc= w_inc
        self.eh_b= eh_b
        self.eh_c= eh_c
        self.eh_inc= eh_inc
        self.ev_b= ev_b
        self.ev_cr= ev_cr
        ev_ct= ev_ct* ev_cr
        self.ev_ct= ev_ct #ev_ct é porcentagem da corda da raíz (ev_cr)
        self.eh_x= eh_x
        self.eh_z= eh_z
        ev_x= ev_x* eh_x
        self.ev_x= ev_x #ev_x é porcentagem da distância horizontal do eh (eh_x)
        self.ev_z= ev_z
        self.w_z= w_z
        self.m= m
        x_cg= x_cg * w_cr
        self.x_cg= x_cg #x_cg é input em porcentagem
        self.z_cg= z_cg
        self.ge= ge
        self.g_const= max(w_bt+ev_z+ev_b , w_bt+eh_z) # Restrição geométrica

        #Dividindo as envergaduras pela metade devido à simetria
        w_baf= w_baf/2
        w_bt= w_bt/2
        eh_b= eh_b/2

        #Clmax dos perfis da asa tirados do xflr5
        self.w_root_clmax= 2.27
        self.w_tip_clmax= 2.27

        #Definindo as polares para contabilização do arrasto parasita em cada perfil. Também vindo do xf
        s1223_profile_drag= ProfileDrag(cl=[0.53,1.58,2.27],cd=[0.039,0.019,0.044])
        naca0013_profile_drag= ProfileDrag(cl=[-1.15,0.0,1.15],cd=[0.042,0.008,0.042])
        
        #Definindo as secções de cada superfície
        self.w_root_section = Section(leading_edge_point=Point(0, 0, w_z),
                                    chord=w_cr,
                                    airfoil=FileAirfoil('s1223.dat'),
                                    profile_drag= s1223_profile_drag
                                    )
        
        self.w_trans_section = Section(leading_edge_point=Point(0, w_baf, w_z),
                                    chord=w_cr,
                                    airfoil=FileAirfoil('s1223.dat'),
                                    profile_drag= s1223_profile_drag
                                    )
        
        self.w_tip_section = Section(leading_edge_point=Point((w_cr-w_ct)/4, w_bt, w_z),
                                    chord=w_ct,
                                    airfoil=FileAirfoil('s1223.dat'),
                                    profile_drag= s1223_profile_drag
                                    )

        self.eh_root_section = Section(leading_edge_point=Point(eh_x, 0, eh_z),
                                        chord=eh_c,
                                        airfoil=NacaAirfoil(naca='0013'),
                                        profile_drag= naca0013_profile_drag
                                        )
        
        self.eh_tip_section = Section(leading_edge_point=Point(eh_x, eh_b, eh_z),
                                        chord=eh_c,
                                        airfoil=NacaAirfoil(naca='0013'),
                                        profile_drag= naca0013_profile_drag
                                        )
        
        self.ev_root_section = Section(leading_edge_point=Point(ev_x, 0, ev_z),
                                        chord=ev_cr,
                                        airfoil=NacaAirfoil(naca='0013'),
                                        profile_drag= naca0013_profile_drag
                                        )
        
        self.ev_tip_section = Section(leading_edge_point=Point(ev_x+(ev_cr-ev_ct)/2, 0, ev_z+ev_b),
                                        chord=ev_ct,
                                        airfoil=NacaAirfoil(naca='0013'),
                                        profile_drag= naca0013_profile_drag
                                        )
        
        #Definindo as superfícies com base nas secções
        self.wing_surface = Surface(name="Wing",
                                    n_chordwise=12,
                                    chord_spacing=Spacing.cosine,
                                    n_spanwise=25,
                                    span_spacing=Spacing.neg_sine,
                                    y_duplicate=0.0,
                                    sections=[self.w_root_section,self.w_trans_section, self.w_tip_section],
                                    angle= self.w_inc
                                    )
        
        self.eh_surface = Surface(name="Horizontal_Stabilizer",
                                    n_chordwise=6,
                                    chord_spacing=Spacing.cosine,
                                    n_spanwise=15,
                                    span_spacing=Spacing.equal,
                                    y_duplicate=0.0,
                                    sections=[self.eh_root_section, self.eh_tip_section],
                                    angle= self.eh_inc
                                    )
        
        self.ev_surface = Surface(name="Vertical_Stabilizer",
                                    n_chordwise=6,
                                    chord_spacing=Spacing.cosine,
                                    n_spanwise=15,
                                    span_spacing=Spacing.equal,
                                    #y_duplicate=0.0,
                                    sections=[self.ev_root_section, self.ev_tip_section]
                                    )

        #Definição da geometria com e sem o efeito solo (método das imagens)
        if ge:
            #Todas as dimensões de referência são calculadas diretamente, mas podem ser implementadas funções mais acima
            self.geometry = Geometry(name="Prototype",
                                    reference_area= (w_cr*w_baf + ((w_cr+w_ct)/2)*(w_bt-w_baf))*2,
                                    reference_chord= (w_cr*w_baf + ((w_cr+w_ct)/2)*(w_bt-w_baf))/w_bt,
                                    reference_span= w_baf+(((w_cr*w_baf + ((w_cr+w_ct)/2)*(w_bt-w_baf))/w_bt)/w_cr)*(w_bt-w_baf),
                                    reference_point=Point(self.x_cg, 0, z_cg),
                                    surfaces=[self.wing_surface, self.eh_surface, self.ev_surface],
                                    y_symmetry=Symmetry.none,
                                    z_symmetry=Symmetry.symmetric,
                                    z_symmetry_plane= 0.00
                                    )

        else:

            self.geometry = Geometry(name="Prototype",
                                    reference_area= (w_cr*w_baf + ((w_cr+w_ct)/2)*(w_bt-w_baf))*2,
                                    reference_chord= (w_cr*w_baf + ((w_cr+w_ct)/2)*(w_bt-w_baf))/w_bt,
                                    reference_span= w_baf+(((w_cr*w_baf + ((w_cr+w_ct)/2)*(w_bt-w_baf))/w_bt)/w_cr)*(w_bt-w_baf),
                                    reference_point=Point(self.x_cg, 0, z_cg),
                                    surfaces=[self.wing_surface, self.eh_surface, self.ev_surface],
                                    y_symmetry=Symmetry.none
                                    )

        #Cálculos de valores de referência (ficar atento à implementação do cg aqui)
        #Para o volume de cauda vertical
        self.s= (w_cr*w_baf + ((w_cr+w_ct)/2)*(w_bt-w_baf))*2
        self.lvt= ((ev_x-(self.x_cg))**2+(ev_z)**2)**0.5
        self.svt= ((ev_cr+ev_ct)/2)*ev_b

        self.vvt= (self.lvt*self.svt)/(w_bt*self.s)

        #Para o volume horizontal
        self.c_med= (w_cr*w_baf + ((w_cr+w_ct)/2)*(w_bt-w_baf))/w_bt
        self.sht= eh_b*eh_c
        self.lht= ((eh_x-(self.x_cg))**2+(eh_z)**2)**0.5

        self.vht= (self.lht*self.sht)/(self.c_med*self.s)

    #Método utilizado para mostrar em interface gráfica a geometria do protótipo
    def show_geometry(self):

        geometry_session= Session(geometry= self.geometry, cases=[])
        geometry_session.show_geometry()