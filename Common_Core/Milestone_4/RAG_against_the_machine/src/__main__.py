import fire
from dataset import run_search_dataset
from generate import RAGGenerator, run_answer_dataset
from index import index_corpus
from search import search_query


class RAGCLI:
  """Interface de Linha de Comandos para o sistema RAG against the machine."""

  def index(
      self,
      max_chunk_size: int = 2000,
      raw_dir: str = "data/raw",
      processed_dir: str = "data/processed",
  ) -> None:
    """Ingere os dados da pasta raw e constrói o índice."""
    print(f"A iniciar a indexação com max_chunk_size={max_chunk_size}...")
    index_corpus(
        max_chunk_size=max_chunk_size,
        raw_dir=raw_dir,
        processed_dir=processed_dir,
    )

  def search(
      self,
      query: str,
      k: int = 5,
      processed_dir: str = "data/processed",
  ) -> None:
    """Retorna os top-k sources para uma única query[cite: 12, 17]."""
    try:
      results = search_query(query=query, k=k, processed_dir=processed_dir)
      for res in results:
        print(
            f"{res.file_path} [{res.first_character_index}:{res.last_character_index}]"
        )
    except Exception as e:
      print(f"Erro durante a pesquisa: {e}")

  def search_dataset(
      self,
      dataset_path: str,
      k: int = 5,
      save_directory: str = "data/output/search_results",
  ) -> None:
    """Executa a pesquisa sobre um dataset completo e guarda em JSON[cite: 17, 18]."""
    try:
      run_search_dataset(
          dataset_path=dataset_path, k=k, save_directory=save_directory
      )
    except Exception as e:
      print(f"Erro ao processar o dataset: {e}")

  def answer(self, query: str, k: int = 5) -> None:
    """Responde a uma única query utilizando o contexto recuperado[cite: 12, 17]."""
    try:
      sources = search_query(query=query, k=k)
      generator = RAGGenerator()
      answer_text = generator.generate_answer(query, sources)
      print(f"\nPergunta: {query}\n")
      print(f"Resposta:\n{answer_text}")
    except Exception as e:
      print(f"Erro ao gerar resposta: {e}")

  def answer_dataset(
      self,
      student_search_results_path: str,
      save_directory: str = "data/output/search_results_and_answer",
  ) -> None:
    """Gera respostas para um dataset de resultados de busca[cite: 17, 19]."""
    try:
      run_answer_dataset(
          student_search_results_path=student_search_results_path,
          save_directory=save_directory,
      )
    except Exception as e:
      print(f"Erro ao processar answer_dataset: {e}")

  def evaluate(
      self, student_search_results_path: str, dataset_path: str, k: int = 10
  ) -> None:
    """Avalia o recall@k[cite: 17, 20]."""
    print(f"A avaliar resultados de {student_search_results_path} com k={k}")


if __name__ == "__main__":
  fire.Fire(RAGCLI)
