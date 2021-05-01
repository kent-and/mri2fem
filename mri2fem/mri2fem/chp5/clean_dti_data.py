import argparse
import numpy
import nibabel
try : from check_dti import check_dti_data
except : from .check_dti import check_dti_data

def find_valid_adjacent_tensor(data, i, j, k ,max_iter): 
    # Start at 1, since 0 is an invalid tensor 
    for m in range(1, max_iter+1) :
        # Extract the adjacent data to voxel i, j, k
        # and compute the mean diffusivity. 
        A = data[i-m:i+m+1, j-m:j+m+1, k-m:k+m+1,:]
        A = A.reshape(-1, 9)
        MD = (A[:, 0]+ A[:, 4] + A[:,8])/3.

        # If valid tensor is found:
        if MD.sum() > 0.0:             
           # Find index of the median valid tensor, and return
           # corresponding tensor.     
           index = (numpy.abs(MD - numpy.median(MD[MD>0]))).argmin()
           return A[index]
                      
    print("Failed to find valid tensor")
    return data[i, j, k]  

def clean_dti_data(dti_file, mask_file, out_file, order=3,
                   max_search=9):
    valid, mask, D = check_dti_data(dti_file, mask_file,
                                    order=order)
    # Zero out "invalid" tensor entries outside mask, 
    # and extrapolate from valid neighbors
    D[~mask] = numpy.zeros(9)
    D[(~valid)*mask] = numpy.zeros(9)
    ii, jj, kk = numpy.where((~valid)*mask)
    for i, j, k in zip(ii, jj, kk): 
        D[i, j, k, :] = \
            find_valid_adjacent_tensor(D, i, j, k, max_search)

    # Create and save clean DTI image in T1 voxel space:
    mask_image = nibabel.load(mask_file)
    M1, M2, M3 = mask.shape
    shape = numpy.zeros((M1, M2, M3, 9)) 

    vox2ras = mask_image.header.get_vox2ras()
    Nii = nibabel.nifti1.Nifti1Image
    dti_image = Nii(D, vox2ras)

    nibabel.save(dti_image, out_file)

if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument("--dti", type=str)   
   parser.add_argument("--mask", type=str) 
   parser.add_argument("--out", type=str) 
   parser.add_argument("--max_search", default=9, type=int) 
   parser.add_argument("--order", default=3, type=int) 

   Z = parser.parse_args()

   clean_dti_data(Z.dti, Z.mask, Z.out, Z.order, Z.max_search)





