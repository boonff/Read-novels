def split_novel(input_file):
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()

    # 以特定的字符串作为章节分隔符，这里假设使用“第一章”作为分隔符
    chapters = content.split("第一卷")

    # 去除列表中的空白元素（第一个元素是空的，因为在第一章之前）
    chapters = [chapter.strip() for chapter in chapters[1:]]

    return chapters


if __name__ == "__main__":
    input_file_path = "in/怪人的沙拉碗0.txt"  # 替换为你的小说文件路径

    novel_chapters = split_novel(input_file_path)

    # 打印每一章的内容
    print(f"第1章:\n{novel_chapters[0]}\n")
