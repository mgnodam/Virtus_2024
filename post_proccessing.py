import openmdao.api as om
from stability import *

np=1
proc_case=[]

if (np > 1):
    for p in range(np):

        crp= om.CaseReader('cases.db_'+str(p))
        driver_cases = crp.list_cases('driver')
        cases = crp.get_cases()
        proc_case.append(cases)

else:
    crp= om.CaseReader('cases.db')
    driver_cases = crp.list_cases('driver')
    cases = crp.get_cases()
    proc_case.append(cases)

for proc_n in range(len(proc_case)):

    proc_case[proc_n]= proc_case[proc_n][-100:]


    for case in proc_case[proc_n]:

        if (
            #True
            (case.outputs['individual_scorer.a_trim'] <= a_trim_max)
            and (case.outputs['individual_scorer.a_trim'] >= a_trim_min) 
            and (case.outputs['individual_scorer.me'] <= 0.40)
            and (case.outputs['individual_scorer.ar'] >= 5)
            and (case.outputs['individual_scorer.vht'] <= 0.8)
            and (case.outputs['individual_scorer.vvt'] >= vvt_min)
            and (case.outputs['individual_scorer.score'] >= 7.0)
            #and (case.outputs['individual_scorer.g_const'] <= 2.9)
            #and (case.outputs['individual_scorer.g_const'] >= 2.8)
            ):

            print('-------------- PROTOTIPO:', case.name[-4:]+'-'+str(proc_n)+' --------------\n')
            print(
                ' Variaveis de design: (',
                  #' w_baf= ',float(case.outputs['w_baf']),','
                  #' w_bt= ',float(case.outputs['w_bt']),','
                  ' w_cr= ',float(case.outputs['w_cr']),','
                  ' w_ct= ',float(case.outputs['w_ct']),','
                  ' w_z= ',float(case.outputs['w_z']),','
                  ' w_inc= ',float(case.outputs['w_inc']),','
                  #' w_wo= ',float(case.outputs['w_wo']),','
                  ' eh_b= ',float(case.outputs['eh_b']),','
                  ' eh_c= ',float(case.outputs['eh_c']),','
                  ' eh_inc= ',float(case.outputs['eh_inc']),','
                  ' ev_b= ',float(case.outputs['ev_b']),','
                  ' eh_x= ',float(case.outputs['eh_x']),','
                  ' eh_z= ',float(case.outputs['eh_z']),','
                  ' motor_x= ',float(case.outputs['motor_x']),','
                  #' motor_z= ',float(case.outputs['motor_z']),','
                  ')'
                  , sep=''
                  )
            
            print(
                '\n Objetivos\n',
                  '     Carga paga=', float(case.outputs['individual_scorer.score'])
                  )
            
            print(
                '\n Restricoes\n',
                  #'     Geometrica=', float(case.outputs['individual_scorer.g_const']),'\n',
                  '     VHT=', float(case.outputs['individual_scorer.vht']),'\n',
                  '     VVT=', float(case.outputs['individual_scorer.vvt']),'\n',
                  '     AR=', float(case.outputs['individual_scorer.ar']),'\n',
                  '     AR do EH=', float(case.outputs['individual_scorer.eh_ar']),'\n',
                  '     Cm0=', float(case.outputs['individual_scorer.cm0']),'\n',
                  '     Angulo de trimagem=', float(case.outputs['individual_scorer.a_trim']),'\n',
                  '     Margem Estatica=', float(case.outputs['individual_scorer.me']),'\n'
                  )