import os
import math

ncore = 24
n = 625

with open('run_eight_years_template.m', 'rU') as f:
    template = f.read()

each1 = math.floor(n / float(ncore))
each2 = math.ceil(n / float(ncore))

n1 = each2 * ncore - n
n2 = ncore - n1

start = 1
end = each1

for i in range(ncore):
    if i == 0:
        pass
    elif i < n1:
        start += each1
        end += each1
    else:
        start += each2
        end += each2
    print(start, end)
    
    out = template.replace('template', '{:d}:{:d}'.format(start, end))
    fname = 'NIVAserver_{:03d}.m'.format(i+1)
    with open(fname, 'w') as g:
        g.write(out)











