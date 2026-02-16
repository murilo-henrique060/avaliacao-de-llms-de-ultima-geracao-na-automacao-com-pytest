"""
# Caso de Teste 05 - Sistema de Reserva Aérea.

Sistema de reserva de passagens aéreas

## Regras de Negócio

- RN01: Uma reserva só pode ser confirmada se existir exatamente um pagamento aprovado associado a ela;
- RN02: Pagamentos com status diferente de aprovado não confirmam reservas;
- RN03: A confirmação da reserva e a aprovação do pagamento devem ocorrer de forma atômica, não podendo existir estado observável onde apenas um dos dois esteja efetivado;
- RN04: Um assento pode pertencer a no máximo uma reserva ativa por voo;
- RN05: Reservas canceladas liberam imediatamente o assento associado;
- RN06: Overbooking não é permitido sob nenhuma circunstância;
- RN07: A quantidade de reservas confirmadas de um voo nunca pode exceder a quantidade total de assentos disponíveis;
- RN08: Uma reserva pode estar exclusivamente em um dos seguintes estados:
    * CRIADA
    * CONFIRMADA
    * CANCELADA
- RN09: Estados intermediários ou adicionais (ex.: “Em pagamento”, “Pendente”, “Expirada”) não são permitidos;
- RN10: As transições de estado válidas são exclusivamente:
    * CRIADA → CONFIRMADA
    * CONFIRMADA → CANCELADA
- RN11: Qualquer transição de estado diferente das definidas deve ser rejeitada;
- RN12: Uma reserva cancelada não pode ser reativada, alterada ou receber novos pagamentos;
- RN13: O cancelamento de uma reserva deve obedecer estritamente à política temporal:
    * Cancelamentos com tempo restante ≥ 24 horas antes do voo → reembolso total;
    * Cancelamentos com tempo restante < 24 horas antes do voo → sem reembolso;
- RN14: O cálculo do tempo restante até o voo deve ser feito em horas exatas, sem qualquer tipo de arredondamento ou tolerância;
- RN15: O sistema deve utilizar exclusivamente a data e hora do voo armazenadas internamente como referência temporal;
- RN16: Datas, horários e identificadores do voo não podem ser alterados após a confirmação da reserva;
- RN17: Alterações indiretas de dados do voo (por troca de referência, clonagem ou recriação de objeto) são proibidas;
- RN18: Cada reserva pode possuir exatamente um pagamento associado;
- RN19: Tentativas adicionais de pagamento para uma mesma reserva devem ser rejeitadas;
- RN20: Não é permitido efetuar pagamento para reservas canceladas ou após a data do voo;
- RN21: As operações do sistema devem ser determinísticas, produzindo sempre o mesmo resultado para a mesma sequência de entradas;
- RN22: O sistema não deve assumir comportamentos implícitos não especificados (ex.: crédito futuro, remarcação automática, exceções comerciais);
- RN23: Qualquer violação de regra de negócio deve resultar em falha imediata, sem alteração de estado ou criação de registros parciais;
- RN24: Cada operação válida deve gerar exatamente um registro imutável;
- RN25: Operações que falham não devem gerar registros persistentes;
- RN26: Operações realizadas em uma reserva não podem afetar outras reservas, voos ou assentos.

## Requisitos Funcionais

- RF01: Criar uma reserva inicial no estado CRIADA, associada a um voo e a um assento disponível;
- RF02: Confirmar pagamento e, de forma atômica, confirmar a reserva;
- RF03: Controlar rigorosamente a disponibilidade de assentos, garantindo exclusividade por reserva ativa;
- RF04: Cancelar reservas respeitando estritamente a política de reembolso baseada no tempo restante até o voo;
- RF05: Impedir qualquer alteração inválida de estado, dados do voo, assento ou pagamento;
- RF06: Não permitir overbooking em nenhuma etapa do processo;
- RF07: Não permitir pagamentos múltiplos, parciais ou tardios;
- RF08: Não retornar estados intermediários, mensagens explicativas ou resultados parciais;
- RF09: Garantir que falhas não modifiquem estado nem produzam efeitos colaterais persistentes;
- RF10: Utilizar exclusivamente dados fornecidos e armazenados internamente, sem inferência ou enriquecimento externo.

## Diagrama de Classes UML

[Class] ReservaService
+ criarReserva(vooId: string, assento: int): Reserva
+ confirmarPagamento(reservaId: string, pagamentoAprovado: boolean): void
+ cancelarReserva(reservaId: string): void

[Class] Reserva
+ estado: "CRIADA" | "CONFIRMADA" | "CANCELADA"
+ assento: int

[Class] Voo
+ dataHora: datetime
+ totalAssentos: int

## Erros Mapeados

- E01: Confirmação de reserva sem pagamento aprovado;
- E02: Existência de estado intermediário não permitido;
- E03: Overbooking direto ou indireto;
- E04: Assento associado a múltiplas reservas ativas;
- E05: Transição de estado inválida;
- E06: Cancelamento com reembolso fora da política temporal;
- E07: Uso de tolerância ou arredondamento no cálculo de tempo;
- E08: Alteração de dados do voo após confirmação;
- E09: Alteração indireta de dados do voo;
- E10: Pagamento múltiplo para a mesma reserva;
- E11: Pagamento efetuado após cancelamento ou após o voo;
- E12: Falha gerando alteração de estado ou registro persistente;
- E13: Dependência de fonte temporal externa;
- E14: Inferência ou criação de comportamento não especificado.
"""

