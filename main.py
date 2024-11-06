import csv

with open('./hcl.csv', 'r') as f:
    data = csv.reader(f)

    start = True
    body = []
    for row in data:
        if start:
            start = False
            head = row
            continue
        body.append(row)

#print(head.index('20C'))
#print(list(map(lambda x: x[head.index('20C')], body)))


# ------------------------
# POLYNOMIAL INTERPOLATION
# ------------------------

# f(t, d) = c
# f(1) = 2
# f(2) = 3
# f(x) = 2*(x-2)/(1-2) + 3*(x-1)/(2-1) = -2x+4+3x-3 = x + 1
# ---------------------------------------------------------
# f(1, 0) = 2
# f(2, 0) = 3
# f(1, 1) = 3
# f(2, 1) = 4
# f(x, y) = (x+1)*(y-1)/(0-1) + (x+2)*(y-0)/(1-0) = (x+1)(1-y) + (x+2)y = x+1 - xy - y + xy + 2y = x+1+y
# ------------------------------------------------------------------------------------------------------

def prod_fn(xs):
    def r(x):
        prod = 1
        for x_i in xs:
            prod *= (x - x_i)
        return prod

    return r

def rm_nth(xs, index):
    return xs[:index] + xs[index+1 :]

temps = list(map(lambda t: float(t.replace('C','')), head[1:]))
concs = list(map(lambda x: float(x[0]), body))

fx = []
for t_i,t in enumerate(head):
    if t_i == 0:
        continue

    temp = float(t.replace('C',''))
    ds_str = map(lambda x: x[t_i], body)
    ds = list(map(lambda x: float(x), filter(lambda x: len(x)>0, ds_str)))
    conc_denss = list(zip(concs, list(ds)))

    def r_(conc_denss):
        def r(d): 
            sum = 0
            for cd_i, conc_dens in enumerate(conc_denss):
                conc, density = conc_dens
                ds_no_ith = list(map(lambda x: x[1], rm_nth(conc_denss, cd_i)))
                sum += conc * prod_fn(ds_no_ith)(d) / prod_fn(ds_no_ith)(density) 
            return sum
        return r

    fx.append((temp, r_(conc_denss)))

def pred(d, t):
    sum = 0
    for tf_i, tf in enumerate(fx):
        temp, f = tf
        sum += f(d) * prod_fn(rm_nth(temps, tf_i))(t) / prod_fn(rm_nth(temps, tf_i))(temp)
    return sum

while True:
    print('ENTER Temperature °C > ', end='')
    t = float(input())
    print('ENTER Density g/mL > ', end='')
    d = float(input())
    print(pred(d, t))
    print('_'*50)

