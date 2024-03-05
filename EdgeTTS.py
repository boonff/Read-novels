import os
import subprocess as sp


def edge_tts_string(text, out_path, file_name):
    if os.path.isfile(os.path.join(out_path, file_name + ".vtt")):
        print(os.path.join(out_path, file_name + ".vtt") + "已存在")
        return
    with open("tts.txt", "w", encoding="utf-8") as file:  # 暂存字符串到tts.txt
        file.write(text)
    lang = "zh-CN-XiaoyiNeural"
    rate = "+0%"
    volume = "+0%"
    write_media = os.path.join(out_path, file_name + ".mp3")
    write_subtitles = os.path.join(out_path, file_name + ".vtt")
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
        write_media,
        "--write-subtitles",
        write_subtitles,
    ]
    print(f"运行指令：{command}")
    p = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE)
    print(p.poll())
    p.wait()
    try:
        os.remove("tts.txt")
    except OSError as e:
        print(f"发生错误：{e}")
