# Feature Specification: Gestor de Gastos MVP

**Feature Branch**: `001-gestor-gastos-mvp`

**Created**: 2026-10-15

**Status**: Design Complete

**Input**: User description: "Generar el spec de Gestor Gastos a partir del PRD.md completo, con historias de usuario, escenarios y criterios de aceptación verificables, casos borde y criterios de éxito, sin decisiones técnicas ni implementación."

## Problem Statement and Objectives

El control manual mediante planillas consume tiempo y facilita errores de carga y cálculo,
especialmente cuando varias personas comparten gastos. El producto debe separar con claridad el
monto total que reduce el disponible mensual, la parte asignada a cada persona y las deudas de
otras personas con quien pagó. A la vez, debe conservar una carga rápida y revisable y permitir
consultar, modificar y corregir datos sin perder integridad.

El MVP persigue cuatro resultados de negocio:

- simplificar el control cotidiano de gastos personales y compartidos;
- reducir el tiempo y esfuerzo de registrar y mantener actualizado ese control;
- hacer comprensible la distribución de los gastos para apoyar la planificación del ahorro; y
- diferenciar el dinero destinado a consumo del destinado a ahorro.

## Clarifications

### Session 2026-10-15

- Q: En un gasto de tipo personal, ¿a quién debe asignarse el monto total? → A: Al pagador.
- Q: ¿Qué debe mostrar el resumen mensual cuando todavía no se configuró el disponible base? → A: Mostrar el consumido y el restante como “no disponible”.
- Q: ¿Cómo debe identificarse a un miembro con cuenta cuando se lo selecciona como pagador o participante de un gasto? → A: Con nombre visible y email para desambiguar.
- Q: ¿Durante cuánto tiempo y cuántas veces debe poder usarse el código de invitación de un tablero? → A: Reutilizable durante 7 días.
- Q: ¿Cuánto tiempo debe permanecer vigente un mecanismo de recuperación de contraseña antes de vencer? → A: 30 minutos desde su emisión.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Acceder de forma segura (Priority: P1)

Como persona usuaria, quiero crear una cuenta, iniciar y cerrar sesión y recuperar el acceso para
administrar mis tableros sin exponer mis credenciales.

**Why this priority**: El acceso autenticado es la condición previa para usar el producto y
proteger la información financiera.

**Independent Test**: Puede probarse creando una cuenta nueva, entrando y saliendo con ella y
restableciendo su contraseña mediante un mecanismo recibido por email.

**Acceptance Scenarios**:

1. **AC-01 / RF-01 — Registro**: **Given** un nombre visible, un email válido no registrado y una
   contraseña de al menos 8 caracteres, **When** la persona confirma el registro, **Then** existe
   exactamente una cuenta asociada al email normalizado y conserva el nombre visible.
2. **AC-02 / RF-02 — Inicio de sesión**: **Given** una cuenta registrada, **When** el usuario
   ingresa su email y contraseña válidos, **Then** accede a una sesión correspondiente a esa
   cuenta.
3. **AC-03 / RF-03 — Cierre de sesión**: **Given** una sesión autenticada, **When** el usuario la
   cierra, **Then** dejan de mostrarse los datos de sus tableros y se exige autenticación para
   volver a acceder.
4. **AC-04 / RF-04 — Recuperación**: **Given** una cuenta registrada con un email accesible,
   **When** el usuario solicita recuperar el acceso, **Then** recibe en ese email un mecanismo
   de un solo uso, asociado a la cuenta y vigente durante 30 minutos desde su emisión.
5. **AC-05 / RF-05 — Restablecimiento**: **Given** un mecanismo de recuperación vigente, **When**
   el usuario define una contraseña nueva válida, **Then** la anterior es rechazada y la nueva
   permite iniciar sesión.

---

### User Story 2 - Compartir un tablero (Priority: P1)

Como usuario autenticado, quiero crear un tablero o incorporarme a uno mediante un código para
administrar gastos y ahorros junto con otras personas.

**Why this priority**: El tablero es el límite de propiedad y colaboración de todos los datos
financieros del producto.

**Independent Test**: Puede probarse creando un tablero con una cuenta, obteniendo su código e
incorporando una segunda cuenta, que debe poder consultar el tablero.

**Acceptance Scenarios**:

1. **AC-06 / RF-06 — Creación**: **Given** un usuario autenticado sin un tablero llamado Hogar,
   **When** crea el tablero Hogar, **Then** existe exactamente un tablero con ese nombre y el
   creador figura como miembro.
2. **AC-07 / RF-07 — Invitación**: **Given** un miembro de Hogar, **When** solicita el código de
   invitación, **Then** ve un código asociado a ese tablero, reutilizable durante 7 días desde su
   emisión, que puede compartir.
3. **AC-08 / RF-08 — Incorporación**: **Given** un usuario autenticado que no pertenece a Hogar y
   un código válido del tablero, **When** ingresa el código, **Then** pasa a ser miembro y puede
   consultar su listado de gastos.

---

### User Story 3 - Administrar personas del tablero (Priority: P1)

Como miembro, quiero representar a personas que no tienen cuenta para incluirlas como pagadores
o participantes de gastos sin darles acceso a la aplicación.

