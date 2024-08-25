import os
import numpy as np
from PIL import Image

# Paths to dataset
DATASET_PATH = r"D:\HCC_DataSet\manifest-1643035385102\output_Arterial\Data"
OUTPUT_PATH = "Tumor_DATA/images"

# Folders for images and masks
image_folder = os.path.join(DATASET_PATH, "images")
mask_folder = os.path.join(DATASET_PATH, "masks")

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_PATH, exist_ok=True)

# List of images and masks
images = os.listdir(image_folder)
masks = os.listdir(mask_folder)

# Ensure the image and mask file names match
for image_name in images:
    # Construct full paths to the image and mask
    image_path = os.path.join(image_folder, image_name)
    mask_path = os.path.join(mask_folder, image_name)

    # Ensure corresponding mask exists
    if not os.path.exists(mask_path):
        print(f"Mask for image {image_name} not found, skipping...")
        continue

    # Load the image and mask
    image = Image.open(image_path).convert('L')  # Convert to grayscale if needed
    mask = Image.open(mask_path).convert('L')
    mask = mask.point(lambda x: 0 if x<128 else 255, '1')

    # Convert images to numpy arrays
    image_array = np.array(image)
    mask_array = np.array(mask)

    # Multiply image and mask
    multiplied_array = image_array * mask_array

    # Convert back to an image
    multiplied_image = Image.fromarray(multiplied_array)

    # Save the result
    output_path = os.path.join(OUTPUT_PATH, image_name)
    multiplied_image.save(output_path)

    print(f"Saved multiplied image to {output_path}")

print("Processing complete.")
