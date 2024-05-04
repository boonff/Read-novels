from noval import Noval

if __name__ == "__main__":
    chapter_sign = r"^\s*(?:[上下]+[章回部节集卷话]+\s*)?[第卷话](?:\d+|[一二三四五六七八九十零〇百千两]+)[章回部节集卷话](.*)"
    part_sign = r"(^\s*\d{3}.*)"
    roll_position = {
        "怪人的沙拉碗3.txt": "第四卷",
    }

    novel = Noval(
        chapter_sign,
        part_sign,
        in_path="docs/in/怪人的沙拉碗",
        out_path="docs/out/怪人的沙拉碗",
    )
    novel.run(roll_position)
