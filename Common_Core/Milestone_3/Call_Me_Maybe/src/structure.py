"""Trie structure for efficient prefix-based function selection."""

class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_end_of_word: bool = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insere uma palavra na Trie."""
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True

    def search_prefix(self, prefix: str) -> TrieNode | None:
        """Busca o nó correspondente ao prefixo informado."""
        current = self.root
        for char in prefix:
            if char not in current.children:
                return None
            current = current.children[char]
        return current
