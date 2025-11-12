import cv2
import dlib
import numpy as np
import glob
import os
import imageio

# === CONFIG ===
input_folder = r"D:\code\chess\data\photos without spec\clean_faces"
predictor_path = r"D:\code\chess\data\shape_predictor_68_face_landmarks.dat"
output_avg_path = os.path.join(input_folder, "average_face_aligned.jpg")
output_gif_path = os.path.join(input_folder, "averaging_aligned.gif")

# Initialize dlib's face detector + landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

def get_landmarks(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)
    if len(rects) == 0:
        return None
    shape = predictor(gray, rects[0])
    return np.array([[p.x, p.y] for p in shape.parts()])

def warp_image(img, src_points, dest_points, size=(600, 600)):
    h, _ = cv2.findHomography(src_points, dest_points)
    warped = cv2.warpPerspective(img, h, size)
    return warped

images, landmarks_list = [], []
for file in glob.glob(os.path.join(input_folder, "*.jpg")):
    img = cv2.imread(file)
    if img is None:
        continue
    landmarks = get_landmarks(img)
    if landmarks is None:
        print(f"⚠️ Skipping (no face found): {file}")
        continue
    landmarks_list.append(landmarks)
    images.append(img)
    print(f"✅ Loaded: {file}")

if not images:
    raise RuntimeError("No valid faces found!")

# Compute mean landmarks
mean_landmarks = np.mean(landmarks_list, axis=0)

# Warp every face to average shape
aligned_faces = []
for img, lm in zip(images, landmarks_list):
    warped = warp_image(img, lm, mean_landmarks)
    aligned_faces.append(warped)

# Average aligned faces
avg_face = np.mean(aligned_faces, axis=0).astype(np.uint8)
cv2.imwrite(output_avg_path, avg_face)
print(f"\n🎉 Saved aligned average face: {output_avg_path}")

# Animated GIF of progressive averaging
frames = []
for i in range(1, len(aligned_faces) + 1):
    partial_avg = np.mean(aligned_faces[:i], axis=0).astype(np.uint8)
    frames.append(cv2.cvtColor(partial_avg, cv2.COLOR_BGR2RGB))
imageio.mimsave(output_gif_path, frames, duration=0.8)
print(f"🎬 Saved animation: {output_gif_path}")
