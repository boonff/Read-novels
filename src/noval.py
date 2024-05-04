import os

from EdgeTTS import edge_tts_string
from cut import chapter_cut, part_cut


class Noval:
    def __init__(self, chapter_sign, part_sign, in_path, out_path):
        self.chapter_sign = chapter_sign
        self.part_sign = part_sign
        self.in_path = in_path
        self.out_path = out_path

    def run(self, position: dict):
        for file_name, roll_name in position.items():
            roll_path = os.path.join(self.out_path, roll_name)
            if not os.path.exists(roll_path):  # 创建“卷”目录
                try:
                    os.makedirs(roll_path)
                    print(f"文件夹 '{roll_path}' 创建成功。")
                except OSError as e:
                    print(f"创建文件夹 '{roll_path}' 时发生错误： {e}")
            else:
                print(f"文件夹 '{roll_path}' 已创建")
            chapters = chapter_cut(
                self.chapter_sign, os.path.join(self.in_path, file_name)
            )  # 划分章节
            parts = part_cut(self.part_sign, chapters)  # 划分“部分”

            for chapter_name, part_dir in parts.items():
                for part_name, part_value in part_dir.items():
                    edge_tts_string(
                        part_value, roll_path, f"{chapter_name}_{part_name}"
                    )
