"""
Modulo dedicado a estimar as propriedades de massa e inercia de cada protótipo
"""

# Dados de densidade das estruturas do avião
dens_w= 1       #kg/m2
dens_fus= 46.296  #kg/m3 considerando fuselagem pesando 400 g
dens_boom= 0.8    #kg/m
dens_stab= 0.8    #kg/m2

# Dados de massa dos componentes principais em kg

m_batt= 0.60
m_motor= 0.540      # Motor + hélice
m_tdp= 0.331
m_beq= 0.300

# Dados geométricos fixados

def total_m(w_s, eh_s, ev_s, fus_w, fus_h, fus_l, boom_l):

    m_w= dens_w*w_s
    m_fus= dens_fus*fus_w*fus_h*fus_l
    m_boom= dens_boom*boom_l
    m_eh= dens_stab*eh_s
    m_ev= dens_stab*ev_s

    m_total= (m_w + m_fus + m_boom + m_eh + m_ev) + (m_batt + m_motor + m_tdp + m_beq)

    return m_total

def cg(w_s, w_z, w_cr, eh_s, eh_x, eh_z, eh_c, ev_s, ev_x, ev_z, ev_c, fus_z, fus_w, fus_h, fus_l, boom_l, motor_x, motor_z):

    m_w= dens_w*w_s
    m_fus= dens_fus*fus_w*fus_h*fus_l
    m_boom= dens_boom*boom_l
    m_eh= dens_stab*eh_s
    m_ev= dens_stab*ev_s

    # Posições do cg não especificadas:
    #X
    fus_x= fus_l*0.4 + motor_x
    boom_x= boom_l*0.4 + fus_l + motor_x
    batt_x= fus_l*0.25 + motor_x
    tdp_x= fus_l*0.8 + motor_x
    beq_x= fus_l*0.1 + motor_x
    #Z
    fus_z= fus_z+0.5*fus_h              # O input de altura da fuselagem se refere ao chão da mesma
    boom_z= (fus_z + eh_z)*0.5
    batt_z= fus_z
    tdp_z= fus_z - 0.5*fus_h
    beq_z= fus_z - 0.2*fus_h

    # Contribuição de cada componente:
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
    x_cg= ((cx_w + cx_eh + cx_ev + cx_fus + cx_boom + cx_batt + cx_motor + cx_tdp + cx_beq))/total_m(w_s, eh_s, ev_s, fus_w, fus_h , fus_l, boom_l)
    z_cg= ((cz_w + cz_eh + cz_ev + cz_fus + cz_boom + cz_batt + cz_motor + cz_tdp + cz_beq))/total_m(w_s, eh_s, ev_s, fus_w, fus_h , fus_l, boom_l)

    return [x_cg,z_cg]





