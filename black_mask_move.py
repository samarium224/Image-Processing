import os
import shutil
from PIL import Image
import numpy as np

# Define paths
mask_image_path = r"D:\HCC_DataSet\manifest-1643035385102\Tumor_DATA\masks"
tumor_image_path = r"D:\HCC_DataSet\manifest-1643035385102\Tumor_DATA\images"

# Define the output directory for black images
output_black_masks = r"D:\HCC_DataSet\manifest-1643035385102\Tumor_DATA\black_masks"
output_black_tumor_images = r"D:\HCC_DataSet\manifest-1643035385102\Tumor_DATA\black_tumor_images"

# Create output directories if they do not exist
os.makedirs(output_black_masks, exist_ok=True)
os.makedirs(output_black_tumor_images, exist_ok=True)

# List all mask images
mask_images = os.listdir(mask_image_path)

# Loop through mask images to find black masks
for mask_image_name in mask_images:
    mask_image_full_path = os.path.join(mask_image_path, mask_image_name)

    # Open the mask image using PIL
    with Image.open(mask_image_full_path) as mask_image:
        # Convert the image to a NumPy array
        mask_array = np.array(mask_image)

        # Check if the mask is completely black
        if np.max(mask_array) == 0:
            # The mask is completely black, move the mask and corresponding tumor image
            tumor_image_full_path = os.path.join(tumor_image_path, mask_image_name)

            # Move the black mask image
            shutil.move(mask_image_full_path, os.path.join(output_black_masks, mask_image_name))

            # Move the corresponding tumor image if it exists
            if os.path.exists(tumor_image_full_path):
                shutil.move(tumor_image_full_path, os.path.join(output_black_tumor_images, mask_image_name))

            print(f"Moved black mask and corresponding tumor image: {mask_image_name}")

print("Completed moving black masks and their corresponding tumor images.")
