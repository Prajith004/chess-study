import cv2
import glob
import os


input_folder = r"D:\code\chess\data\photos without spec"
output_folder = os.path.join(input_folder, "clean_faces")


os.makedirs(output_folder, exist_ok=True)


for file_path in glob.glob(os.path.join(input_folder, "*")):
    # Read the image
    img = cv2.imread(file_path)
    if img is None:
        print(f"Skipping unreadable file: {file_path}")
        continue

    
    height, width = img.shape[:2]

    
    file_name = os.path.basename(file_path)
    file_name = os.path.splitext(file_name)[0].replace(" ", "_") + ".jpg"

    
    output_path = os.path.join(output_folder, file_name)
    success = cv2.imwrite(output_path, img)

    if success:
        print(f" Cleaned ({width}x{height}) → {output_path}")
    else:
        print(f" Failed to save: {output_path}")

print(" Done! All cleaned images are in:", output_folder)
