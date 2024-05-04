import re
import os
import sys, getopt
import pysubs2


class Kaa:
    def __init__(self, sub_path_vtt="", sub_path_ass=""):
        self.sub_path_vtt = sub_path_vtt
        self.sub_path_ass = sub_path_ass
        self.tmp_sub_path_ass = os.path.join(
            os.path.dirname(sub_path_ass), "tmp_" + os.path.basename(sub_path_ass)
        )

        # --ReGex patterns--
        self.re_subLineVtt = re.compile(
            r"\d\d:\d\d:\d\d\.\d\d\d --> \d\d:\d\d:\d\d\.\d\d\d"
        )
        self.re_subLineAss = re.compile(r"\d,\d:\d\d:\d\d\.\d\d,\d:\d\d:\d\d\.\d\d")

    def main(self):
        pys2_subs = pysubs2.load(self.sub_path_vtt)
        pys2_subs.save(self.tmp_sub_path_ass)
        linesVtt = self.readSubFile(self.sub_path_vtt)
        tmp_linesAss = self.readSubFile(self.tmp_sub_path_ass)
        slVtt = self.getSubLines(linesVtt, self.re_subLineVtt)
        slAss = self.getSubLines(tmp_linesAss, self.re_subLineAss)
        subLines = self.mergeSubLines(slVtt, slAss)
        fixed_linesAss = self.fixMarginTop(subLines, linesVtt, tmp_linesAss)
        fixed_linesAss = self.fixWeirdChars(subLines, linesVtt, fixed_linesAss)
        self.writeSubFile(self.sub_path_ass, "".join(fixed_linesAss))
        os.remove(self.tmp_sub_path_ass)
        print(f"Sub converted: {self.sub_path_ass}")

    def mergeSubLines(self, slVtt, slAss):
        if len(slVtt) == len(slAss):
            subLines = []
            for i in range(len(slVtt)):
                subLines.append(
                    {
                        "vtt": slVtt[i],
                        "ass": slAss[i],
                    }
                )
        return subLines

    def fixMarginTop(self, subLines, linesVtt, linesAss):
        max_margin_top_ass = 285
        for sl in subLines:
            lPercent = re.search(r"line:\d+%", linesVtt[sl["vtt"]])
            if lPercent:
                percentMatch = re.search(r"\d+", lPercent.group())
                margin_top_vttPercent = int(percentMatch.group())
                margin_top_ass = int(
                    round(max_margin_top_ass * (margin_top_vttPercent / 100))
                )
                tmp = re.sub(
                    r"0,0,0,,", rf"0,0,{margin_top_ass},,{{\\a6}}", linesAss[sl["ass"]]
                )
                linesAss[sl["ass"]] = tmp
        return linesAss

    def fixWeirdChars(self, subLines, linesVtt, linesAss):
        # replace "&amp;" with "&"
        for sl in subLines:
            tmp = re.sub("&amp;", "&", linesAss[sl["ass"]])
            if tmp != linesAss[sl["ass"]]:
                linesAss[sl["ass"]] = tmp
        return linesAss

    def fixSubBeforeSub(self, subLines, linesVtt, linesAss):
        # fixes a when a sub is not finished and the other
        # come right before the first one finishes,
        # causing one to shift up by a little.
        # (this issue is caused by ffmpeg when converting)
        pass

    def getSubLines(self, lines, reComp):
        indexList = []
        for i, line in enumerate(lines):
            if reComp.findall(line):
                indexList.append(i)
        return indexList

    def readSubFile(self, subPath):
        with open(subPath) as subFile:
            lines = subFile.readlines()
        return lines

    def writeSubFile(self, subPath, lines):
        with open(subPath, "w") as subFile:
            subFile.write(lines)
