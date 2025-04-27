import cv2
import numpy as np

# Create a blank image (white background)
img = np.ones((800, 600, 3), np.uint8) * 255

# Add title
cv2.putText(img, "Customer Satisfaction Survey", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

# Question 1
cv2.putText(img, "1. How would you rate our service?", (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
# Options for Question 1
options = ["Excellent", "Good", "Average", "Poor"]
y_pos = 150
for option in options:
    # Draw circle (bubble)
    cv2.circle(img, (70, y_pos), 10, (0, 0, 0), 1)
    # Add option text
    cv2.putText(img, option, (100, y_pos + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    y_pos += 40

# Question 2
cv2.putText(img, "2. Would you recommend us to others?", (50, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
# Options for Question 2
options = ["Yes", "No", "Maybe"]
y_pos = 350
for option in options:
    # Draw circle (bubble)
    cv2.circle(img, (70, y_pos), 10, (0, 0, 0), 1)
    # Add option text
    cv2.putText(img, option, (100, y_pos + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    y_pos += 40

# Question 3
cv2.putText(img, "3. How often do you use our product?", (50, 480), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
# Options for Question 3
options = ["Daily", "Weekly", "Monthly", "Rarely"]
y_pos = 510
for option in options:
    # Draw circle (bubble)
    cv2.circle(img, (70, y_pos), 10, (0, 0, 0), 1)
    # Add option text
    cv2.putText(img, option, (100, y_pos + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    y_pos += 40

# Save the image
cv2.imwrite('/home/ubuntu/survey_ocr_project/test_images/blank_survey.png', img)

# Create a filled version (with some bubbles filled)
filled_img = img.copy()

# Fill some bubbles
# Question 1 - "Good" option
cv2.circle(filled_img, (70, 190), 8, (0, 0, 0), -1)  # Filled circle

# Question 2 - "Yes" option
cv2.circle(filled_img, (70, 350), 8, (0, 0, 0), -1)  # Filled circle

# Question 3 - "Weekly" option
cv2.circle(filled_img, (70, 550), 8, (0, 0, 0), -1)  # Filled circle

# Save the filled image
cv2.imwrite('/home/ubuntu/survey_ocr_project/test_images/filled_survey.png', filled_img)

print("Test survey images created successfully!")
