import sys 
from dolfin import *
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--mesh',default="DTI_16", type=str)      
parser.add_argument('--time_steps',default=90, type=int)      
parser.add_argument('--final_time', default=9, type=float) # default is 9 hours :w
parser.add_argument('--lumped',default="lumped", type=str)      
parser.add_argument('--annotation', default="std", type=str)
args = parser.parse_args()



# read mesh and subdomain data 
# We assume the following subdomains 1, 2, 17, 1035, 1028, 3028, 3035 
# marked as in all.sh 
mesh = Mesh()
hdf = HDF5File(mesh.mpi_comm(),args.mesh, "r")
hdf.read(mesh, "/mesh", False)  
subdomains = MeshFunction("size_t", mesh, mesh.topology().dim())
hdf.read(subdomains, "/subdomains")
boundaries  = MeshFunction("size_t", mesh, mesh.topology().dim() - 1)
hdf.read(boundaries, "/boundaries")
dx = Measure("dx", domain=mesh, subdomain_data=subdomains)
ds = Measure("ds", domain=mesh, subdomain_data=boundaries)

# print vertices, cells and volume 
print ("mesh num vertices ", mesh.num_vertices())
print ("mesh num cells", mesh.num_cells())
brain_volume = assemble(Constant(1)*dx)  
print( "Brain volume (mm)^3 ", brain_volume) 

# read the DTI 
T = TensorFunctionSpace(mesh, "DG", 0)
D = Function(T) 
hdf.read(D, "/DTI")

# determine scaling with the DTI data expressing the brain's diffusivity of water
MD_water    = 0.001049
MD_grey = Constant(MD_water)
MD_gadovist = 0.00013
MD_Amyloid  = 0.000062
MD_grey = Constant(0.001049)
scale_diffusion_amy = MD_Amyloid / MD_water 
scale_diffusion_gad = MD_gadovist/ MD_water 
D_scale = Constant(scale_diffusion_gad) 


# various parameters   
time_steps = args.time_steps 
time_final = args.final_time    
dt         = 3600*(time_final / time_steps) # units are mm and s
u_0 = Constant(0.0) 
f   = Constant(0.0)

# output file 
vtkfile = File('chp6-diffusion-mritracer-{}/solution.pvd'.format(args.annotation) )

# function space for solution 
V    = FunctionSpace(mesh, 'Lagrange', 1)

# bc
ud_str = '1.0'   
u_d    = Expression(ud_str,degree=1)
bc   = DirichletBC(V, u_d, 'on_boundary')

# previous time step 
u_n = interpolate(u_0, V)
bc.apply(u_n.vector())

# Rename u_n to Concentration and have unit M (Molar)
u_n.rename("Concentration","M")

# dump initial condition 
vtkfile << (u_n,0.00) 

# trial and test function 
u = TrialFunction(V)
v = TestFunction(V)


# in case of mass lumping a separate lumped mass matrix 
M = u_n*dx
mass_form = v*u*dx
mass_action_form = action(mass_form, Constant(1))
M_lumped = assemble(mass_form)
M_lumped.zero()
M_lumped.set_diagonal(assemble(mass_action_form))

# replace the lumped mass matrix with a standard Galerkin matrix 
if args.lumped == "not":     
    print ("not lumped ")
    M_lumped = assemble(mass_form)


# the variational forms (without the mass matrix) 
F = dt*D_scale*MD_grey*dot(grad(u),grad(v))*dx(1)+    dt*D_scale*dot(grad(u), dot(D,grad(v) ) )*dx(2)  + \
    dt*D_scale*dot(grad(u), dot(D,grad(v) ) )*dx(3028) + dt*D_scale*dot(grad(u), dot(D,grad(v) ) )*dx(3035) +\
    dt*D_scale*MD_grey*dot(grad(u),grad(v))*dx(17) +  dt*D_scale*MD_grey*dot(grad(u),grad(v))*dx(1035) +  dt*D_scale*MD_grey*dot(grad(u),grad(v))*dx(1028) - \
 (u_n + dt*f)*v*dx
a, L = lhs(F), rhs(F)

# (Re-)define u as the solution at the current time 
u = Function(V)    # AU

# Rename u_n to Concentration and have unit M (Molar)
u_n.rename("Concentration","M")

# Create system matrix 
A = assemble(a)
A = A+M_lumped 

# compute the volumes of the various subdomains 
vol17 = assemble(1.0*dx(17)) 
vol1035 = assemble(1.0*dx(1035))
vol1028 = assemble(1.0*dx(1028))
vol3028 = assemble(1.0*dx(3028))
vol3035 = assemble(1.0*dx(3035))
print( "Volume of domains 17, 1035, 1028, 3028, 3035: ", vol17 ,vol1035,vol1028, vol3028, vol3035) 

# initialize lists for the concentrations of the different subdomains 
unit17   = []
unit1028 = []
unit1035 = []
unit3028 = []
unit3035 = []



# time loop 
time_points = []
t = 0
for n in range(time_steps):
    # update time
    t += dt

    # solve the system 
    b = assemble(L)
    bc.apply(A,b)
    solve(A,u.vector(),b, "gmres", "amg")

    # store results every hour 
    if t/(60*60) - int(t/(60*60)) < dt/(60*60):  vtkfile << (u, t)

    # update previous solution 
    u_n.assign(u)

    # compute the amount in the various subdomains 
    unit17 += [assemble(u*dx(17))/vol17]
    unit1035 += [assemble(u*dx(1035))/vol1035]
    unit1028 += [assemble(u*dx(1028))/vol1028]
    unit3028 += [assemble(u*dx(3028))/vol3028]
    unit3035 += [assemble(u*dx(3035))/vol3035]
    time_points += [t] 
    
    # print to screen 
    print( "time [hours]", t/(60*60), " concentrations at  17 1035 1028 3028 3035 are: ",  unit17[-1], unit1028[-1], unit1035[-1], unit3028[-1], unit3035[-1])  


# write the various results to csv files 
import csv
with  open('time_{}.csv'.format(args.annotation), 'w') as outfile:
   writer = csv.writer(outfile)
   writer.writerows(map(lambda x: [x], time_points))

with  open('tracer17_{}.csv'.format(args.annotation), 'w') as outfile:
   writer = csv.writer(outfile)
   writer.writerows(map(lambda x: [x], unit17))

with  open('tracer1028_{}.csv'.format(args.annotation), 'w') as outfile:
   writer = csv.writer(outfile)
   writer.writerows(map(lambda x: [x], unit1028))

with  open('tracer1035_{}.csv'.format(args.annotation) , 'w') as outfile:
   writer = csv.writer(outfile)
   writer.writerows(map(lambda x: [x], unit1035))

with  open('tracer3028_{}.csv'.format(args.annotation), 'w') as outfile:
   writer = csv.writer(outfile)
   writer.writerows(map(lambda x: [x], unit3028))

with  open('tracer3035_{}.csv'.format(args.annotation) , 'w') as outfile:
   writer = csv.writer(outfile)
   writer.writerows(map(lambda x: [x], unit3035))

















