# Checklist de preparación integral: Gestor de Gastos MVP

**Propósito**: Evaluar si el spec y sus artefactos de diseño expresan requisitos completos, claros, consistentes, trazables y verificables antes de generar `tasks.md`.
**Creado**: 2026-10-15
**Feature**: [spec.md](../spec.md)

**Nota**: Este checklist personalizado fue generado por `$speckit-checklist` a partir del contexto de la feature y sus requisitos.
**Responsabilidad de revisión**: Este artefacto pertenece al revisor de calidad de requisitos. Marcar un ítem `[x]` únicamente cuando el revisor determine que el criterio de calidad está satisfecho.
**Semántica de marcadores**: `[x]` significa que el criterio fue revisado y satisfecho respecto de la calidad de los requisitos; no significa que la implementación esté completa.

## 1. Alcance, objetivos y trazabilidad

- [ ] CHK001 ¿El problema, los objetivos y los límites del MVP permiten distinguir inequívocamente qué capacidades están incluidas y cuáles quedan fuera, sin depender del PRD original? [Spec §Problem Statement and Objectives; Spec §Scope Boundaries]
- [ ] CHK002 ¿Cada requisito funcional FR-001–FR-050 está respaldado por al menos una historia o escenario de aceptación, y cada escenario AC-01–AC-60 remite al requisito correcto? [Spec §User Scenarios & Testing; Spec §Functional Requirements]
- [ ] CHK003 ¿Las prioridades P1/P2 son coherentes con el objetivo del MVP y están justificadas por valor de usuario, sin introducir dependencias contradictorias entre historias? [Spec §User Scenarios & Testing]
- [ ] CHK004 ¿Las cinco aclaraciones adoptadas están incorporadas de forma consistente en requisitos, escenarios, modelo y contratos, en vez de permanecer sólo como notas históricas? [Spec §Clarifications; Data Model §BoardPerson; Contract `InvitationCode`, `Money`]
- [ ] CHK005 ¿Las decisiones del plan se mantienen dentro del alcance aprobado y toda complejidad adicional está justificada por un requisito identificable? [Constitution §V; Plan §Summary; Plan §Complexity Tracking]
- [ ] CHK006 ¿Las suposiciones distinguen con claridad lo confirmado de lo pendiente y describen el efecto que tendría invalidar cada supuesto relevante? [Spec §Assumptions; Research §§6–8]

## 2. Identidad, autenticación e incorporación

- [ ] CHK007 ¿Los requisitos de registro, login, logout y consulta de sesión definen entradas, resultados observables y condiciones de error suficientes para una validación objetiva? [Spec AC-01–AC-03; FR-001–FR-003; Contract `/auth/register`, `/auth/login`, `/auth/logout`, `/auth/me`]
- [ ] CHK008 ¿La recuperación de contraseña especifica de manera consistente vigencia de 30 minutos, uso único, respuesta frente a token inválido/vencido y no revelación de cuentas registradas? [Spec AC-04–AC-05; FR-004–FR-005; Research §6; Contract `/auth/password-recovery`, `/auth/password-reset`]
- [ ] CHK009 ¿El requisito de cierre de sesión expresa con precisión qué sesión se invalida y qué comportamiento posterior es observable, en consonancia con la sesión JWT persistida? [Spec AC-03; FR-003; Research §5; Data Model §AuthSession]
- [ ] CHK010 ¿La identidad visible de miembros y participantes, incluida la desambiguación por email, está definida de forma uniforme en vistas, respuestas y reglas de selección? [Spec §Clarifications; Spec FR-009–FR-012; Data Model §BoardPerson; Contract `BoardPerson`]
- [ ] CHK011 ¿El ciclo de vida del código de invitación cubre emisión, reutilización durante siete días, vencimiento, reemplazo y unión repetida o inválida con resultados verificables? [Spec AC-07–AC-08; FR-007–FR-008; Research §7; Data Model §BoardInvitationState]

## 3. Autorización y aislamiento entre tableros

