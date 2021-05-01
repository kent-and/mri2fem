
# script for Fig 6.5 

from numpy import *
import matplotlib.pyplot as plt

time_16 = loadtxt("time_uniform16notlumped.csv")
time_16 = time_16 / 3600 
t17_16 = loadtxt("tracer17_uniform16notlumped.csv")
t1035_16 = loadtxt("tracer1035_uniform16notlumped.csv")
t1028_16 = loadtxt("tracer1028_uniform16notlumped.csv")

time_32 = loadtxt("time_uniform32notlumped.csv")
time_32 = time_32 / 3600 
t17_32 = loadtxt("tracer17_uniform32notlumped.csv")
t1035_32 = loadtxt("tracer1035_uniform32notlumped.csv")
t1028_32 = loadtxt("tracer1028_uniform32notlumped.csv")

time_64 = loadtxt("time_uniform64notlumped.csv")
time_64 = time_64 / 3600 
t17_64 = loadtxt("tracer17_uniform64notlumped.csv")
t1035_64 = loadtxt("tracer1035_uniform64notlumped.csv")
t1028_64 = loadtxt("tracer1028_uniform64notlumped.csv")

time_128 = loadtxt("time_uniform128notlumped.csv")
time_128 = time_128 / 3600 
t17_128 = loadtxt("tracer17_uniform128notlumped.csv")
t1035_128 = loadtxt("tracer1035_uniform128notlumped.csv")
t1028_128 = loadtxt("tracer1028_uniform128notlumped.csv")

plt.rc('xtick', labelsize=16) 
plt.rc('ytick', labelsize=16) 
plt.ylim(0,1)
plt.plot(time_16, t17_16,  linewidth=7)
plt.plot(time_16, t17_32,  linewidth=7)
plt.plot(time_16, t17_64,  linewidth=7)
plt.plot(time_16, t17_128,  linewidth=7)
plt.legend([ "16", "32", "64", "128"], prop={"size" : 16})
plt.savefig("tracer_hippocampus_uniform_notlump")
plt.show()



time_16l = loadtxt("time_uniform16lumped.csv")
time_16l = time_16 / 3600 
t17_16l = loadtxt("tracer17_uniform16lumped.csv")
t1035_16l = loadtxt("tracer1035_uniform16lumped.csv")
t1028_16l = loadtxt("tracer1028_uniform16lumped.csv")

time_32l = loadtxt("time_uniform32lumped.csv")
time_32l = time_32 / 3600 
t17_32l = loadtxt("tracer17_uniform32lumped.csv")
t1035_32l = loadtxt("tracer1035_uniform32lumped.csv")
t1028_32l = loadtxt("tracer1028_uniform32lumped.csv")

time_64l = loadtxt("time_uniform64lumped.csv")
time_64l = time_64 / 3600 
t17_64l = loadtxt("tracer17_uniform64lumped.csv")
t1035_64l = loadtxt("tracer1035_uniform64lumped.csv")
t1028_64l = loadtxt("tracer1028_uniform64lumped.csv")

time_128l = loadtxt("time_uniform128lumped.csv")
time_128l = time_128 / 3600 
t17_128l = loadtxt("tracer17_uniform128lumped.csv")
t1035_128l = loadtxt("tracer1035_uniform128lumped.csv")
t1028_128l = loadtxt("tracer1028_uniform128lumped.csv")


plt.rc('xtick', labelsize=16) 
plt.rc('ytick', labelsize=16) 
plt.ylim(0,1)
plt.plot(time_16, t17_16l,  linewidth=7)
plt.plot(time_16, t17_32l,  linewidth=7)
plt.plot(time_16, t17_64l,  linewidth=7)
plt.plot(time_16, t17_128l,  linewidth=7)
plt.legend([ "16", "32", "64", "128"], prop={"size" : 16})
plt.savefig("tracer_hippocampus_uniform_lump")
plt.show()







