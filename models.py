from typing import List

class Question():
    def __init__(self, id, text, options: List[str]):
        self.id = id
        self.text = text
        self.options = options
