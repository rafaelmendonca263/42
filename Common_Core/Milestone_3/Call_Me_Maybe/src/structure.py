"""Trie structure and VocabularyManager for efficient constrained decoding."""

import json


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


class VocabularyManager:
    """Gerencia e indexa o vocabulário do LLM uma única vez."""

    def __init__(self, vocab_path: str) -> None:
        self.vocab = self._load_vocab(vocab_path)
        self.char_to_tokens: dict[str, list[int]] = {}

        # ⚙️ Mapeia os caracteres iniciais uma única vez
        for token_str, token_id in self.vocab.items():
            if token_str:
                first_char = token_str[0]
                self.char_to_tokens.setdefault(first_char, []).append(token_id)

    def _load_vocab(self, path: str) -> dict[str, int]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
