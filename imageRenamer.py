import os
from ImageProcessingHelpers import hcc_image_pro_helper_func as helper
# Define the path to the folder containing the images
folder_path = r"D:\HCC_DataSet\manifest-1643035385102\Tumor_DATA\tumor_CLAHE\images"

# List all files in the folder and filter out only image files
images =helper.sort_img_files(folder_path)
print(images)

# Loop through the images and rename them
for i, image_name in enumerate(images):
    
    new_name = f"{i + 1}.png"
    # Get the full path for the current image and the new image name
    old_path = os.path.join(folder_path, image_name)
    new_path = os.path.join(folder_path, new_name)

    # Rename the image
    os.rename(old_path, new_path)

    print(f"Renamed: {old_path} -> {new_path}")

print("Renaming complete!")