import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance
from geopy.geocoders import Nominatim
from sentinelhub import SentinelHubRequest, DataCollection, MimeType, bbox_to_dimensions, BBox, SHConfig
from lake_segmentation import segment_lake  
import os

# Sentinel Hub Configuration 
INSTANCE_ID = "6ecfe366-be85-4b42-81df-3cfd544f7955"
CLIENT_ID = "debcfdb4-f192-4a57-bf3c-f45b250e7262"
CLIENT_SECRET = "bfcJz94yIgeOOvKEV68rX9wcU78x6ihY"

config = SHConfig()
config.instance_id = INSTANCE_ID
config.sh_client_id = CLIENT_ID
config.sh_client_secret = CLIENT_SECRET

# Fetching Latitude And Longitude
def get_lake_coordinates(lake_name):
    geolocator = Nominatim(user_agent="lake_locator")
    location = geolocator.geocode(lake_name)

    if location:
        print(f"Found '{lake_name}' at: {location.latitude}, {location.longitude}")
        return location.latitude, location.longitude
    else:
        print(f"Lake '{lake_name}' not found!")
        return None, None

# Fetching Satellite Image of the Lake
def fetch_lake_image(lake_name):
    lat, lon = get_lake_coordinates(lake_name)
    if lat is None or lon is None:
        return None, None  

    # Define bounding box 
    bbox_size = 0.05  
    lake_bbox = BBox(bbox=[lon - bbox_size, lat - bbox_size, lon + bbox_size, lat + bbox_size], crs="EPSG:4326")
    
    # image size
    image_size = bbox_to_dimensions(lake_bbox, resolution=10)


    request = SentinelHubRequest(
        evalscript="""
        function setup() {
            return {
                input: ["B04", "B03", "B02"],
                output: { bands: 3 }
            };
        }
        function evaluatePixel(sample) {
            return [sample.B04, sample.B03, sample.B02];
        }
        """,
        input_data=[SentinelHubRequest.input_data(DataCollection.SENTINEL2_L1C, time_interval=("2024-03-01", "2024-03-05"))],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=lake_bbox,
        size=image_size,
        config=config,
    )

    # Get the image
    image = request.get_data()[0]

    if image is None:
        print("❌ Failed to fetch satellite image.")
        return None, None

    return image, lat, lon  

#  Enhance the Lake Image
def enhance_image(image, lake_name):
   
    image_pil = Image.fromarray(image)

    
    enhancer = ImageEnhance.Brightness(image_pil)
    image_pil = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Contrast(image_pil)
    image_pil = enhancer.enhance(1.8)
    enhancer = ImageEnhance.Sharpness(image_pil)
    image_pil = enhancer.enhance(2.0)

    # Converting back to OpenCV format
    enhanced_image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    image_path = f"static/images/{lake_name.replace(' ', '_')}_enhanced.jpg"
    os.makedirs("static/images", exist_ok=True)
    cv2.imwrite(image_path, enhanced_image)

    return image_path  

# Function to Process Lake Image
def process_lake(lake_name):
    lake_image, lat, lon = fetch_lake_image(lake_name)

    if lake_image is not None:
        enhanced_image_path = enhance_image(lake_image, lake_name)

        #  Apply Lake Segmentation
        lake_mask, lake_area = segment_lake(cv2.imread(enhanced_image_path))

        return enhanced_image_path, lake_area
    else:
        return None, None  
