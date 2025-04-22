import subprocess
import os

def get_fps(video_path):
    """使用 ffprobe 获取参考视频帧率"""
    cmd = [
        "ffprobe", "-v", "0",
        "-select_streams", "v:0",
        "-show_entries", "stream=r_frame_rate",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    output = subprocess.check_output(cmd).decode().strip()
    num, denom = map(int, output.split('/')) if '/' in output else (int(output), 1)
    return round(num / denom, 2)

def convert_to_reference_fps(reference_video, target_videos, output_dir):
    """将所有目标视频重编码为参考视频帧率"""
    os.makedirs(output_dir, exist_ok=True)

    ref_fps = get_fps(reference_video)
    print(f"🎯 参考视频帧率: {ref_fps} fps")

    for target in target_videos:
        filename = os.path.basename(target)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}_matched{ext}")

        print(f"⚙️ 转换中: {filename} -> {output_path}")
        cmd = [
            "ffmpeg", "-y", "-i", target,
            "-r", str(ref_fps),
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "aac",
            output_path
        ]
        subprocess.run(cmd, check=True)

    print("✅ 所有视频处理完成！")

# 示例用法
if __name__ == "__main__":
    reference_video = "./multi-subject/ActionAuto/original.mp4"
    target_videos = [
        "./multi-subject/ActionAuto/edited_dmt.mp4",
        "./multi-subject/ActionAuto/edited_ours.mp4",
    ]
    output_folder = "./multi-subject/ActionAuto/output"

    convert_to_reference_fps(reference_video, target_videos,output_folder)
