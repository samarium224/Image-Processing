import os
import shutil
from tqdm import tqdm

# Define the root path containing the folders like HCC_1, HCC_2, etc.
root_path = r"D:\HCC_DataSet\manifest-1643035385102\output\nonsegment"
output_path = r"D:\HCC_DataSet\manifest-1643035385102\output\nonsegment\Data"
# Define the paths for the new directories to store all segmentation and CT images
# segmentation_dir = os.path.join(output_path, "masks")
ct_dir = os.path.join(output_path, "images")

# Create the new directories if they don't exist
# os.makedirs(segmentation_dir, exist_ok=True)
os.makedirs(ct_dir, exist_ok=True)

# Get the list of folders in the root path (e.g., HCC_1, HCC_2, etc.)
folders = [f for f in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, f)) and f.startswith('HCC_')]

# Initialize counters for naming files serially
seg_counter = 1
ct_counter = 1

# Loop through each folder and process the images
for folder in tqdm(folders):
    # seg_folder = os.path.join(root_path, folder, "Mask")
    ct_folder = os.path.join(root_path, folder, "CT")
    
    # Check if the segmentation and CT directories exist
    # if not os.path.exists(seg_folder) or not os.path.exists(ct_folder):
    #     print(f"Skipping {folder} because required subdirectories do not exist.")
    #     continue

    # Get the list of segmentation and CT image files
    # seg_files = os.listdir(seg_folder)
    ct_files = os.listdir(ct_folder)
    
    # Copy segmentation images to the new directory with serial naming
    # for seg_file in seg_files:
    #     src_path = os.path.join(seg_folder, seg_file)
    #     dest_path = os.path.join(segmentation_dir, f"{seg_counter:04d}.png")  # Save with a serial number
    #     shutil.copy(src_path, dest_path)
    #     seg_counter += 1
    #     # print(f"success for Mask: {seg_counter}")
    
    # Copy CT images to the new directory with serial naming
    for ct_file in ct_files:
        src_path = os.path.join(ct_folder, ct_file)
        dest_path = os.path.join(ct_dir, f"{ct_counter:04d}.png")  # Save with a serial number
        shutil.copy(src_path, dest_path)
        ct_counter += 1
        # print(f"success for CT: {ct_counter}")

# print(f"Copied {seg_counter-1} segmentation images to {segmentation_dir}")
print(f"Copied {ct_counter-1} CT images to {ct_dir}")
