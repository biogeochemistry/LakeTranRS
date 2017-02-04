import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os.path

ser = pd.period_range('2010-01-01', periods=(365*4+1)*2)
sns.set_style('whitegrid')

basedir = '../simulations/id/00163/'

design = pd.read_csv('../intermediate/parameterdict.csv')
bath = pd.read_csv('../bathymetry.csv', header=None)
bath.columns = ['zz', 'Az']
volume1d = 0.1 * (bath.Az + np.array(bath.Az[1:].tolist() + [0])) / 2.0 
# m3 for the 10cm slices
volume2d = np.ones(((365*4+1)*2, 1)) * volume1d.reshape((1, 90))


def plotsim(simids, fname):
    '''plots various outputs against the original simulation'''

    if type(simids) is not list:
        simids = [simids]
    simdir = ['../simulations/id/{:05d}/'.format(simid) for simid in simids]
    dirs = [basedir] + simdir
    designlevels = [design.loc[design.simid == id]\
                    .as_matrix().flatten().tolist() for id in simids]
    simnames = ['T{:d}W{:d}P{:d}C{:d}'.format(v1, v2, v3, v4) 
                for v1, v2, v3, v4, i in designlevels]
    colnames = ['T3W3P2C2 base'] + simnames
    
    
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
    t0.iloc[:, 0].plot(color='lightgray', ax=a1, ylim=[0, 25])
    t0.iloc[:, 1:].plot(ax=a1, linewidth=0.5)
    a1.legend()
    a1s.plot([0, 25], [0, 25], color='lightgray', linewidth=0.5)
    for ci in range(1, t0s.shape[1]):
        a1s.plot(t0s.iloc[:, 0], t0s.iloc[:, ci])
    a1s.set_xlim([0, 25])
    a1s.set_ylim([0, 25])
    t1.iloc[:, 0].plot(color='lightgray', ax=a2, ylim=[0, 25])
    t1.iloc[:, 1:].plot(ax=a2, linewidth=0.5)
    a2.legend()
    a2s.plot([0, 25], [0, 25], color='lightgray', linewidth=0.5)
    for ci in range(1, t1s.shape[1]):
        a2s.plot(t1s.iloc[:, 0], t1s.iloc[:, ci])
    a2s.set_xlim([0, 25])
    a2s.set_ylim([0, 25])
    t2.iloc[:, 0].plot(color='lightgray', ax=a3, ylim=[0, 25])
    t2.iloc[:, 1:].plot(ax=a3, linewidth=0.5)
    a3.legend()
    a3s.plot([0, 25], [0, 25], color='lightgray', linewidth=0.5)
    for ci in range(1, t2s.shape[1]):
        a3s.plot(t2s.iloc[:, 0], t2s.iloc[:, ci])
    a3s.set_xlim([0, 25])
    a3s.set_ylim([0, 25])
    
    ## ice
    his = [pd.read_csv(os.path.join(dir, 'His.csv.bz2'), header=None)
           for dir in dirs]
    ice = pd.concat([d.iloc[:, 0] for d in his], axis=1)
    ice.columns = colnames
    ice.index = ser
    ice['doy'] = ice.index.day_of_year
    ices = ice.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
    ice = ice.drop('doy', 1)
    ice.iloc[:, 0].plot(color='lightgray', ax=a4, ylim=[0, 0.8])
    ice.iloc[:, 1:].plot(ax=a4, linewidth=0.5)
    a4.legend()
    a4s.plot([0, 0.8], [0, 0.8], color='lightgray', linewidth=0.5)
    for ci in range(1, ices.shape[1]):
        a4s.plot(ices.iloc[:, 0], ices.iloc[:, ci])
    a4s.set_xlim([0, 0.8])
    a4s.set_ylim([0, 0.8])

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
    o22.iloc[:, 0].plot(color='lightgray', ax=a5, ylim=[0, 0.8])
    o22.iloc[:, 1:].plot(ax=a5, linewidth=0.5)
    a5.legend()
    a5s.plot([0, 0.8], [0, 0.8], color='lightgray', linewidth=0.5)
    for ci in range(1, o22s.shape[1]):
        a5s.plot(o22s.iloc[:, 0], o22s.iloc[:, ci])
    a5s.set_xlim([0, 0.8])
    a5s.set_ylim([0, 0.8])
    o23.iloc[:, 0].plot(color='lightgray', ax=a6, ylim=[0, 0.8])
    o23.iloc[:, 1:].plot(ax=a6, linewidth=0.5)
    a6.legend()
    a6s.plot([0, 0.8], [0, 0.8], color='lightgray', linewidth=0.5)
    for ci in range(1, o23s.shape[1]):
        a6s.plot(o23s.iloc[:, 0], o23s.iloc[:, ci])
    a6s.set_xlim([0, 0.8])
    a6s.set_ylim([0, 0.8])

    ## chl (grams per whole lake)
    chl = [pd.read_csv(os.path.join(dir, 'chl.csv.bz2'), header=None)
          for dir in dirs]
    chlp = pd.concat([np.sum(d * volume2d, axis=1) / 1e3 for d in chl], axis=1)
    chlp.columns = colnames
    chlp.index = ser
    chlp['doy'] = chlp.index.day_of_year
    chlps = chlp.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
    chlp = chlp.drop('doy', 1)    
    chlp.iloc[:, 0].plot(color='lightgray', ax=a7, ylim=[0, 2e0])
    chlp.iloc[:, 1:].plot(ax=a7, linewidth=0.5)
    a7.legend()
    a7s.plot([0, 2e0], [0, 2e0], color='lightgray', linewidth=0.5)
    for ci in range(1, chlps.shape[1]):
        a7s.plot(chlps.iloc[:, 0], chlps.iloc[:, ci])
    a7s.set_xlim([0, 2e0])
    a7s.set_ylim([0, 2e0])

    ## tp (grams per whole lake)
    tp = [pd.read_csv(os.path.join(dir, 'totp.csv.bz2'), header=None)
          for dir in dirs]
    tpp = pd.concat([np.sum(d * volume2d, axis=1) / 1e3 for d in tp], axis=1)
    tpp.columns = colnames
    tpp.index = ser
    tpp['doy'] = tpp.index.day_of_year
    tpps = tpp.iloc[(365*4+1):, :].groupby('doy').mean().iloc[:365, :]
    tpp = tpp.drop('doy', 1)    
    tpp.iloc[:, 0].plot(color='lightgray', ax=a8, ylim=[2e0, 6e0])
    tpp.iloc[:, 1:].plot(ax=a8, linewidth=0.5)
    a8.legend()
    a8s.plot([2e0, 6e0], [2e0, 6e0], color='lightgray', linewidth=0.5)
    for ci in range(1, tpps.shape[1]):
        a8s.plot(tpps.iloc[:, 0], tpps.iloc[:, ci])
    a8s.set_xlim([2e0, 6e0])
    a8s.set_ylim([2e0, 6e0])


    fig.savefig(fname)
    return(fig)

sns.set_palette('coolwarm', 4)
plotsim([161, 162, 164, 165], 'results_raw/Air Temperature.pdf')

sns.set_palette('Reds_r', 3)
plotsim([153, 158, 168], 'results_raw/Wind Speed.pdf')

sns.set_palette('Greens_r', 3)
plotsim([138, 213, 238], 'results_raw/Total P.pdf')

sns.set_palette('Reds_r', 1)
plotsim([38], 'results_raw/DOC.pdf')
