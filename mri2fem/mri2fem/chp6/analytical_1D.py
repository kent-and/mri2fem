
import scipy
from scipy import sqrt

from scipy.special import erfc 
import matplotlib.pyplot as plt 

plt.gcf().subplots_adjust(bottom=0.15)
plt.ylim(0,1)
plt.rc('xtick', labelsize=24) 
plt.rc('ytick', labelsize=24) 
plt.xlabel("distance [mm]", size=24)
plt.ylabel("concentration", size=24)

Lmax = 2  # 2 mm 
xx = scipy.arange(0, Lmax, 0.001)

MD_Water    = 0.001049
MD_Gadovist = 0.00013
MD_Amyloid  = 0.000062
D = MD_Amyloid 

analytical_solution_15min = erfc(xx / (2*sqrt( D * 15*60))) 
analytical_solution_1hour = erfc(xx / (2*sqrt( D * 60*60))) 
analytical_solution_9hour = erfc(xx / (2*sqrt( D * 9*60*60))) 
analytical_solution_24hour = erfc(xx / (2*sqrt( D * 24*60*60))) 
analytical_solution_49hour = erfc(xx / (2*sqrt( D * 48*60*60))) 
analytical_solution_1week = erfc(xx / (2*sqrt( D * 7*24*60*60))) 

plt.gcf().subplots_adjust(bottom=0.25, left=0.25)
plt.ylim(0,1)
plt.rc('xtick', labelsize=24) 
plt.rc('ytick', labelsize=24) 
plt.xlabel("distance [mm]", size=24)
plt.ylabel("concentration", size=24)
plt.plot(xx, analytical_solution_15min, "r", linewidth=7)
plt.plot(xx, analytical_solution_1hour, "b", linewidth=7)
plt.plot(xx, analytical_solution_9hour, "g", linewidth=7)
plt.plot(xx, analytical_solution_24hour, "c", linewidth=7)
plt.plot(xx, analytical_solution_1week, "c", linewidth=7)
plt.legend(["15 min", "1 hour", "9 hours", "24 hours", "48 hours", "1 week"], prop={"size" : 24}, loc=1)
plt.savefig("Amyloid_1D_2mm.png")
plt.show()

Lmax = 10  # 1 cm in mm 
xx = scipy.arange(0, Lmax, 0.001)

analytical_solution_15min  = erfc(xx / (2*sqrt( D * 15*60))) 
analytical_solution_1hour  = erfc(xx / (2*sqrt( D * 60*60))) 
analytical_solution_9hour  = erfc(xx / (2*sqrt( D * 9*60*60))) 
analytical_solution_24hour = erfc(xx / (2*sqrt( D * 24*60*60))) 
analytical_solution_49hour = erfc(xx / (2*sqrt( D * 48*60*60))) 
analytical_solution_1week  = erfc(xx / (2*sqrt( D * 7*24*60*60))) 

plt.gcf().subplots_adjust(bottom=0.25, left=0.25)
plt.ylim(0,1)
plt.rc('xtick', labelsize=24) 
plt.rc('ytick', labelsize=24) 
plt.xlabel("distance [mm]", size=24)
plt.ylabel("concentration", size=24)
plt.plot(xx, analytical_solution_15min, "r", linewidth=7)
plt.plot(xx, analytical_solution_1hour, "b", linewidth=7)
plt.plot(xx, analytical_solution_9hour, "g", linewidth=7)
plt.plot(xx, analytical_solution_24hour, "c", linewidth=7)
plt.plot(xx, analytical_solution_1week, "c", linewidth=7)
plt.legend(["15 min", "1 hour", "9 hours", "24 hours", "48 hours", "1 week"], prop={"size" : 24}, loc=1)
plt.savefig("Amyloid_1D_1cm.png")
plt.show()

Lmax = 2  # 1 cm in mm 
xx = scipy.arange(0, Lmax, 0.001)
analytical_solution_9hour_Water    = erfc(xx / (2*sqrt( MD_Water   * 9*60*60))) 
analytical_solution_9hour_Amyloid  = erfc(xx / (2*sqrt( MD_Amyloid * 9*60*60))) 
analytical_solution_9hour_Gadovist = erfc(xx / (2*sqrt( MD_Gadovist* 9*60*60))) 

plt.gcf().subplots_adjust(bottom=0.25, left=0.25)
plt.ylim(0,1)
plt.rc('xtick', labelsize=24) 
plt.rc('ytick', labelsize=24) 
plt.xlabel("distance [mm]", size=24)
plt.ylabel("concentration", size=24)
plt.plot(xx, analytical_solution_9hour_Water, "r", linewidth=7)
plt.plot(xx, analytical_solution_9hour_Amyloid, "b", linewidth=7)
plt.plot(xx, analytical_solution_9hour_Gadovist, "g", linewidth=7)
plt.legend(["Water", "Amyloid", "Gadovist"], prop={"size" : 24}, loc=1)
plt.savefig("9hours_2mm_WAG.png")
plt.show()

