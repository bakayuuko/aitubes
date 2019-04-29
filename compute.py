import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

def compute(jarak, power, bagian):
    x_qual = np.arange(0, 101, 1)
    x_serv = np.arange(0, 101, 1)
    x_tip  = np.arange(0, 101, 1)

    jrk_dkt    = fuzz.trimf(x_qual, [0, 0, 40])
    jrk_sdg    = fuzz.trimf(x_qual, [0, 40, 100])
    jrk_jauh    = fuzz.trimf(x_qual, [40, 100, 100])
    pwr_kcl     = fuzz.trimf(x_serv, [0, 0, 50])
    pwr_sdg     = fuzz.trimf(x_serv, [0, 50, 100])
    pwr_kwt     = fuzz.trimf(x_serv, [50, 100, 100])
    dmg_lo   = fuzz.trimf(x_tip, [0, 0, 25])
    dmg_md   = fuzz.trimf(x_tip, [0, 25, 50])
    dmg_hi   = fuzz.trimf(x_tip, [25, 50, 75])
    dmg_mhig  = fuzz.trimf(x_tip, [50, 75, 100])
    dmg_ultra = fuzz.trimf(x_tip, [75, 100, 100])
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

    ax0.plot(x_qual, jrk_dkt, 'b', linewidth=1.5, label='dekat')
    ax0.plot(x_qual, jrk_sdg, 'g', linewidth=1.5, label='sedang')
    ax0.plot(x_qual, jrk_jauh, 'r', linewidth=1.5, label='jauh')
    ax0.set_title('Jarak')
    ax0.legend()

    ax1.plot(x_serv, pwr_kcl, 'b', linewidth=1.5, label='kecil')
    ax1.plot(x_serv, pwr_sdg, 'g', linewidth=1.5, label='sedang')
    ax1.plot(x_serv, pwr_kwt, 'r', linewidth=1.5, label='kuat')
    ax1.set_title('Daya Serang')
    ax1.legend()

    ax2.plot(x_tip, dmg_lo, 'b', linewidth=1.5, label='Low')
    ax2.plot(x_tip, dmg_md, 'g', linewidth=1.5, label='Medium')
    ax2.plot(x_tip, dmg_hi, 'r', linewidth=1.5, label='High')
    ax2.plot(x_tip, dmg_mhig, 'm', linewidth=1.5, label='ultra')
    ax2.plot(x_tip, dmg_ultra, 'c', linewidth=1.5, label='Ultra')
    ax2.set_title('Damage')
    ax2.legend()
    for ax in (ax0, ax1, ax2):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    levt_lo = fuzz.interp_membership(x_qual, jrk_dkt, jarak)
    levt_md = fuzz.interp_membership(x_qual, jrk_sdg, jarak)
    levt_hi = fuzz.interp_membership(x_qual, jrk_jauh, jarak)

    levh_lo = fuzz.interp_membership(x_serv, pwr_kcl, power)
    levh_md = fuzz.interp_membership(x_serv, pwr_sdg, power)
    levh_hi = fuzz.interp_membership(x_serv, pwr_kwt, power)

    kena=int(bagian)
    if(kena == 1):
        active_rule1 = np.fmax(levt_lo, levh_lo)
        active_rule2 = np.fmax(levt_lo, levh_md)
        active_rule3 = np.fmax(levt_lo, levh_hi)
        active_rule4 = np.fmax(levt_md, levh_lo)
        active_rule5 = np.fmax(levt_md, levh_md)
        active_rule6 = np.fmax(levt_md, levh_hi)
        active_rule7 = np.fmax(levt_hi, levh_lo)
        active_rule8 = np.fmax(levt_hi, levh_md)
        active_rule9 = np.fmax(levt_hi, levh_hi)
        factive_rule1=np.fmin(active_rule1, dmg_mhig)
        factive_rule2=np.fmin(active_rule2, dmg_ultra)
        factive_rule3=np.fmin(active_rule3, dmg_ultra)
        factive_rule4=np.fmin(active_rule4, dmg_md)
        factive_rule5=np.fmin(active_rule5, dmg_hi)
        factive_rule6=np.fmin(active_rule6, dmg_mhig)
        factive_rule7=np.fmin(active_rule7, dmg_lo)
        factive_rule8=np.fmin(active_rule8, dmg_md)
        factive_rule9=np.fmin(active_rule9, dmg_md)
        aggregated = np.fmax(factive_rule1,
                             np.fmax(factive_rule2,
                                     np.fmax(factive_rule3,
                                             np.fmax(factive_rule4,
                                                     np.fmax(factive_rule5,
                                                             np.fmax(factive_rule6,
                                                                     np.fmax(factive_rule7,
                                                                             np.fmax(factive_rule8,factive_rule9))))))))
        output_specifier=['low damage','medium damage','medium damage','high damage','high damage','more high damage','more high damage','ultra damage','ultra damage']
        possible_aggregate=[active_rule1,active_rule2,active_rule3,active_rule4,active_rule5,active_rule6,active_rule7,active_rule8,active_rule9]
        print(possible_aggregate)
        aggregate = np.argwhere(possible_aggregate == np.amax(possible_aggregate))
        aggregate = aggregate.flatten().tolist()
        print("Possible values:-")
        for i in range(len(aggregate)):
            print(output_specifier[aggregate[i]])
         
        final_dmg = fuzz.defuzz(x_tip, aggregated, 'centroid')
        return final_dmg
    elif(kena == 2):
        active_rule10 = np.fmax(levt_lo, levh_lo)
        active_rule11 = np.fmax(levt_lo, levh_md)
        active_rule12 = np.fmax(levt_lo, levh_hi)
        active_rule13 = np.fmax(levt_md, levh_lo)
        active_rule14 = np.fmax(levt_md, levh_md)
        active_rule15 = np.fmax(levt_md, levh_hi)
        active_rule16 = np.fmax(levt_hi, levh_lo)
        active_rule17 = np.fmax(levt_hi, levh_md)
        active_rule18 = np.fmax(levt_hi, levh_hi)
        factive_rule10=np.fmin(active_rule10, dmg_md)
        factive_rule11=np.fmin(active_rule11, dmg_mhig)
        factive_rule12=np.fmin(active_rule12, dmg_ultra)
        factive_rule13=np.fmin(active_rule13, dmg_lo)
        factive_rule14=np.fmin(active_rule14, dmg_md)
        factive_rule15=np.fmin(active_rule15, dmg_hi)
        factive_rule16=np.fmin(active_rule16, dmg_lo)
        factive_rule17=np.fmin(active_rule17, dmg_lo)
        factive_rule18=np.fmin(active_rule18, dmg_md)
        aggregated = np.fmax(factive_rule10,
                             np.fmax(factive_rule11,
                                     np.fmax(factive_rule12,
                                             np.fmax(factive_rule13,
                                                     np.fmax(factive_rule14,
                                                             np.fmax(factive_rule15,
                                                                     np.fmax(factive_rule16,
                                                                             np.fmax(factive_rule17,factive_rule18))))))))
        output_specifier=['low damage','medium damage','medium damage','high damage','high damage','more high damage','more high damage','ultra damage','ultra damage']
        possible_aggregate=[active_rule10,active_rule11,active_rule12,active_rule13,active_rule14,active_rule15,active_rule16,active_rule17,active_rule18]
        print(possible_aggregate)
        aggregate = np.argwhere(possible_aggregate == np.amax(possible_aggregate))
        aggregate = aggregate.flatten().tolist()
        print("Possible values:-")
        for i in range(len(aggregate)):
            print(output_specifier[aggregate[i]])
        
        final_dmg = fuzz.defuzz(x_tip, aggregated, 'centroid')
        return final_dmg
    elif(kena == 3):
        active_rule19 = np.fmax(levt_lo, levh_lo)
        active_rule20 = np.fmax(levt_lo, levh_md)
        active_rule21 = np.fmax(levt_lo, levh_hi)
        active_rule22 = np.fmax(levt_md, levh_lo)
        active_rule23 = np.fmax(levt_md, levh_md)
        active_rule24 = np.fmax(levt_md, levh_hi)
        active_rule25 = np.fmax(levt_hi, levh_lo)
        active_rule26 = np.fmax(levt_hi, levh_md)
        active_rule27 = np.fmax(levt_hi, levh_hi)
        factive_rule19=np.fmin(active_rule19, dmg_lo)
        factive_rule20=np.fmin(active_rule20, dmg_md)
        factive_rule21=np.fmin(active_rule21, dmg_hi)
        factive_rule22=np.fmin(active_rule22, dmg_lo)
        factive_rule23=np.fmin(active_rule23, dmg_lo)
        factive_rule24=np.fmin(active_rule24, dmg_md)
        factive_rule25=np.fmin(active_rule25, dmg_lo)
        factive_rule26=np.fmin(active_rule26, dmg_lo)
        factive_rule27=np.fmin(active_rule27, dmg_lo)
        aggregated = np.fmax(factive_rule19,
                             np.fmax(factive_rule20,
                                     np.fmax(factive_rule21,
                                             np.fmax(factive_rule22,
                                                     np.fmax(factive_rule23,
                                                             np.fmax(factive_rule24,
                                                                     np.fmax(factive_rule25,
                                                                             np.fmax(factive_rule26,factive_rule27))))))))
        output_specifier=['low damage','medium damage','medium damage','high damage','high damage','more high damage','more high damage','ultra damage','ultra damage']
        possible_aggregate=[active_rule19,active_rule20,active_rule21,active_rule22,active_rule23,active_rule24,active_rule25,active_rule26,active_rule27]
        print(possible_aggregate)
        aggregate = np.argwhere(possible_aggregate == np.amax(possible_aggregate))
        aggregate = aggregate.flatten().tolist()
        print("Possible values:-")
        for i in range(len(aggregate)):
            print(output_specifier[aggregate[i]])
        
        final_dmg = fuzz.defuzz(x_tip, aggregated, 'centroid')
        return final_dmg