- [ ] CHK012 ¿El alcance de “toda lectura, creación, modificación o eliminación” enumera o permite trazar todos los recursos protegidos del tablero, incluidos audio, invitaciones, personas, presupuestos y ahorros? [Spec FR-047; Spec AC-47–AC-54; Contract `/boards/{boardId}/...`]
- [ ] CHK013 ¿Los requisitos describen tanto los casos autorizados como los denegados para cada familia de operaciones, sin confiar en controles del frontend? [Constitution §III; Spec User Story 9; Plan §Constitution Check]
- [ ] CHK014 ¿La respuesta ante acceso cruzado está especificada de forma consistente para evitar revelar existencia o datos de recursos ajenos, incluidos identificadores anidados válidos de otro tablero? [Constitution §III; Spec §Edge Cases; Contract responses `Unauthorized`, `NotFound`]
- [ ] CHK015 ¿Está explicitado que todos los miembros poseen las mismas capacidades y que no existen excepciones de propietario o administrador en ningún flujo del MVP? [Spec FR-048; Spec §Scope Boundaries; Data Model §Membership]
- [ ] CHK016 ¿Las invariantes de pertenencia para pagadores, participantes y recursos anidados están alineadas entre requisitos, modelo y contrato? [Spec FR-012, FR-047; Data Model §Referential and authorization invariants; Contract `ExpenseInput`]

## 4. Exactitud monetaria y reglas deterministas

- [ ] CHK017 ¿Todos los campos monetarios identifican moneda, precisión de centavos, signo permitido y límites de formato sin ambigüedad? [Spec FR-012, FR-018, FR-033, FR-037, FR-040, FR-049; Research §2; Contract `Money`, `NonNegativeMoney`]
- [ ] CHK018 ¿La división personal, equitativa y personalizada está definida para todas las cardinalidades válidas, incluida una sola persona y participantes repetidos? [Spec AC-14–AC-18; FR-014–FR-018; Spec §Edge Cases]
- [ ] CHK019 ¿La regla de residuos identifica de forma inequívoca el orden estable usado para asignar centavos y garantiza la misma salida para la misma entrada? [Constitution §II; Spec AC-16; FR-016; Data Model §ExpenseShare]
- [ ] CHK020 ¿Las validaciones de distribución cubren partes negativas, más de dos decimales, suma distinta del total, lista vacía y personas ajenas o retiradas del tablero? [Spec AC-18; FR-018; Spec §Edge Cases; Data Model §Expense]
- [ ] CHK021 ¿La fórmula de deuda diferencia con claridad al pagador de las demás personas y define el resultado cuando el pagador también recibe una parte? [Spec AC-19–AC-20; FR-019–FR-020; Data Model §ExpenseShare]
- [ ] CHK022 ¿Las reglas de edición y eliminación establecen qué agregados se recalculan y preservan exactitud y determinismo en gastos, presupuesto mensual y compras de USD? [Spec AC-23–AC-24, AC-42–AC-44; FR-023–FR-024, FR-042–FR-044]
- [ ] CHK023 ¿Se mantiene una separación explícita entre montos ARS y cantidades USD, evitando conversiones o sumas entre monedas no requeridas? [Spec FR-040, FR-044–FR-046; Spec §Scope Boundaries; Data Model §UsdPurchase]

## 5. Gastos, disponible mensual y ahorros

- [ ] CHK024 ¿Los requisitos de gasto definen de manera completa campos obligatorios, opcionales, valores válidos, fecha predeterminada y catálogo de categorías? [Spec AC-12–AC-13; FR-012–FR-013; Contract `ExpenseInput`, `Category`]
- [ ] CHK025 ¿El retiro de participantes distingue claramente disponibilidad para operaciones futuras de preservación de identidad y distribuciones históricas? [Spec AC-10–AC-11; FR-010–FR-011; Data Model §BoardPerson]
- [ ] CHK026 ¿El listado y detalle de gastos especifican los datos que deben exponerse y el comportamiento esperado de paginación, orden y ausencia de resultados? [Spec AC-21–AC-22; FR-021–FR-022; Contract `/boards/{boardId}/expenses`, `ExpensePage`]
- [ ] CHK027 ¿El período mensual y la “fecha vigente en Argentina” tienen una definición uniforme de formato, zona horaria y límites de inclusión? [Spec FR-013, FR-032–FR-036, FR-041; Data Model §MonthlyBudget; Contract `Month`]
- [ ] CHK028 ¿Las reglas del disponible cubren ausencia de base, base cero, modificación, consumo por gastos y compras de USD, y restante negativo con resultados inequívocos? [Spec AC-32–AC-36, AC-44; FR-032–FR-036, FR-044; Contract `MonthlySummary`]
- [ ] CHK029 ¿El ahorro inicial define unicidad, creación o reemplazo, edición, eliminación y concurrencia sin permitir registros iniciales duplicados? [Spec AC-37–AC-39; FR-037–FR-039; Data Model §InitialSavings; Contract `/savings/initial`]
- [ ] CHK030 ¿Las compras de USD definen creación, edición, eliminación, filtrado mensual y actualización de totales con criterios observables para cada operación? [Spec AC-40–AC-46; FR-040–FR-046; Contract `/usd-purchases`, `SavingsSummary`]