**Why this priority**: Los gastos compartidos sólo pueden distribuirse correctamente si todas
las personas involucradas pueden representarse en el tablero.

**Independent Test**: Puede probarse creando, renombrando y retirando un participante sin cuenta,
y verificando que los gastos históricos conserven su identidad y distribución.

**Acceptance Scenarios**:

1. **AC-09 / RF-09 — Alta**: **Given** un miembro de Hogar, **When** registra un participante sin
   cuenta llamado Ana, **Then** existe exactamente un participante llamado Ana disponible para
   nuevos gastos del tablero.
2. **AC-10 / RF-10 — Modificación**: **Given** el participante Ana, **When** un miembro cambia su
   nombre a Ana Pérez, **Then** existe un único participante llamado Ana Pérez y los gastos
   históricos asociados conservan sus montos y distribuciones.
3. **AC-11 / RF-11 — Eliminación**: **Given** Ana asociada a un gasto histórico, **When** un
   miembro la elimina, **Then** deja de estar disponible para nuevos gastos y el gasto histórico
   conserva su monto y distribución.

---

### User Story 4 - Registrar y distribuir gastos (Priority: P1)

Como miembro, quiero registrar gastos personales o compartidos y asignar sus partes para conocer
el impacto total en el disponible y cuánto debe devolver cada persona al pagador.

**Why this priority**: Es el flujo central que reemplaza el control manual y evita confundir el
monto pagado con la parte que corresponde a cada persona.

**Independent Test**: Puede probarse registrando gastos personales, equitativos y personalizados,
verificando montos, partes, residuos de centavos y deudas resultantes.

**Acceptance Scenarios**:

1. **AC-12 / RF-12 — Registro**: **Given** Hogar y una persona del tablero como pagador, **When**
   un miembro registra Supermercado por ARS 30.000,00, categoría Alimentos y fecha 15/01/2026,
   **Then** existe exactamente un gasto con esos datos y pagador.
2. **AC-13 / RF-13 — Fecha predeterminada**: **Given** que en Argentina es 15/01/2026, **When**
   se registra un gasto sin fecha, **Then** queda fechado el 15/01/2026.
3. **AC-14 / RF-14 — Tipo**: **Given** un nuevo gasto, **When** el miembro selecciona personal,
   compartido en partes iguales o distribución personalizada y confirma, **Then** se conserva
   exactamente el tipo elegido.
4. **AC-15 / RF-15 — División equitativa**: **Given** un gasto de ARS 30.000,00 y dos personas,
   **When** se elige partes iguales, **Then** cada persona recibe ARS 15.000,00.
5. **AC-16 / RF-16 — Residuo determinista**: **Given** un gasto de ARS 100,00 y tres personas
   seleccionadas en el mismo orden, **When** se calcula varias veces la división equitativa,
   **Then** siempre se obtiene la misma asignación, los centavos indivisibles se asignan a las
   primeras personas según ese orden y la suma es ARS 100,00.
6. **AC-17 / RF-17 — División personalizada**: **Given** un gasto de ARS 150.000,00, **When** el
   miembro asigna ARS 40.000,00 al pagador y ARS 110.000,00 a Ana, **Then** se guardan exactamente
   esas dos partes.
7. **AC-18 / RF-18 — División inválida**: **Given** un gasto de ARS 150.000,00, **When** se intenta
   confirmar una parte negativa o partes cuya suma difiere del total, **Then** no se guarda el
   gasto y se identifica la distribución inválida.
8. **AC-19 / RF-19 — Consulta de partes**: **Given** una distribución de ARS 40.000,00 para el
   pagador y ARS 110.000,00 para Ana, **When** un miembro la consulta, **Then** ve ambos importes
   asociados a las personas correctas.
9. **AC-20 / RF-20 — Deuda**: **Given** el gasto anterior pagado por el miembro, **When** se
   consulta la deuda, **Then** se muestra que Ana debe devolver ARS 110.000,00 al pagador y no se
   genera deuda del pagador consigo mismo.

---

### User Story 5 - Consultar y corregir gastos (Priority: P1)

Como miembro, quiero revisar, editar y eliminar gastos para corregir errores y mantener exactos
los totales mensuales.

**Why this priority**: La posibilidad de corrección conserva la utilidad de una planilla sin
sacrificar la consistencia de cálculos derivados.

**Independent Test**: Puede probarse registrando un gasto, consultando lista y detalle,
modificándolo y eliminándolo, y verificando el recálculo del dinero restante.

**Acceptance Scenarios**:

1. **AC-21 / RF-21 — Listado**: **Given** Supermercado por ARS 30.000,00 en Alimentos, **When**
   un miembro consulta los gastos, **Then** se muestra exactamente un gasto con esos valores.
2. **AC-22 / RF-22 — Detalle**: **Given** un gasto con fecha, pagador, tipo y distribución,
   **When** un miembro abre el detalle, **Then** ve esos cuatro datos con sus valores almacenados.
3. **AC-23 / RF-23 — Edición**: **Given** un disponible base de ARS 500.000,00, sin compras de
   USD y un único gasto de ARS 30.000,00 en enero de 2026, **When** se cambia el gasto a
   ARS 35.000,00, **Then** queda un único gasto por ese monto y el restante es ARS 465.000,00.
