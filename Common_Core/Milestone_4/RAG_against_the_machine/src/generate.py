import json
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from models import MinimalAnswer, StudentSearchResultsAndAnswer, MinimalSource
from search import search_query

MODEL_NAME = "Qwen/Qwen3-0.6B"


class RAGGenerator:
    """Classe responsável por carregar o modelo Qwen e gerar respostas baseadas no contexto."""

    def __init__(self, model_name: str = MODEL_NAME) -> None:
        self.model_name = model_name
        self.tokenizer = None
        self.model = None

    def _load_model(self) -> None:
        if self.model is None:
            print(f"A carregar o modelo {self.model_name}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            is_cuda = torch.cuda.is_available()
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if is_cuda else torch.float32,
                device_map="auto" if is_cuda else None,
            )
            if not is_cuda:
                self.model = self.model.to("cpu")

    def generate_answer(
        self, question: str, sources: list[MinimalSource], max_new_tokens: int = 512
    ) -> str:
        """Gera uma resposta em linguagem natural com base nos chunks recuperados."""
        self._load_model()

        context_parts = []
        for src in sources:
            try:
                file_text = Path(src.file_path).read_text(encoding="utf-8", errors="ignore")
                snippet = file_text[src.first_character_index : src.last_character_index]
                context_parts.append(f"Source ({src.file_path}):\n{snippet}")
            except Exception:
                continue

        context = "\n\n".join(context_parts)

        prompt = (
            "You are a helpful coding assistant. Answer the user's question accurately "
            "based strictly on the provided context below. If the answer cannot be found in the context, "
            "say so clearly.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            "Answer:"
        )

        inputs = self.tokenizer(prompt, return_tensors="pt")
        device = next(self.model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.2,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        input_len = inputs["input_ids"].shape[1]
        generated_tokens = outputs[0][input_len:]
        answer = self.tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
        return answer


def run_answer_dataset(
    student_search_results_path: str,
    save_directory: str = "data/output/search_results_and_answer",
) -> None:
    """Gera respostas para um dataset completo de resultados de busca."""
    path = Path(student_search_results_path)
    if not path.exists():
        raise FileNotFoundError(f"Ficheiro de resultados não encontrado em {student_search_results_path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    search_results = data.get("search_results", [])
    k = data.get("k", 5)

    generator = RAGGenerator()
    minimal_answers = []

    print(f"A gerar respostas para {len(search_results)} perguntas...")
    for item in search_results:
        q_id = item.get("question_id")
        q_text = item.get("question")
        raw_sources = item.get("retrieved_sources", [])

        sources = [MinimalSource(**src) for src in raw_sources]
        answer_text = generator.generate_answer(q_text, sources)

        minimal_answers.append(
            MinimalAnswer(
                question_id=q_id,
                question=q_text,
                retrieved_sources=sources,
                answer=answer_text,
            )
        )

    student_answer_results = StudentSearchResultsAndAnswer(
        search_results=minimal_answers, k=k
    )

    save_dir = Path(save_directory)
    save_dir.mkdir(parents=True, exist_ok=True)
    out_file = save_dir / path.name

    out_file.write_text(
        json.dumps(student_answer_results.model_dump(), indent=2), encoding="utf-8"
    )
    print(f"Saved student_search_results_and_answer to {out_file}")