## 6. Audio y confirmación explícita

- [ ] CHK031 ¿El flujo de audio distingue con precisión captura, procesamiento, propuesta transitoria, revisión y confirmación, dejando claro que ninguna etapa previa registra un gasto? [Spec AC-25–AC-31; FR-025–FR-031; Data Model §AudioProposal]
- [ ] CHK032 ¿Los estados de captura y procesamiento, incluidos permiso denegado, audio vacío, formato no admitido, tamaño o duración excedidos y fallo de reconocimiento, tienen resultados de usuario definidos? [Spec §Edge Cases; Research §8; Contract `/audio-proposals`]
- [ ] CHK033 ¿Una propuesta incompleta o ambigua identifica qué datos faltan o requieren elección y conserva todos sus campos editables antes de confirmar? [Spec AC-28–AC-30; FR-028–FR-030; Contract `AudioAmbiguity`, `AudioProposal`]
- [ ] CHK034 ¿La confirmación de una propuesta reutiliza explícitamente las mismas validaciones de dominio y autorización que la carga manual? [Spec AC-31; FR-031; Constitution §§III–IV; Plan §Constitution Check]
- [ ] CHK035 ¿El criterio de precisión de audio define de forma reproducible el conjunto fijo, los valores esperados, el tratamiento de campos ausentes y la regla exacta para contabilizar aciertos? [Spec AC-58; NFR-004; SC-005; Quickstart §7]
- [ ] CHK036 ¿La retención o descarte de audio y propuestas transitorias está expresada de modo consistente con los límites de privacidad y persistencia del producto? [Spec §Scope Boundaries; Research §8; Data Model §AudioProposal]

## 7. Contratos, persistencia y concurrencia

- [ ] CHK037 ¿Cada operación requerida posee un contrato identificable con entrada, respuesta exitosa y errores de autenticación, autorización, validación y conflicto pertinentes? [Spec FR-001–FR-050; Contract §paths]
- [ ] CHK038 ¿Los nombres, tipos, obligatoriedad y restricciones de campos coinciden entre spec, modelo de datos y esquemas OpenAPI, especialmente para dinero, fechas, personas y versiones? [Spec §Key Entities; Data Model §Shared conventions; Contract §components/schemas]
- [ ] CHK039 ¿Las reglas de concurrencia optimista establecen qué recursos usan versión, cómo la aporta el cliente y cuál es el resultado observable ante una versión obsoleta? [Research §10; Data Model §§Expense, MonthlyBudget, InitialSavings, UsdPurchase; Contract `Version`, `Conflict`]
- [ ] CHK040 ¿Las garantías transaccionales definen qué cambios relacionados deben confirmarse o rechazarse como una unidad para evitar totales y distribuciones parciales? [Research §3; Data Model §Referential and authorization invariants; Spec FR-023–FR-024, FR-042–FR-044]
- [ ] CHK041 ¿El alcance de persistencia enumera todos los datos confirmados y distingue de manera explícita datos transitorios, revocaciones y registros retirados? [Spec AC-55; FR-050; NFR-001; Data Model §§AuthSession–AudioProposal]

## 8. UX, accesibilidad y estados visibles

