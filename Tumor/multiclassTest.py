import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Load the grayscale mask images
image_path_liver = r'P:\Samir\Seg\1_liver40.png'
mask_image_liver = Image.open(image_path_liver)
image_path_tumor = r'P:\Samir\Seg\2_tumor40.png'
mask_image_tumor = Image.open(image_path_tumor)

# Convert the grayscale images to NumPy arrays
mask_array_liver = np.array(mask_image_liver)
mask_array_tumor = np.array(mask_image_tumor)

# Create an RGB image with the same dimensions as the mask images
combined_image = np.zeros((mask_array_liver.shape[0], mask_array_liver.shape[1], 3), dtype=np.uint8)

# Define the new mask colors (R, G, B)
mask_color_liver = (71, 39, 119)
mask_color_tumor = (62, 73, 137)

# Apply the liver mask color where the mask is white (255 in grayscale)
combined_image[mask_array_liver == 255] = mask_color_liver

# Apply the tumor mask color where the mask is white (255 in grayscale)
# If the tumor mask overlaps with the liver mask, we can blend the colors.
for i in range(3):
    combined_image[mask_array_tumor == 255, i] = np.maximum(combined_image[mask_array_tumor == 255, i], mask_color_tumor[i])

# Display the result using matplotlib
plt.imshow(combined_image)
plt.axis('off')  # Hide the axis
plt.show()