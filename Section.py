class Section:
    def __init__(self, sign):
        self.sign = sign
        self.split_novel

    def split_novel(self, file_path):  # 按照sign将文件分段保存到列表
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        sections = content.split(self.sign)
        sections = [
            section.strip() for section in sections[1:]
        ]  # 去除列表中的空白元素（第一个元素是空的，因为在第一章之前）

        return sections
