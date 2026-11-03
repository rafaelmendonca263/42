import json
from pathlib import Path
from models import MinimalSearchResults, StudentSearchResults
from search import search_query


def run_search_dataset(
    dataset_path: str,
    k: int = 5,
    save_directory: str = "data/output/search_results",
    processed_dir: str = "data/processed",
) -> None:
  """Lê um dataset de perguntas, executa a busca para cada uma e guarda o resultado em JSON."""
  path = Path(dataset_path)
  if not path.exists():
    raise FileNotFoundError(f"Dataset não encontrado em {dataset_path}")

  data = json.loads(path.read_text(encoding="utf-8"))

  questions = []
  if isinstance(data, dict) and "rag_questions" in data:
    questions = data["rag_questions"]
  elif isinstance(data, list):
    questions = data

  search_results_list = []

  print(
      f"A processar {len(questions)} perguntas do dataset com k={k}..."
  )
  for q in questions:
    q_id = q.get("question_id")
    q_text = q.get("question")

    if not q_text:
      continue

    retrieved_sources = search_query(
        query=q_text, k=k, processed_dir=processed_dir
    )

    search_results_list.append(
        MinimalSearchResults(
            question_id=q_id, question=q_text, retrieved_sources=retrieved_sources
        )
    )

  student_results = StudentSearchResults(
      search_results=search_results_list, k=k
  )

  save_dir = Path(save_directory)
  save_dir.mkdir(parents=True, exist_ok=True)
  out_file = save_dir / path.name

  out_file.write_text(
      json.dumps(student_results.model_dump(), indent=2), encoding="utf-8"
  )
  print(f"Saved student_search_results to {out_file}[cite: 18]")
