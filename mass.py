"""
Modulo dedicado a estimar as propriedades de massa e inercia de cada protótipo

Configuração atual 24/02/2024 - Fuselagem e tailboom de placas, elementos integrados à asa.
"""

# Dados de densidade das estruturas do avião
dens_w= 0.9       #kg/m2
dens_fus= 2.3138507103521686  #kg/m2 - Considerando DivinyCell com 2 camadas de carbono em cada lado
dens_boom= 0.4627701420704337    #kg/m - Com o mesmo material da fuselagem, com largura média de 10 cm e contabilizando já duas placas
dens_stab= 1.0328202094747172    #kg/m2

# Dados de massa dos componentes principais em kg

m_batt= 0.60    # kg
m_motor= 0.540      # kg- Motor + hélice
m_tdp= 0.331 + 0.05    # kg - TDP + Rodas e rolamentos
m_beq= 0.300 + 0.05 + 0.05    # kg - Garfo de aço + Rodas e Rolamentos + Mancais e rolamentos do mecanismo

# Dados geométricos fixados

def total_m(w_s, eh_s, ev_s, fus_h, fus_l, boom_l):

    m_w= dens_w*w_s
    m_fus= 2*dens_fus*fus_h*fus_l # Contando a fuselagem como 2 placas paralelas
    m_boom= dens_boom*boom_l
    m_eh= dens_stab*eh_s
    m_ev= dens_stab*ev_s

    m_total= (m_w + m_fus + m_boom + m_eh + m_ev) + (m_batt + m_motor + m_tdp + m_beq)

    return m_total

def cg(w_s, w_z, w_cr, eh_s, eh_x, eh_z, eh_c, ev_s, ev_x, ev_z, ev_c, fus_z, fus_h, fus_l, boom_l, motor_x, motor_z):

    m_w= dens_w*w_s
    m_fus= 2*dens_fus*fus_h*fus_l # Contando a fuselagem como 2 placas paralelas
    m_boom= dens_boom*boom_l
    m_eh= dens_stab*eh_s
    m_ev= dens_stab*ev_s

    # Definição de posições do cg não especificadas:
    #X
    #Considera-se a fuselagem se iniciando junto ao bordo de ataque da asa
    fus_x= fus_l*0.15                   # Considerando 10% da fuselagem à frente do bordo de ataque, CG da fuselagem em 25%
    boom_x= boom_l*0.33 + fus_l*0.40     # Considerando  o tailboom iniciando na metade da fuselagem (20% dela está para frente) 
    batt_x= fus_l*0.00                  # Considerando 10% da fuselagem à frente do bordo de ataque, bateria em 10% da fuselagem
    tdp_x= fus_l*0.55                   # Considerando 10% da fuselagem à frente do bordo de ataque
    beq_x= -fus_l*0.2                   # Considerando 10% da fuselagem à frente do bordo de ataque
    motor_x= motor_x - 0.1*fus_l        # Considerando 10% da fuselagem à frente do bordo de ataque
    #Z
    fus_z= fus_z+0.5*fus_h              # O input de altura da fuselagem se refere ao chão da mesma, transformando no CG da fuselagem
    boom_z= fus_z*0.67 + eh_z*0.33
    batt_z= fus_z- 0.25*fus_h           # 1/4 da Altura da fuselagem
    tdp_z= fus_z - 0.75*fus_h           # 1/4 da altura da fuselagem abaixo do Chão da fuselagem
    beq_z= fus_z - 0.5*fus_h            # Chão da fuselagem

    # Contribuição de cada componente (massa x posição do cg):
    #X
    cx_w= m_w*(w_cr/3)
    cx_eh= m_eh*(eh_x + eh_c/3)
    cx_ev= m_ev*(ev_x + ev_c/3)
    cx_fus= m_fus*fus_x
    cx_boom= m_boom*boom_x
    cx_batt= m_batt*batt_x
    cx_motor= m_motor*motor_x
    cx_tdp= m_tdp*tdp_x
    cx_beq= m_beq*beq_x

    #Z
    cz_w= m_w*w_z
    cz_eh= m_eh*eh_z
    cz_ev= m_ev*ev_z
    cz_fus= m_fus*fus_z
    cz_boom= m_boom*boom_z
    cz_batt= m_batt*batt_z
    cz_motor= m_motor*motor_z
    cz_tdp= m_tdp*tdp_z
    cz_beq= m_beq*beq_z

    #CG:
    x_cg= ((cx_w + cx_eh + cx_ev + cx_fus + cx_boom + cx_batt + cx_motor + cx_tdp + cx_beq))/total_m(w_s, eh_s, ev_s, fus_h , fus_l, boom_l)
    z_cg= ((cz_w + cz_eh + cz_ev + cz_fus + cz_boom + cz_batt + cz_motor + cz_tdp + cz_beq))/total_m(w_s, eh_s, ev_s, fus_h , fus_l, boom_l)

    return [x_cg,z_cg]





