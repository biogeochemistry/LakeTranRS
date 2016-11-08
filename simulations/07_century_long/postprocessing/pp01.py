import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

atdepths = [0, 15, 30, 45, 60, 75, 89]


dlist = [pd.read_csv('../results/{:d}O2abs.csv.bz2'.format(cent), header=None)
         for cent in range(10)]
d = pd.concat(dlist, ignore_index=True)
d.index = pd.period_range('2001-01-01', '3000-12-29')

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



dlist = [pd.read_csv('../results/{:d}totp.csv.bz2'.format(cent), header=None)
         for cent in range(10)]
d = pd.concat(dlist, ignore_index=True)
d.index = pd.period_range('2001-01-01', '3000-12-29')

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

plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111)
for ad in atdepths:
    d4 = d.groupby((d.index.year - 1) // 4, as_index=False, group_keys=False).mean()
    d4.index = pd.PeriodIndex(pd.PeriodIndex(range(2001, 3000, 4), freq='4A'))
    d4.plot(ax=ax)
leg = ax.legend(loc='upper left', frameon=True)

ax.set_ylabel('Total P by depth 4-y mean')
fig.savefig('../figures/TotP4y.png', bbox_inches='tight')

ax.set_ylim((0.0175, 0.028))
ax.set_ylabel('Total P by depth 4-y mean (zoomed) ')
fig.savefig('../figures/TotP4y_zoomed.png', bbox_inches='tight')



dlist = [pd.read_csv('../results/{:d}chl.csv.bz2'.format(cent), header=None)
         for cent in range(10)]
d = pd.concat(dlist, ignore_index=True)
d.index = pd.period_range('2001-01-01', '3000-12-29')

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

