import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import numpy.ma as ma

n1 = 10
n2 = 10
n4 = 10
nt = 1461
nz = 90
nr = 4 # responses

aa = np.ndarray((n1, n2, n4, nt, nz, nr), dtype=np.float) * np.nan
m = np.zeros((n1, n2, n4, nt, nz, nr), dtype=bool) 

d = pd.read_csv('../intermediate//parameterdict.csv')

for i, x1, x2, x3, x4, id in d.itertuples():
    if i % 100 == 100:
        print(i)
    if not os.path.exists('../simulations/id/{:05d}/t.csv.bz2'.format(id)):
        print(i, x1, x2, x3, x4, id)
        continue
    t = pd.read_csv('../simulations/id/{:05d}/t.csv.bz2'.format(id), header=None).as_matrix()
    chl = pd.read_csv('../simulations/id/{:05d}/chl.csv.bz2'.format(id), header=None).as_matrix()
    tp = pd.read_csv('../simulations/id/{:05d}/totp.csv.bz2'.format(id), header=None).as_matrix()
    o2a = pd.read_csv('../simulations/id/{:05d}/O2abs.csv.bz2'.format(id), header=None).as_matrix()
    aa[x1-1, x2-1, x4-1, :, :, 0] = t
    aa[x1-1, x2-1, x4-1, :, :, 1] = chl
    aa[x1-1, x2-1, x4-1, :, :, 2] = tp
    aa[x1-1, x2-1, x4-1, :, :, 3] = o2a
    # aa[x1-1, x2-1, x3-1, x4-1, :, :, 4] = o2r

for i, x1, x2, x3, x4, id in d.itertuples():
    if not os.path.exists('../simulations/id/{:05d}/t.csv.bz2'.format(id)):
        print(i, x1-1, x2-1, x3-1, x4-1, id)
        m[x1-1, x2-1, x4-1, :, :, :] = True

a = ma.masked_array(aa, mask=m)
a = aa

## maximum chl in last year
r1 = a[:, :, :, (365*3+180):(365*3+270), 0, 1].mean(axis=3)
r1max = r1.max() ; r1min = r1.min()

## number days surface anoxia in last year
r2 = (a[:, :, :, (365*3):, 0, 3] < 0.01).sum(axis=3)
r2max = r2.max() ; r2min = r2.min()


cmg = plt.get_cmap('Greens')
normg = matplotlib.colors.Normalize(r1min, r1max, True)

cmr = plt.get_cmap('Reds')
normr = matplotlib.colors.Normalize(r2min, r2max, True)



## T, TP, TPR, DOC on CHL, ANOXIA
## figures 
## fig = plt.figure()

# fig1, ((a1, a2, a3), (a4, a5, a6), (a7, a8, a9), (a10, a11, a12)) = \
# plt.subplots(nrows=4, ncols=3)
fig1, ((a1, a3, a5), (a7, a9, a11), (a2, a4, a6), (a8, a10, a12)) = \
plt.subplots(nrows=4, ncols=3)

fig1.set_size_inches((8, 10))

## contour preparation
x = np.arange(10)
y = np.arange(10)
X, Y = np.meshgrid(x, y)



