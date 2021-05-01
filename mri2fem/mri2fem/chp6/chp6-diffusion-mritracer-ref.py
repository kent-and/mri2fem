import sys 
from dolfin import *
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--mesh',default="DTI_16", type=str)      
parser.add_argument('--time_steps',default=90, type=int)      
parser.add_argument('--final_time', default=9, type=float) # default is 9 hours :w
parser.add_argument('--lumped',default="lumped", type=str)      
parser.add_argument('--label', default="std", type=str)
args = parser.parse_args()


mesh = Mesh()
hdf = HDF5File(mesh.mpi_comm(),args.mesh, "r")
hdf.read(mesh, "/mesh", False)  
print ("mesh num vertices ", mesh.num_vertices())
print ("mesh num cells", mesh.num_cells())
subdomains = MeshFunction("size_t", mesh, mesh.topology().dim())
hdf.read(subdomains, "/subdomains")
boundaries  = MeshFunction("size_t", mesh, mesh.topology().dim() - 1)
hdf.read(boundaries, "/boundaries")
dx = Measure("dx", domain=mesh, subdomain_data=subdomains)
ds = Measure("ds", domain=mesh, subdomain_data=boundaries)

#File('tst_sub_{}.pvd'.format(sys.argv[2])) << subdomains
T = TensorFunctionSpace(mesh, "DG",0)
Kt = Function(T) 
hdf.read(Kt, "/DTI")

W = VectorFunctionSpace(mesh, "DG",0)
DG0 = FunctionSpace(mesh, "DG",0) 
surface_area = assemble(Constant(1)*ds(5))  
print( "Surface area (mm)^2 ", surface_area) 
brain_volume = assemble(Constant(1)*dx)  
print( "Brain volume (mm)^3 ", brain_volume) 


MD_water    = 0.001049
MD_grey = Constant(MD_water)
MD_gadovist = 0.00013
MD_Amyloid  = 0.000062
MD_grey = Constant(0.001049)
scale_diffusion_amy = MD_Amyloid / MD_water 
scale_diffusion_gad = MD_gadovist/ MD_water 
D_scale = Constant(scale_diffusion_gad) 


time_final = args.final_time     
time_steps = args.time_steps 
dt         = 3600*(time_final / time_steps) # units are mm and s
u_0 = Constant(0.0) 
f   = Constant(0.0)



ud_str = '1.0'   
u_d    = Expression(ud_str,degree=1)

vtkfile = File('chp6-diffusion-mritracer-{}/solution.pvd'.format(args.label) )

V    = FunctionSpace(mesh, 'Lagrange', 1)

bc   = DirichletBC(V, u_d, 'on_boundary')

u_n = interpolate(u_0, V)
bc.apply(u_n.vector())

# Rename u_n to Concentration and have unit M (Molar)
u_n.rename("Concentration","M")

vtkfile << u_n # selecitve sync error 

u = TrialFunction(V)
v = TestFunction(V)


mass_form = v*u*dx
mass_action_form = action(mass_form, Constant(1))
M_lumped = assemble(mass_form)
M_lumped.zero()
M_lumped.set_diagonal(assemble(mass_action_form))
if args.lumped == "not": # replace the lumped mass matrix with a standard Galerkin matrix 
    print ("not lumped ")
    M_lumped = assemble(mass_form)
# 1 -> coritcal grey matter, 2-> white and subcoritcal grey matter   17 left hippocampus 35 lrft insula


# 1 -> coritcal grey matter, 2-> white and subcoritcal grey matter   17 left hippocampus 35 lrft insula


# TODO : dx and tensor on all domains
F = dt*D_scale*MD_grey*dot(grad(u),grad(v))*dx(1)+    dt*D_scale*dot(grad(u), dot(Kt,grad(v) ) )*dx(2)  + \
    dt*D_scale*MD_grey*dot(grad(u),grad(v))*dx(17) - (u_n + dt*f)*v*dx
a, L = lhs(F), rhs(F)

t = 0

u = Function(V)

# Rename u to Concentration and have unit M (Molar)
u.rename("Concentration","M")

A = assemble(a)
A = A+M_lumped 
vol17 = assemble(1.0*dx(17)) 

print( "size of domain 17: ", vol17) 

unit17   = []
time_points = []
for n in range(time_steps):
    t += dt
    b = assemble(L)
    bc.apply(A,b)

    solve(A,u.vector(),b, "gmres", "amg")

    # only store every hour 
    if t/(60*60) - int(t/(60*60)) < dt/(60*60):  vtkfile << (u, t)

    u_n.assign(u)

    unit17 += [assemble(u*dx(17))/vol17]
    time_points += [t] 
    
    print( "time  u17  ", t/(60*60),  unit17[-1])  


import csv

with  open('time_{}.csv'.format(args.label), 'w') as outfile:
   writer = csv.writer(outfile)
   writer.writerows(map(lambda x: [x], time_points))

with  open('tracer17_{}.csv'.format(args.label), 'w') as outfile:
   writer = csv.writer(outfile)
   writer.writerows(map(lambda x: [x], unit17))

















