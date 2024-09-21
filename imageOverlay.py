import os
import random
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from ImageProcessingHelpers import hcc_image_pro_helper_func as helper
#set parameters

# Define the paths to the directories containing the images
main_img_path = rf"D:\HCC_DataSet\manifest-1643035385102\Tumor_DATA\low_dice_images"
seg_img_path = rf"D:\HCC_DataSet\manifest-1643035385102\Tumor_DATA\low_dice_masks" #ground truth

# predicted_img_mask = rf"D:\HCC_DataSet\manifest-1643035385102\results\Generated_mask\resnet50_UnetPlusPlus_Multi"

# Get the list of all images in the CT directory
# all_img_filenames = helper.sort_img_files(main_img_path)
all_img_filenames = os.listdir(main_img_path)
# print(all_img_filenames)
# select 15 images 11 15
Index = 4
Index = Index * 4                 # /// start from

selected_images = all_img_filenames[Index:Index+4]
# selected_images = ['5493.png', '5494.png', '5495.png', '5496.png']
print(selected_images)

# Plot the images
figure, axes = plt.subplots(2, 4, figsize=(10, 5))

for i, img_filename in enumerate(selected_images):
    # Construct the full paths to the images
    ground_truth_img_full_path = os.path.join(seg_img_path, img_filename)
    main_img_full_path = os.path.join(main_img_path, img_filename)
    # predicted_img_full_path = os.path.join(predicted_img_mask, img_filename)

    # Load the main image and the mask
    img = Image.open(main_img_full_path).convert('RGB')
    img = np.array(img)
    mask = Image.open(ground_truth_img_full_path).convert('RGB')
    color_mask = np.array(mask)

    # predicted_mask = Image.open(predicted_img_full_path).convert('RGB')
    # predicted_mask = np.array(predicted_mask)

    # Find the indices where the color in the mask is black [0, 0, 0]
    black_pixels = np.all(color_mask == [0, 0, 0], axis=-1)
    tumor_pixels = np.all(color_mask == [62, 73, 137], axis=-1)
    liver_pixels = np.all(color_mask == [255, 255, 255], axis=-1)

    # Replace black pixels in the mask with the corresponding pixels from the image
    color_mask[black_pixels] = img[black_pixels]
    # predicted_mask[black_pixels] = img[black_pixels]
    # color_mask[tumor_pixels] = [255,0,0]
    color_mask[liver_pixels] = [255, 0, 0]

    # Show the main image with the red mask overlay
    ax = axes[0, i]
    # ax.set_title(img_filename)
    ax.imshow(img)
    # ax.imshow(predicted_mask, alpha=1)
    ax.imshow(color_mask, alpha = 0.0)  # Overlay the mask with transparency
    ax.axis('off')

    if i == 0:
        bx = axes[1, 0]
        bx.imshow(mask, alpha=1)
        bx.axis('off')

    if i == 1:
        cx = axes[1, 1]
        cx.imshow(mask, alpha=1)
        cx.axis('off')

    if i == 2:
        cx = axes[1, 2]
        cx.imshow(mask, alpha=1)
        cx.axis('off')
    
    if i == 3:
        cx = axes[1, 3]
        cx.imshow(mask, alpha=1)
        cx.axis('off')

plt.tight_layout(pad=0)
plt.show()
