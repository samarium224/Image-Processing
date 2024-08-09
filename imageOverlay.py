import os
import random
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

#set parameters

# Define the paths to the directories containing the images
main_img_path = rf"D:\HCC_DataSet\manifest-1643035385102\output-tumor-multiclass\A_HCC_Tumor_Data\images"
seg_img_path = rf"D:\HCC_DataSet\manifest-1643035385102\output-tumor-multiclass\A_HCC_Tumor_Data\masks" #ground truth

predicted_img_mask = rf"D:\HCC_DataSet\manifest-1643035385102\results\Generated_mask\resnet50_UnetPlusPlus_Multi"

# Get the list of all images in the CT directory
all_img_filenames = os.listdir(main_img_path)

# select 15 images
Index = 55
Index = Index * 4                 # /// start from

# selected_images = all_img_filenames[Index:Index+4]
selected_images = ['5493.png', '5494.png', '5495.png', '5496.png']
print(selected_images)

# Plot the images
figure, axes = plt.subplots(2, 4, figsize=(10, 5))

for i, img_filename in enumerate(selected_images):
    # Construct the full paths to the images
    ground_truth_img_full_path = os.path.join(seg_img_path, img_filename)
    main_img_full_path = os.path.join(main_img_path, img_filename)
    predicted_img_full_path = os.path.join(predicted_img_mask, img_filename)

    # Load the main image and the mask
    img = Image.open(main_img_full_path).convert('RGB')
    img = np.array(img)
    mask = Image.open(ground_truth_img_full_path).convert('RGB')
    color_mask = np.array(mask)

    predicted_mask = Image.open(predicted_img_full_path).convert('RGB')
    predicted_mask = np.array(predicted_mask)

    # Find the indices where the color in the mask is black [0, 0, 0]
    black_pixels = np.all(color_mask == [0, 0, 0], axis=-1)
    tumor_pixels = np.all(color_mask == [62, 73, 137], axis=-1)
    liver_pixels = np.all(color_mask == [71, 39, 119], axis=-1)

    # Replace black pixels in the mask with the corresponding pixels from the image
    color_mask[black_pixels] = img[black_pixels]
    predicted_mask[black_pixels] = img[black_pixels]
    # color_mask[tumor_pixels] = [255,0,0]
    # color_mask[liver_pixels] = [130, 198, 60]

    # Show the main image with the red mask overlay
    ax = axes[0, i]
    # ax.set_title(img_filename)
    # ax.imshow(img)
    ax.imshow(predicted_mask, alpha=1)
    ax.imshow(color_mask, alpha = 0.5)  # Overlay the mask with transparency
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
