# Oasis_lake_gurdian
This system detects unauthorized land use around Bengaluru's lakes using Sentinel satellite imagery and a K means clustering. Built with Python (backend) and HTML, CSS, JavaScript (frontend), it provides real-time encroachment detection and automated alerts to help authorities take timely action, supporting sustainable lake conservation and urban planning.

# Project Content and technology
# Fetch_Lake_image
  Libraries - numpy, cv2, matplotlib, PIL, geopy
  It fetches the lake image from Sentinental Hub API, while taking the lake name as input form the frontend. Then enhances the image 
  using Image processing techniques and PIL library.
# Lake_segmentation
  It uses k means clustering to find the edges  and finally calculate the area.
# send_email_alert
  It compares the calculated area with the threshold and send the email alert which contains lake area and the enchrochment details 
  to the users.
# app.py
  Main file which uses flask technology and integrates everything.
 