4. **AC-24 / RF-24 — Eliminación confirmada**: **Given** el mismo disponible y un único gasto de
   ARS 30.000,00, **When** un miembro solicita eliminarlo y confirma, **Then** desaparece del
   listado y el restante vuelve a ARS 500.000,00.

---

### User Story 6 - Cargar un gasto mediante audio (Priority: P2)

Como miembro, quiero describir un gasto por audio y revisar una propuesta editable para reducir
el esfuerzo de carga sin registrar datos incorrectos automáticamente.

**Why this priority**: Acelera el flujo principal, pero depende de que el registro manual y la
revisión segura ya funcionen.

**Independent Test**: Puede probarse con audios de resultados esperados completos e incompletos,
comprobando que sólo una confirmación explícita crea el gasto.

**Acceptance Scenarios**:

1. **AC-25 / RF-25 — Captura**: **Given** la captura inactiva, **When** un miembro inicia el
   registro por audio, **Then** ve un indicador de captura activa.
2. **AC-26 / RF-26 — Extracción**: **Given** un audio cuyo resultado esperado contiene
   Supermercado, ARS 30.000,00, Alimentos, partes iguales, pagador Carla y participantes Carla y
   Ana, **When** se procesa, **Then** todos los valores interpretados coinciden con el esperado.
3. **AC-27 / RF-27 — Propuesta**: **Given** esos datos interpretados, **When** finaliza el
   procesamiento, **Then** existe una propuesta no registrada con todos esos valores.
4. **AC-28 / RF-28 — Propuesta incompleta**: **Given** un audio del que sólo se extrajeron nombre
   y monto, **When** finaliza el procesamiento, **Then** se muestra una propuesta editable con la
   categoría marcada como faltante y no existe un gasto nuevo.
5. **AC-29 / RF-29 — Revisión**: **Given** una propuesta completa, **When** el miembro abre la
   revisión, **Then** ve nombre, monto, categoría, tipo, pagador y participantes antes de confirmar.
6. **AC-30 / RF-30 — Modificación**: **Given** una propuesta por ARS 30.000,00, **When** se cambia
   el monto a ARS 35.000,00, **Then** la propuesta muestra el nuevo monto y todavía no existe un
   gasto nuevo.
7. **AC-31 / RF-31 — Confirmación**: **Given** una propuesta revisada con todos los datos
   obligatorios válidos, **When** un miembro confirma, **Then** existe exactamente un gasto nuevo
   con los valores de la propuesta.

---

### User Story 7 - Controlar el disponible mensual (Priority: P1)

Como miembro, quiero definir el dinero disponible y ver cuánto se consumió y cuánto queda por mes
para controlar el presupuesto común del tablero.

**Why this priority**: Responde al problema principal de perder el seguimiento del dinero
disponible cuando crecen los movimientos compartidos.

**Independent Test**: Puede probarse configurando un mes con gastos y compras de USD y verificando
la distribución por categoría, el total consumido y el restante, incluso cuando es negativo.

**Acceptance Scenarios**:

1. **AC-32 / RF-32 — Categorías**: **Given** gastos de enero de 2026 por ARS 40.000,00 en
   Alimentos y ARS 60.000,00 en Transporte, **When** se consulta el gráfico del mes, **Then** se
   muestran ambas categorías, sus importes y un total de ARS 100.000,00.
2. **AC-33 / RF-33 — Disponible base**: **Given** enero de 2026 sin disponible base, **When** un
   miembro define ARS 500.000,00, **Then** el mes conserva ese disponible base.
3. **AC-34 / RF-34 — Modificación**: **Given** ARS 500.000,00 de base, ARS 40.000,00 en gastos y
   ARS 150.000,00 en compras de USD, **When** se cambia la base a ARS 600.000,00, **Then** el
   restante es ARS 410.000,00.
4. **AC-35 / RF-35 — Consumido**: **Given** gastos totales por ARS 150.000,00 distribuidos entre
   varias personas y compras de USD por ARS 40.000,00 en enero, **When** se consulta el consumido,
   **Then** se muestran ARS 190.000,00 sin alterar el total por la distribución de los gastos.
5. **AC-36 / RF-36 — Restante negativo**: **Given** ARS 100.000,00 de base y ARS 120.000,00 en
   gastos, **When** se consulta enero, **Then** se muestran ARS -20.000,00 restantes.

---

### User Story 8 - Administrar ahorros en USD (Priority: P2)

Como miembro, quiero registrar un ahorro inicial y las compras de USD para diferenciar el dinero
destinado al ahorro del consumo y conocer el total ahorrado.

**Why this priority**: Completa la visión financiera del tablero y separa ahorro de consumo, pero
el control básico de gastos conserva valor sin esta historia.

**Independent Test**: Puede probarse creando, editando y eliminando el ahorro inicial y compras de
USD, comprobando el total ahorrado y su impacto mensual en ARS.

**Acceptance Scenarios**:

