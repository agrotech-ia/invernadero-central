# Arquitectura AWS SaaS objetivo - Piloto evolutivo

Estado: DRAFT  
Fecha: 2026-08-24  
Owner: Solution / IoT Architect  
Reviewer: QA Engineer

## Decision base

La plataforma se disenara como SaaS multi-tenant desde el modelo de dominio, identidad y datos, pero el piloto se implementara con complejidad operativa minima.

Principio:

```text
Multi-tenant by design, pilot-light in execution.
```

Esto significa:

- Todo dato operacional relevante debe estar asociado a `tenant_id`, `greenhouse_id`, `actor_id` y timestamps.
- El primer despliegue puede operar con un solo tenant/invernadero.
- No se crean microservicios fisicos antes de tener limites de dominio, contratos y necesidad real de despliegue independiente.
- Los limites de servicios se definen desde el inicio para poder extraerlos despues.

## Estado AWS confirmado

Confirmado por humano:

- S3 para hosting/artefactos estaticos.
- CloudFront para distribucion.
- Route53 para DNS.
- AWS Certificate Manager para TLS.

Pendiente de formalizar:

- Nombres de buckets/distribuciones/dominios.
- Pipeline de despliegue.
- Ambientes: dev, staging, prod.
- Politica de cache/invalidation.
- WAF/security headers.

## Capas objetivo

### 1. Public Web

Proposito: vender la solucion, educar, generar interes y captar demos/leads.

AWS candidata:

- S3
- CloudFront
- Route53
- ACM
- CloudWatch
- WAF cuando exista exposicion publica real

### 2. Private Web App

Proposito: aplicacion privada por roles.

Roles iniciales:

- Admin / operador
- Agricultor
- Agronomo
- Tecnico / instalador
- Owner / empresa

Capacidades:

- Login.
- Seleccion de tenant/invernadero.
- Dashboard por rol.
- Alertas.
- Decisiones e historial.
- Chat agricola experto.

### 3. Identity & Access

AWS candidata:

- Amazon Cognito para autenticacion.
- Grupos/claims por rol.
- `tenant_id` como claim o resolucion server-side.
- IAM solo para servicios internos, no para permisos de usuario final.

Regla:

- Ningun endpoint privado debe depender solo del frontend para filtrar tenant.

### 4. Backend modular

Inicio recomendado:

- Un backend modular desplegado como ECS Fargate o Lambda/API Gateway, segun velocidad de implementacion y experiencia del equipo.
- Modulos internos con limites claros antes de extraer microservicios.

Modulos:

- Identity facade / user profile
- Tenant & organization
- Greenhouse management
- Device & sensor registry
- Telemetry query
- Alerts
- Agronomic decisions
- Evidence & reports
- Agro expert chat facade

Extraccion futura a microservicios cuando exista:

- escalado independiente;
- equipo/ownership separado;
- carga distinta;
- seguridad/aislamiento especial;
- contrato estable;
- dolor real de despliegue conjunto.

### 5. Data

Opcion relacional recomendada para piloto SaaS:

- Aurora PostgreSQL o PostgreSQL administrado cuando se formalice cloud.

Motivo:

- Usuarios, roles, invernaderos, dispositivos, alertas, decisiones y auditoria son relacionales.
- Permite evolucionar a schema-per-tenant si aparece cliente enterprise.

Opciones complementarias:

- DynamoDB para eventos de alta escala o lecturas agregadas si el volumen lo justifica.
- S3 para evidencia, reportes, documentos, exports y archivos de soporte.

Modelo inicial de aislamiento:

- Pool multi-tenant con `tenant_id` obligatorio.
- Evaluar bridge/silo cuando haya requisitos enterprise o regulados.

### 6. Telemetry & Events

Piloto:

- Edge local sigue siendo fuente primaria de pruebas.
- API/ingestor cloud recibe eventos cuando el contrato este validado.

AWS candidata:

- IoT Core o MQTT bridge cuando se formalice ingestion cloud.
- EventBridge para eventos de dominio.
- SNS para notificaciones fan-out.
- SQS para desacoplar procesamiento.
- Lambda para consumidores puntuales.
- ECS Fargate para procesos largos o servicios de ingestion si aplica.

Eventos candidatos:

- `telemetry.received`
- `sensor.status.changed`
- `alert.created`
- `recommendation.created`
- `decision.approved`
- `evidence.attached`

### 7. Agro Expert Chat

Separado del chat interno de proyecto.

Objetivo:

- Responder preguntas agricolas con contexto del tenant/invernadero/cultivo.
- Citar fuentes cientificas o tecnicas versionadas.
- Distinguir dato observado, inferencia y recomendacion.
- Escalar recomendaciones criticas a aprobacion de agronomo.

AWS candidata:

- S3 para documentos fuente.
- Vector store administrado a decidir.
- Lambda/ECS para orquestacion.
- CloudWatch para trazabilidad.

Reglas:

- No dar recomendaciones agronomicas criticas sin fuente, contexto y limites.
- No accionar control fisico.
- Registrar decisiones y aprobaciones.

## Roadmap tecnico AWS

### Fase A - SaaS foundation light

- Formalizar dominio, tenants, roles y permisos.
- Definir navegacion privada por rol.
- Definir contratos API iniciales.
- Publicar decision de arquitectura AWS.

### Fase B - Private app mock contractual

- Login simulado o Cognito si ya se decide cuenta/ambiente.
- Layout privado.
- Selector de invernadero.
- Dashboard por rol usando datos mock contractuales.

### Fase C - Backend modular

- Crear API base.
- Crear tablas/colecciones base.
- Implementar tenant/greenhouse/device registry.
- Alertas y decisiones en modo basico.

### Fase D - Telemetry cloud path

- Definir contrato de ingestion.
- Publicar lecturas desde edge o simulador.
- Persistir mediciones.
- Visualizar en dashboard.

### Fase E - Agro expert chat

- Curar fuentes iniciales.
- Crear RAG agricola.
- Integrar contexto de cultivo/invernadero.
- Implementar aprobaciones agronomicas.

## Riesgos

- Sobreingenieria por microservicios prematuros.
- Subingenieria por no modelar tenant desde el inicio.
- Costos AWS sin carga real.
- Seguridad de tenant basada solo en frontend.
- Recomendaciones agronomicas sin fuentes o sin contexto.

## Decisiones pendientes

- Cognito desde la primera version privada o login mock temporal.
- Backend inicial en Lambda/API Gateway o ECS Fargate.
- Aurora PostgreSQL vs PostgreSQL local/cloud inicial.
- Uso de IoT Core vs bridge MQTT propio.
- Vector store para Agro Expert Chat.
