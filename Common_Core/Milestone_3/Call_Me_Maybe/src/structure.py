from typing import cast
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

        # ⚙️ Mapeia os caracteres limpando espaços ou prefixos dos tokens
        for token_str, token_id in self.vocab.items():
            if token_str:
                clean_str = token_str.strip()
                for char in clean_str:
                    self.char_to_tokens.setdefault(char, []).append(token_id)

    def _load_vocab(self, path: str) -> dict[str, int]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cast(dict[str, int], data)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