- [ ] CHK042 ¿Cada historia describe estados inicial, carga, éxito, vacío, validación y error suficientes para construir una experiencia verificable, especialmente en operaciones destructivas? [Spec §User Scenarios & Testing; Spec §Edge Cases; Quickstart §End-to-end validation scenarios]
- [ ] CHK043 ¿La exigencia de abrir un gasto en una interacción define con claridad el punto de partida, qué cuenta como interacción y qué variantes de pantalla se evalúan? [Spec AC-56; NFR-002; SC-007]
- [ ] CHK044 ¿La matriz responsive identifica todas las pantallas incluidas, anchos de 360/768/1280 px y condiciones objetivas de operación sin pérdida de acciones o datos? [Spec AC-57; NFR-003; SC-006; Quickstart §8]
- [ ] CHK045 ¿Los requisitos de accesibilidad aplicables a formularios, errores, foco, teclado y estados de audio son explícitos y verificables, sin quedar sólo como instrucciones de validación manual? [Spec User Story 10; Quickstart §8; Plan §Technical Context]
- [ ] CHK046 ¿Las confirmaciones, mensajes y visualización de valores distinguen de forma inequívoca eliminación, retiro, restante “no disponible”, restante negativo y propuestas no confirmadas? [Spec AC-11, AC-24, AC-28, AC-36; FR-011, FR-024, FR-028, FR-036]

## 9. Calidad no funcional y preparación para tareas

- [ ] CHK047 ¿Cada NFR posee métrica, población o muestra, entorno, procedimiento y umbral suficientes para producir un resultado repetible? [Spec NFR-001–NFR-006; Spec SC-004–SC-009]
- [ ] CHK048 ¿El criterio de rendimiento de login fija de forma suficiente hardware o entorno, estado de datos, medición, calentamiento, concurrencia y tratamiento de fallos? [Spec AC-60; NFR-006; SC-008; Research §11]
- [ ] CHK049 ¿El criterio de usabilidad define perfiles representativos, tareas, condiciones de asistencia y forma de contabilizar que 4 de 5 usuarios completaron los flujos? [Spec SC-010]
- [ ] CHK050 ¿Los requisitos de seguridad abarcan almacenamiento y exposición de contraseñas, tokens, secretos y credenciales, con una definición verificable de “texto plano”? [Constitution §III; Spec AC-59; NFR-005; SC-009; Research §§5–7]
- [ ] CHK051 ¿La estrategia test-first traza las reglas críticas a escenarios de prueba concretos para dinero, distribución, disponible mensual, permisos y validaciones de dominio? [Constitution §I; Plan §Constitution Check; Research §11; Quickstart §Test-first validation order]
- [ ] CHK052 ¿Los criterios de éxito miden resultados del producto y son consistentes con las cantidades declaradas —60 escenarios, 20 audios, 100 logins y 5 usuarios— sin depender de detalles de implementación? [Spec SC-001–SC-010]
- [ ] CHK053 ¿Los casos borde cubren entradas inválidas, límites temporales, concurrencia, duplicados, recursos retirados, acceso cruzado y fallos externos relevantes, y cada uno tiene destino trazable en requisitos o escenarios? [Spec §Edge Cases; Research §§6, 7, 10]
- [ ] CHK054 ¿El plan, modelo, contrato y guía de validación no contienen requisitos funcionales nuevos ni omiten comportamientos exigidos por el spec? [Constitution §V; Plan §Summary; Data Model; Contract; Quickstart]
- [ ] CHK055 ¿Las dependencias y el orden implícito entre autenticación, tableros, personas, gastos, agregados, ahorros y audio están suficientemente definidos para generar tareas implementables y verificables? [Spec §User Scenarios & Testing; Plan §Project Structure; Quickstart §Test-first validation order]

## Notas

- Marcar `[x]` únicamente después de que la revisión confirme que el criterio de calidad del requisito está satisfecho.
- Dejar sin marcar los ítems que requieran aclaración, corrección o evaluación adicional del revisor.
- `$speckit-implement` interpreta el estado de los marcadores como una puerta de calidad y no debe modificarlos.
- `checklists/requirements.md` tiene un ciclo de vida interno separado, mantenido por `$speckit-specify` y `$speckit-clarify`.
- Agregar hallazgos y decisiones de revisión en línea.
- Vincular cualquier corrección con el requisito y artefacto afectado.
- Los ítems están numerados secuencialmente para facilitar trazabilidad y discusión.
