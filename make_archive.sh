# Create tar ball of mri2fem folder
git archive --format=tar --output=./mri2fem.tar HEAD mri2fem
gzip mri2fem.tar

# Upload mri2fem.tar.gz to Zenodo.
