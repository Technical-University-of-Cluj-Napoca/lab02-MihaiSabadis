# BST.py
import urllib.request

class Node:
    def __init__(self, word: str):
        self.word = word
        self.left = None
        self.right = None


class BST:
    def __init__(self, source: str, **kwargs):
        from_url = kwargs.get("url", False)
        from_file = kwargs.get("file", False)
        if from_url and from_file:
            raise ValueError("Choose either url=True or file=True, not both.")

        words = self._load_from_url(source) if from_url else self._load_from_file(source)
        self.root = self._build_balanced(words, 0, len(words) - 1)

    def _load_from_file(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
        words.sort()
        return words

    def _load_from_url(self, url: str):
        with urllib.request.urlopen(url) as resp:
            data = resp.read().decode("utf-8")
        words = [line.strip() for line in data.splitlines() if line.strip()]
        words.sort()
        return words

    def _build_balanced(self, words, left, right):
        if left > right:
            return None
        mid = (left + right) // 2
        node = Node(words[mid])
        node.left = self._build_balanced(words, left, mid - 1)
        node.right = self._build_balanced(words, mid + 1, right)
        return node

    def autocomplete(self, prefix: str):
        results = []
        self._collect(self.root, prefix, results)
        return results

    def _collect(self, node: Node, prefix: str, results: list):
        if node is None:
            return
        self._collect(node.left, prefix, results)
        if node.word.startswith(prefix):
            results.append(node.word)
        self._collect(node.right, prefix, results)
