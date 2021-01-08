
from dolfin import *
import string
import scipy
from scipy.special import erfc 
from numpy import sqrt 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--L_max',default=10, type=int)      
parser.add_argument('--Ns',default=100, type=int, nargs='+')      
parser.add_argument('--dt',default=100, type=int)      
parser.add_argument('--final_time', default=9*60*60, type=float)
parser.add_argument('--lumped',default="lumped", type=str)      
parser.add_argument('--check_point',default=0.1, type=float)      
args = parser.parse_args()

print ("args ", args)

numerical_solutions = []
for N in args.Ns: 
    print ("solving for ", N)

    mesh = UnitIntervalMesh(N)
    mesh.coordinates()[:] *= args.L_max  
    V = FunctionSpace(mesh, "Lagrange", 1)
    u = TrialFunction(V)
    v = TestFunction(V) 


    # units are mm and seconds
    MD_water    = 0.001049
    MD_gadovist = 0.00013
    MD_Amyloid  = 0.000062
    D = Constant(MD_Amyloid )

    dt = Constant(args.dt)

    def left_boundary(x): 
      return x[0] < DOLFIN_EPS

    # assume these are set to zero
    U = Function(V)
    U_prev = Function(V)

    a =  u*v*dx + dt*D*inner(grad(u), grad(v))*dx 
    L = dt*Constant(0)*v*dx + U_prev*v*dx  

    t = 0.0
    bc_func = Constant(1)  
    bc = DirichletBC(V, bc_func, left_boundary)

    # make lumped mass matrix and add to the stiffness matrix
    M = assemble(u*v*dx)
    unity = U.vector().copy()
    unity[:] = 1 
    lm = M*unity 
    MM = M.copy()
    MM.zero()
    MM.set_diagonal(lm)
    A = assemble(dt*D*inner(grad(u), grad(v))*dx) 
    MA = MM + A 

    # if not lumped simply make new matrix 
    if not args.lumped=="lumped": 
        MA = assemble(u*v*dx + dt*D*inner(grad(u), grad(v))*dx) 

    bc.apply(MA)

    ts = []
    u0s = []
    uls = []
    urs = []
    done = False
    check_point = 0.001
    while t < args.final_time: 
        bc_func.t = t 
        t += args.dt  
        ts.append(t)
        b = assemble(L) 
        bc.apply(b) 
        solve(MA,U.vector(), b, "gmres", "ilu")
        U_prev.assign(U)
        v = U(check_point) 
        print ("tracer at check_point ", check_point, v)
    numerical_solutions.append((V.tabulate_dof_coordinates(), U.vector()))



x = V.tabulate_dof_coordinates()
xx = scipy.arange(0, args.L_max, 0.001)
analytical_solution = erfc(xx / (2*sqrt( D.values()[0] * t))) 

import matplotlib.pyplot as plt 
plt.rc('xtick', labelsize=16) 
plt.rc('ytick', labelsize=16) 

for x, vec in numerical_solutions: 
    plt.plot(x, vec, linewidth=7)
plt.plot(xx, analytical_solution, linewidth=7)
legend = ["N=%d"%N for N in args.Ns]
legend.append("analytical sol")
plt.legend(legend,  prop={"size" : 16}, loc=1)
file_str = "Amyloid_numerical_1D_L_max%d_dt%d_final%d_lumped%s"% (args.L_max,args.dt, args.final_time,args.lumped)
plt.savefig(file_str)
plt.show()





