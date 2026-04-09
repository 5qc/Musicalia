from ._headers import headers

import re
import requests

class wikipedia:
    def __init__(self, page: str):
        self.text = requests.get(f"https://en.wikipedia.org/w/api.php?action=parse&page={page}&prop=text&formatversion=2&format=json", headers=headers).json()["parse"]["text"]
        self.page = page
        self.image = re.search(r'<img.*?src="(.*?)"', self.text)
        self.lead = re.sub(r"<a.*?>(.*?)<\/a>", r"\1", self.text.split("<p>")[1])