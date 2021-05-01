from fenics import *
import numpy

# Read the mesh
mesh = Mesh()
file = XDMFFile(MPI.comm_world, "ernie.xdmf") # mm 
file.read(mesh)
file.close()
# Compute and print basic info about the mesh
print("#vertices =", mesh.num_vertices())
print("#cells =", mesh.num_cells())
print("max cell size (mm) =", mesh.hmax())
print("Volume (mm^3) = ", assemble(1*dx(mesh)))

# Define time discretization parameters
T = 72*60             # 72 hours in min
tau = Constant(3.0)   # Time step (min)
time = Constant(0.0)

# Define the diffusion parameter
D = Constant(7.2e-3)  # mm^2/min

# Define the source function and initial condition
f = Constant(0.0)
u0 = Constant(0.0)    

# Define the finite element spaces and functions
V = FunctionSpace(mesh, "Lagrange", 1)
u = TrialFunction(V)
v = TestFunction(V)

# Define function to hold solution at previous time and
# assign initial condition to it
u_ = Function(V)   # AU (Arbitrary Unit)
u_.assign(u0)

# Define the variational system to be solved at each time
a = (u*v + tau*D*dot(grad(u), grad(v)))*dx
L = (u_*v + tau*f*v)*dx

# (Re-)define u as the solution at the current time 
u = Function(V)    # AU

# Rename u to Concentration and have unit M (Molar)
u.rename("Concentration","M")

# Define the boundary condition: grow linearly up
# to the value c in the first 6 hours:
u_d = Expression("t < 6*60 ? t/(6*60)*c : c",  
                 t=time, c=2.813e-3, degree=1)  # AU
bc = DirichletBC(V, u_d, 'on_boundary')

# Assemble the left hand side matrix outside time loop
# for efficiency
A = assemble(a)

# Define file to store solutions and store initial solution
vtkfile = File("results/u.pvd")
u.assign(u_)
vtkfile << (u, float(time))

# Compute number of time steps and create arrays for
# computational quantities of interest
N = int(T/float(tau))
times = numpy.zeros(N+1)
amounts = numpy.zeros(N+1)
p = (-22.66, -48.23, 12.50) 
concs = numpy.zeros(N+1)

# Iterate over the time steps
for n in range(1, N+1):
    
    # Update time
    time.assign(time + tau)
    times[n] = float(time)

    # Assemble right-hand side 
    b = assemble(L)

    # Apply boundary condition to linear system and solve it
    bc.apply(A, b)
    solve(A, u.vector(), b, "gmres", "amg")

    # Set previous solution to the current before moving on
    u_.assign(u)

    # Compute the total amount of solute and concentration
    # at given point:
    amounts[n] = assemble(u*dx) # AU mm^3
    concs[n] = u(p)             # AU 

    # Output progress and store solution every 10th time step:
    if n%10==0:
        print("Storing at n = %d (of %d), t = %g (min)"
              % (n, N, time))
        vtkfile << (u, float(time))

# Store amounts, times and concs to file 
numpy.savetxt("results/times.csv", times, delimiter=",")
numpy.savetxt("results/amounts.csv", amounts, delimiter=",")
numpy.savetxt("results/concs.csv", concs, delimiter=",")

import matplotlib.pyplot as plt 
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
plt.rc('xtick', labelsize=16) 
plt.rc('ytick', labelsize=16) 
plt.rc('axes', labelsize=16) 
plt.rc('lines', linewidth=7) 

# Read amounts, time and concs from file and plot
times = numpy.genfromtxt("results/times.csv", delimiter=",")
concs = numpy.genfromtxt("results/concs.csv", delimiter=",")
amounts = numpy.genfromtxt("results/amounts.csv", delimiter=",")

plt.plot(times, amounts, 'b-')
plt.xlabel("t (min)")
plt.ylabel("Q (AU)")
plt.yticks([500, 1000, 1500])
plt.grid(True)
plt.savefig("results/amounts.png")

plt.figure()
plt.plot(times, concs, 'r--')
plt.xlabel("t (min)")
plt.ylabel("u(p) (AU/mm$^3$)")
plt.yticks([-0.0002, 0.0, 0.0002, 0.0004, 0.0006])
plt.grid(True)
plt.savefig("results/concentrations.png")


