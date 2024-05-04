import re


# 按照sign划分章节
def chapter_cut(sign, file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    # 抛弃标题前的所有内容，如果不抛弃，注意列表merged_chapters发生out of runge错误
    chapters = re.split(sign, content, flags=re.MULTILINE)[1:]
    merged_chapters = {}

    if len(chapters) != 0:  # 合并标题和正文
        for i in range(0, len(chapters), 2):
            merged_chapters[f"[{i // 2 + 1}]{chapters[i].strip()}"] = chapters[i + 1]

    else:
        merged_chapters["[0]"] = content

        # 打印划分后的大致信息
        print("-" * 50 + "划分章节" + "-" * 50)
        for i, (key, value) in enumerate(merged_chapters.items()):
            print(f"[{i+1}]{key}")
            print(value[:50])

    return merged_chapters


# 按照sign划分“部分”
def part_cut(sign, chapters: dict):
    parts = {}
    for chapter_name, chapter_value in chapters.items():
        part = re.split(sign, chapter_value, flags=re.MULTILINE)
        m_parts = {}
        if not part[0]:  # 抛弃sign前的空字符串
            part = part[1:]
            part[1] = chapter_name + "。" + part[1]
        else:  # 文章中的第一“部分”可能没有sign，将其添加到part字典(这里没有debug过，可能有bug)
            m_parts[""] = (
                chapter_name + "。" + part[0] + "。"
            )  # 注意与上面不同，这里需要将标题添加至字典
            part = part[1:]
        # 合并标题和正文

        for i in range(0, len(part), 2):
            key = part[i].strip()
            val = part[i + 1]
            m_parts[key] = key + ":" + val
        parts[chapter_name] = m_parts
    # 打印“部分”信息太麻烦，不做了，debug看吧
    return parts
