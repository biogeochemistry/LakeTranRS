import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

n1 = 3
n2 = 3
n3 = 3
n4 = 3
nt = 1461
nz = 90
nr = 4 # responses

a = np.ndarray((n1, n2, n3, n4, nt, nz, nr), dtype=np.float) * np.nan

d = pd.read_csv('../intermediate//parameterdict.csv')

for i, x1, x2, x3, x4, id in d.itertuples():
    t = pd.read_csv('../simulations/id/{:02d}/t.csv.bz2'.format(id), header=None).as_matrix()
    chl = pd.read_csv('../simulations/id/{:02d}/chl.csv.bz2'.format(id), header=None).as_matrix()
    tp = pd.read_csv('../simulations/id/{:02d}/totp.csv.bz2'.format(id), header=None).as_matrix()
    o2a = pd.read_csv('../simulations/id/{:02d}/O2abs.csv.bz2'.format(id), header=None).as_matrix()
    # o2r = pd.read_csv('../simulations/id/{:02d}/O2rel.csv.bz2'.format(id), header=None).as_matrix()
    a[x1-1, x2-1, x3-1, x4-1, :, :, 0] = t
    a[x1-1, x2-1, x3-1, x4-1, :, :, 1] = chl
    a[x1-1, x2-1, x3-1, x4-1, :, :, 2] = tp
    a[x1-1, x2-1, x3-1, x4-1, :, :, 3] = o2a
    # a[x1-1, x2-1, x3-1, x4-1, :, :, 4] = o2r


## maximum chl in last year
r1 = a[:, :, :, :, (365*3+180):(365*3+270), 0, 1].mean(axis=4)
r1max = r1.max() ; r1min = r1.min()

## number days surface anoxia in last year
r2 = (a[:, :, :, :, (365*3):, 0, 3] < 0.01).sum(axis=4)
r2max = r1.max() ; r2min = r2.min()


cmr = plt.get_cmap('Reds')
normr = matplotlib.colors.Normalize(r1.min(), r1.max(), True)

cmg = plt.get_cmap('Greens')
normg = matplotlib.colors.Normalize(r2.min(), r2.max(), True)



## T, TP, TPR, DOC on CHL, ANOXIA
## figures 
## fig = plt.figure()

fig1, ((a1, a2, a3), (a4, a5, a6), (a7, a8, a9), (a10, a11, a12)) = \
plt.subplots(nrows=4, ncols=3)

fig1.set_size_inches((8, 10))

a4.imshow(r1[:, :, 0, 0].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
# # fig.savefig('../figures/T+TP on chl.png')
a6.imshow(r1[:, 0, :, 0].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
# # fig.savefig('../figures/T+TPR on chl.png')
a2.imshow(r1[:, 0, 0, :].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
# fig.savefig('../figures/T+DOC on chl.png')
a10.imshow(r1[1, :, :, 0].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
# fig.savefig('../figures/TP+TPR on chl.png')
a8.imshow(r1[1, :, 0, :].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
# fig.savefig('../figures/TP+DOC on chl.png')
a12.imshow(r1[1, 0, :, :].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
# fig.savefig('../figures/TPR+DOC on chl.png')

a3.imshow(r2[:, :, 0, 0].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
# fig.savefig('../figures/T+TP on anoxia.png')
a5.imshow(r2[:, 0, :, 0].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
# fig.savefig('../figures/T+TPR on anoxia.png')
a1.imshow(r2[:, 0, 0, :].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
# fig.savefig('../figures/T+DOC on anoxia.png')
a9.imshow(r2[1, :, :, 0].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
# fig.savefig('../figures/TP+TPR on anoxia.png')
a7.imshow(r2[1, :, 0, :].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
# fig.savefig('../figures/TP+DOC on anoxia.png')
a11.imshow(r2[1, 0, :, :].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
# fig.savefig('../figures/TPR+DOC on anoxia.png')

a1.text(1.0, -0.7, 'T', ha='center', va='center') ; a1.text(-0.5, 1.0, 'DOC', va='center', ha='right', rotation='vertical')
a2.text(1.0, -0.7, 'T', ha='center', va='center') ; a2.text(-0.5, 1.0, 'DOC', va='center', ha='right', rotation='vertical')
a3.text(1.0, -0.7, 'T', ha='center', va='center') ; a3.text(-0.5, 1.0, 'TP', va='center', ha='right', rotation='vertical')
a4.text(1.0, -0.7, 'T', ha='center', va='center') ; a4.text(-0.5, 1.0, 'TP', va='center', ha='right', rotation='vertical')
a5.text(1.0, -0.7, 'T', ha='center', va='center') ; a5.text(-0.5, 1.0, 'TPR', va='center', ha='right', rotation='vertical')
a6.text(1.0, -0.7, 'T', ha='center', va='center') ; a6.text(-0.5, 1.0, 'TPR', va='center', ha='right', rotation='vertical')
a7.text(1.0, -0.7, 'TP', ha='center', va='center') ; a7.text(-0.5, 1.0, 'DOC', va='center', ha='right', rotation='vertical')
a8.text(1.0, -0.7, 'TP', ha='center', va='center') ; a8.text(-0.5, 1.0, 'DOC', va='center', ha='right', rotation='vertical')
a9.text(1.0, -0.7, 'TP', ha='center', va='center') ; a9.text(-0.5, 1.0, 'TPR', va='center', ha='right', rotation='vertical')
a10.text(1.0, -0.7, 'TP', ha='center', va='center') ; a10.text(-0.5, 1.0, 'TPR', va='center', ha='right', rotation='vertical')
a11.text(1.0, -0.7, 'TPR', ha='center', va='center') ; a11.text(-0.5, 1.0, 'DOC', va='center', ha='right', rotation='vertical')
a12.text(1.0, -0.7, 'TPR', ha='center', va='center') ; a12.text(-0.5, 1.0, 'DOC', va='center', ha='right', rotation='vertical')


for a in fig1.get_axes():
    a.get_xaxis().set_visible(False)
    a.get_yaxis().set_visible(False)

fig1.savefig('../figures/combined.png')
