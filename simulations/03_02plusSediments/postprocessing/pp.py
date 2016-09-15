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
nr = 5 # responses

a = np.ndarray((n1, n2, n3, n4, nt, nz, nr), dtype=np.float) * np.nan

d = pd.read_csv('../intermediate//parameterdict.csv')

for i, x1, x2, x3, x4, id in d.itertuples():
    t = pd.read_csv('../simulations/id/{:02d}/t.csv.bz2'.format(id), header=None).as_matrix()
    chl = pd.read_csv('../simulations/id/{:02d}/chl.csv.bz2'.format(id), header=None).as_matrix()
    tp = pd.read_csv('../simulations/id/{:02d}/totp.csv.bz2'.format(id), header=None).as_matrix()
    o2a = pd.read_csv('../simulations/id/{:02d}/O2abs.csv.bz2'.format(id), header=None).as_matrix()
    o2r = pd.read_csv('../simulations/id/{:02d}/O2rel.csv.bz2'.format(id), header=None).as_matrix()
    a[x1-1, x2-1, x3-1, x4-1, :, :, 0] = t
    a[x1-1, x2-1, x3-1, x4-1, :, :, 1] = chl
    a[x1-1, x2-1, x3-1, x4-1, :, :, 2] = tp
    a[x1-1, x2-1, x3-1, x4-1, :, :, 3] = o2a
    a[x1-1, x2-1, x3-1, x4-1, :, :, 4] = o2r


## maximum chl in last year
r1 = a[:, :, :, :, (365*3):, 0, 1].max(axis=4)
r1max = r1.max() ; r1min = r1.min()

## number days surface anoxia in last year
r2 = (a[:, :, :, :, (365*3):, 0, 3] < 0.01).sum(axis=4)
r2max = r1.max() ; r2min = r2.min()


cm = plt.get_cmap('YlGnBu')

## T, TP, TPR, DOC on CHL, ANOXIA
## figures 
fig = plt.figure() ; ax = fig.add_subplot(111)
ax.imshow(r1[:, :, 0, 0], vmin=r1min, vmax=r1max, cmap=cm)
fig.savefig('../figures/T+TP on chl.png')
fig = plt.figure() ; ax = fig.add_subplot(111)
ax.imshow(r1[:, 0, :, 0], vmin=r1min, vmax=r1max, cmap=cm)
fig.savefig('../figures/T+TPR on chl.png')
fig = plt.figure() ; ax = fig.add_subplot(111)
ax.imshow(r1[:, 0, 0, :], vmin=r1min, vmax=r1max, cmap=cm)
fig.savefig('../figures/T+DOC on chl.png')
fig = plt.figure() ; ax = fig.add_subplot(111)
ax.imshow(r1[0, :, :, 0], vmin=r1min, vmax=r1max, cmap=cm)
fig.savefig('../figures/TP+TPR on chl.png')
fig = plt.figure() ; ax = fig.add_subplot(111)
ax.imshow(r1[0, :, 0, :], vmin=r1min, vmax=r1max, cmap=cm)
fig.savefig('../figures/TP+DOC on chl.png')
fig = plt.figure() ; ax = fig.add_subplot(111)
ax.imshow(r1[0, 0, :, :], vmin=r1min, vmax=r1max, cmap=cm)
fig.savefig('../figures/TPR+DOC on chl.png')

fig = plt.figure() ; ax = fig.add_subplot(111)
ax.imshow(r2[:, :, 0, 0], vmin=r2min, vmax=r2max, cmap=cm)
fig.savefig('../figures/T+TP on anoxia.png')
fig = plt.figure() ; ax = fig.add_subplot(111)
ax.imshow(r2[:, 0, :, 0], vmin=r2min, vmax=r2max, cmap=cm)
fig.savefig('../figures/T+TPR on anoxia.png')
fig = plt.figure() ; ax = fig.add_subplot(111)
ax.imshow(r2[:, 0, 0, :], vmin=r2min, vmax=r2max, cmap=cm)
fig.savefig('../figures/T+DOC on anoxia.png')
fig = plt.figure() ; ax = fig.add_subplot(111)
ax.imshow(r2[0, :, :, 0], vmin=r2min, vmax=r2max, cmap=cm)
fig.savefig('../figures/TP+TPR on anoxia.png')
fig = plt.figure() ; ax = fig.add_subplot(111)
ax.imshow(r2[0, :, 0, :], vmin=r2min, vmax=r2max, cmap=cm)
fig.savefig('../figures/TP+DOC on anoxia.png')
fig = plt.figure() ; ax = fig.add_subplot(111)
ax.imshow(r2[0, 0, :, :], vmin=r2min, vmax=r2max, cmap=cm)
fig.savefig('../figures/TPR+DOC on anoxia.png')
