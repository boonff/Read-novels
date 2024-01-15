import os

from EdgeTTS import EdgeTTS
from Section import Section


class Novel:
    def __init__(self, sign, in_path="in", out_path="out"):
        self.in_path = in_path
        self.out_path = out_path
        self.edge_tts = EdgeTTS(in_path, out_path)
        self.section = Section(sign)

    def run(self, file_name, chapter_name):
        sections = self.section.split_novel(os.path.join(self.in_path, file_name))
        os.makedirs(os.path.join(self.out_path, chapter_name))
        for i, section in enumerate(sections):
            self.edge_tts.edge_tts_string(
                section,
                os.path.join(
                    chapter_name,
                    "第" + str(i) + "节",
                ),
            )