1. **AC-37 / RF-37 — Ahorro inicial**: **Given** un tablero sin ahorro inicial, **When** un
   miembro registra USD 1.000,00, **Then** se muestran USD 1.000,00 como ahorro inicial.
2. **AC-38 / RF-38 — Edición inicial**: **Given** USD 1.000,00 iniciales, **When** se modifican a
   USD 1.200,00, **Then** existe un único registro inicial por USD 1.200,00.
3. **AC-39 / RF-39 — Eliminación inicial**: **Given** USD 1.000,00 iniciales y ninguna compra,
   **When** se elimina el ahorro inicial, **Then** el total ahorrado es USD 0,00.
4. **AC-40 / RF-40 — Compra**: **Given** USD 1.000,00 ahorrados, **When** se registra una compra
   de USD 100,00 por ARS 150.000,00 con fecha 15/01/2026, **Then** existe exactamente una compra
   con esos valores y fecha.
5. **AC-41 / RF-41 — Fecha predeterminada**: **Given** que en Argentina es 15/01/2026, **When**
   se registra una compra sin fecha, **Then** queda fechada el 15/01/2026.
6. **AC-42 / RF-42 — Edición de compra**: **Given** una compra de USD 100,00 por ARS 150.000,00
   en enero, **When** se modifica a USD 120,00 por ARS 180.000,00, **Then** existe una única compra
   con los nuevos importes y el consumido mensual aumenta ARS 30.000,00.
7. **AC-43 / RF-43 — Eliminación de compra**: **Given** ARS 500.000,00 disponibles y una compra
   de USD 100,00 por ARS 150.000,00, **When** se elimina, **Then** desaparece de enero y el
   restante vuelve a ARS 500.000,00.
8. **AC-44 / RF-44 — Impacto mensual**: **Given** ARS 500.000,00 disponibles y ningún otro
   movimiento, **When** se registra en enero una compra de USD por ARS 150.000,00, **Then** el
   consumido es ARS 150.000,00 y el restante ARS 350.000,00.
9. **AC-45 / RF-45 — Total**: **Given** USD 1.000,00 iniciales y compras vigentes por USD 100,00,
   **When** se consulta el total, **Then** se muestran USD 1.100,00.
10. **AC-46 / RF-46 — Compras mensuales**: **Given** una compra de USD 100,00 en enero y otra de
    USD 50,00 en febrero, **When** se consulta enero, **Then** sólo aparece la compra de
    USD 100,00 y el total mensual es USD 100,00.

---

### User Story 9 - Mantener aislamiento entre tableros (Priority: P1)

Como miembro, quiero que sólo quienes pertenecen a mi tablero puedan leer o cambiar sus datos
para preservar la privacidad e integridad de la información financiera.

**Why this priority**: Una falla de aislamiento expone o altera información sensible y viola el
límite de propiedad central del producto.

**Independent Test**: Puede probarse intentando leer, modificar y eliminar recursos de Hogar con
una cuenta autenticada que no sea miembro, y verificando que no reciba datos ni produzca cambios.

**Acceptance Scenarios**:

1. **AC-47 / RF-21 — Gastos**: **Given** un usuario autenticado no miembro de Hogar, **When**
   consulta sus gastos, **Then** se rechaza la solicitud sin devolver gastos.
2. **AC-48 / RF-35 y RF-36 — Disponible**: **Given** el mismo usuario, **When** consulta el
   resumen mensual, **Then** se rechaza la solicitud sin devolver consumido ni restante.
3. **AC-49 / RF-45 y RF-46 — Ahorros**: **Given** el mismo usuario, **When** consulta los ahorros,
   **Then** se rechaza la solicitud sin devolver total ni compras de USD.
4. **AC-50 / RF-34 — Modificar disponible**: **Given** el no miembro y una base de
   ARS 500.000,00, **When** intenta cambiarla a ARS 600.000,00, **Then** se rechaza la operación y
   la base continúa en ARS 500.000,00.
5. **AC-51 / RF-23 — Modificar gasto**: **Given** el no miembro y un gasto de ARS 30.000,00,
   **When** intenta cambiarlo a ARS 35.000,00, **Then** se rechaza y el gasto no cambia.
6. **AC-52 / RF-10 — Modificar participante**: **Given** el no miembro y Ana, **When** intenta
   renombrarla Ana Pérez, **Then** se rechaza y el nombre continúa siendo Ana.
7. **AC-53 / RF-24 — Eliminar gasto**: **Given** el no miembro y un gasto de ARS 30.000,00,
   **When** intenta eliminarlo, **Then** se rechaza y el gasto continúa en el tablero.
8. **AC-54 / RF-11 — Eliminar participante**: **Given** el no miembro y Ana, **When** intenta
   eliminarla, **Then** se rechaza y Ana continúa disponible.

---

### User Story 10 - Conservar una experiencia confiable (Priority: P2)

Como usuario, quiero que mis datos confirmados persistan y que las pantallas principales sean
rápidas y utilizables en los dispositivos objetivo para confiar en el producto cotidianamente.

**Why this priority**: La pérdida de datos, la exposición de credenciales o una interfaz
inaccesible invalidan los flujos funcionales aunque éstos existan.

