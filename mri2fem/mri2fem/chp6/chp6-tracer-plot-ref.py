
# script for Fig 6.6 

from numpy import *
import matplotlib.pyplot as plt

time_16 = loadtxt("time_DTI16lumped_ref1.csv")
time_16 = time_16 / 3600 
#t17_16 = loadtxt("tracer17_16.csv")
t17_16_ref1 = loadtxt("tracer17_DTI16lumped_ref1.csv")
t17_16_ref2 = loadtxt("tracer17_DTI16lumped_ref2.csv")
t17_16_ref3 = loadtxt("tracer17_DTI16lumped_ref3.csv")
t17_16_ref4 = loadtxt("tracer17_DTI16lumped_ref4.csv")

t17_16_ref1n = loadtxt("tracer17_DTI16notlumped_ref1.csv")
t17_16_ref2n = loadtxt("tracer17_DTI16notlumped_ref2.csv")
t17_16_ref3n = loadtxt("tracer17_DTI16notlumped_ref3.csv")
t17_16_ref4n = loadtxt("tracer17_DTI16notlumped_ref4.csv")


plt.gcf().subplots_adjust(bottom=0.25, left=0.25)
plt.rc('xtick', labelsize=16) 
plt.rc('ytick', labelsize=16) 
plt.ylim(0,1)
plt.xlabel("time [h]", size=16)
plt.ylabel("concentration", size=16)
plt.plot(time_16, t17_16_ref1, linewidth=7)
plt.plot(time_16, t17_16_ref2, linewidth=7)
plt.plot(time_16, t17_16_ref3, linewidth=7)
plt.plot(time_16, t17_16_ref4, linewidth=7)
plt.legend(["refinement 1", "refinement 2", "refinement 3", "refinement 4"], prop={"size" : 16})
plt.savefig("tracer_hippocampus_lumped_addaptive")
plt.show()



plt.gcf().subplots_adjust(bottom=0.25, left=0.25)
plt.rc('xtick', labelsize=16) 
plt.rc('ytick', labelsize=16) 
plt.ylim(0,1)
plt.xlabel("time [h]", size=16)
plt.ylabel("concentration", size=16)
plt.plot(time_16, t17_16_ref1n, linewidth=7)
plt.plot(time_16, t17_16_ref2n, linewidth=7)
plt.plot(time_16, t17_16_ref3n, linewidth=7)
plt.plot(time_16, t17_16_ref4n, linewidth=7)
plt.legend(["refinement 1", "refinement 2", "refinement 3", "refinement 4"], prop={"size" : 16})
plt.savefig("tracer_hippocampus_notlumped_addaptive")
plt.show()



