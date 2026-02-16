"""
# Caso de Teste 03 - Sistema de Assinaturas

Sistema de controle de assinaturas

## Regras de Negócio

- RN01: Uma assinatura pode estar Ativa, Suspensa ou Cancelada;
- RN02: Assinaturas canceladas não podem ser reativadas;
- RN03: Suspensão ocorre automaticamente após 3 falhas de pagamento consecutivas;
- RN04: Pagamento bem-sucedido zera o contador de falhas;
- RN05: Cobranças não podem ser retroativas.

## Requisitos Funcionais

- RF01: O sistema deve registrar pagamentos;
- RF02: o sistema deve atualizar status da assinatura, a partir do sucesso ou falha no pagamento;
- RF03: O sistema deve controlar falhas consecutivas;
- RF04: Impedir transições inválidas de estado;
- RF05: O sistema deve lançar uma exceção em caso de uma falha.

## Diagrama de Classes UML

[Class] Pagamento
+ sucesso: bool

[Class] Assinatura
+ status: "ATIVA" | "SUSPENSA" | "CANCELADA"
+ falhas_pagamento: int
+ registrar_pagamento(pagamento: Paramento): Decimal

## Erros Mapeados

- E01: Contagem incorreta de falhas;
- E02: Pagamento retroativo;
- E03: Não resetar contador;
- E04: Transições inválidas de estado.
"""

class Payment:
    def __init__(self, success: bool):
        self.success: bool = success

class Subscription:
    def __init__(self, status: str = "ACTIVE", payment_failures: int = 0):
        self.status: str = status
        self.payment_failures: int = payment_failures

    def record_payment(self, payment: Payment) -> None:
        # Aceita pagamento retroativo
        if payment.success:
            # Não zera falhas
            self.status = "ACTIVE"
        else:
            self.payment_failures += 1

        # Suspende com 2 falhas (deveria ser 3)
        if self.payment_failures >= 2:
            self.status = "SUSPENDED"

    def cancel(self):
        self.status = "CANCELLED"

    def reactivate(self):
        # Permite reativar assinatura cancelada
        self.status = "ACTIVE"
