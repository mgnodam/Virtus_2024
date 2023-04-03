import openmdao.api as om

<<<<<<< HEAD
np=1
=======
np=4
>>>>>>> 41fb2e1b0069758b5982af0da4b7716e09998c82
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

    proc_case[proc_n]= proc_case[proc_n][-20:]


    for case in proc_case[proc_n]:

        if (
<<<<<<< HEAD
            (case.outputs['individual_scorer.a_trim'] <= 6) 
            and (case.outputs['individual_scorer.me'] <= 0.4) 
            and (case.outputs['individual_scorer.score'] <= -13.2) 
            and (case.outputs['individual_scorer.g_const'] <= 2.9) 
            #and (case.outputs['individual_scorer.g_const'] >= 2.8)
=======
            (case.outputs['individual_scorer.a_trim'] <= 6) and 
            (case.outputs['individual_scorer.me'] <= 0.4) and 
            (case.outputs['individual_scorer.score'] <= -13.3) and 
            (case.outputs['individual_scorer.g_const'] <= 2.9) and 
            (case.outputs['individual_scorer.g_const'] >= 2.8)
>>>>>>> 41fb2e1b0069758b5982af0da4b7716e09998c82
            ):

            print('-------------- PROTOTIPO:', case.name[-3:]+'-'+str(proc_n)+' --------------\n')
            print(
                ' Variaveis de design: (',
                  ' w_baf= ',float(case.outputs['w_baf']),','
                  ' w_bt= ',float(case.outputs['w_bt']),','
                  ' w_cr= ',float(case.outputs['w_cr']),','
                  ' w_ct= ',float(case.outputs['w_ct']),','
                  ' w_z= ',float(case.outputs['w_z']),','
                  ' w_inc= ',float(case.outputs['w_inc']),','
                  ' w_wo= ',float(case.outputs['w_wo']),','
                  ' eh_b= ',float(case.outputs['eh_b']),','
                  ' eh_c= ',float(case.outputs['eh_c']),','
                  ' eh_inc= ',float(case.outputs['eh_inc']),','
                  ' ev_b= ',float(case.outputs['ev_b']),','
                  ' ev_cr= ',float(case.outputs['ev_cr']),','
                  ' ev_ct= ',float(case.outputs['ev_ct']),','
                  ' eh_x= ',float(case.outputs['eh_x']),','
                  ' eh_z= ',float(case.outputs['eh_z']),','
                  ' ev_x= ',float(case.outputs['ev_x']),','
<<<<<<< HEAD
                  ' ev_y= ',float(case.outputs['ev_y']),','
=======
                  ' ev_z= ',float(case.outputs['ev_z']),','
>>>>>>> 41fb2e1b0069758b5982af0da4b7716e09998c82
                  ' x_cg= ',float(case.outputs['x_cg']),','
                  ' z_cg= ',float(case.outputs['z_cg']),
                  ')'
                  , sep=''
                  )
            
            print(
                '\n Objetivos\n',
                  '     MTOW=', -float(case.outputs['individual_scorer.score'])
                  )
            
            print(
                '\n Restricoes\n',
                  '     Geométrica=', float(case.outputs['individual_scorer.g_const']),'\n',
                  '     VHT=', float(case.outputs['individual_scorer.vht']),'\n',
                  '     VVT=', float(case.outputs['individual_scorer.vvt']),'\n',
                  '     Cm0=', float(case.outputs['individual_scorer.cm0']),'\n',
                  '     Cma=', float(case.outputs['individual_scorer.cma']),'\n',
                  '     Cnb=', float(case.outputs['individual_scorer.cnb']),'\n',
                  '     Angulo de trimmagem=', float(case.outputs['individual_scorer.a_trim']),'\n',
                  '     Margem Estatica=', float(case.outputs['individual_scorer.me']),'\n'
                  )