**Independent Test**: Puede probarse reiniciando el servicio después de confirmar datos,
recorriendo los flujos en la matriz de dispositivos y ejecutando las evaluaciones de audio,
seguridad y acceso definidas.

**Acceptance Scenarios**:

1. **AC-55 / NFR-01 — Persistencia**: **Given** una cuenta, tablero, participante, gasto,
   disponible mensual y ahorro confirmados, **When** se reinicia el servicio y se consultan,
   **Then** el 100% conserva sus valores previos.
2. **AC-56 / NFR-02 — Acceso a carga**: **Given** un miembro en la pantalla principal del
   tablero, **When** realiza una interacción sobre nuevo gasto, **Then** se abre el formulario.
3. **AC-57 / NFR-03 — Adaptabilidad**: **Given** cada pantalla cubierta por estos criterios,
   **When** se usa en la matriz objetivo, **Then** el 100% opera sin desplazamiento horizontal,
   contenido cortado ni controles inaccesibles.
4. **AC-58 / NFR-04 — Audio**: **Given** el conjunto fijo de 20 audios consentidos y no sensibles,
   con manifiesto, hashes y valores esperados, congelado antes de implementar o ajustar las reglas
   de extracción, **When** se procesan todos, **Then** al menos 12 coinciden en todos los valores
   esperados presentes.
5. **AC-59 / NFR-05 — Credenciales**: **Given** cuentas registradas y sesiones iniciadas,
   **When** se inspeccionan las credenciales almacenadas o expuestas, **Then** se encuentran cero
   credenciales de autenticación en texto plano.
6. **AC-60 / NFR-06 — Acceso oportuno**: **Given** 100 inicios de sesión válidos con 5 usuarios
   concurrentes, 10 intentos previos de calentamiento y un entorno fijo de 2 vCPU y 4 GB de RAM
   sin servicios externos, **When** se ejecuta la prueba, **Then** al menos 95 finalizan en no más
   de 4 segundos desde la solicitud hasta la respuesta completa.

### Edge Cases

- Un email ya registrado no crea una segunda cuenta; la comparación usa el email normalizado y
  el resultado no revela credenciales.
- Un mecanismo de recuperación vencido, ya utilizado o ajeno a la cuenta no cambia la contraseña.
- Un código de invitación inexistente o no válido no incorpora al usuario ni revela datos del
  tablero; ingresar nuevamente un código de un tablero al que ya pertenece no duplica membresías.
- Vencido el código de invitación, deja de aceptar incorporaciones y cualquier miembro puede
  solicitar uno nuevo; pedir el código mientras el actual sigue vigente devuelve el mismo código.
- Dos tableros distintos pueden tener el mismo nombre; dentro de la experiencia de un usuario,
  cada tablero conserva identidad propia más allá de su nombre visible.
- Un participante retirado no puede seleccionarse para movimientos nuevos, pero continúa
  identificado en gastos históricos.
- Un gasto requiere nombre, monto positivo, categoría, fecha, pagador y tipo; la descripción es
  opcional. No se confirma si falta un dato obligatorio.
- Un gasto personal asigna automáticamente el total al pagador y no permite seleccionar otra
  persona; un gasto compartido requiere al menos una persona seleccionada.
- Los importes aceptan exactamente dos decimales. Ninguna suma monetaria usa aproximaciones y las
  partes siempre suman exactamente el total del gasto.
- En una división equitativa con centavos indivisibles, los centavos residuales se asignan uno por
  uno a las primeras personas según el orden de selección, sin cambiar dicho orden entre cálculos.
- Cambiar monto, tipo o participantes de un gasto obliga a obtener una distribución nuevamente
  válida antes de guardar; los totales derivados se recalculan una sola vez sobre el estado final.
- Cancelar una eliminación de gasto conserva el gasto y todos los totales sin cambios.
- Un audio silencioso, ilegible, interrumpido o incompleto produce una propuesta editable con los
  campos faltantes identificados, nunca un gasto automático.
- Si un nombre extraído del audio coincide con más de una persona del tablero, la propuesta marca
  esa referencia como ambigua y exige que el miembro elija la persona correcta antes de confirmar.
- Una propuesta de audio descartada o no confirmada no afecta gastos, disponible ni ahorros.
- Un período sin disponible base se distingue de un disponible base de ARS 0,00: se muestra el
  dinero consumido, pero el restante se indica como “no disponible” hasta que un miembro configure
  la base. Los movimientos se conservan y se incorporan al cálculo cuando se define la base.
- El dinero restante puede ser cero o negativo y se muestra sin ocultar ni truncar el signo.
- Editar o eliminar un movimiento fechado en otro mes recalcula el período original y, si cambia
  la fecha, también el período destino.
- El ahorro inicial admite un único registro vigente por tablero. Sin ahorro inicial ni compras,
  el total es USD 0,00.
- Los importes en USD y ARS de una compra son positivos y se conservan por separado; no se calcula
  una cotización ni una conversión automática.
- Toda operación sobre un recurso inexistente, de otro tablero o cuyo identificador fue alterado
  se rechaza sin revelar si el recurso existe y sin modificar datos.
