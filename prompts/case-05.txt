You are a senior test engineer specialized in critical, transactional, and highly regulated systems.

Your task is to generate automated test cases in Python using exclusively the pytest library,
based on the formal specifications provided below.

⚠️ GENERAL CONSTRAINTS (MANDATORY)

1. Do not create rules, requirements, states, exceptions, transitions, or behaviors that are not explicitly described.
2. Do not assume temporal tolerances, rounding, implicit exceptions, or “domain-standard” behaviors.
3. Do not simplify rules, do not group validations, and do not infer intentions.
4. Clearly distinguish between:
   - validation failure (exception)
   - valid state transition (allowed effect)
5. Each test must validate exactly one specific behavior.
6. Use precise (exact) values only; never use ranges, margins, or intervals.
7. All tests must be deterministic and reproducible.
8. Use only pytest, with no additional external libraries.
9. Do not implement the system — tests only.
10. Do not include explanatory text outside code comments.

---

## SYSTEM CONTEXT

Airline reservation system responsible for creating reservations, confirming payments,
controlling seat allocation, and canceling reservations, operating under strict rules
of atomicity, immutability, resource exclusivity, and transactional consistency.

---

## BUSINESS RULES (BR)

- BR01: A reservation may only be confirmed if exactly one approved payment is associated with it;
- BR02: Payments with a status other than approved must not confirm reservations;
- BR03: Reservation confirmation and payment approval must occur atomically, and no observable state may exist in which only one of the two has been completed;
- BR04: A seat may belong to at most one active reservation per flight;
- BR05: Canceled reservations must immediately release the associated seat;
- BR06: Overbooking is not permitted under any circumstances;
- BR07: The number of confirmed reservations for a flight must never exceed the total number of available seats;
- BR08: A reservation may be exclusively in one of the following states:
    * CREATED
    * CONFIRMED
    * CANCELED
- BR09: Intermediate or additional states (e.g., “In payment”, “Pending”, “Expired”) are not permitted;
- BR10: The only valid state transitions are:
    * CREATED → CONFIRMED
    * CONFIRMED → CANCELED
- BR11: Any state transition other than those defined must be rejected;
- BR12: A canceled reservation must not be reactivated, modified, or receive new payments;
- BR13: Reservation cancellation must strictly comply with the temporal policy:
    * Remaining time ≥ 24 hours before the flight → full refund;
    * Remaining time < 24 hours before the flight → no refund;
- BR14: Remaining time until the flight must be calculated in exact hours, with no rounding or tolerance of any kind;
- BR15: The system must use exclusively the internally stored flight date and time as the temporal reference;
- BR16: Flight dates, times, and identifiers must not be altered after reservation confirmation;
- BR17: Indirect modifications of flight data (reference swapping, cloning, or object recreation) are prohibited;
- BR18: Each reservation may have exactly one associated payment;
- BR19: Additional payment attempts for the same reservation must be rejected;
- BR20: Payments must not be accepted for canceled reservations or after the flight date;
- BR21: System operations must be deterministic, always producing the same result for the same sequence of inputs;
- BR22: The system must not assume unspecified implicit behaviors (e.g., future credit, automatic rebooking, commercial exceptions);
- BR23: Any business rule violation must result in immediate failure, with no state change or creation of partial records;
- BR24: Each valid operation must generate exactly one immutable record;
- BR25: Failed operations must not generate persistent records;
- BR26: Operations performed on one reservation must not affect other reservations, flights, or seats.

---

## FUNCTIONAL REQUIREMENTS (FR)

- FR01: Create an initial reservation in the CREATED state, associated with a flight and an available seat;
- FR02: Confirm payment and, atomically, confirm the reservation;
- FR03: Strictly control seat availability, ensuring exclusivity per active reservation;
- FR04: Cancel reservations while strictly respecting the refund policy based on remaining time until the flight;
- FR05: Prevent any invalid modification of state, flight data, seat, or payment;
- FR06: Do not allow overbooking at any stage of the process;
- FR07: Do not allow multiple, partial, or late payments;
- FR08: Do not return intermediate states, explanatory messages, or partial results;
- FR09: Ensure that failures do not modify state or produce persistent side effects;
- FR10: Use exclusively provided and internally stored data, with no inference or external enrichment.

---

## CLASS DIAGRAM (SIMPLIFIED UML)

[Class] ReservationService
+ createReservation(flightId: string, seat: int): Reservation
+ confirmPayment(reservationId: string, paymentApproved: boolean): void
+ cancelReservation(reservationId: string): void

[Class] Reservation
+ state: "CREATED" | "CONFIRMED" | "CANCELED"
+ seat: int

[Class] Flight
+ dateTime: datetime
+ totalSeats: int

---

## TASK

Based EXCLUSIVELY on the information above:

1. Generate automated tests in Python using pytest.
2. For each Business Rule (BR), create at least one test that:
   - validates correct behavior
   - exposes violations when applicable
3. For each Functional Requirement (FR), create at least one test that:
   - validates its fulfillment
4. Create both positive and negative tests.
5. Create edge case tests whenever explicitly required by the rules.
6. Tests involving exceptions must use pytest.raises.
7. Each test must have a clear and self-explanatory name.
8. Do not reuse tests to cover multiple business rules.
9. Do not use generic parameterization that hides specific scenarios.

---

## OUTPUT FORMAT (MANDATORY)

- Return exclusively valid Python code.
- Use the standard pytest structure.
- Each test must include comments explicitly indicating:
  - which BR and/or FR is being validated.

Mandatory comment example:
# BR03 – Reservation confirmation and payment must be atomic

---

## EVALUATION CRITERIA (IMPLICIT)

Your response will be evaluated based on:
- Literal adherence to the rules
- Complete coverage of BR and FR
- Semantic correctness of the tests
- Absence of invented behavior
- Clarity, precision, and isolation of the generated tests

⚠️ Any test that assumes unspecified behavior will be considered incorrect.

Generate tests only.
