import SVMTK as svmtk

def create_gwv_mesh(pial_stl, white_stl, ventricles_stl,
                    output, remove_ventricles=True):

    # Create SVMTk Surfaces from STL files
    pial  = svmtk.Surface(pial_stl)
    white = svmtk.Surface(white_stl)
    ventricles = svmtk.Surface(ventricles_stl)
    surfaces = [pial, white, ventricles]

    # Define identifying tags for the different regions 
    tags = {"pial": 1, "white": 2, "ventricle": 3}

    # Define the corresponding subdomain map
    smap = svmtk.SubdomainMap()
    smap.add("100", tags["pial"])
    smap.add("110", tags["white"])
    smap.add("111", tags["ventricle"])

    # Mesh and tag the domain from the surfaces and map
    domain = svmtk.Domain(surfaces, smap)
    resolution = 32
    domain.create_mesh(resolution)
    
    # Remove subdomain with right tag from the domain
    if remove_ventricles:
        domain.remove_subdomain(tags["ventricle"])
        
    # Save the mesh  
    domain.save(output) 

create_gwv_mesh("lh.pial.stl", "lh.white.stl",
                "lh.ventricles.stl",
                "lh.no-ventricles.mesh")