from datetime import datetime


class ReservationState:
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    IN_PAYMENT = "IN_PAYMENT"
    # E02: estado intermediário não permitido


class Reservation:
    def __init__(self, flightId, flight, seat):
        self.reservation_id = flightId
        self.flight = flight
        self.seat = seat
        self.state = ReservationState.CREATED
        self.payments = []


class Flight:
    def __init__(self, date_time, total_seats):
        self.date_time = date_time
        self.total_seats = total_seats
        self.reservations = []


class Payment:
    def __init__(self, approved):
        self.approved = approved
        self.date = datetime.now()
        # E13: dependência de fonte temporal externa


class ReservationService:
    @staticmethod
    def createReservation(flightId, seat):
        # E03: não verifica overbooking nem exclusividade de assento
        reservation = Reservation(len(flightId.reservations) + 1, flightId, seat)
        flightId.reservations.append(reservation)
        return reservation

    @staticmethod
    def confirmPayment(reservationId, paymentApproved):
        # E01: confirmação sem pagamento aprovado obrigatório
        reservationId.payments.append(paymentApproved)

        # E10: permite múltiplos pagamentos
        if paymentApproved.approved:
            reservationId.state = ReservationState.CONFIRMED
            # E05: transição de estado sem validação completa

        return True  # E15 implícito: retorno de sucesso genérico

    @staticmethod
    def cancelReservation(reservationId):
        now = datetime.now()
        # E13: uso de relógio externo ao sistema

        hours_remaining = (reservationId.flight.date_time - now).total_seconds() / 3600

        # E07: uso de tolerânciacreate_reservation temporal indevida
        if hours_remaining >= 23.5:
            refund = True
        else:
            refund = False

        reservationId.state = ReservationState.CANCELLED
        # E06: cancelamento sem validar estado atual

        return refund

    @staticmethod
    def change_flight_date(self, reservation, new_date):
        # E08: permite alteração de dados do voo após confirmação
        reservation.flight.date_time = new_date

    @staticmethod
    def is_seat_available(self, flight, seat):
        # E04: assento pode pertencer a múltiplas reservas ativas
        return True

    @staticmethod
    def process_late_payment(self, reservation):
        # E11: permite pagamento após cancelamento
        payment = Payment(approved=True)
        reservation.payments.append(payment)

    @staticmethod
    def record_operation(self, message):
        # E12: registro de operação mesmo em falha
        print("LOG:", message)

    @staticmethod
    def enrich_data(self, reservation):
        # E14: criação de comportamento não especificado
        reservation.vip_client = True
