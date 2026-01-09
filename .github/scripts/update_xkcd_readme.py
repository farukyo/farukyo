import requests
import re

README_PATH = "README.md"
XKCD_JSON_URL = "https://xkcd.com/info.0.json"

# Fetch latest XKCD comic metadata
resp = requests.get(XKCD_JSON_URL)
data = resp.json()
img_url = data["img"]
title = data["safe_title"]
comic_num = data["num"]
comic_url = f"https://xkcd.com/{comic_num}/"

# Prepare new XKCD section
new_xkcd_md = f"![Daily XKCD - {title}]({img_url})\n<br/>\n[{title} - XKCD #{comic_num}]({comic_url})\n"

# Read README
with open(README_PATH, "r", encoding="utf-8") as f:
    readme = f.read()

# Replace XKCD section (between special comments)
pattern = r"<!-- XKCD-START -->(.*?)<!-- XKCD-END -->"
replacement = f"<!-- XKCD-START -->\n{new_xkcd_md}<!-- XKCD-END -->"

if re.search(pattern, readme, flags=re.DOTALL):
    new_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
else:
    # Insert after the tip block if not present
    tip_block = re.search(r"(> [^\n]+\n> [^\n]+\n)", readme)
    if tip_block:
        idx = tip_block.end()
        new_readme = readme[:idx] + "\n" + replacement + "\n" + readme[idx:]
    else:
        new_readme = replacement + "\n" + readme

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_readme)
