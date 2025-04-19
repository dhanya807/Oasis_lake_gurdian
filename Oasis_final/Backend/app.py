from flask import Flask, render_template, request, redirect, url_for, session
import os
import cv2
from PIL import Image
from lake_segmentation import segment_lake
from fetch_lake_image import fetch_lake_image
from send_email_alert import send_email_alert
from database import db, User

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session["user"] = user.email  
            return redirect(url_for("home"))
        else:
            return "Invalid credentials"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route("/process", methods=["POST"])
def process_lake():
    if "user" not in session:
        return redirect(url_for("login"))
    
    lake_name = request.form["lake_name"]
    user_email = session["user"]
    
    # Fetching satellite image 
    result = fetch_lake_image(lake_name)
    if result is None:
        return "Error: Could not retrieve satellite image."
    
    # Assuming first element of tuple as image
    if isinstance(result, tuple):
        image = result[0]
    else:
        image = result
    
    # saving image using PIL.Image.fromarray
    if not hasattr(image, "save"):
        try:
            image = Image.fromarray(image)
        except Exception as e:
            return f"Error converting image: {e}"
    
    # Saving the image to a file in the static folder
    image_path = os.path.join("static", "enhanced_lake_image.jpg")
    try:
        image.save(image_path)
    except Exception as e:
        return f"Error saving image: {e}"
    
    # Loading the saved image with OpenCV for segmentation
    processed_image = cv2.imread(image_path)
    if processed_image is None:
        return "Error: Unable to read the saved image."
    
    # Perform lake segmentation and calculate the area
    _, lake_area = segment_lake(processed_image)
    
    
    print(f"Calculated lake area: {lake_area} square meters")
    
    
    AREA_THRESHOLD = 50000 
    send_email_alert(user_email, lake_name, lake_area, AREA_THRESHOLD)
    
    
    enhanced_image_path = "enhanced_lake_image.jpg"
    return render_template("result.html", lake_name=lake_name, lake_area=lake_area, enhanced_image_path=enhanced_image_path)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
