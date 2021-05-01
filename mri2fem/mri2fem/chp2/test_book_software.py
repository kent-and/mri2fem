#!/usr/bin/python
import os
error=False
#FreeSurfer FSL 

print("Checking FreeSurfer home directory.", end = '') 
if not "FREESURFER_HOME" in os.environ.keys():
   print("\n\tFreeSurfer is not found.") 
   print("\tIf FreeSurfer is downloaded add\n \t export <FreeSurfer directory> \n\tto .bashrc")  
   print("\tOtherwise install FreeSurfer following the guide at \n\thttps://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall")
   error=True 
else :
    print("\t=> FreeSurfer home directory found.")
    
print("\nChecking FreeSurfer configuration.",end = '')     
if not "SUBJECTS_DIR" in os.environ.keys():
   print("\n\tFreeSurfer not fully  configured.") 
   print("\tAdd\n \t $FREESURFER_HOME/SetUpFreeSurfer.sh \n to .bashrc") 
   error=True
else :
    print("\t=> FreeSurfer configuration found")


print("\nChecking license file.",end = '') 
if os.path.exists(os.environ["FREESURFER_HOME"]+"/license.txt") or \
   os.path.exists(os.environ["FREESURFER_HOME"]+"/.license")  : 
   print("\t=> Found license file.")    
else: 
   print("\n\tNo FreeSurfer license")   
   error=True  
   
print("\nChecking FSL directory.",end = '') 
if not "FSL_DIR" in os.environ.keys():
   print("\n\n\tNo FSL detected") 
   print("\tFollow the installation guide at\n\thttps://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation") 
   error=True
else:
   print("\t=> Found FSL directory")  
   
   
from subprocess import call,check_output

print("\nChecking tcsh installation.",end = '')

try :
    "bin/tcsh" in str(check_output(["dpkg","-S","/bin/tcsh"]))
    print("\t=> tcsh installed")
except : 
    print("\n\n\ttcsh is not installed")
    print("\tTo install type\n \tsudo apt-get install tcsh \n\tin the terminal") 
    error=True
 

   
   
print("\nChecking python utility pip installation.",end = '')  
try :  
   import pip
   print("\t=> pip installed") 
except : 
   print("\n\n\tpip is not installed")
   print("\tTo install type\n \t\t sudo apt-get install pip \nin the terminal")
   error=True

print("\nChecking meshio with h5py installation.",end = '')  
try : 
    import meshio,h5py 
    print("\t=> meshio with h5py installed")  
except:
    print("\n\n\tmeshio with h5py is not installed") 
    print("\tTo install type\n \t\t pip install meshio[all] \nin the terminal")
    error=True

print("\nChecking matplotlib  installation.",end = '')  
try : 
    import matplotlib 
    print("\t=> matplotlib installed")  
except:
    print("\n\n\tmatplotlib is not installed") 
    print("\tTo install type\n \t\t pip install matplotlib\nin the terminal")
    error=True

print("\nChecking scipy installation.",end = '')  
try : 
    import scipy 
    print("\t=> scipy installed")  
except:
    print("\n\n\tscipy is not installed") 
    print("\tTo install type\n \t\t pip install scipy\nin the terminal")
    error=True

print("\nChecking SVMTK installation.",end = '') 
try : 
    import SVMTK 
    print("\t=> SVMTK installed") 
except:
    print("\n\n\tSVMTK is not found") 
    print("\tFollow the installation guide at\n \thttps://github.com/SVMTK/SVMTK\n")
    error=True

print("\nChecking FEniCS installation.",end = '') 
try : 
    import dolfin,fenics 
    print("\t=> FEniCS installed.") 
except: 
    print("\n\n\tFEniCS is not installed") 
    print("\tFollow the installation guide at\n \thttps://fenicsproject.org/\n")
    error=True
#if error:
#   print("\nIf errors presists, try to use the book docker image at")
#   print("fill inn")  




