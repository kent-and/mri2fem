
# Fig 6.4 

from numpy import *
import matplotlib.pyplot as plt

time_64 = loadtxt("time_uniform64notlumped.csv")
time_64 = time_64 / 3600 
t17_64 = loadtxt("tracer17_uniform64notlumped.csv")
t1035_64 = loadtxt("tracer1035_uniform64notlumped.csv")
t1028_64 = loadtxt("tracer1028_uniform64notlumped.csv")
t3035_64 = loadtxt("tracer3035_uniform64notlumped.csv")
t3028_64 = loadtxt("tracer3028_uniform64notlumped.csv")


plt.gcf().subplots_adjust(bottom=0.25, left=0.25)
plt.rc('xtick', labelsize=16) 
plt.rc('ytick', labelsize=16) 
plt.ylim(0,1)
plt.xlabel("time [h]", size=16)
plt.ylabel("concentration", size=16)
plt.plot(time_64, t17_64,  linewidth=7)
plt.plot(time_64, t1035_64,  linewidth=7)
plt.plot(time_64, t1028_64,  linewidth=7)
plt.plot(time_64, t3035_64,  linewidth=7)
plt.plot(time_64, t3028_64,  linewidth=7)
plt.legend([ "17", "1035", "1028", "3035", "3028"], prop={"size" : 16})
plt.savefig("tracer_uniform_notlump_regions_64")
plt.show()



time_128 = loadtxt("time_uniform128notlumped.csv")
time_128 = time_128 / 3600 
t17_128 = loadtxt("tracer17_uniform128notlumped.csv")
t1035_128 = loadtxt("tracer1035_uniform128notlumped.csv")
t1028_128 = loadtxt("tracer1028_uniform128notlumped.csv")
t3035_128 = loadtxt("tracer3035_uniform128notlumped.csv")
t3028_128 = loadtxt("tracer3028_uniform128notlumped.csv")



plt.gcf().subplots_adjust(bottom=0.25, left=0.25)
plt.rc('xtick', labelsize=16) 
plt.rc('ytick', labelsize=16) 
plt.ylim(0,1)
plt.xlabel("time [h]", size=16)
plt.ylabel("concentration", size=16)
plt.plot(time_128, t17_128,  linewidth=7)
plt.plot(time_128, t1035_128,  linewidth=7)
plt.plot(time_128, t1028_128,  linewidth=7)
plt.plot(time_128, t3035_128,  linewidth=7)
plt.plot(time_128, t3028_128,  linewidth=7)
plt.legend([ "17", "1035", "1028", "3035", "3028"], prop={"size" : 16})
plt.savefig("tracer_uniform_notlump_regions_128")
plt.show()






