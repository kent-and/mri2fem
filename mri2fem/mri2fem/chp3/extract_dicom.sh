#!/bin/bash

echo "FreeSurfer configuration is required to run this script" 
if [ ! -z "${FREESURFER_HOME}" ];
then
   echo "FreeSurfer found"  
else 
   echo "FreeSurfer not found" 
   exit 
fi

#  $1 = input of the DICOM folder
#  $2 = the output copy directory
#  $3 = the key reference

files=$(find $1 -type f ) # Finds all files in the directory and subdirectories
for j in ${files}; do
    name=$(${FREESURFER_HOME}/bin/mri_probedicom --i ${j} --t 18 1030)  #returns Protocol Name
    if [ "${name/$3}" != "$name" ]  # Checks if specific tag is part of the protocol name
    then
       mkdir -p ${2}/${name//[[:blank:]]/}  # Removes spaces in protocol name, which can be a problem with recon-all 
       cp ${j}  ${2}/${name//[[:blank:]]/}  
    fi
done

