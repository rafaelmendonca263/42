import argparse
from src.parser import load_test_inputs, load_function_definitions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--functions", required=True)
    parser.add_argument("--tests", required=True)
    args = parser.parse_args()

    functions = load_function_definitions(args.functions)
    tests = load_test_inputs(args.tests)

    for test in tests:
        # 1. Enviar o prompt e as ferramentas para o modelo
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": test.prompt}],
            tools=functions,
        )

        # 2. Obter o nome da função que o modelo chamou
        called_function_name = response.choices[0].message.tool_calls[0].function.name

        # 3. Comparar com o esperado pelo teste
        if called_function_name == test.expected_function:
            print(f"✅ Teste passou para: {test.prompt}")
        else:
            print(f"❌ Teste falhou. Esperado: {test.expected_function}, Chamado: {called_function_name}")


if __name__ == "__main__":
    main()
