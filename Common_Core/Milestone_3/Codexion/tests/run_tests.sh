#!/bin/sh

# Cores para o output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Determinar o caminho absoluto do executável na raiz do projeto independentemente de onde o script é corrido
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
BIN="$ROOT_DIR/codexion"

total_tests=0
passed_tests=0
failed_tests=0

run_test() {
    name="$1"
    cmd="$2"
    expected_status="$3" # 0 para sucesso, 1 para erro esperado
    
    printf "A testar: $name\n"

    total_tests=$((total_tests + 1))
    
    # Executa o comando com timeout de 2 segundos para evitar locks/congelamentos infinitos
    if command -v timeout > /dev/null 2>&1; then
        timeout 5s sh -c "$cmd" > /dev/null 2>&1
        status=$?
        if [ $status -eq 124 ]; then
            # Timeout atingido (possível deadlock)
            printf "${RED}[TIMEOUT/FAIL]${NC} $name (simulação bloqueou)\n"
            failed_tests=$((failed_tests + 1))
            return
        fi
    else
        eval "$cmd" > /dev/null 2>&1
        status=$?
    fi
    
    if [ "$expected_status" -eq 0 ]; then
        if [ $status -eq 0 ]; then
            passed_tests=$((passed_tests + 1))
        else
            printf "${RED}[FAIL]${NC} $name (esperava sucesso, obteve código $status)\n"
            failed_tests=$((failed_tests + 1))
        fi
    else
        if [ $status -ne 0 ]; then
            passed_tests=$((passed_tests + 1))
        else
            printf "${RED}[FAIL]${NC} $name (esperava erro, mas passou com código 0)\n"
            failed_tests=$((failed_tests + 1))
        fi
    fi
}

echo "=================================================="
echo "=== FASE 1: TESTES DE EDGE CASES E ERROS (PARSING) ==="
echo "=================================================="

# Testes de argumentos em falta ou excesso
run_test "0 argumentos" "$BIN" 1
run_test "7 argumentos (em falta 1)" "$BIN 1 800 200 200 200 1 50" 1
run_test "9 argumentos (em excesso 1)" "$BIN 1 800 200 200 200 1 50 fifo extra" 1

# Testes de valores inválidos para number_of_coders
for val in 0 -1 abc "" " 1" "1 "; do
    run_test "Coder inválido: '$val'" "$BIN '$val' 800 200 200 200 1 50 fifo" 1
done

# Testes de valores inválidos para time_to_burnout
for val in 0 -500 xyz ""; do
    run_test "Burnout inválido: '$val'" "$BIN 2 '$val' 200 200 200 1 50 fifo" 1
done

# Testes de valores inválidos para tempos de ação
for val in 0 -10 abc; do
    run_test "Compile inválido: '$val'" "$BIN 2 800 '$val' 200 200 1 50 fifo" 1
    run_test "Debug inválido: '$val'" "$BIN 2 800 200 '$val' 200 1 50 fifo" 1
    run_test "Refactor inválido: '$val'" "$BIN 2 800 200 200 '$val' 1 50 fifo" 1
done

# Testes de required compiles
for val in 0 -2 abc; do
    run_test "Compiles required inválido: '$val'" "$BIN 2 800 200 200 200 '$val' 50 fifo" 1
done

# Testes de cooldown (cooldown pode ser 0, mas não negativo ou string inválida)
for val in -1 abc; do
    run_test "Cooldown inválido: '$val'" "$BIN 2 800 200 200 200 1 '$val' fifo" 1
done

# Testes de scheduler inválido
for val in random rr sstf FIFO EDF ""; do
    run_test "Scheduler inválido: '$val'" "$BIN 2 800 200 200 200 1 50 '$val'" 1
done


echo ""
echo "=================================================="
echo "=== FASE 2: MATRIZ DE >1000 TESTES DE SIMULAÇÃO ==="
echo "=================================================="
echo "A gerar e executar mais de 1000 combinações de testes..."

for coders in 1 2 3 4 5; do
    for burnout in 400 800 1500; do
        for compile in 50 100 200; do
            for debug in 50 100; do
                for refactor in 50 100; do
                    for req in 1 2 3; do
                        for cooldown in 0 10; do
                            for sched in fifo edf; do
                                run_test "Simul(C=$coders,B=$burnout,Cp=$compile,D=$debug,R=$refactor,Req=$req,Cd=$cooldown,$sched)" \
                                "$BIN $coders $burnout $compile $debug $refactor $req $cooldown $sched" 0
                            done
                        done
                    done
                done
            done
        done
    done
done

echo ""
echo "=================================================="
echo "=== RESUMO DOS TESTES ==="
echo "Total de testes executados: $total_tests"
printf "${GREEN}Passaram:${NC} $passed_tests\n"
if [ $failed_tests -gt 0 ]; then
    printf "${RED}Falharam:${NC} $failed_tests\n"
    exit 1
else
    printf "${GREEN}Todos os testes passaram com sucesso!${NC}\n"
    exit 0
fi
