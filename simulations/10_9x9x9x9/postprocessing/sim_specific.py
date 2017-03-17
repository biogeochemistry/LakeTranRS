import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os.path

ser = pd.period_range('2010-01-01', periods=(365*4+1)*2)
sns.set_style('whitegrid')

# bz2 = '.bz2'  
bz2 = ''

basedir = '../simulations/id/003281/'  # 5,5,5,5
inbasedir = '../intermediate/id/003281/'

design = pd.read_csv('../intermediate/parameterdict.csv')
bath = pd.read_csv('../bathymetry05.csv', header=None)
bath.columns = ['zz', 'Az']

dz = bath.zz[1] - bath.zz[0]
if dz == 0.1:
    z1i = 20
    z1 = 2.0
    z2i = 89
    z2 = 8.9
elif dz == 0.5:
    z1i = 4
    z1 = 2.0
    z2i = 17
    z2 = 8.5

nl = 9
nv = 11
nvmarch = 5


nb = bath.shape[0] # number of rows, depth gradient slices
dres = bath.zz[1] - bath.zz[0]
volume1d = 0.1 * (bath.Az + np.array(bath.Az[1:].tolist() + [0])) / 2.0 
# m3 for the 10cm slices
volume2d = np.ones(((365*4+1)*2, 1)) * volume1d.reshape((1, bath.shape[0]))


