import json
import re


def main(pathtofile):
    with open(pathtofile, "r") as metadata:
        data = metadata.read().splitlines()

    output = {}
    pointer = 0
    while pointer <= len(data) - 1:
        current_line = data[pointer]
        if "[youtube] Extracting URL:" in current_line:
            video_name = ""
            counter = 0
            for i in range(pointer, len(data)):
                info_line = data[i]
                if "[download] Destination:" in info_line:
                    video_name = data[i]
                    break
                counter += 1
            pointer = pointer + counter
            if video_name:
                video_name = video_name.split("\\")[-1]
                # You might need this code below depending on the structure
                # of the video names
                #
                # results = [
                #     (m.start(0), m.end(0))
                #     for m in re.finditer(r"\[(.*?)\]", video_name)
                # ]
                # if not results:
                #     continue
                # idxs = results[-2] if len(results) >1 else results[-1]
                # start = "Destination:"
                # idx1 = video_name.index(start)
                # idx2 = idxs[0]
                # res = ""
                # for idx in range(idx1 + len(start) + 1, idx2):
                #     res = res + video_name[idx]
                output[video_name.strip()] = current_line.split("URL:")[-1].strip()
        else:
            pointer += 1

    return output


if __name__ == "__main__":
    pathtofile = "data/TheoreticalBullshit_metadata.txt"
    titles_path = "data/TheoreticalBullshit_titles.json"
    results = main(pathtofile=pathtofile)
    with open(titles_path, "w") as f:
        json.dump(results, f)
