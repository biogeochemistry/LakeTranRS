import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os.path

ser = pd.period_range('2010-01-01', periods=(365*4+1)*2)
sns.set_style('whitegrid')

basedir = '../simulations/id/00313/'

design = pd.read_csv('../intermediate/parameterdict.csv')
bath = pd.read_csv('../bathymetry.csv', header=None)
bath.columns = ['zz', 'Az']
volume1d = 0.1 * (bath.Az + np.array(bath.Az[1:].tolist() + [0])) / 2.0 
# m3 for the 10cm slices
volume2d = np.ones(((365*4+1)*2, 1)) * volume1d.reshape((1, 90))


def plotsim(simids, fname, stitle):
    '''plots various outputs against the original simulation'''

    if type(simids) is not list:
        simids = [simids]
    simdir = ['../simulations/id/{:05d}/'.format(simid) for simid in simids]
    dirs = [basedir] + simdir
    designlevels = [design.loc[design.simid == id]\
                    .as_matrix().flatten().tolist() for id in simids]
    simnames = ['T{:d}W{:d}P{:d}C{:d}'.format(v1, v2, v3, v4) 
                for v1, v2, v3, v4, _ in designlevels]
    colnames = ['T3W3P3C3 base'] + simnames
    
    if len(simids) == 1:
        lw = 1.0
    else:
        lw = 0.5
    
    plt.clf()
    fig = plt.figure(0)
    fig.set_figheight(14)
    fig.set_figwidth(10)
    a1 = plt.subplot2grid((8, 4), (0, 0), colspan = 3)
    a1s = plt.subplot2grid((8, 4), (0, 3))
    a2 = plt.subplot2grid((8, 4), (1, 0), colspan = 3)
    a2s = plt.subplot2grid((8, 4), (1, 3))
    a3 = plt.subplot2grid((8, 4), (2, 0), colspan = 3)
    a3s = plt.subplot2grid((8, 4), (2, 3)) 
    a4 = plt.subplot2grid((8, 4), (3, 0), colspan = 3)
    a4s = plt.subplot2grid((8, 4), (3, 3)) 
    a5 = plt.subplot2grid((8, 4), (4, 0), colspan = 3)
    a5s = plt.subplot2grid((8, 4), (4, 3)) 
    a6 = plt.subplot2grid((8, 4), (5, 0), colspan = 3)
    a6s = plt.subplot2grid((8, 4), (5, 3)) 
    a7 = plt.subplot2grid((8, 4), (6, 0), colspan = 3)
    a7s = plt.subplot2grid((8, 4), (6, 3)) 
    a8 = plt.subplot2grid((8, 4), (7, 0), colspan = 3)
    a8s = plt.subplot2grid((8, 4), (7, 3)) 

    ## water temperature
    t = [pd.read_csv(os.path.join(dir, 't.csv.bz2'), header=None)
         for dir in dirs]
    t0 = pd.concat([d.iloc[:, 0] for d in t], axis=1)
    t0.columns = colnames
    t0.index = ser
    t0['doy'] = t0.index.day_of_year
    t0s = t0.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
    t0 = t0.drop('doy', 1)
    t1 = pd.concat([d.iloc[:, 20] for d in t], axis=1)
    t1.columns = colnames
    t1.index = ser
    t1['doy'] = t1.index.day_of_year
    t1s = t1.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
    t1 = t1.drop('doy', 1)
    t2 = pd.concat([d.iloc[:, 89] for d in t], axis=1)
    t2.columns = colnames
    t2.index = ser
    t2['doy'] = t2.index.day_of_year
    t2s = t2.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
    t2 = t2.drop('doy', 1)
    t0.iloc[:, 0].plot(color='lightgray', ax=a1, ylim=[0, 25], legend=False)
    t0.iloc[:, 1:].plot(ax=a1, linewidth=lw, legend=False)
    a1s.plot([0, 25], [0, 25], color='lightgray', linewidth=lw)
    for ci in range(1, t0s.shape[1]):
        a1s.plot(t0s.iloc[:, 0], t0s.iloc[:, ci])
    a1s.set_xlim([0, 25])
    a1s.set_ylim([0, 25])
    t1.iloc[:, 0].plot(color='lightgray', ax=a2, ylim=[0, 25], legend=False)
    t1.iloc[:, 1:].plot(ax=a2, linewidth=lw, legend=False)
    a2s.plot([0, 25], [0, 25], color='lightgray', linewidth=lw)
    for ci in range(1, t1s.shape[1]):
        a2s.plot(t1s.iloc[:, 0], t1s.iloc[:, ci])
    a2s.set_xlim([0, 25])
    a2s.set_ylim([0, 25])
    t2.iloc[:, 0].plot(color='lightgray', ax=a3, ylim=[0, 25], legend=False)
    t2.iloc[:, 1:].plot(ax=a3, linewidth=lw, legend=False)
    a3s.plot([0, 25], [0, 25], color='lightgray', linewidth=lw)
    for ci in range(1, t2s.shape[1]):
        a3s.plot(t2s.iloc[:, 0], t2s.iloc[:, ci])
    a3s.set_xlim([0, 25])
    a3s.set_ylim([0, 25])
    a1.set_ylabel('water temperature\nsurface')
    a2.set_ylabel('water temperature\nmiddle')
    a3.set_ylabel('water temperature\nbottom')

    ## ice
    his = [pd.read_csv(os.path.join(dir, 'His.csv.bz2'), header=None)
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
    o2 = [pd.read_csv(os.path.join(dir, 'O2abs.csv.bz2'), header=None)
          for dir in dirs]
    o22 = pd.concat([d.iloc[:, 20] for d in o2], axis=1)
    o22.columns = colnames
    o22.index = ser
    o22['doy'] = o22.index.day_of_year
    o22s = o22.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
    o22 = o22.drop('doy', 1)
    o23 = pd.concat([d.iloc[:, 89] for d in o2], axis=1)
    o23.columns = colnames
    o23.index = ser
    o23['doy'] = o23.index.day_of_year
    o23s = o23.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
    o23 = o23.drop('doy', 1)
    o22.iloc[:, 0].plot(color='lightgray', ax=a5, ylim=[0, 0.8], legend=False)
    o22.iloc[:, 1:].plot(ax=a5, linewidth=lw, legend=False)
    a5s.plot([0, 0.8], [0, 0.8], color='lightgray', linewidth=lw)
    for ci in range(1, o22s.shape[1]):
        a5s.plot(o22s.iloc[:, 0], o22s.iloc[:, ci])
    a5s.set_xlim([0, 0.8])
    a5s.set_ylim([0, 0.8])
    o23.iloc[:, 0].plot(color='lightgray', ax=a6, ylim=[0, 0.8], legend=False)
    o23.iloc[:, 1:].plot(ax=a6, linewidth=lw, legend=False)
    a6s.plot([0, 0.8], [0, 0.8], color='lightgray', linewidth=lw)
    for ci in range(1, o23s.shape[1]):
        a6s.plot(o23s.iloc[:, 0], o23s.iloc[:, ci])
    a6s.set_xlim([0, 0.8])
    a6s.set_ylim([0, 0.8])
    a5.set_ylabel('O2 concentration\nmiddle')
    a6.set_ylabel('O2 concentration\nbottom')

    ## chl (grams per whole lake)
    chl = [pd.read_csv(os.path.join(dir, 'chl.csv.bz2'), header=None)
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

    ## tp (grams per whole lake)
    tp = [pd.read_csv(os.path.join(dir, 'totp.csv.bz2'), header=None)
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

    a1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
              ncol=4, mode="expand", borderaxespad=0.)

    # for a in [a1, a2, a3, a4, a5, a6, a7, a8]:
    #     a.set_xlim(yl)
    a1s.set_title('2014-2017 DOY mean\ncompared against base')

    st = fig.suptitle(stitle, fontsize='x-large')
    st.set_y(0.95)

    fig.savefig(fname, dpi=150)
    return(fig)


# sns.set_palette('coolwarm', 2)
# plotsim([311, 315], 'results_raw/Air Temperature.png',
#         'impact of air temperature')

# sns.set_palette('Reds_r', 2)
# plotsim([303, 323], 'results_raw/Wind Speed.png', 
#         'impact of wind speed')

# sns.set_palette('Greens_r', 2)
# plotsim([263, 363], 'results_raw/Total P.png',
#         'impact of total P loading')

sns.set_palette('Reds', 2)
plotsim([63, 563], 'results_raw/DOC.png',
             'impact of DOC loading')

sns.set_palette('Oranges_d', 1)
# plotsim(311, 'results_raw/AT colder.png', 
#         '"lower air temperature" compared to "base"')
# plotsim(315, 'results_raw/AT warmer.png',
#         '"higher air temperature" compared to "base"')
plotsim(303, 'results_raw/WS calmer.png',
        '"calmer wind compared" to "base"')
# plotsim(323, 'results_raw/WS stronger.png',
#         '"stronger wind compared" to "base"')
# plotsim(263, 'results_raw/TP lower.png', 
#         '"less TP loading compared" to "base"')
# plotsim(363, 'results_raw/TP higher.png',
#         '"greater TP loading compared" to "base"')
# plotsim(63, 'results_raw/DOC lower.png',
#         '"less DOC loading compared" to "base"')
plotsim(563, 'results_raw/DOC higher.png',
        '"greater DOC loading compared" to "base"')

# plotsim(1, 'test001.png', '"low in everything" compared to "base"')
# plotsim(505, 'test505.png', '"id505" compared to "base"')
# plotsim(5, 'test005.png', '"id005" compared to "base"')
# plotsim(105, 'test105.png', '"id105" compared to "base"')
# plotsim(605, 'test605.png', '"id605" compared to "base"')
# plotsim(101, 'test101.png', '"id101" compared to "base"')
# plotsim(601, 'test601.png', '"id601" compared to "base"')
# plotsim(501, 'test501.png', '"id501" compared to "base"')
# plotsim(21, 'test021.png', '"id021" compared to "base"')
# plotsim(121, 'test121.png', '"id121" compared to "base"')
# plotsim(521, 'test521.png', '"id521" compared to "base"')
# plotsim(621, 'test621.png', '"id621" compared to "base"')