- Acciones simultáneas sobre el mismo recurso no deben producir duplicados ni totales derivados de
  una combinación parcial de estados confirmados.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El producto DEBE permitir registrar una cuenta única mediante nombre visible, email
  válido y una contraseña de al menos 8 caracteres, normalizando el email para detectar duplicados.
- **FR-002**: El producto DEBE permitir iniciar sesión mediante email y contraseña válidos.
- **FR-003**: El producto DEBE permitir cerrar la sesión activa e impedir acceso posterior a datos
  protegidos sin una nueva autenticación.
- **FR-004**: El producto DEBE enviar al email de una cuenta un mecanismo de recuperación de uso
  único que venza 30 minutos después de su emisión.
- **FR-005**: El producto DEBE permitir reemplazar la contraseña mediante un mecanismo de
  recuperación válido e invalidar la contraseña anterior.
- **FR-006**: Un usuario autenticado DEBE poder crear un tablero y quedar incorporado como miembro.
- **FR-007**: Todo miembro DEBE poder obtener el código de invitación vigente de su tablero. El
  código DEBE poder usarse varias veces durante 7 días calendario desde su emisión; vencido ese
  plazo, cualquier miembro DEBE poder obtener uno nuevo.
- **FR-008**: Un usuario autenticado DEBE poder incorporarse una sola vez a un tablero mediante un
  código de invitación válido.
- **FR-009**: Todo miembro DEBE poder registrar un participante sin cuenta en su tablero.
- **FR-010**: Todo miembro DEBE poder modificar el nombre de un participante sin cuenta sin alterar
  las referencias ni distribuciones históricas.
- **FR-011**: Todo miembro DEBE poder retirar un participante sin cuenta de operaciones futuras sin
  eliminarlo de gastos históricos.
- **FR-012**: Todo miembro DEBE poder registrar un gasto con nombre, monto total positivo en ARS,
  categoría, fecha, pagador, tipo y descripción opcional. El catálogo cerrado del MVP DEBE contener
  Alimentos, Transporte, Vivienda, Servicios, Salud, Educación, Ocio y Otros.
- **FR-013**: Si no se indica fecha, el gasto DEBE usar la fecha calendario vigente en Argentina.
- **FR-014**: Cada gasto DEBE conservar uno de tres tipos: personal, compartido en partes iguales o
  compartido con distribución personalizada. El tipo personal DEBE asignar automáticamente el
  monto total al pagador y no generar deuda del pagador consigo mismo.
- **FR-015**: La división equitativa DEBE asignar el monto total entre las personas seleccionadas
  con diferencias máximas de un centavo.
- **FR-016**: Los residuos de la división equitativa DEBEN asignarse de forma repetible, un centavo
  por vez, a las primeras personas según el orden de selección.
- **FR-017**: La distribución personalizada DEBE permitir indicar la parte exacta de cada persona.
- **FR-018**: El producto DEBE rechazar partes negativas, importes con más de dos decimales y
  distribuciones cuya suma no coincida exactamente con el monto total.
- **FR-019**: El detalle del gasto DEBE mostrar la parte exacta asignada a cada persona.
- **FR-020**: Para cada persona distinta del pagador, el producto DEBE calcular como deuda con el
  pagador su parte asignada; la parte del pagador no genera deuda consigo mismo.
- **FR-021**: Todo miembro DEBE poder consultar el listado de gastos de su tablero, ordenado por
  fecha descendente, luego por instante de creación descendente y finalmente por identificador
  ascendente como desempate estable.
- **FR-022**: Todo miembro DEBE poder consultar nombre, monto, categoría, descripción si existe,
  fecha, pagador, tipo, distribución y deudas de un gasto.
- **FR-023**: Todo miembro DEBE poder editar un gasto y el producto DEBE recalcular sus partes,
  deudas, agrupaciones y totales mensuales afectados.
- **FR-024**: Todo miembro DEBE poder eliminar un gasto sólo después de confirmar la operación; la
  eliminación DEBE actualizar todos los totales afectados.
- **FR-025**: Todo miembro DEBE poder iniciar y reconocer el estado de una captura de audio y usar
  archivos WAV, MP3, M4A/MP4, WebM u Ogg; cualquier otro contenedor DEBE rechazarse antes del
  procesamiento sin crear una propuesta ni un gasto.
- **FR-026**: El producto DEBE intentar extraer del audio nombre, monto, categoría, fecha,
  descripción, tipo, pagador y participantes cuando estén expresados.
- **FR-027**: El procesamiento de audio DEBE generar una propuesta de gasto sin registrarla.
- **FR-028**: Una propuesta incompleta DEBE permanecer editable, identificar campos obligatorios
  faltantes y no poder confirmarse mientras sea inválida.
- **FR-029**: Todo miembro DEBE poder revisar la totalidad de una propuesta antes de registrarla.
- **FR-030**: Todo miembro DEBE poder modificar cualquier campo de la propuesta.
- **FR-031**: Sólo la confirmación explícita de una propuesta completa y válida DEBE crear
  exactamente un gasto.
- **FR-032**: Todo miembro DEBE poder consultar por período mensual los gastos agrupados por
  categoría, el importe de cada categoría y el total del período.
