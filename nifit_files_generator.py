import os
import numpy as np
import nibabel as nib
from PIL import Image
from tqdm import tqdm
from ImageProcessingHelpers import hcc_image_pro_helper_func as helper

# Directories
image_dir = r'D:\HCC_DataSet\manifest-1643035385102\output_Arterial_Tumor'
mask_dir = r'D:\HCC_DataSet\manifest-1643035385102\output_Arterial_Tumor'
output_dir = 'output_Tumor_Nifti'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to load PNG images and convert to numpy array
def load_images_from_folder(folder):
    images = []
    for filename in helper.sort_img_files(folder):  # Sort to maintain order
        if filename.endswith('.png'):
            img = Image.open(os.path.join(folder, filename))
            img = np.array(img)
            images.append(img)
    return np.array(images)

# Loop over each patient's image and mask folders
for patient_id in tqdm(helper.sort_subfolders(image_dir)):  # Assuming each patient has its own folder
    patient_image_folder = os.path.join(image_dir, patient_id, 'CT')
    patient_mask_folder = os.path.join(mask_dir, patient_id, 'Mask')

    if os.path.isdir(patient_image_folder) and os.path.isdir(patient_mask_folder):
        # Load images and masks
        images = load_images_from_folder(patient_image_folder)
        masks = load_images_from_folder(patient_mask_folder)

        # Create NIfTI images for both images and masks
        image_nifti = nib.Nifti1Image(images, np.eye(4))  # Identity matrix for affine
        mask_nifti = nib.Nifti1Image(masks, np.eye(4))

        # Save as .nii.gz files
        nib.save(image_nifti, os.path.join(output_dir, f'{patient_id}_images.nii.gz'))
        nib.save(mask_nifti, os.path.join(output_dir, f'{patient_id}_masks.nii.gz'))

        print(f'Processed patient {patient_id}')
