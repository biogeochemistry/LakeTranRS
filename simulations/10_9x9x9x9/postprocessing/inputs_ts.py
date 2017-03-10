'''creates input time series, 
need to add black line over the base input'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

## change these for customisation
ser = pd.period_range('2010-01-01', periods=(365*4+1)*1)
sns.set_style('whitegrid')
nvars = 4
nlevels = 9
shortnames = ['Var{:d}'.format(ci) for ci in range(1, 5)]
palettes = ['coolwarm', 'Reds', 'Greens', 'cubehelix_r']
longnames = ['Air Temperature', 
             'Wind Speed',
             'Total P',
             'DOC']
# longnames = ['Air Temperature (degree C)', 
#              'Wind Speed (m s-1)',
#              'Total P (kg)',
#              'DOC (tonne)']
ylabels = ['Air Temperature (degree C)', 
           'Wind Speed (m s-1)',
           'Total P (mg d-1)',
           'DOC (mg d-1)']
columnnames = [['AirTemperature'], 
               ['WindSpeed'], 
               ['InflowQ', 'InflowTP'], # [mg] no need to include DOP and Chla?
               ['InflowQ', 'InflowDOC']] # [mg]
keynames = ['AT', 'WS', 'TP', 'DOC']
functions = [np.mean, 
             np.mean, 
             lambda x: sum(x) / 1e6, # [kg]
             lambda x: sum(x) / 1e9] # [tonne]
functionnames = ['mean', 'mean', 'total', 'total']
statunits = ['deg C', 'm s-1', 'kg', 't']
formats = ['{:.2f}', '{:.2f}', '{:.2f}', '{:.1f}']


design = pd.read_csv('../intermediate/parameterdict.csv')
levels = range(1, 1 + nlevels)

for vi in range(nvars):
    sn = shortnames[vi]
    ln = longnames[vi]
    cn = columnnames[vi]
    kn = keynames[vi]
    fn = functions[vi]
    fnn = functionnames[vi]
    ft = formats[vi]
    un = statunits[vi]
    yl = ylabels[vi]
    pl = palettes[vi]

    ## get the 9 time series for the 9 levels 
    simids = [design.loc[design[sn] == li].simid.iloc[0] for li in levels]
    paths = ['../intermediate/id/{:06d}/input.txt'.format(id) for id in simids]
    inputs0 = [pd.read_table(p, skiprows=1, header=0)[cn] for p in paths]
    inputs = [df.product(axis=1) for df in inputs0]  # converts to flux if necessary
    d = pd.concat(inputs, axis=1)  # put together sideways
    stats = d.apply(fn, axis=0)
    d.columns = ['{:s}{:d}: {:s} {:s} {:s}'.format(kn, li, fnn, 
                                                   ft.format(stats[li-1]), un)
                 for li in levels]  # rename
    d.index = ser

    sns.set_palette(pl)
    plt.clf()
    fig = plt.figure(0)
    a0 = fig.add_subplot(111)

    # d.plot(ax=a0)
    d.iloc[:, [0, 4, 8]].plot(ax=a0) # use only the extremes and middle

    a0.set_ylabel(yl)
    fig.savefig('inputs/{:s}.png'.format(ln), dpi=150)