imgg = a4.imshow(r1[:, :, 2].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
c4 = a4.contour(X, Y, r1[:, :, 2].transpose(), colors='black')
a4.clabel(c4, inline=1, fontsize=8, colors='black', fmt='%.2f')
# # fig.savefig('../figures/T+TP on chl.png')
# a6.imshow(r1[:, 0, :, 0].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
# c6 = a6.contour(X, Y, r1[:, 0, :, 0].transpose(), colors='black')
# a6.clabel(c6, inline=1, fontsize=8, colors='black', fmt='%.2f')
# # # fig.savefig('../figures/T+FE on chl.png')
a2.imshow(r1[:, 2, :].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
c2 = a2.contour(X, Y, r1[:, 2, :].transpose(), colors='black')
a2.clabel(c2, inline=1, fontsize=8, colors='black', fmt='%.2f')
# fig.savefig('../figures/T+DOC on chl.png')
# a10.imshow(r1[1, :, :, 0].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
# c10 = a10.contour(X, Y, r1[1, :, :, 0].transpose(), colors='black')
# a10.clabel(c10, inline=1, fontsize=8, colors='black', fmt='%.2f')
# # fig.savefig('../figures/TP+FE on chl.png')
a8.imshow(r1[6, :, :].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
c8 = a8.contour(X, Y, r1[6, :, :].transpose(), colors='black')
a8.clabel(c8, inline=1, fontsize=8, colors='black', fmt='%.2f')
# fig.savefig('../figures/TP+DOC on chl.png')
# a12.imshow(r1[1, 0, :, :].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
# c12 = a12.contour(X, Y, r1[1, 0, :, :].transpose(), colors='black')
# a12.clabel(c12, inline=1, fontsize=8, colors='black', fmt='%.2f')
# # fig.savefig('../figures/FE+DOC on chl.png')

imgr = a3.imshow(r2[:, :, 2].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
c3 = a3.contour(X, Y, r2[:, :, 2].transpose(), colors='black')
a3.clabel(c3, inline=1, fontsize=8, colors='black', fmt='%d')
# fig.savefig('../figures/T+TP on anoxia.png')
# a5.imshow(r2[:, 0, :, 0].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
# c5 = a5.contour(X, Y, r2[:, 0, :, 0].transpose(), colors='black')
# a5.clabel(c5, inline=1, fontsize=8, colors='black', fmt='%d')
# # fig.savefig('../figures/T+FE on anoxia.png')
a1.imshow(r2[:, 2, :].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
c1 = a1.contour(X, Y, r2[:, 2, :].transpose(), colors='black')
a1.clabel(c1, inline=1, fontsize=8, colors='black', fmt='%d')
# fig.savefig('../figures/T+DOC on anoxia.png')
# a9.imshow(r2[1, :, :, 0].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
# c9 = a9.contour(X, Y, r2[1, :, :, 0].transpose(), colors='black')
# a9.clabel(c9, inline=1, fontsize=8, colors='black', fmt='%d')
# # fig.savefig('../figures/TP+FE on anoxia.png')
a7.imshow(r2[6, :, :].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
c7 = a7.contour(X, Y, r2[6, :, :].transpose(), colors='black')
a7.clabel(c7, inline=1, fontsize=8, colors='black', fmt='%d')
# fig.savefig('../figures/TP+DOC on anoxia.png')
# a11.imshow(r2[1, 0, :, :].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
# c11 = a11.contour(X, Y, r2[1, 0, :, :].transpose(), colors='black')
# a11.clabel(c11, inline=1, fontsize=8, colors='black', fmt='%d')
# # fig.savefig('../figures/FE+DOC on anoxia.png')

a1.text(4.5, -1.5, 'T', ha='center', va='center') ; a1.text(-0.9, 4.5, 'DOC', va='center', ha='right', rotation='vertical')
a2.text(4.5, -1.5, 'T', ha='center', va='center') ; a2.text(-0.9, 4.5, 'DOC', va='center', ha='right', rotation='vertical')
a3.text(4.5, -1.5, 'T', ha='center', va='center') ; a3.text(-0.9, 4.5, 'TP', va='center', ha='right', rotation='vertical')
a4.text(4.5, -1.5, 'T', ha='center', va='center') ; a4.text(-0.9, 4.5, 'TP', va='center', ha='right', rotation='vertical')
# a5.text(4.5, -1.5, 'T', ha='center', va='center') ; a5.text(-0.9, 4.5, 'FE', va='center', ha='right', rotation='vertical')
# a6.text(4.5, -1.5, 'T', ha='center', va='center') ; a6.text(-0.9, 4.5, 'FE', va='center', ha='right', rotation='vertical')
a7.text(4.5, -1.5, 'TP', ha='center', va='center') ; a7.text(-0.9, 4.5, 'DOC', va='center', ha='right', rotation='vertical')
a8.text(4.5, -1.5, 'TP', ha='center', va='center') ; a8.text(-0.9, 4.5, 'DOC', va='center', ha='right', rotation='vertical')
# a9.text(4.5, -1.5, 'TP', ha='center', va='center') ; a9.text(-0.9, 4.5, 'FE', va='center', ha='right', rotation='vertical')
# a10.text(4.5, -1.5, 'TP', ha='center', va='center') ; a10.text(-0.9, 4.5, 'FE', va='center', ha='right', rotation='vertical')
# a11.text(4.5, -1.5, 'FE', ha='center', va='center') ; a11.text(-0.9, 4.5, 'DOC', va='center', ha='right', rotation='vertical')
# a12.text(4.5, -1.5, 'FE', ha='center', va='center') ; a12.text(-0.9, 4.5, 'DOC', va='center', ha='right', rotation='vertical')


for ax in fig1.get_axes():
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_axis_bgcolor('black')

# add colorbars with own axes
cbar = fig1.add_axes([0.92, 0.55, 0.03, 0.3])
plt.colorbar(imgr, cax = cbar)
cbag = fig1.add_axes([0.92, 0.15, 0.03, 0.3])
plt.colorbar(imgg, cax = cbag)

fig1.text(0.07, 0.3, 'mean summer Chla concentration', rotation='vertical', weight='bold', va='center')
fig1.text(0.07, 0.7, 'number surface anoxia days 2013', rotation='vertical', weight='bold', va='center')


fig1.savefig('../figures/combined_reordered.png')
fig1.savefig('../figures/combined_reordered.pdf')






## maximum chl in last year
r1 = a[:, :, :, (365*3+180):(365*3+270), 80, 1].mean(axis=3)
r1max = r1.max() ; r1min = r1.min()

## number days surface anoxia in last year
r2 = (a[:, :, :, (365*3):, 80, 3] < 0.01).sum(axis=3)
r2max = r2.max() ; r2min = r2.min()


cmg = plt.get_cmap('Greens')
normg = matplotlib.colors.Normalize(r1min, r1max, True)

cmr = plt.get_cmap('Reds')
normr = matplotlib.colors.Normalize(r2min, r2max, True)



## T, TP, TPR, DOC on CHL, ANOXIA
## figures 
## fig = plt.figure()

# fig1, ((a1, a2, a3), (a4, a5, a6), (a7, a8, a9), (a10, a11, a12)) = \
# plt.subplots(nrows=4, ncols=3)
fig1, ((a1, a3, a5), (a7, a9, a11), (a2, a4, a6), (a8, a10, a12)) = \
plt.subplots(nrows=4, ncols=3)

fig1.set_size_inches((8, 10))

## contour preparation
x = np.arange(10)
y = np.arange(10)
X, Y = np.meshgrid(x, y)



imgg = a4.imshow(r1[:, :, 2].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
c4 = a4.contour(X, Y, r1[:, :, 2].transpose(), colors='black')
a4.clabel(c4, inline=1, fontsize=8, colors='black', fmt='%.2f')
# # fig.savefig('../figures/T+TP on chl.png')
# a6.imshow(r1[:, 0, :, 0].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
# c6 = a6.contour(X, Y, r1[:, 0, :, 0].transpose(), colors='black')
# a6.clabel(c6, inline=1, fontsize=8, colors='black', fmt='%.2f')
# # # fig.savefig('../figures/T+FE on chl.png')
a2.imshow(r1[:, 2, :].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
c2 = a2.contour(X, Y, r1[:, 2, :].transpose(), colors='black')
a2.clabel(c2, inline=1, fontsize=8, colors='black', fmt='%.2f')
# fig.savefig('../figures/T+DOC on chl.png')
# a10.imshow(r1[1, :, :, 0].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
# c10 = a10.contour(X, Y, r1[1, :, :, 0].transpose(), colors='black')
# a10.clabel(c10, inline=1, fontsize=8, colors='black', fmt='%.2f')
# # fig.savefig('../figures/TP+FE on chl.png')
a8.imshow(r1[6, :, :].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
c8 = a8.contour(X, Y, r1[6, :, :].transpose(), colors='black')
a8.clabel(c8, inline=1, fontsize=8, colors='black', fmt='%.2f')
# fig.savefig('../figures/TP+DOC on chl.png')
# a12.imshow(r1[1, 0, :, :].transpose(), cmap=cmg, norm=normg, origin='lower', interpolation='none')
# c12 = a12.contour(X, Y, r1[1, 0, :, :].transpose(), colors='black')
# a12.clabel(c12, inline=1, fontsize=8, colors='black', fmt='%.2f')
# # fig.savefig('../figures/FE+DOC on chl.png')

imgr = a3.imshow(r2[:, :, 2].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
c3 = a3.contour(X, Y, r2[:, :, 2].transpose(), colors='black')
a3.clabel(c3, inline=1, fontsize=8, colors='black', fmt='%d')
# fig.savefig('../figures/T+TP on anoxia.png')
# a5.imshow(r2[:, 0, :, 0].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
# c5 = a5.contour(X, Y, r2[:, 0, :, 0].transpose(), colors='black')
# a5.clabel(c5, inline=1, fontsize=8, colors='black', fmt='%d')
# # fig.savefig('../figures/T+FE on anoxia.png')
a1.imshow(r2[:, 2, :].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
c1 = a1.contour(X, Y, r2[:, 2, :].transpose(), colors='black')
a1.clabel(c1, inline=1, fontsize=8, colors='black', fmt='%d')
# fig.savefig('../figures/T+DOC on anoxia.png')
# a9.imshow(r2[1, :, :, 0].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
# c9 = a9.contour(X, Y, r2[1, :, :, 0].transpose(), colors='black')
# a9.clabel(c9, inline=1, fontsize=8, colors='black', fmt='%d')
# # fig.savefig('../figures/TP+FE on anoxia.png')
a7.imshow(r2[6, :, :].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
c7 = a7.contour(X, Y, r2[6, :, :].transpose(), colors='black')
a7.clabel(c7, inline=1, fontsize=8, colors='black', fmt='%d')
# fig.savefig('../figures/TP+DOC on anoxia.png')
# a11.imshow(r2[1, 0, :, :].transpose(), cmap=cmr, norm=normr, origin='lower', interpolation='none')
# c11 = a11.contour(X, Y, r2[1, 0, :, :].transpose(), colors='black')
# a11.clabel(c11, inline=1, fontsize=8, colors='black', fmt='%d')
# # fig.savefig('../figures/FE+DOC on anoxia.png')

a1.text(4.5, -1.5, 'T', ha='center', va='center') ; a1.text(-0.9, 4.5, 'DOC', va='center', ha='right', rotation='vertical')
a2.text(4.5, -1.5, 'T', ha='center', va='center') ; a2.text(-0.9, 4.5, 'DOC', va='center', ha='right', rotation='vertical')
a3.text(4.5, -1.5, 'T', ha='center', va='center') ; a3.text(-0.9, 4.5, 'TP', va='center', ha='right', rotation='vertical')
a4.text(4.5, -1.5, 'T', ha='center', va='center') ; a4.text(-0.9, 4.5, 'TP', va='center', ha='right', rotation='vertical')
# a5.text(4.5, -1.5, 'T', ha='center', va='center') ; a5.text(-0.9, 4.5, 'FE', va='center', ha='right', rotation='vertical')
# a6.text(4.5, -1.5, 'T', ha='center', va='center') ; a6.text(-0.9, 4.5, 'FE', va='center', ha='right', rotation='vertical')
a7.text(4.5, -1.5, 'TP', ha='center', va='center') ; a7.text(-0.9, 4.5, 'DOC', va='center', ha='right', rotation='vertical')
a8.text(4.5, -1.5, 'TP', ha='center', va='center') ; a8.text(-0.9, 4.5, 'DOC', va='center', ha='right', rotation='vertical')
# a9.text(4.5, -1.5, 'TP', ha='center', va='center') ; a9.text(-0.9, 4.5, 'FE', va='center', ha='right', rotation='vertical')
# a10.text(4.5, -1.5, 'TP', ha='center', va='center') ; a10.text(-0.9, 4.5, 'FE', va='center', ha='right', rotation='vertical')
# a11.text(4.5, -1.5, 'FE', ha='center', va='center') ; a11.text(-0.9, 4.5, 'DOC', va='center', ha='right', rotation='vertical')
# a12.text(4.5, -1.5, 'FE', ha='center', va='center') ; a12.text(-0.9, 4.5, 'DOC', va='center', ha='right', rotation='vertical')


for ax in fig1.get_axes():
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_axis_bgcolor('black')

# add colorbars with own axes
cbar = fig1.add_axes([0.92, 0.55, 0.03, 0.3])
plt.colorbar(imgr, cax = cbar)
cbag = fig1.add_axes([0.92, 0.15, 0.03, 0.3])
plt.colorbar(imgg, cax = cbag)

fig1.text(0.07, 0.3, 'mean summer Chla concentration', rotation='vertical', weight='bold', va='center')
fig1.text(0.07, 0.7, 'number bottom anoxia days 2013', rotation='vertical', weight='bold', va='center')


fig1.savefig('../figures/combined_reordered_bottom.png')
fig1.savefig('../figures/combined_reordered_bottom.pdf')
