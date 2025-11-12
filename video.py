import cv2
import numpy as np
import imageio
import os

# Paths
input_folder = r"D:\code\chess\data\photos without spec\clean_faces"
final_img_path = os.path.join(input_folder, "average_face_aligned.jpg")
gif_path = os.path.join(input_folder, "averaging_aligned.gif")
output_video_path = os.path.join(input_folder, "average_comparison.mp4")

# Load the final averaged image
final_img = cv2.imread(final_img_path)
final_img = cv2.resize(final_img, (600, 600))

# Load frames from GIF
gif_frames = imageio.mimread(gif_path)

# Set up video writer
frame_height, frame_width = 600, 600 * 2  # two panels side by side
fps = 5  # frames per second (lower = slower video)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Create frames
for gif_frame in gif_frames:
    frame = cv2.cvtColor(np.array(gif_frame), cv2.COLOR_RGB2BGR)
    frame = cv2.resize(frame, (600, 600))

    # Combine side-by-side: left = final face, right = current stage
    combined = np.hstack((final_img, frame))
    out.write(combined)

out.release()
print(f"🎥 Video saved: {output_video_path}")
