# Implementation Plan: Gestor de Gastos MVP

**Branch**: `001-gestor-gastos-mvp` | **Date**: 2026-10-15 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-gestor-gastos-mvp/spec.md`

**Note**: El plan finaliza en diseño de Fase 1. Las tareas de implementación se generan por
separado con `$speckit-tasks`.

## Summary

Construir una aplicación web responsive para que usuarios autenticados colaboren dentro de
tableros, registren y distribuyan gastos, controlen el disponible mensual, administren ahorros en
USD y generen propuestas revisables desde audio. La solución será un monolito modular con frontend
React en JavaScript y backend FastAPI síncrono. La lógica crítica residirá en servicios y objetos de
dominio puros, con dinero representado como centavos enteros, persistencia SQLAlchemy/SQLite y
autorización por membresía aplicada en cada caso de uso.

La arquitectura evita componentes distribuidos, cachés, colas y gestores de estado global. Las dos
integraciones inevitables quedan detrás de puertos pequeños: SMTP para recuperación por email y
transcripción local con `faster-whisper` para audio. La extracción posterior del gasto será
determinista y toda propuesta requerirá revisión y confirmación antes de crear un movimiento.

## Technical Context

**Language/Version**: Python 3.12 en backend; JavaScript moderno con JSX en frontend, sin
TypeScript

**Primary Dependencies**: FastAPI, Pydantic, SQLAlchemy 2.x, PyJWT, `pwdlib[argon2]`, pytest y
`faster-whisper`; React, React DOM, React Router y Vite gestionados con npm

**Storage**: SQLite mediante SQLAlchemy; importes persistidos como enteros de centavos; archivos de
audio sólo temporales durante el procesamiento

**Testing**: pytest para dominio, aplicación, persistencia, contratos HTTP, seguridad, evaluación
de audio y prueba opt-in de rendimiento; build de frontend, validación manual de la matriz móvil y
evaluación de usabilidad sin asistencia con cinco usuarios representativos

**Target Platform**: Aplicación web responsive; backend en un único proceso/instancia; frontend
compatible con Safari en iOS 14 a 390 × 844 y Chrome en Android 12 a 360 × 800

**Project Type**: Aplicación web con frontend y backend separados dentro del mismo repositorio

**Performance Goals**: Al menos 95 de 100 inicios de sesión válidos, con 5 usuarios concurrentes,
completados en 4 segundos o menos tras 10 solicitudes de calentamiento en 2 vCPU/4 GB RAM

**Constraints**: Cálculos monetarios sin `float`; autorización backend por tablero; exactitud y
residuos deterministas; propuesta de audio nunca auto-confirmada; cero credenciales en texto plano;
sin bancos, billeteras, apps nativas, conversión USD/ARS, roles ni liquidación de deudas. El catálogo
cerrado usa los códigos `food`, `transport`, `housing`, `services`, `health`, `education`, `leisure`
y `other`, presentados como Alimentos, Transporte, Vivienda, Servicios, Salud, Educación, Ocio y
Otros.

**Scale/Scope**: MVP de una sola instancia con SQLite. El único compromiso de concurrencia es el
objetivo explícito de 5 inicios de sesión simultáneos; no se diseña escalado horizontal ni una
plataforma multi-servicio. Los listados de gastos se ordenan por fecha descendente, creación
descendente e ID ascendente; las compras de USD usan el mismo criterio con su fecha de compra. Ambos
se paginan desde el inicio para evitar acoplar el contrato al volumen real.

**Audio inputs**: Se admiten contenedores WAV, MP3, M4A/MP4, WebM y Ogg hasta 60 segundos y 15 MB.
Los demás se rechazan antes de transcribir. Los 20 archivos consentidos y no sensibles del corpus,
su manifiesto, hashes y valores esperados se congelan antes de implementar o ajustar el extractor.

## Constitution Check

*GATE: Debe aprobar antes de Fase 0 y se reevalúa después del diseño de Fase 1.*

### Evaluación previa a investigación

| Principio | Estado | Evidencia del plan |
|-----------|--------|--------------------|
| I. Test-first para reglas críticas | PASS | Dinero, distribución, disponible, autorización y validaciones comienzan con tests pytest fallidos de dominio/servicio. |
| II. Exactitud monetaria y determinismo | PASS | HTTP usa strings decimales; dominio y SQLite usan centavos enteros; residuos siguen el orden estable de selección. |
| III. Seguridad y aislamiento | PASS | Cada caso de uso valida membresía; secretos provienen del entorno; contraseñas y tokens recuperables no se guardan en texto plano. |
| IV. Separación de responsabilidades | PASS | Routers, casos de uso, dominio e infraestructura están separados; frontend consume resultados autoritativos. |
| V. Alcance gobernado | PASS | El diseño cubre sólo el spec; no agrega integraciones financieras, roles, pagos de deuda ni gestión avanzada de categorías. |
| Stack y puertas de calidad | PASS | React/JavaScript/npm, Python 3.12/FastAPI/uv, SQLite/SQLAlchemy y pytest coinciden con la constitución. |

No existen violaciones que requieran excepción. `faster-whisper` es la dependencia adicional mínima
para satisfacer el registro por audio sin incorporar un servicio externo de IA; SMTP es inevitable
para entregar recuperaciones por email y permanece proveedor-agnóstico.

### Reevaluación posterior al diseño

| Gate | Estado | Evidencia de Fase 1 |
|------|--------|---------------------|
| Reglas críticas testeables fuera del transporte | PASS | `data-model.md` separa valores derivados; `research.md` fija servicios de dominio puros; `quickstart.md` exige tests rojos/verdes. |
| Exactitud de almacenamiento y contratos | PASS | Todos los importes se modelan como `*_cents` y se exponen como strings de dos decimales en `contracts/openapi.yaml`. |
| Aislamiento por tablero | PASS | Las relaciones incluyen `board_id`; los contratos anidan recursos bajo tablero y normalizan respuestas no autorizadas. |
| Simplicidad | PASS | Un backend, un frontend y una base; sin broker, worker, caché, CQRS, Redux, librería de gráficos ni servicio de IA remoto. |
| Alcance y trazabilidad | PASS | Contratos, entidades y escenarios remiten exclusivamente a FR/NFR y aclaraciones vigentes. |

## Project Structure

### Documentation (this feature)

```text
specs/001-gestor-gastos-mvp/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── openapi.yaml
├── checklists/
│   └── requirements.md
└── tasks.md                 # Se crea posteriormente con $speckit-tasks
```

### Source Code (repository root)

```text
backend/
├── pyproject.toml
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── schemas/
│   │   └── routers/
│   │       ├── auth.py
│   │       ├── boards.py
│   │       ├── people.py
│   │       ├── expenses.py
│   │       ├── monthly.py
│   │       ├── savings.py
│   │       └── audio.py
│   ├── application/
│   │   ├── auth_service.py
│   │   ├── board_service.py
│   │   ├── expense_service.py
│   │   ├── monthly_service.py
│   │   ├── savings_service.py
│   │   └── audio_service.py
│   ├── domain/
│   │   ├── money.py
│   │   ├── expenses.py
│   │   ├── monthly.py
│   │   ├── savings.py
│   │   └── errors.py
│   ├── db/
│   │   ├── base.py
│   │   ├── models.py
│   │   └── session.py
│   ├── infrastructure/
│   │   ├── repositories.py
│   │   ├── email.py
│   │   ├── transcription.py
│   │   └── speech_extractor.py
│   └── core/
│       ├── config.py
│       ├── security.py
│       └── clock.py
└── tests/
    ├── unit/
    ├── integration/
    ├── api/
    ├── performance/
    └── fixtures/audio-eval/

frontend/
├── package.json
├── vite.config.js
├── index.html
└── src/
    ├── main.jsx
    ├── app/
    │   ├── App.jsx
    │   └── router.jsx
    ├── pages/
    ├── features/
    │   ├── auth/
    │   ├── boards/
    │   ├── people/
    │   ├── expenses/
    │   ├── monthly/
    │   ├── savings/
    │   └── audio/
    ├── components/
    ├── lib/
    │   ├── api.js
    │   ├── money.js
    │   └── dates.js
    └── styles/
```

**Structure Decision**: Se adopta una aplicación web de dos proyectos. El backend es un monolito
modular síncrono: `api` adapta HTTP, `application` coordina transacciones y autorización, `domain`
contiene reglas puras e `infrastructure` implementa persistencia e integraciones. El frontend se
organiza por flujos de producto con utilidades compartidas pequeñas. No se crean paquetes comunes
entre JavaScript y Python; `contracts/openapi.yaml` es la frontera explícita.

## Complexity Tracking

No aplica: todos los gates constitucionales pasan sin excepciones.
