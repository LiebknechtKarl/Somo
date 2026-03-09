# 音频信息    视频信息
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import wave
import contextlib
import os
if __name__ == "__main__":

    # 音频文件路径
    # 音频路径
    audio_path = "data_origin/normal_voice/s2/video1.wav"

    # 打印 .wav 文件基本信息
    with contextlib.closing(wave.open(audio_path, 'rb')) as f:
        n_channels = f.getnchannels()
        sample_width = f.getsampwidth()
        framerate = f.getframerate()
        n_frames = f.getnframes()
        duration = n_frames / float(framerate)

        print("🎵 音频文件信息：")
        print(f"路径: {audio_path}")
        print(f"持续时间 (秒): {duration:.2f}")
        print(f"采样率 (fps): {framerate}")
        print(f"总帧数: {n_frames}")
        print(f"声道数: {n_channels}")
        print(f"样本宽度 (字节): {sample_width}")

    # 视频文件路径（如果你想对比）
    video_path = "data_origin/normal_voice/s2/video1.mp4"

    # --- 视频信息（可选）---
    if os.path.exists(video_path):
        video_clip = VideoFileClip(video_path)
        print("\n🎬 视频文件信息")
        print(f"持续时间 (秒): {video_clip.duration:.2f}")
        print(f"帧率 (fps): {video_clip.fps}")
        print(f"帧数: {int(video_clip.duration * video_clip.fps)}")
        print(f"分辨率: {video_clip.size}")
        # ✅ 主动关闭
        video_clip.close()