def plotsim(simids, fname, stitle, writedata=False, marchversion=False):
    '''plots various outputs against the original simulation'''

    ni = len(simids)
    if marchversion:
        loopd = np.zeros((nvmarch, 365, (ni+1))) * np.nan
    else:
        loopd = np.zeros((nv, 365, (ni+1))) * np.nan

    if type(simids) is not list:
        simids = [simids]
    simdir = ['../simulations/id/{:06d}/'.format(simid) for simid in simids]
    indir = ['../intermediate/id/{:06d}/'.format(simid) for simid in simids]
    dirs = [basedir] + simdir
    indirs = [inbasedir] + indir
    designlevels = [design.loc[design.simid == id]\
                    .as_matrix().flatten().tolist() for id in simids]
    simnames = ['T{:d}W{:d}P{:d}C{:d}'.format(v1, v2, v3, v4) 
                for v1, v2, v3, v4, _ in designlevels]
    colnames = ['T5W5P5C5 base'] + simnames

    for thisname in colnames:
        print('using simulation ' + thisname)
    
    if ni == 1:
        lw = 1.0
    else:
        lw = 0.5
    
    plt.clf()

    if marchversion:
        fig = plt.figure(0)
        fig.set_figheight(10)
        fig.set_figwidth(9)
        a9 = plt.subplot2grid((nv, 4), (0, 0), colspan = 3)
        a9s = plt.subplot2grid((nv, 4), (0, 3)) 
        a1 = plt.subplot2grid((nv, 4), (1, 0), colspan = 3)
        a1s = plt.subplot2grid((nv, 4), (1, 3))
        a4 = plt.subplot2grid((nv, 4), (4, 0), colspan = 3)
        a4s = plt.subplot2grid((nv, 4), (4, 3)) 
        a6 = plt.subplot2grid((nv, 4), (6, 0), colspan = 3)
        a6s = plt.subplot2grid((nv, 4), (6, 3)) 
        a8 = plt.subplot2grid((nv, 4), (8, 0), colspan = 3)
        a8s = plt.subplot2grid((nv, 4), (8, 3)) 
    else:
        fig = plt.figure(0)
        fig.set_figheight(20)
        fig.set_figwidth(9)
        a9 = plt.subplot2grid((nv, 4), (0, 0), colspan = 3)
        a9s = plt.subplot2grid((nv, 4), (0, 3)) 
        a1 = plt.subplot2grid((nv, 4), (1, 0), colspan = 3)
        a1s = plt.subplot2grid((nv, 4), (1, 3))
        a2 = plt.subplot2grid((nv, 4), (2, 0), colspan = 3)
        a2s = plt.subplot2grid((nv, 4), (2, 3))
        a3 = plt.subplot2grid((nv, 4), (3, 0), colspan = 3)
        a3s = plt.subplot2grid((nv, 4), (3, 3)) 
        a4 = plt.subplot2grid((nv, 4), (4, 0), colspan = 3)
        a4s = plt.subplot2grid((nv, 4), (4, 3)) 
        a5 = plt.subplot2grid((nv, 4), (5, 0), colspan = 3)
        a5s = plt.subplot2grid((nv, 4), (5, 3)) 
        a6 = plt.subplot2grid((nv, 4), (6, 0), colspan = 3)
        a6s = plt.subplot2grid((nv, 4), (6, 3)) 
        a7 = plt.subplot2grid((nv, 4), (7, 0), colspan = 3)
        a7s = plt.subplot2grid((nv, 4), (7, 3)) 
        a8 = plt.subplot2grid((nv, 4), (8, 0), colspan = 3)
        a8s = plt.subplot2grid((nv, 4), (8, 3)) 
        a10 = plt.subplot2grid((nv, 4), (9, 0), colspan = 3)
        a10s = plt.subplot2grid((nv, 4), (9, 3)) 
        a11 = plt.subplot2grid((nv, 4), (10, 0), colspan = 3)
        a11s = plt.subplot2grid((nv, 4), (10, 3)) 
        
    if not marchversion:
        ## light related matters
        qst = [pd.read_csv(os.path.join(dir, 'Qst.csv{:s}'.format(bz2)), header=None)
               for dir in dirs] # ('sw', 'lw', 'sl')
        sw = pd.concat([d.iloc[:, 0] for d in qst], axis=1)
        sw.columns = colnames
        sw.index = ser
        lam = [pd.read_csv(os.path.join(dir, 'lambda.csv{:s}'.format(bz2)), header=None)
               for dir in dirs]

        # lambda to irradiance at depth1
        lam1 = pd.concat([d.iloc[:, z1i] for d in lam], axis=1)
        lam1.columns = colnames
        lam1.index = ser
        ir1 = sw * np.exp(-z1 * lam1)
        ir1['doy'] = ir1.index.day_of_year
        ir1s = ir1.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
        ir1 = ir1.drop('doy', 1)
        ir1.iloc[:, 0].plot(color='lightgray', ax=a10, ylim=[0, 40], legend=False)
        ir1.iloc[:, 1:].plot(ax=a10, linewidth=lw, legend=False)
        a10s.plot([0, 40], [0, 40], color='lightgray', linewidth=lw)
        for ci in range(1, ir1s.shape[1]):
            a10s.plot(ir1s.iloc[:, 0], ir1s.iloc[:, ci])
        a10s.set_xlim([0, 40])
        a10s.set_ylim([0, 40])    

        # lambda to irradiance at depth2
        lam2 = pd.concat([d.iloc[:, z2i] for d in lam], axis=1)
        lam2.columns = colnames
        lam2.index = ser
        ir2 = sw * np.exp(-z2 * lam2)
        ir2['doy'] = ir1.index.day_of_year
        ir2s = ir2.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
        ir2 = ir2.drop('doy', 1)
        ir2.iloc[:, 0].plot(color='lightgray', ax=a11, ylim=[0, 0.08], legend=False)
        ir2.iloc[:, 1:].plot(ax=a11, linewidth=lw, legend=False)
        a11s.plot([0, 0.08], [0, 0.08], color='lightgray', linewidth=lw)
        for ci in range(1, ir2s.shape[1]):
            a11s.plot(ir2s.iloc[:, 0], ir2s.iloc[:, ci])
        a11s.set_xlim([0, 0.08])
        a11s.set_ylim([0, 0.08])    

        a10.set_ylabel('irradiance\nmiddle')
        a11.set_ylabel('irradiance\nbottom')

        ## tp (grams per whole lake)
        tp = [pd.read_csv(os.path.join(dir, 'totp.csv{:s}'.format(bz2)), header=None)
              for dir in dirs]
        tpp = pd.concat([np.sum(d * volume2d, axis=1) / 1e3 for d in tp], axis=1)
        tpp.columns = colnames
        tpp.index = ser
        tpp['doy'] = tpp.index.day_of_year
        tpps = tpp.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
        tpp = tpp.drop('doy', 1)    
        tpp.iloc[:, 0].plot(color='lightgray', ax=a8, ylim=[0, 20e0], legend=False)
        tpp.iloc[:, 1:].plot(ax=a8, linewidth=lw, legend=False)
        a8s.plot([0e0, 20e0], [0e0, 20e0], color='lightgray', linewidth=lw)
        for ci in range(1, tpps.shape[1]):
            a8s.plot(tpps.iloc[:, 0], tpps.iloc[:, ci])
        a8s.set_xlim([0, 20e0])
        a8s.set_ylim([0, 20e0])
        a8.set_ylabel('total P pool\nentire lake')




    ## water temperature
    t = [pd.read_csv(os.path.join(dir, 't.csv{:s}'.format(bz2)), header=None)
         for dir in dirs]
    t0 = pd.concat([d.iloc[:, 0] for d in t], axis=1)
    t0.columns = colnames
    t0.index = ser
    t0['doy'] = t0.index.day_of_year
    t0s = t0.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
    t0 = t0.drop('doy', 1)
    t0.iloc[:, 0].plot(color='lightgray', ax=a1, ylim=[0, 25], legend=False)
    t0.iloc[:, 1:].plot(ax=a1, linewidth=lw, legend=False)
    a1s.plot([0, 25], [0, 25], color='lightgray', linewidth=lw)
    for ci in range(1, t0s.shape[1]):
        a1s.plot(t0s.iloc[:, 0], t0s.iloc[:, ci])
    a1s.set_xlim([0, 25])
    a1s.set_ylim([0, 25])
    a1.set_ylabel('water temperature\nsurface')

    if not marchversion:
        t1 = pd.concat([d.iloc[:, z1i] for d in t], axis=1)
        t1.columns = colnames
        t1.index = ser
        t1['doy'] = t1.index.day_of_year
        t1s = t1.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
        t1 = t1.drop('doy', 1)
        t1.iloc[:, 0].plot(color='lightgray', ax=a2, ylim=[0, 25], legend=False)
        t1.iloc[:, 1:].plot(ax=a2, linewidth=lw, legend=False)
        a2s.plot([0, 25], [0, 25], color='lightgray', linewidth=lw)
        for ci in range(1, t1s.shape[1]):
            a2s.plot(t1s.iloc[:, 0], t1s.iloc[:, ci])
        a2s.set_xlim([0, 25])
        a2s.set_ylim([0, 25])
        a2.set_ylabel('water temperature\nmiddle')

        t2 = pd.concat([d.iloc[:, z2i] for d in t], axis=1)
        t2.columns = colnames
        t2.index = ser
        t2['doy'] = t2.index.day_of_year
        t2s = t2.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
        t2 = t2.drop('doy', 1)
        t2.iloc[:, 0].plot(color='lightgray', ax=a3, ylim=[0, 25], legend=False)
        t2.iloc[:, 1:].plot(ax=a3, linewidth=lw, legend=False)
        a3s.plot([0, 25], [0, 25], color='lightgray', linewidth=lw)
        for ci in range(1, t2s.shape[1]):
            a3s.plot(t2s.iloc[:, 0], t2s.iloc[:, ci])
        a3s.set_xlim([0, 25])
        a3s.set_ylim([0, 25])
        a3.set_ylabel('water temperature\nbottom')

    ## ice
    his = [pd.read_csv(os.path.join(dir, 'His.csv{:s}'.format(bz2)), header=None)
           for dir in dirs]
    ice = pd.concat([d.iloc[:, 0] for d in his], axis=1)
    ice.columns = colnames
    ice.index = ser
    ice['doy'] = ice.index.day_of_year
    ices = ice.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
    ice = ice.drop('doy', 1)
    ice.iloc[:, 0].plot(color='lightgray', ax=a4, ylim=[0, 0.8], legend=False)
    ice.iloc[:, 1:].plot(ax=a4, linewidth=lw, legend=False)
    a4s.plot([0, 0.8], [0, 0.8], color='lightgray', linewidth=lw)
    for ci in range(1, ices.shape[1]):
        a4s.plot(ices.iloc[:, 0], ices.iloc[:, ci])
    a4s.set_xlim([0, 0.8])
    a4s.set_ylim([0, 0.8])
    a4.set_ylabel('ice thickness')

    ## oxygen
    o2 = [pd.read_csv(os.path.join(dir, 'O2zt.csv{:s}'.format(bz2)), header=None)
          for dir in dirs]
    
    if not marchversion:
        o22 = pd.concat([d.iloc[:, z1i] for d in o2], axis=1)
        o22.columns = colnames
        o22.index = ser
        o22['doy'] = o22.index.day_of_year
        o22s = o22.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
        o22 = o22.drop('doy', 1)
        o22.iloc[:, 0].plot(color='lightgray', ax=a5, ylim=[1e0, 1e4], legend=False)
        o22.iloc[:, 1:].plot(ax=a5, linewidth=lw, legend=False)
        a5s.plot([1e0, 1e4], [1e0, 1e4], color='lightgray', linewidth=lw)
        for ci in range(1, o22s.shape[1]):
            a5s.plot(o22s.iloc[:, 0], o22s.iloc[:, ci])
        a5s.set_xlim([1e0, 1e4])
        a5s.set_ylim([1e0, 1e4])
        a5.axhline(16, color='pink')
        a5.axhline(3000, color='pink')
        a5s.axhline(3000, color='pink', linewidth=lw)
        a5s.axhline(16, color='pink', linewidth=lw)
        a5s.axvline(3000, color='pink', linewidth=lw)
        a5s.axvline(16, color='pink', linewidth=lw)
        a5.set_yscale('log')
        a5s.set_xscale('log')
        a5s.set_yscale('log')
        a5.set_ylabel('O2 concentration\nmiddle')


    o23 = pd.concat([d.iloc[:, z2i] for d in o2], axis=1)
    o23.columns = colnames
    o23.index = ser
    o23['doy'] = o23.index.day_of_year
    o23s = o23.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
    o23 = o23.drop('doy', 1)
    o23.iloc[:, 0].plot(color='lightgray', ax=a6, ylim=[1e0, 1e4], legend=False)
    o23.iloc[:, 1:].plot(ax=a6, linewidth=lw, legend=False)
    a6s.plot([1e0, 1e4], [1e0, 1e4], color='lightgray', linewidth=lw)
    for ci in range(1, o23s.shape[1]):
        a6s.plot(o23s.iloc[:, 0], o23s.iloc[:, ci])
    a6s.set_xlim([1e0, 1e4])
    a6s.set_ylim([1e0, 1e4])
    a6.axhline(16, color='pink')
    a6.axhline(3000, color='pink')
    a6s.axhline(3000, color='pink', linewidth=lw)
    a6s.axhline(16, color='pink', linewidth=lw)
    a6s.axvline(3000, color='pink', linewidth=lw)
    a6s.axvline(16, color='pink', linewidth=lw)
    a6.set_yscale('log')
    a6s.set_xscale('log')
    a6s.set_yscale('log')
    a6.set_ylabel('O2 concentration\nbottom')


    ## chl (grams per whole lake)
    chl = [pd.read_csv(os.path.join(dir, 'chl.csv{:s}'.format(bz2)), header=None)
          for dir in dirs]
    chlp = pd.concat([np.sum(d * volume2d, axis=1) / 1e3 for d in chl], axis=1)
    chlp.columns = colnames
    chlp.index = ser
    chlp['doy'] = chlp.index.day_of_year
    chlps = chlp.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
    chlp = chlp.drop('doy', 1)    
    chlp.iloc[:, 0].plot(color='lightgray', ax=a7, ylim=[0, 5e0], legend=False)
    chlp.iloc[:, 1:].plot(ax=a7, linewidth=lw, legend=False)
    a7s.plot([0, 5e0], [0, 5e0], color='lightgray', linewidth=lw)
    for ci in range(1, chlps.shape[1]):
        a7s.plot(chlps.iloc[:, 0], chlps.iloc[:, ci])
    a7s.set_xlim([0, 5e0])
    a7s.set_ylim([0, 5e0])
    a7.set_ylabel('chl pool\nentire lake')


    ## mixing depth, as in MyLake, 
    ## same as the salinity version of doi:10.1016/j.envsoft.2011.05.006 
    ## otherwise from MyLake
    # % Calculate pycnocline depth
    # pycno_thres=0.1;  %treshold density gradient value (kg m-3 m-1)
    # rho = polyval(ies80,max(0,Tz(:))) + min(Tz(:),0);
    # dRdz = [NaN; abs(diff(rho))];
    # di=find((dRdz<(pycno_thres*dz)) | isnan(dRdz));
    # %dRdz(di)=NaN;
    # %TCz = nansum(zz .* dRdz) ./ nansum(dRdz);
    # dRdz(di)=0; %modified for MATLAB version 7
    # TCz = sum(zz .* dRdz) ./ sum(dRdz);
    pycnothresholdunit = 0.1 ## as per MyLake, kg m-3 m-1
    # pycnothresholdunit = 0.5 ## kg m-3 m-1 
    # 0.5 allows rigidness of the finer resolution? 
    pycnothreshold = pycnothresholdunit * dres
    tm = [d.as_matrix() for d in t]
    rho = [999.842594 + d * (6.793952e-2 + d * (-9.09529e-3 + 
        d * (1.001685e-4 + d * (-1.120083e-6 + 6.536332e-9 * d)))) for d in tm]
    drho = [d[:, 1:] - d[:, :(nb-1)] for d in rho]
    drhosig = [d * (d > pycnothreshold) for d in drho]
    mdepbottom = np.zeros((drhosig[0].shape[0], len(drhosig))) * np.nan
    zzbottom = (np.flipud(bath.zz[:(nb-1)].as_matrix()+(dres/2)).\
                reshape((nb-1, 1))).flatten()
    for i, d in enumerate(drhosig):
        for ri in range(d.shape[0]):
            dsum = d[ri, :].sum()
            if dsum == 0:
                mdepbottom[ri, i] = 0
            else:
                mdepbottom[ri, i] = (d[ri, :] * zzbottom).sum() / dsum
    mdep = bath.zz.max() + dres - mdepbottom
    mdep = pd.DataFrame(mdep, index=ser)
    mdep.columns = colnames
    mdep['doy'] = mdep.index.day_of_year
    mdepJJ = mdep[(mdep.index.month > 5) & (mdep.index.month < 8)]
    mdepALLYEARs = mdep.iloc[((30+31)*4):, :].groupby('doy').mean().iloc[:365, :]
    mdeps = mdepJJ.iloc[((30+31)*4):, :].groupby('doy').mean()
    mdep = mdep.drop('doy', 1)    

    mdep.iloc[:, 0].plot(color='lightgray', ax=a9, ylim=[9, 0], legend=False)
    mdep.iloc[:, 1:].plot(ax=a9, linewidth=lw, legend=False)
    a9s.plot([0, 9], [0, 9], color='lightgray', linewidth=lw)
    for ci in range(1, mdeps.shape[1]):
        a9s.plot(mdeps.iloc[:, 0], mdeps.iloc[:, ci])
    a9s.set_xlim([9, 0])
    a9s.set_ylim([9, 0])
    a9s.text(8, 8, 'only JJ months')
    a9.set_ylabel('mixing depth, m\ntentative def')

    a9.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
              ncol=4, mode="expand", borderaxespad=0.)

    # for a in [a1, a2, a3, a4, a5, a6, a7, a8]:
    #     a.set_xlim(yl)
    a9s.set_title('2014-2017 DOY mean\ncompared against base')

    st = fig.suptitle(stitle, fontsize='x-large')
    st.set_y(0.95)

    fig.savefig('{:s}.png'.format(fname), dpi=150, bbox_inches='tight')
    fig.savefig('{:s}.pdf'.format(fname), dpi=150, bbox_inches='tight')

    if marchversion:
        loopd[0, :, :] = mdepALLYEARs
        loopd[1, :, :] = t0s
        loopd[2, :, :] = ices
        loopd[3, :, :] = o23s
        loopd[4, :, :] = chlps
    else:
        loopd[0, :, :] = t0s
        loopd[1, :, :] = t1s
        loopd[2, :, :] = t2s
        loopd[3, :, :] = ices
        loopd[4, :, :] = o22s
        loopd[5, :, :] = o23s
        loopd[6, :, :] = chlps
        loopd[7, :, :] = tpps
        loopd[8, :, :] = mdepALLYEARs
        loopd[9, :, :] = ir1s
        loopd[10, :, :] = ir2s
        
    np.save('{:s}.npy'.format(fname), loopd)

    return(fig)



