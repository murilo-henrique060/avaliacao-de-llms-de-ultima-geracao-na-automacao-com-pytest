"""
# Caso de Teste 04 - Sistema de Aprovação de Crédito Bancário.

Sistema de aprovação de crédito pessoal

## Regras de Negócio

- RN01: Crédito só pode ser aprovado se:
    * Score ≥ 700
    * Renda ≥ R$ 5.000
    * Idade ≥ 21
- RN02: Se qualquer critério falhar, o crédito é negado;
- RN03: Não são permitidos valores mágicos (NaN e Infinity), caso encontrados, o sistema deve lançar uma exceção;
- RN04: Os critérios devem ser validados seguindo as seguintes regras:
    * Score: valor inteiro positivo
    * Renda: valor decimal positivo
    * Idade: valor inteiro positivo
- RN05: Valores não devem ser normalizados (4999.9999 != 5000)
- RN06: Se qualquer validação falhar, o sistema deve lançar uma exceção;
- RN07: O sistema não deve fazer adivinhações sobre valores não fornecidos;
- RN08: Não há níveis intermediários de aprovação;
- RN09: A análise deve ser uma operação indivisível, ou seja:
    * Não pode ser dividida em etapas observáveis
    * Não pode retornar resultados parciais
    * Não pode expor logs de decisão ao consumidor da API

## Requisitos Funcionais

- RF01: Avaliar proposta de crédito utilizando exclusivamente os valores fornecidos de score, renda e idade, sem inferir, normalizar ou enriquecer dados;
- RF02: Validar obrigatoriamente todos os critérios definidos nas regras de negócio antes de retornar qualquer resultado;
- RF03: Retornar exclusivamente um dos seguintes resultados: Aprovado ou Negado, quando todas as validações forem bem-sucedidas;
- RF04: Registrar exatamente um resultado da análise apenas quando uma decisão válida (Aprovado ou Negado) for produzida;
- RF05: Lançar uma exceção sempre que ocorrer qualquer falha de validação, tipo inválido, valor ausente, valor mágico (NaN ou Infinity) ou violação de regra de negócio;
- RF06: Não retornar qualquer resultado de negócio quando uma exceção for lançada;
- RF07: Não expor estados intermediários, resultados parciais ou mensagens de progresso durante ou após a análise;
- RF08: Não realizar qualquer tipo de normalização, arredondamento ou ajuste automático nos valores de entrada.

## Diagrama de Classes UML

[Class] CreditoService
+ avaliar(score: int, salario: decimal, idade: int): "APROVADO" | "NEGADO"

## Erros Mapeados

- E01: Estado intermediário proibido;
- E02: Inferência implícita de valores ausentes;
- E03: Normalização silenciosa;
- E04: Uso de tipos flexíveis;
- E05: Erro técnico retornando decisão de negócio;
- E06: Dependência temporal proibida;
- E07: Ordem de validação influencia resultado;
- E08: Compensação indevida entre critérios;
- E09: Conversão de unidade implícita;
- E10: Falha parcial ignorada;
- E11: Ausência de validação completa obrigatória;
- E12: Enriquecimento de dados externo proibido.
"""

from datetime import datetime
from decimal import Decimal

class CreditService:
    @staticmethod
    def evaluate(score: int, income: Decimal, age: int):
        # Inferência implícita de valores ausentes
        if score is None:
            score = 0

        # Normalização silenciosa
        score = round(score)

        # Uso de tipos flexíveis
        try:
            score = int(score)
            income = float(income)
            age = int(age)
        except Exception:
            # Erro técnico retornando decisão de negócio
            return "DENIED"

        # Dependência temporal proibida
        current_hour = datetime.now().hour
        if current_hour < 6:
            return "UNDER_REVIEW" # Estado Intermediário Proibido

        # ❌ Ordem de validação influencia resultado
        if score < 700:
            return "DENIED"

        # Enriquecimento de dados externo proibido
        print("Partial evaluation: APPROVED")

        # Compensação indevida entre critérios
        if income < 5000 and score > 800:
            income = 5000

        # Conversão de unidade implícita
        if income < 100:
            income = income * 1000  # assume renda em milhares

        # Falha parcial ignorada
        if age < 21:
            pass  # deveria negar

        # Ausência de validação completa obrigatória
        if score >= 700 and income >= 5000:
            result = "APPROVED"
        else:
            result = "DENIED"

        return result
