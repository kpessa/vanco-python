import math
import numpy as np
import matplotlib.pyplot as plt


Dose = 1000 # mgs
t_inf = 1 # hrs
# Ke of 0.100 ~ 105 mL/min CrCl using 1985 Matze eqn
K_e = 0.100 # -> t1_2 = 6.9 hrs 
V_d = 45.5 # L <- 70 * 0.65
tau = 12


def c_inf(t):
    return R_0 / CL_vanco * (1 - math.exp(-K_e * t))


R_0 = Dose / t_inf
CL_vanco = K_e * V_d


X = np.linspace(0,tau,100) 
Y = [c_inf(t) for t in X]
plt.figure(figsize = (10,6))
plt.plot(X,Y,'--k')

plt.title("Continuous infusion over 12 hrs")
plt.style.use(plt.style.available[8])
plt.xlabel("Hours")
plt.ylabel("Concentration")
plt.ylim(0,200)
plt.tight_layout()
plt.savefig("Images/cont_infusion.png")


cmax = R_0 / CL_vanco * (1 - math.exp(-K_e * t_inf))


def  c_elim(t):
    return cmax * math.exp(-K_e * (t - t_inf))


X = np.linspace(t_inf,tau,100) 
Y = [ c_elim(t) for t in X]
plt.figure(figsize = (10,6))
plt.plot(X,Y,'--k')

plt.title(f"First-order elimination starting at Cmax={cmax:.1f}, {t_inf} hr post-infusion")
plt.style.use(plt.style.available[8])
plt.xlabel("Hours")
plt.ylabel("Concentration")
plt.ylim(0,25)
plt.tight_layout()
plt.savefig("Images/elmination.png")


def concentration(t):
    if t <= t_inf:
        return c_inf(t)
    else:
        return  c_elim(t)


def labelPlot():
    plt.xlabel('hrs')
    plt.ylabel('concentration')
    plt.ylim(0,25)
    plt.xlim(0-0.5,tau+0.5)
    plt.title('First-order Concentration Plot')
    
def annotateInterestingPoints():
    plt.annotate(f"Cmax: {cmax:.1f}",xy = (1,cmax),xytext = (-20,20),textcoords ='offset points')
    plt.annotate(f"Cpeak: {cpeak:.1f}",(1+1,cpeak),xytext = (10,25),textcoords ='offset points')
    plt.annotate(f"Ctrough: {ctrough:.1f}",(tau-0.5,ctrough),xytext = (-70,-23),textcoords ='offset points')
    plt.annotate(f"Cmin: {cmin:.1f}",(tau,cmin),xytext = (-65,-40),textcoords ='offset points')


X = np.linspace(0,12,100) 
Y = [concentration(t) for t in X]
plt.figure(figsize = (10,6))

plt.plot(X,Y,'--k')

#interesting points
cmax = concentration(1)
cpeak = concentration(1+1) # <~ wait 1? hr after infusion
ctrough = concentration(tau-0.5) # <~ 30 min before next dose
cmin = concentration(tau)
plt.scatter(x=[1,1+1,tau-0.5,tau],y=[cmax,cpeak,ctrough,cmin],linewidths=8,c='k')

#annotate points
plt.annotate(f"Cmax: {cmax:.1f}",xy = (1,cmax),xytext = (-30,20),textcoords ='offset points')
plt.annotate(f"Cpeak: {cpeak:.1f}",(1+1,cpeak),xytext = (10,25),textcoords ='offset points')
plt.annotate(f"Ctrough: {ctrough:.1f}",(tau-0.5,ctrough),xytext = (-70,-23),textcoords ='offset points')
plt.annotate(f"Cmin: {cmin:.1f}",(tau,cmin),xytext = (-65,-40),textcoords ='offset points')

#stylize plot
plt.style.use(plt.style.available[8])
plt.title("First-order elimination concentration plot")
plt.xlabel("Hours")
plt.ylabel("Concentration")
plt.ylim(0,30)
plt.tight_layout()
plt.savefig("Images/onedose.png")