- **FR-033**: Todo miembro DEBE poder definir un único disponible base en ARS para cada tablero y
  período mensual.
- **FR-034**: Todo miembro DEBE poder modificar el disponible base y ver recalculado el restante.
- **FR-035**: El dinero consumido de un período DEBE ser la suma exacta de los montos totales de
  gastos y los importes en ARS de compras de USD fechados en ese período, sin usar las partes para
  reducir o duplicar el total.
- **FR-036**: Cuando existe un disponible base, el dinero restante DEBE ser el disponible base
  menos el dinero consumido y DEBE admitir resultados negativos. Cuando no existe, el producto
  DEBE seguir mostrando el consumido y marcar el restante como “no disponible”, sin asumir ni
  crear una base de ARS 0,00.
- **FR-037**: Todo miembro DEBE poder registrar un único ahorro inicial en USD por tablero.
- **FR-038**: Todo miembro DEBE poder editar el ahorro inicial sin crear registros iniciales
  duplicados.
- **FR-039**: Todo miembro DEBE poder eliminar el ahorro inicial.
- **FR-040**: Todo miembro DEBE poder registrar una compra con cantidad positiva de USD, importe
  positivo utilizado en ARS y fecha.
- **FR-041**: Si no se indica fecha, la compra de USD DEBE usar la fecha calendario vigente en
  Argentina.
- **FR-042**: Todo miembro DEBE poder editar una compra de USD y actualizar los totales del período
  original y del nuevo cuando cambie la fecha.
- **FR-043**: Todo miembro DEBE poder eliminar una compra de USD y actualizar los totales afectados.
- **FR-044**: El importe en ARS de cada compra DEBE sumarse al dinero consumido del período de su
  fecha; la cantidad en USD NO DEBE sumarse al consumo en ARS.
- **FR-045**: El total de ahorros DEBE ser el ahorro inicial vigente más las cantidades en USD de
  todas las compras vigentes del tablero.
- **FR-046**: Todo miembro DEBE poder consultar las compras de USD y su total en USD filtrados por
  período mensual, ordenados por fecha de compra descendente, luego por instante de creación
  descendente y finalmente por identificador ascendente como desempate estable.
- **FR-047**: Toda lectura, creación, modificación o eliminación de recursos de un tablero DEBE
  exigir que el usuario sea miembro de ese tablero; un rechazo no debe revelar datos ni cambiar
  el estado.
- **FR-048**: Todos los miembros de un tablero DEBEN tener las mismas capacidades dentro del MVP;
  el producto NO DEBE introducir roles diferenciados.
- **FR-049**: Todos los importes DEBEN conservar precisión de centavos y producir resultados
  exactos y deterministas para una misma entrada y orden de personas.
- **FR-050**: Todo dato confirmado DEBE persistir hasta que un miembro autorizado lo modifique o
  elimine explícitamente.

### Quality Requirements and Constraints

- **NFR-001 — Persistencia**: El 100% de cuentas, membresías, participantes, gastos, disponibles
  mensuales y ahorros confirmados DEBE conservarse después de reiniciar el servicio.
- **NFR-002 — Accesibilidad de carga**: Desde la pantalla principal del tablero, abrir un nuevo
  gasto DEBE requerir como máximo una interacción.
- **NFR-003 — Matriz adaptable**: El 100% de las pantallas cubiertas por los criterios DEBE ser
  operable, en orientación vertical y zoom del 100%, a 390 × 844 píxeles en Safari sobre iOS 14 y
  a 360 × 800 píxeles en Chrome sobre Android 12, sin desplazamiento horizontal, contenido
  cortado ni controles inaccesibles.
- **NFR-004 — Precisión de audio**: Al menos 12 de 20 audios consentidos y no sensibles de un
  conjunto fijo en español de Argentina DEBEN coincidir en todos los valores esperados presentes.
  Los 20 archivos, su manifiesto, hashes y valores esperados DEBEN quedar congelados antes de
  implementar o ajustar las reglas de extracción.
- **NFR-005 — Protección de credenciales**: La cantidad de credenciales de autenticación
  almacenadas o expuestas en texto plano DEBE ser cero.
- **NFR-006 — Inicio de sesión oportuno**: En 100 intentos válidos con 5 usuarios concurrentes,
  después de 10 intentos de calentamiento, al menos 95 DEBEN completarse en 4 segundos o menos en
  un entorno fijo de 2 vCPU y 4 GB de RAM sin llamadas externas.

### Scope Boundaries

Quedan fuera del MVP: integraciones automáticas con bancos, tarjetas, billeteras o Mercado Pago;
gestión o recomendación de inversiones; aplicaciones móviles nativas; cotizaciones automáticas
del dólar; conversión automática de ahorros USD a ARS; funciones contables o impositivas
avanzadas; recomendaciones avanzadas de IA; roles diferentes entre miembros; liquidación,
compensación, cobro o registro de pagos de deudas; y gestión avanzada de categorías. La IA del
MVP se limita a facilitar la propuesta revisable de un gasto desde audio.

### Key Entities *(include if feature involves data)*

- **Cuenta**: Identidad de una persona usuaria; posee un nombre visible, un email único, credencial
  protegida y mecanismos de sesión y recuperación. Al seleccionar personas se muestra el nombre y,
  cuando existen homónimos, también el email para desambiguarlas.
