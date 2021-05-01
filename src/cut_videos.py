# cut videos into 5:00
# open it in src
import os
from tqdm import tqdm
total = 40
def fin_name(x): return "../Records/test{}.mp4".format(x)
def fout_name(x): return "../EditedVideo/test{}.mp4".format(x)


def cmd_line(
    x): return "ffmpeg -ss 00:00:00 -t 00:05:00 -i {0} -vcodec copy -acodec copy {1}".format(fin_name(x), fout_name(x))


if __name__ == "__main__":
    for i in tqdm(range(1, total + 1)):
        os.system(cmd_line(i))