Lmax = 2  # 1 cm in mm 
xx = scipy.arange(0, Lmax, 0.001)
analytical_solution_24hour_Water    = erfc(xx / (2*sqrt( MD_Water   * 24*60*60))) 
analytical_solution_24hour_Amyloid  = erfc(xx / (2*sqrt( MD_Amyloid * 24*60*60))) 
analytical_solution_24hour_Gadovist = erfc(xx / (2*sqrt( MD_Gadovist* 24*60*60))) 

plt.gcf().subplots_adjust(bottom=0.25, left=0.25)
plt.ylim(0,1)
plt.rc('xtick', labelsize=24) 
plt.rc('ytick', labelsize=24) 
plt.xlabel("distance [mm]", size=24)
plt.ylabel("concentration", size=24)
plt.plot(xx, analytical_solution_24hour_Water, "r", linewidth=7)
plt.plot(xx, analytical_solution_24hour_Amyloid, "b", linewidth=7)
plt.plot(xx, analytical_solution_24hour_Gadovist, "g", linewidth=7)
plt.legend(["Water", "Amyloid", "Gadovist"], prop={"size" : 24}, loc=1)
plt.savefig("24hours_2mm_WAG.png")
plt.show()

Lmax = 10  # 1 cm in mm 
xx = scipy.arange(0, Lmax, 0.001)
analytical_solution_9hour_Water    = erfc(xx / (2*sqrt( MD_Water   * 9*60*60))) 
analytical_solution_9hour_Amyloid  = erfc(xx / (2*sqrt( MD_Amyloid * 9*60*60))) 
analytical_solution_9hour_Gadovist = erfc(xx / (2*sqrt( MD_Gadovist* 9*60*60))) 

plt.gcf().subplots_adjust(bottom=0.25, left=0.25)
plt.ylim(0,1)
plt.rc('xtick', labelsize=24) 
plt.rc('ytick', labelsize=24) 
plt.xlabel("distance [mm]", size=24)
plt.ylabel("concentration", size=24)
plt.plot(xx, analytical_solution_9hour_Water, "r", linewidth=7)
plt.plot(xx, analytical_solution_9hour_Amyloid, "b", linewidth=7)
plt.plot(xx, analytical_solution_9hour_Gadovist, "g", linewidth=7)
plt.legend(["Water", "Amyloid", "Gadovist"], prop={"size" : 24}, loc=1)
plt.savefig("9hours_1cm_WAG.png")
plt.show()

Lmax = 10  # 1 cm in mm 
xx = scipy.arange(0, Lmax, 0.001)
analytical_solution_24hour_Water    = erfc(xx / (2*sqrt( MD_Water    * 24*60*60))) 
analytical_solution_24hour_Amyloid  = erfc(xx / (2*sqrt( MD_Amyloid  * 24*60*60))) 
analytical_solution_24hour_Gadovist = erfc(xx / (2*sqrt( MD_Gadovist* 24*60*60))) 

plt.gcf().subplots_adjust(bottom=0.25, left=0.25)
plt.ylim(0,1)
plt.rc('xtick', labelsize=24) 
plt.rc('ytick', labelsize=24) 
plt.xlabel("distance [mm]", size=24)
plt.ylabel("concentration", size=24)
plt.plot(xx, analytical_solution_24hour_Water, "r", linewidth=7)
plt.plot(xx, analytical_solution_24hour_Amyloid, "b", linewidth=7)
plt.plot(xx, analytical_solution_24hour_Gadovist, "g", linewidth=7)
plt.legend(["Water", "Amyloid", "Gadovist"], prop={"size" : 24}, loc=1)
plt.savefig("24hours_1cm_WAG.png")
plt.show()

Lmax = 1  # 1mm 
xx = scipy.arange(0, Lmax, 0.001)
analytical_solution_15min_Water    = erfc(xx / (2*sqrt( MD_Water   * 15*60))) 
analytical_solution_15min_Amyloid  = erfc(xx / (2*sqrt( MD_Amyloid * 15*60))) 
analytical_solution_15min_Gadovist = erfc(xx / (2*sqrt( MD_Gadovist* 15*60))) 

plt.gcf().subplots_adjust(bottom=0.25, left=0.25)
plt.ylim(0,1)
plt.rc('xtick', labelsize=24) 
plt.rc('ytick', labelsize=24) 
plt.xlabel("distance [mm]", size=24)
plt.ylabel("concentration", size=24)
plt.plot(xx, analytical_solution_15min_Water, "r", linewidth=7)
plt.plot(xx, analytical_solution_15min_Amyloid, "b", linewidth=7)
plt.plot(xx, analytical_solution_15min_Gadovist, "g", linewidth=7)
plt.legend(["Water", "Amyloid", "Gadovist"], prop={"size" : 24}, loc=1)
plt.savefig("15min_1mm_WAG.png")
plt.show()



