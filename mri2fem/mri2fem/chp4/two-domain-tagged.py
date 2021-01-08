import SVMTK as svmtk 

def create_gw_mesh(pial_stl, white_stl, output):
    # Load the surfaces into SVM-Tk and combine in list
    pial  = svmtk.Surface(pial_stl)
    white = svmtk.Surface(white_stl)
    surfaces = [pial, white]
    
    # Create a map for the subdomains with tags
    # 1 for inside the first and outside the second ("10")
    # 2 for inside the first and inside the second ("11")
    smap = svmtk.SubdomainMap()
    smap.add("10", 1)
    smap.add("11", 2)

    # Create a tagged domain from the list of surfaces
    # and the map
    domain = svmtk.Domain(surfaces, smap)
       
    # Create and save the volume mesh 
    resolution = 32
    domain.create_mesh(resolution)
    domain.save(output) 

create_gw_mesh("lh.pial.stl", "lh.white.stl", "ernie-gw.mesh")