if not os.path.exists('results_raw'):
    os.makedirs('results_raw')
if not os.path.exists('results_raw2'):
    os.makedirs('results_raw2')
if not os.path.exists('sim_specific'):
    os.makedirs('sim_specific')

    

sns.set_palette('coolwarm', 2)
plotsim([3277, 3285], 'results_raw/AT',
        'impact of air temperature')
plotsim([3277, 3285], 'results_raw2/AT',
        'impact of air temperature', True, True)

sns.set_palette('Reds_r', 2)
plotsim([3245, 3317], 'results_raw/WS', 
        'impact of wind speed')
plotsim([3245, 3317], 'results_raw2/WS', 
        'impact of wind speed', True, True)

sns.set_palette('Greens_r', 2)
plotsim([2957, 3605], 'results_raw/TP',
        'impact of total P loading')
plotsim([2957, 3605], 'results_raw2/TP',
        'impact of total P loading', True, True)

sns.set_palette('Reds', 2)
plotsim([365, 6197], 'results_raw/DOC',
             'impact of DOC loading')
plotsim([365, 6197], 'results_raw2/DOC',
             'impact of DOC loading', True, True)


# sns.set_palette('Oranges_d', 1)
# plotsim(3227, 'results_raw/AT colder', 
#         '"lower air temperature" compared to "base"')
# plotsim(3285, 'results_raw/AT warmer',
#         '"higher air temperature" compared to "base"')
# plotsim(3245, 'results_raw/WS calmer',
#         '"calmer wind compared" to "base"')
# plotsim(3317, 'results_raw/WS stronger',
#         '"stronger wind compared" to "base"')
# plotsim(2957, 'results_raw/TP lower', 
#         '"less TP loading compared" to "base"')
# plotsim(3605, 'results_raw/TP higher',
#         '"greater TP loading compared" to "base"')
# plotsim(365, 'results_raw/DOC lower',
#         '"less DOC loading compared" to "base"')
# plotsim(6197, 'results_raw/DOC higher',
#         '"greater DOC loading compared" to "base"')

# plotsim(1, 'sim_specific/test001', '"low in everything" compared to "base"')
# plotsim(505, 'sim_specific/test505', '"id505" compared to "base"')


