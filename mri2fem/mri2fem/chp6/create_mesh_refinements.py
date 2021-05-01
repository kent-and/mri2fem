import SVMTK as svmtk
import time

# Import surfaces, and merge lh/rh white surfaces
ventricles  = svmtk.Surface("surfaces/lh.ventricles.stl") 
lhpial = svmtk.Surface("surfaces/lh.pial.stl") 
rhpial = svmtk.Surface("surfaces/rh.pial.stl")
white = svmtk.Surface("surfaces/lh.white.stl") 
rhwhite = svmtk.Surface("surfaces/rh.white.stl") 
white.union(rhwhite)

surfaces = [lhpial, rhpial, white, ventricles] 

# Create subdomain map
smap = svmtk.SubdomainMap() 
smap.add("1000", 1)
smap.add("0100", 1) 
smap.add("0110", 2)
smap.add("0010", 2)
smap.add("1010", 2)
smap.add("0111", 3)
smap.add("1011", 3)

# Create domain
domain = svmtk.Domain(surfaces, smap)

# Create meshes of increasing resolutions
Ns = [16, 32, 64, 128]
for N in Ns: 
    print("Creating mesh for N=%d" % N)
    t0 = time.time()
    domain.create_mesh(N) 
    domain.remove_subdomain([3]) 
    domain.save("brain_%d.mesh" % N)
    t1 = time.time()
    print("Done! That took %g sec" % (t1-t0))
