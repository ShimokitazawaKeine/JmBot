import os
import cv2  # Import OpenCV library for video processing
from typing import List, Optional, Union


# Removed math and PIL imports

# Class name changed to reflect its actual function: converting images to video
class ImageToVideoConverter:
    """
    Converts a sequence of local image files into a single MP4 video file.
    The methods use clear, idiomatic Python naming conventions.
    """

    def __init__(self, base_path: str = "data/"):
        """
        Initializes the converter.

        Args:
            base_path (str): The root directory path, e.g., "data/".
        """
        print("初始化本地路径 [Initializing local path]")
        self.base_dir = base_path  # Root path, e.g., "data/"
        self.output_dir = base_path  # Root path for output
        self.image_extension = ".jpg"
        self.sorted_image_paths: List[str] = []  # Stores sorted image paths
        self.job_code: Optional[str] = None
        self.final_output_path: str = ""
        self.output_files: Union[str, List[str]] = self.output_dir
        print("加载完成 [Load complete]")

    def set_job_context(self, job_code: str):
        """
        Updates the subdirectory for images and the final output path.

        Args:
            job_code (str): The file set/album code, e.g., "1225249".
        """
        print(f"设置工作上下文: {job_code} [Setting job context]")
        # Fix: Concatenate base path and job code to form the image directory
        self.image_source_dir = os.path.join(self.base_dir, job_code)

        # Fix: Set the output path to the video file, using .mp4 extension
        self.final_output_path = os.path.join(self.output_dir, f"{job_code}.mp4")
        self.job_code = job_code
        print("加载完成 [Load complete]")

    def _get_sorted_image_paths(self) -> Optional[List[str]]:
        """
        Internal method: Retrieves and sorts the full paths of image files
        in the specified directory.
        """
        if not self.job_code:
            print("❌ 错误: 请先调用 set_job_context 设置任务代码 [Error: Call set_job_context first]")
            return None

        if not os.path.isdir(self.image_source_dir):
            print(f"❌ 错误: 指定的图片目录不存在: {self.image_source_dir} [Error: Image directory not found]")
            return None

        # 1. Get all filenames matching the extension
        filenames = [f for f in os.listdir(self.image_source_dir) if f.lower().endswith(self.image_extension.lower())]

        # 2. Sort by filename (ensuring 00001 -> 00035 order)
        sorted_filenames = sorted(filenames)

        # 3. Combine to full paths and store
        self.sorted_image_paths = [os.path.join(self.image_source_dir, f) for f in sorted_filenames]

        return self.sorted_image_paths

    def convert_to_mp4(self) -> Optional[str]:
        """
        Executes the image sequence to MP4 video conversion operation.

        Returns:
            Optional[str]: The path to the generated MP4 file, or None on failure.
        """
        print("--- 启动图片序列转 MP4 模式 [Starting image sequence to MP4 mode] ---")

        # 确保图片路径已加载
        if not self.sorted_image_paths:
            self._get_sorted_image_paths()

        if not self.sorted_image_paths:
            print("请先调用 set_job_context 并确保图片文件存在 [Call set_job_context and ensure image files exist]")
            return None

        # 1. Check the first image to determine video frame size
        first_frame = cv2.imread(self.sorted_image_paths[0])
        if first_frame is None:
            print(
                f"错误: 无法读取第一张图片 {self.sorted_image_paths[0]}，请检查路径或文件损坏 [Error: Cannot read first image]")
            return None

        height, width, _ = first_frame.shape
        frame_size = (width, height)
        fps = 0.5  # Video frame rate: 1 image per second for viewing stability

        # 2. Define video codec and VideoWriter
        # 'mp4v' is a common MP4 compatible codec
        fourcc = cv2.VideoWriter_fourcc(*'X264')
        output_path = self.final_output_path  # Use the final path set in job context

        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

            video_writer = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

            # Write the first frame
            video_writer.write(first_frame)

            # 3. Loop and write all frames
            for image_path in self.sorted_image_paths[1:]:
                frame = cv2.imread(image_path)

                if frame is None:
                    print(f"警告: 跳过无法读取的图片: {image_path} [Warning: Skipping unreadable image]")
                    continue

                # Check for consistent size, resize if necessary
                if frame.shape[:2] != (height, width):
                    frame = cv2.resize(frame, frame_size)

                video_writer.write(frame)

            # 4. Release resources
            video_writer.release()
            print(
                f"成功将 {len(self.sorted_image_paths)} 张图片转换为 MP4 视频: {output_path} [Success: Converted images to MP4]")
            self.output_files = output_path
            return output_path

        except Exception as e:
            print(f"转换过程中发生错误: {e} [Error during conversion]")
            self.output_files = ""
            return None

    def run_conversion_pipeline(self) -> str:
        """
        Executes the entire image processing pipeline:
        1. Get sorted paths -> 2. Convert to MP4 video.

        Returns:
            str: The path to the output MP4 video file.
        """
        # 1. 获取图片顺序
        self._get_sorted_image_paths()

        # 2. 转换成视频
        result_path = self.convert_to_mp4()

        # 返回输出路径，如果失败则返回空字符串或提示信息
        return result_path if result_path else self.final_output_path

def main():
    # 假设这个变量包含了您要处理的图片文件夹的名称
    jm_code = '1225249'

    # 假设所有图片的父目录是当前程序运行目录下的 'data' 文件夹
    BASE_PATH = 'data/'
    # 1. 实例化转换器
    # 传入 BASE_PATH 作为图片的根目录
    converter = ImageToVideoConverter(base_path=BASE_PATH)

    # 2. 设置任务上下文（图片子目录和输出文件名）
    # 这一步会确定输入目录 (例如 data/1225249) 和输出文件 (例如 data/1225249.mp4)
    converter.set_job_context(job_code=jm_code)

    # 3. 运行转换流程
    # run_conversion_pipeline 会自动完成：
    # a. 扫描目录，获取图片顺序
    # b. 执行 convert_to_mp4 转换
    output_video_path = converter.run_conversion_pipeline()

    if os.path.exists(output_video_path):
        print(f"\n视频文件已成功生成！")
        print(f"输出路径: {output_video_path}")
    else:
        print("\n视频文件生成失败，请检查控制台的错误信息。")

if __name__ == "__main__":
    main()
