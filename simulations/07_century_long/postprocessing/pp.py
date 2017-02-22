import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


d = pd.read_csv('../results/sedfluxes.csv.bz2', 
                names =  ['OM', 'OM2', 'Oxygen', 'PO4', 'Fe2+', 
                          'NO3-', 'NH4+', 'Al(OH)3', 'PO4adsa', 'Fe(OH)3'])
d.index = pd.period_range('2001-01-01', '2100-12-31')


sns.set_style('whitegrid')

for name, ser in d.resample('A').mean().iteritems():
    plt.clf()
    a = ser.iloc[3:].plot()
    a.set_ylabel(name)
    fig = plt.gcf()
    fig.set_figheight(4)
    fig.set_figwidth(6)
    fig.set_dpi(600)
    fig.savefig('../figures/sed{:s}.png'.format(name), bbox_inches='tight')



atdepths = [0, 15, 30, 45, 60, 75, 89]




d = pd.read_csv('../results/01 one-century only/O2abs.csv.bz2', header = None)
d.index = pd.period_range('2001-01-01', '2100-12-31')

plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111)
for ad in atdepths:
    d.iloc[:, ad].resample('A').mean().iloc[3:].plot(ax=ax)
leg = ax.legend(loc='upper left', frameon=True)

ax.set_ylabel('O2 absolute by depth')
fig.savefig('../figures/O2abs.png', bbox_inches='tight')
ax.set_ylim((0.015, 0.08))
ax.set_ylabel('O2 absolute by depth (zoomed)')
fig.savefig('../figures/O2abs_zoomed.png', bbox_inches='tight')




d = pd.read_csv('../results/totp.csv.bz2', header = None)
d.index = pd.period_range('2001-01-01', '2100-12-31')

plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111)
for ad in atdepths:
    d.iloc[:, ad].resample('A').mean().iloc[3:].plot(ax=ax)
leg = ax.legend(loc='upper left', frameon=True)

ax.set_ylabel('Total P by depth')
fig.savefig('../figures/TotP.png', bbox_inches='tight')

ax.set_ylim((0.0175, 0.028))
ax.set_ylabel('Total P by depth (zoomed)')
fig.savefig('../figures/TotP_zoomed.png', bbox_inches='tight')




d = pd.read_csv('../results/chl.csv.bz2', header = None)
d.index = pd.period_range('2001-01-01', '2100-12-31')

plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111)
for ad in atdepths:
    d.iloc[:, ad].resample('A').mean().iloc[3:].plot(ax=ax)
leg = ax.legend(loc='upper left', frameon=True)

ax.set_ylabel('Chl by depth')
fig.savefig('../figures/Chl.png', bbox_inches='tight')
ax.set_ylim((0.0039, 0.0044))
ax.set_ylabel('Chl by depth (zoomed)')
fig.savefig('../figures/Chl_zoomed.png', bbox_inches='tight')

