import cv2
import numpy as np
import matplotlib.pyplot as plt

def segment_lake(image, k_clusters=3, pixel_to_meter_ratio=10):
   
    
    lab_image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)

    # Reshape image into a 2D array of pixels
    pixel_values = lab_image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)

    # Applying K-means clustering
    _, labels, _ = cv2.kmeans(pixel_values, k_clusters, None,
                              (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2),
                              10, cv2.KMEANS_RANDOM_CENTERS)

    # Reshape labels back to image shape
    clustered_image = labels.reshape(lab_image.shape[:2])

    # Identify the cluster representing the lake using color analysis
    unique_clusters, counts = np.unique(clustered_image, return_counts=True)

   
    lake_cluster = unique_clusters[np.argmax(counts)]  

    # Create a mask where the lake cluster is white, others black
    lake_mask = np.uint8(clustered_image == lake_cluster) * 255

    # removing noise
    kernel = np.ones((5, 5), np.uint8)
    lake_mask = cv2.morphologyEx(lake_mask, cv2.MORPH_CLOSE, kernel)

    # Calculating lake area
    lake_pixels = np.sum(lake_mask == 255)
    lake_area_m2 = lake_pixels * (pixel_to_meter_ratio ** 2)

    # results 
    #plt.figure(figsize=(10, 5))
    #plt.subplot(1, 3, 1)
    #plt.imshow(image)
    #plt.title("Original Image")

    #plt.subplot(1, 3, 2)
    #plt.imshow(clustered_image, cmap="jet")
    #plt.title("K-Means Clusters")

    #plt.subplot(1, 3, 3)
    #plt.imshow(lake_mask, cmap="gray")
    #plt.title(f"Final Lake Mask\nArea: {lake_area_m2:.2f} m²")

    #plt.show()

    #print(f"Lake Area: {lake_area_m2:.2f} square meters")
    #print(f"Lake Area: {lake_area_m2 / 1_000_000:.4f} square kilometers")

    return lake_mask, lake_area_m2
