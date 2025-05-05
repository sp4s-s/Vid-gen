import cv2
import os
import sys

def process_video(video_path, output_dir_images, output_dir_videos):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception(f"Could not open video file: {video_path}")
        ret, frame = cap.read()
        if not ret:
            raise Exception(f"Could not read the first frame from video: {video_path}")
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        image_path = os.path.join(output_dir_images, f"{base_name}.jpg")
        cv2.imwrite(image_path, frame)
        print(f"First frame saved as: {image_path}")
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            raise Exception(f"Invalid FPS: {fps}.  Could not clip video.")
        num_frames_to_keep = int(4 * fps)
        output_video_path = os.path.join(output_dir_videos, f"{base_name}.mp4")
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
        if not out.isOpened():
            raise Exception(f"Could not open output video for writing: {output_video_path}")
        frame_count = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        while ret and frame_count < num_frames_to_keep:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
                frame_count += 1
        out.release()
        print(f"Clipped video saved as: {output_video_path}")
        cap.release()
    except Exception as e:
        print(f"Error processing video: {e}")
        return

def process_video_directory(video_dir, output_dir_images, output_dir_videos):
    if not os.path.exists(output_dir_images):
        os.makedirs(output_dir_images)
    if not os.path.exists(output_dir_videos):
        os.makedirs(output_dir_videos)
    files = os.listdir(video_dir)
    for file_name in files:
        file_path = os.path.join(video_dir, file_name)
        if os.path.isfile(file_path):
            if file_name.lower().endswith(('.mp4', '.avi', '.mov', '.wmv')):
                print(f"Processing video: {file_path}")
                process_video(file_path, output_dir_images, output_dir_videos)
            else:
                print(f"Skipping non-video file: {file_path}")
        else:
            print(f"Skipping directory: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_directory = sys.argv[1]
        print(f"Video directory provided as command-line argument: {video_directory}")
    else:
        video_directory = input("Enter the path to the directory containing video files: ")
    output_directory_images = "output_images"
    output_directory_videos = "output_videos"

    if not os.path.exists(video_directory):
        os.makedirs(video_directory)
        print(f"Creating dummy video directory: {video_directory} for demonstration purposes.")
        dummy_video_path = os.path.join(video_directory, "dummy_video.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        dummy_video_writer = cv2.VideoWriter(dummy_video_path, fourcc, 30, (320, 240))
        for _ in range(10):
            dummy_video_writer.write(np.zeros((240, 320, 3), dtype=np.uint8))
        dummy_video_writer.release()

    process_video_directory(video_directory, output_directory_images, output_directory_videos)
    print("Processing complete.")

