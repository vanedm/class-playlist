import requests
import re

API_KEY = "AIzaSyCs9uUNSzB3O2cUv9dQad1-fdmjEgaoPRo"


def get_video_id(url: str) -> str:
    return url.split("v=")[1].split("&")[0]


def get_video_views(video_id: str) -> int:
    url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    view_count = int(data["items"][0]["statistics"]["viewCount"])
    return view_count


def update_readme_with_sorted_urls() -> None:
    with open("playlist.md", "r") as file:
        lines = file.readlines()

    url_lines = [
        line
        for line in lines
        if re.search(r"https://www\.youtube\.com/watch\?v=[a-zA-Z0-9_-]+", line)
    ]

    videos = [
        (
            line,
            get_video_views(
                get_video_id(
                    re.search(
                        r"https://www\.youtube\.com/watch\?v=[a-zA-Z0-9_-]+", line
                    ).group(0)
                )
            ),
        )
        for line in url_lines
    ]

    sorted_videos = sorted(videos, key=lambda x: x[1], reverse=True)

    for idx, (sorted_line, _) in enumerate(sorted_videos):
        lines[lines.index(url_lines[idx])] = sorted_line

    with open("playlist.md", "w") as file:
        file.writelines(lines)


if __name__ == "__main__":
    update_readme_with_sorted_urls()
