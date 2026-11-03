import pickle
from pathlib import Path
from rank_bm25 import BM25Okapi
from tqdm import tqdm
from models import MinimalSource


class Chunker:
    """Classe responsável por dividir ficheiros em chunks respeitando o limite máximo."""

    def __init__(self, max_chunk_size: int = 2000) -> None:
        self.max_chunk_size = max_chunk_size

    def chunk(self, content: str, file_path: str) -> list[MinimalSource]:
        chunks = []
        current_chunk = ""
        start_index = 0
        current_index = 0

        for line in content.splitlines(keepends=True):
            if len(current_chunk) + len(line) > self.max_chunk_size:
                chunks.append(
                    MinimalSource(
                        file_path=file_path,
                        first_character_index=start_index,
                        last_character_index=current_index,
                    )
                )
                start_index = current_index
                current_chunk = line
            else:
                current_chunk += line
            current_index += len(line)

        if current_chunk:
            chunks.append(
                MinimalSource(
                    file_path=file_path,
                    first_character_index=start_index,
                    last_character_index=current_index,
                )
            )

        return chunks

    def markdown(self, content: str, file_path: str) -> list[MinimalSource]:
        return self.chunk(content, file_path)


def save_index(sources: list[MinimalSource], bm25_index: BM25Okapi, output_dir: str = "data/processed") -> None:
    """Persiste os metadados das fontes e o índice BM25 em disco."""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    with open(out_path / "sources.pkl", "wb") as f:
        pickle.dump(sources, f)
    with open(out_path / "bm25.pkl", "wb") as f:
        pickle.dump(bm25_index, f)


def index_corpus(max_chunk_size: int = 2000, raw_dir: str = "data/raw", processed_dir: str = "data/processed") -> None:
    """Percorre a pasta raw, aplica o chunking, constrói o BM25 e guarda o índice."""
    raw_path = Path(raw_dir)
    chunker = Chunker(max_chunk_size=max_chunk_size)
    all_sources: list[MinimalSource] = []

    files = [f for f in raw_path.rglob("*") if f.is_file()]

    for file_path in tqdm(files, desc="Chunking"):
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            str_path = str(file_path)

            if file_path.suffix == ".py":
                chunks = chunker.chunk(content, str_path)
            elif file_path.suffix == ".md":
                chunks = chunker.markdown(content, str_path)
            else:
                continue

            all_sources.extend(chunks)
        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}")

    corpus_tokens = []
    for source in tqdm(all_sources, desc="Tokenizing"):
        try:
            file_text = Path(source.file_path).read_text(encoding="utf-8", errors="ignore")
            chunk_text = file_text[source.first_character_index : source.last_character_index]
            tokens = chunk_text.lower().split()
            corpus_tokens.append(tokens)
        except Exception as e:
            corpus_tokens.append([])

    bm25 = BM25Okapi(corpus_tokens)

    save_index(all_sources, bm25, processed_dir)
    print(f"Ingestion complete! Indexed {len(all_sources)} chunks under {processed_dir}/")
