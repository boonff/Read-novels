import os
import sys
import subprocess as sp

from kaa import Kaa


def edge_tts_string(text, out_path, file_name):
    lang = "zh-CN-XiaoyiNeural"
    rate = "+0%"
    volume = "+0%"
    media = os.path.join(out_path, file_name + ".mp3")
    subtitles_vtt = os.path.join(out_path, file_name + ".vtt")
    subtitles_ass = os.path.join(out_path, file_name + ".ass")
    command = [
        "edge-tts",
        "-f",
        "tts.txt",
        "-v",
        lang,
        "--rate",
        rate,
        "--volume",
        volume,
        "--write-media",
        media,
        "--write-subtitles",
        subtitles_vtt,
    ]

    if os.path.isfile(subtitles_ass):
        print(subtitles_ass + "已存在")
        return
    with open("tts.txt", "w", encoding="utf-8") as file:  # 暂存字符串到tts.txt
        file.write(text)

    print(f"运行指令：{command}")
    p = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE)
    print(p.poll())
    p.wait()
    try:
        os.remove("tts.txt")
    except OSError as e:
        print(f"发生错误：{e}")

    # vtt转换ass
    kaa = Kaa(subtitles_vtt, subtitles_ass)
    kaa.main()
    try:
        os.remove(subtitles_vtt)
    except OSError as e:
        print(f"发生错误：{e}")
