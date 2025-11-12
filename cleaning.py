import cv2
import glob
import os

# Path to your raw photo folder
input_folder = r"D:\code\chess\data\photos without spec"
output_folder = os.path.join(input_folder, "clean_faces")

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all image files in the folder
for file_path in glob.glob(os.path.join(input_folder, "*")):
    # Read the image
    img = cv2.imread(file_path)
    if img is None:
        print(f"❌ Skipping unreadable file: {file_path}")
        continue

    # Keep original size — no resizing
    height, width = img.shape[:2]

    # Get clean filename (replace spaces and ensure .jpg)
    file_name = os.path.basename(file_path)
    file_name = os.path.splitext(file_name)[0].replace(" ", "_") + ".jpg"

    # Save to output folder as clean JPEG (drop weird metadata)
    output_path = os.path.join(output_folder, file_name)
    success = cv2.imwrite(output_path, img)

    if success:
        print(f"✅ Cleaned ({width}x{height}) → {output_path}")
    else:
        print(f"⚠️ Failed to save: {output_path}")

print("\n🎉 Done! All cleaned images are in:", output_folder)
