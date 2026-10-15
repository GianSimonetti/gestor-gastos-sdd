<!--
Sync Impact Report
- Version change: unratified scaffold -> 1.0.0
- Modified principles:
  - Placeholder Principle 1 -> I. Test-first para reglas de negocio críticas
  - Placeholder Principle 2 -> II. Exactitud monetaria y determinismo
  - Placeholder Principle 3 -> III. Seguridad y aislamiento entre tableros
  - Placeholder Principle 4 -> IV. Separación de responsabilidades
  - Placeholder Principle 5 -> V. Alcance gobernado por requisitos
- Added sections:
  - Restricciones técnicas y de producto
  - Flujo de desarrollo y puertas de calidad
  - Reglas completas de gobierno
- Removed sections: none; all scaffold sections were concretized
- Follow-up TODOs: none
-->
# Constitución de Gestor Gastos

## Core Principles

### I. Test-first para reglas de negocio críticas

Toda lógica crítica y determinista DEBE definirse primero mediante tests que fallen y luego
implementarse hasta dejarlos en verde. Esto incluye, como mínimo, cálculos monetarios,
distribuciones de gastos, disponible mensual, permisos y validaciones de dominio. Cada cambio
en estas reglas DEBE aportar evidencia del ciclo rojo-verde. El código puramente visual o
trivial queda exento de TDD estricto cuando no contiene decisiones de negocio.

Rationale: los tests previos hacen explícito el comportamiento esperado y evitan regresiones
en las reglas que afectan dinero, acceso y consistencia de datos.

### II. Exactitud monetaria y determinismo

Todos los importes y cálculos monetarios DEBEN usar representaciones exactas; el uso de
`float` para dinero está prohibido. Las reglas de distribución, redondeo y asignación de
residuos de centavos DEBEN estar documentadas, ser deterministas y estar cubiertas por tests.
La misma entrada, incluido el mismo orden de participantes, DEBE producir exactamente el mismo
resultado.

Rationale: una aplicación financiera no puede introducir errores binarios ni resultados
variables que impidan reconciliar saldos y gastos.

### III. Seguridad y aislamiento entre tableros

Un usuario sólo PUEDE consultar o modificar recursos de tableros a los que pertenece. Cada
operación protegida DEBE validar autorización en el backend, independientemente de los
controles del frontend. Los intentos de acceso cruzado DEBEN rechazarse sin revelar datos del
recurso. Ningún secreto, token o credencial PUEDE estar hardcodeado ni versionado.

Rationale: el aislamiento por tablero protege la confidencialidad e integridad de los datos
entre usuarios y no puede depender de una interfaz manipulable.

### IV. Separación de responsabilidades

La lógica de negocio crítica DEBE permanecer separada de las capas de transporte, interfaz y
persistencia cuando corresponda. El backend es la fuente de verdad para permisos,
validaciones de dominio y cálculos críticos. El frontend PUEDE presentar cálculos auxiliares
para mejorar la experiencia, pero NO DEBE definir ni reemplazar las reglas autoritativas.

Rationale: separar reglas y adaptadores permite probar el dominio de forma determinista,
reutilizarlo y evitar divergencias entre clientes.

### V. Alcance gobernado por requisitos

Toda funcionalidad implementada DEBE estar respaldada por el PRD y las specs vigentes. El
agente NO DEBE agregar por iniciativa propia funciones, integraciones o comportamientos fuera
de ese alcance. Todo cambio funcional nuevo DEBE definirse y aprobarse explícitamente en los
artefactos de requisitos antes de implementarse.

Rationale: un alcance trazable reduce complejidad accidental y mantiene las decisiones de
producto bajo control humano.

## Restricciones técnicas y de producto

- El frontend DEBE implementarse con React y sus paquetes DEBEN gestionarse con npm.
- El backend DEBE usar Python 3.12, FastAPI y JWT; sus dependencias DEBEN gestionarse con uv.
- La persistencia base DEBE usar SQLite y SQLAlchemy. Adoptar Supabase requiere una decisión
  explícita en el PRD o la spec correspondiente.
- Los tests del backend DEBEN ejecutarse con pytest.
- La solución NO DEBE integrar automáticamente bancos, tarjetas, billeteras virtuales ni
  Mercado Pago, ni crear aplicaciones móviles nativas, salvo una enmienda explícita de alcance.
- El soporte de audio permanece sin definir y NO DEBE implementarse hasta que una spec vigente
  establezca su comportamiento.

## Flujo de desarrollo y puertas de calidad

1. Antes de implementar, cada cambio funcional DEBE vincularse con un requisito y criterios de
   aceptación vigentes.
2. Las reglas alcanzadas por el Principio I DEBEN comenzar con tests fallidos observables; la
   implementación sólo se considera completa cuando esos tests pasan.
3. Los cambios monetarios DEBEN incluir casos de borde para precisión, redondeo, residuos y
   repetibilidad. Los cambios de acceso DEBEN incluir casos permitidos y denegados entre
   tableros.
4. La revisión DEBE comprobar que las reglas autoritativas permanecen en el backend o en la
   capa de dominio correspondiente y que no se duplican como fuente de verdad en la interfaz.
5. Antes de integrar un cambio, `cd backend && uv run pytest` DEBE pasar cuando exista impacto
   en el backend, y `cd frontend && npm run build` DEBE pasar cuando exista impacto en el
   frontend. Cualquier excepción DEBE documentarse con su causa y riesgo.
6. La revisión final DEBE verificar ausencia de secretos versionados y conformidad con el
   alcance aprobado.

## Governance

Esta constitución prevalece sobre prácticas, convenciones y decisiones técnicas incompatibles
del proyecto. El PRD y las specs gobiernan el comportamiento funcional; esta constitución
gobierna las restricciones persistentes bajo las cuales se define e implementa ese
comportamiento.

Toda enmienda DEBE documentar el cambio, su motivación, su impacto sobre artefactos existentes
y cualquier plan de migración necesario. La aprobación explícita del responsable del proyecto
es obligatoria antes de que la enmienda entre en vigor.

Las versiones siguen Semantic Versioning: MAJOR para eliminar o redefinir de manera
incompatible principios o reglas de gobierno; MINOR para añadir principios, secciones o ampliar
materialmente obligaciones; PATCH para aclaraciones y correcciones sin cambio semántico. La
fecha de última enmienda DEBE actualizarse en toda modificación efectiva.

Cada spec, plan, conjunto de tareas y revisión de código DEBE comprobar el cumplimiento de los
principios aplicables. Toda desviación DEBE quedar explícitamente justificada y aprobada; una
desviación que contradiga un principio requiere primero enmendar esta constitución.

**Version**: 1.0.0 | **Ratified**: 2026-10-15 | **Last Amended**: 2026-10-15
