import os
import unicodedata
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

from EdgeTTS import edge_tts_string
from cut import chapter_cut, part_cut


class Noval:
    def __init__(self, in_path, out_path, chapter_flag=True):
        self.chapter_sign = r"^\s*(?:[上下]+[章回部节集卷话]+\s*)?[第卷话](?:\d+|[一二三四五六七八九十零〇百千两]+)[章回部节集卷话](.*)"
        self.part_sign = r"(^\s*\d{3}.*)"
        self.in_path = in_path
        self.out_path = out_path

    def get_extension(self, file_path):
        return os.path.splitext(file_path)[1]

    def get_name(self, file_path):
        return os.path.splitext(os.path.basename(file_path))[0]

    def epub_to_txt(self, epub_file):
        txt_dir = os.path.join(self.in_path, "trans")
        if not os.path.exists(txt_dir):
            os.makedirs(txt_dir)

        txt_path = os.path.join(txt_dir, self.get_name(epub_file) + ".txt")
        book = epub.read_epub(epub_file)
        with open(txt_path, "w", encoding="utf-8") as f:
            for item in book.get_items():
                if isinstance(item, ebooklib.epub.EpubHtml):
                    soup = BeautifulSoup(
                        item.get_body_content().decode("utf-8"), "html.parser"
                    )
                    soup = unicodedata.normalize("NFKC", soup.get_text())
                    f.write(soup)
        return txt_path

    def mkdir(self, roll_name):
        roll_path = os.path.join(self.out_path, roll_name)
        if not os.path.exists(roll_path):  # 创建“卷”目录
            try:
                os.makedirs(roll_path)
                print(f"文件夹 '{roll_path}' 创建成功。")
            except OSError as e:
                print(f"创建文件夹 '{roll_path}' 时发生错误： {e}")
        else:
            print(f"文件夹 '{roll_path}' 已创建")
        return roll_path

    def run(self, position: dict):
        for file_name, roll_name in position.items():
            file_path = os.path.join(self.in_path, file_name)
            roll_path = self.mkdir(roll_name)

            if self.get_extension(file_path) == ".epub":
                file_path = self.epub_to_txt(file_path)
            if self.get_extension(file_path) in (".txt", ".text"):
                chapters = chapter_cut(self.chapter_sign, file_path)  # 划分章节
                parts = part_cut(self.part_sign, chapters)  # 划分“部分”
                #
                for chapter_name, part_dic in parts.items():
                    for part_name, part_value in part_dic.items():
                        edge_tts_string(
                            part_value, roll_path, f"{chapter_name}_{part_name}"
                        )
