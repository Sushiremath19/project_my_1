import cv2
import numpy as np

# --- Functions ---

def estimate_pH(image):
    """
    Estimate pH based on HSV hue values
    """
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hue = hsv_image[:, :, 0]

    mean_hue = np.mean(hue)

    # Map hue to pH range (6.5 to 7.5 as example)
    pH = 6.5 + (mean_hue / 180.0) * 2   # Hue max = 180 in OpenCV
    pH = min(max(pH, 6), 8)  # Constrain between 6 and 8
    return pH


def estimate_Dissolved_Oxygen(image):
    """
    Estimate Dissolved Oxygen (DO) based on brightness
    """
    brightness = np.mean(image)
    do = 6 + (brightness / 255.0) * 3  # scale brightness
    do = min(max(do, 5), 10)  # constrain between 5 and 10
    return do


def estimate_Nitrate(image):
    """
    Estimate nitrate with random variability
    """
    nitrate = 4 + np.random.rand() * 6  # between 4 and 10
    return nitrate


# --- Main Program ---

# Read the image
img = cv2.imread("2.jpeg.jpg")  # Replace with your file path

if img is None:
    raise ValueError("Image could not be read. Check the file path.")

# Convert to grayscale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Resize to 256x256
gray_img = cv2.resize(gray_img, (256, 256))

# Mean intensity as turbidity measure
mean_turbidity = np.mean(gray_img)

# Estimates
estimated_pH = estimate_pH(img)
estimated_Dissolved_Oxygen = estimate_Dissolved_Oxygen(img)
estimated_Nitrate = estimate_Nitrate(img)

# Acceptable limits
acceptable_limits = {
    "pH": (6.5, 7.5),
    "Turbidity": (0, 150),
    "Dissolved_Oxygen": (6, 9),
    "Nitrate": (0, 10)
}

# Results
results = "Good"

if estimated_pH < acceptable_limits["pH"][0] or estimated_pH > acceptable_limits["pH"][1]:
    results = "Poor (pH out of range)"

elif mean_turbidity > acceptable_limits["Turbidity"][1]:
    results = "Poor (Turbidity too high)"

elif estimated_Dissolved_Oxygen < acceptable_limits["Dissolved_Oxygen"][0]:
    results = "Poor (Dissolved Oxygen too low)"

elif estimated_Nitrate > acceptable_limits["Nitrate"][1]:
    results = "Poor (Nitrate too high)"


# --- Print Results ---
print(f"Water Quality Assessment: {results}")
print(f"Estimated pH: {estimated_pH:.2f}")
print(f"Mean Turbidity: {mean_turbidity:.2f}")
print(f"Estimated Dissolved Oxygen: {estimated_Dissolved_Oxygen:.2f} mg/L")
print(f"Estimated Nitrate: {estimated_Nitrate:.2f} mg/L")
