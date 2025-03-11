from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os

imgs_dir = os.path.join(os.getcwd(), 'imgs')
image_file = os.path.join(imgs_dir, 'fullpage_screenshot.png')

with Image.open(image_file) as img:
    img = img.convert("RGB")
    print(f"Image size: {img.size}, Mode: {img.mode}")

# Convert image to numpy array
pixels = np.array(img).reshape(-1, 3)  # Flatten to (N, 3)

# Apply K-Means++
num_colors = 8
kmeans = KMeans(n_clusters=num_colors, init="k-means++", n_init="auto", random_state=42)
kmeans.fit(pixels)
colors = kmeans.cluster_centers_.astype(int)

# Convert RGB colors to hex
def rgb_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(*color)

hex_colors = [rgb_to_hex(color) for color in colors]

# Plot the color palette
plt.figure(figsize=(12, 2))
plt.bar(range(num_colors), [1] * num_colors, color=hex_colors, edgecolor='none')
plt.xticks(range(num_colors), hex_colors, rotation='vertical')
plt.yticks([])
plt.title(f'{num_colors} Dominant Colors')
plt.show()

# Print extracted colors
print("Dominant Colors:", hex_colors)