- **Tablero**: Contenedor colaborativo de membresías, participantes, gastos, disponibles mensuales
  y ahorros; constituye el límite de autorización y propiedad de datos.
- **Membresía**: Relación única entre una cuenta y un tablero; todos sus miembros tienen las mismas
  capacidades en el MVP.
- **Código de invitación**: Valor compartible asociado a un tablero que permite incorporar cuentas
  autenticadas como miembros varias veces durante los 7 días calendario posteriores a su emisión.
  El tablero mantiene un único código vigente y, al vencer, un miembro puede obtener uno nuevo.
- **Participante sin cuenta**: Persona representada sólo dentro de un tablero; puede pagar o recibir
  partes, no puede autenticarse y puede retirarse de operaciones futuras sin perder su historial.
- **Gasto**: Movimiento en ARS con nombre, monto total, categoría, fecha, pagador, tipo,
  descripción opcional y una distribución exacta entre personas del tablero.
- **Parte asignada**: Importe de un gasto correspondiente a una persona; todas las partes del gasto
  suman exactamente su monto total.
- **Deuda con el pagador**: Parte asignada a una persona distinta del pagador que debe devolverle;
  es informativa y no representa un pago o liquidación.
- **Disponible mensual**: Importe base en ARS de un tablero para un mes calendario de Argentina.
- **Resumen mensual**: Valores derivados de movimientos del período: consumido, restante y gastos
  agrupados por categoría.
- **Ahorro inicial**: Único importe base en USD vigente para el tablero.
- **Compra de USD**: Movimiento con cantidad adquirida en USD, importe utilizado en ARS y fecha;
  aumenta ahorros en USD y consumo mensual en ARS.
- **Propuesta de audio**: Borrador editable, completo o incompleto, que no altera el estado
  financiero hasta su confirmación explícita.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de los 60 escenarios de aceptación definidos en esta especificación produce
  el resultado observable indicado sin cálculos monetarios discrepantes.
- **SC-002**: El 100% de las distribuciones válidas suma exactamente el total del gasto y repetir
  una misma división equitativa conserva la misma asignación de centavos.
- **SC-003**: El 100% de los intentos probados de lectura o mutación por un usuario autenticado no
  miembro es rechazado sin exponer datos ni alterar el recurso.
- **SC-004**: El 100% de los datos confirmados del conjunto de persistencia conserva sus valores
  después de un reinicio.
- **SC-005**: El conjunto fijo contiene exactamente 20 archivos de audio consentidos y no sensibles
  cuyos hashes coinciden con el manifiesto congelado antes de implementar o ajustar la extracción;
  al menos 12 coinciden en todos los datos relevantes esperados y el 100% de las propuestas
  requiere confirmación antes de crear un gasto.
- **SC-006**: El 100% de las pantallas evaluadas en la matriz móvil definida puede operarse sin
  desplazamiento horizontal, contenido cortado ni controles inaccesibles.
- **SC-007**: Abrir la carga de un gasto desde la pantalla principal requiere como máximo una
  interacción en el 100% de las pruebas.
- **SC-008**: Al menos 95 de 100 inicios de sesión válidos bajo la carga y entorno definidos se
  completan en 4 segundos o menos.
- **SC-009**: Cero credenciales de autenticación se encuentran almacenadas o expuestas en texto
  plano durante la evaluación de seguridad.
- **SC-010**: Al menos 4 de 5 usuarios representativos completan sin asistencia los flujos de
  registrar un gasto compartido, consultar el restante mensual y revisar una propuesta de audio.

## Assumptions

- El MVP usa el mes calendario y la fecha vigente de Argentina para períodos y fechas omitidas.
- Los montos de gastos y disponibles se expresan en ARS; ahorro inicial y cantidades compradas se
  expresan en USD. Ambas monedas admiten centavos y no se convierten automáticamente entre sí.
- Todos los miembros de un tablero tienen las mismas capacidades; no existe rol de propietario o
  administrador dentro del MVP.
- Un participante sin cuenta nunca accede al producto y sólo existe dentro del tablero donde fue
  creado.
- Una contraseña válida tiene al menos 8 caracteres. El mecanismo de recuperación es personal,
  válido durante 30 minutos desde su emisión y de un solo uso.
- Los centavos residuales de una división equitativa se asignan según el orden estable de selección
  de personas, comenzando por la primera.
- Las categorías disponibles son Alimentos, Transporte, Vivienda, Servicios, Salud, Educación,
  Ocio y Otros; crear, editar, eliminar o reordenar categorías queda fuera de alcance.
- La eliminación de participantes conserva referencias históricas; la eliminación de gastos y
  compras elimina el movimiento de consultas y cálculos vigentes tras una confirmación aplicable.
- El procesamiento de audio y el envío de recuperaciones por email son dependencias externas al
  comportamiento de negocio, pero ninguna de ellas puede omitir la revisión, autorización o
  validación exigida por esta especificación.
- No se gestionan pagos de deudas entre personas: sólo se calcula y muestra cuánto corresponde
  devolver al pagador.
