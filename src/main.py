from noval import Noval

if __name__ == "__main__":

    novel = Noval(in_path="docs/in/物语epub", out_path="docs/out/")

    roll_position = {
        "[物语系列][05卷]伪物语（下）.epub": "伪物语下",
    }

    novel.run(roll_position)
