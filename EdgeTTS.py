import os
import subprocess


class EdgeTTS:
    def __init__(self, in_path="in", out_path="out"):
        self.out_path = out_path
        self.in_path = in_path

    def read_text_file(self, file_name):
        file_path = os.path.join(self.in_path, file_name)
        print("读取文件:", file_path)
        with open(file_path, "r", encoding=str("utf-8")) as file:
            content = file.read()
        return content

    def edge_tts_file(self, file_name):
        text = self.read_text_file(file_name)
        lang = "zh-CN-XiaoyiNeural"
        rate = "+0%"
        volume = "+0%"
        gender = "Female"
        output_file = os.path.join(
            self.out_path, os.path.splitext(file_name)[0] + "_tts.wav"
        )
        write_media = os.path.join(
            self.out_path, os.path.splitext(file_name)[0] + "_tts.wav"
        )
        write_subtitles = os.path.join(
            self.out_path, os.path.splitext(file_name)[0] + "_tts.vtt"
        )
        command = [
            "edge-tts",
            "--text",
            text,
            "-v",
            lang,
            "--rate",
            rate,
            "--volume",
            volume,
            "--write-media",
            write_media,
            "--write-subtitles",
            write_subtitles,
        ]
        subprocess.run(command)

    def edge_tts_string(self, text, file_path):
        if file_path is None:
            raise ValueError("保存路径不能为空")
        text = text
        lang = "zh-CN-XiaoyiNeural"
        rate = "+0%"
        volume = "+0%"
        write_media = os.path.join(
            self.out_path, os.path.splitext(file_path)[0] + ".wav"
        )
        write_subtitles = os.path.join(
            self.out_path, os.path.splitext(file_path)[0] + ".vtt"
        )
        command = [
            "edge-tts",
            "--text",
            text,
            "-v",
            lang,
            "--rate",
            rate,
            "--volume",
            volume,
            "--write-media",
            write_media,
            "--write-subtitles",
            write_subtitles,
        ]
        subprocess.run(command)
