# HU-WEB-ROLE-001 - Validacion Final

Fecha local: 2026-09-22

## Resultado

PASS. El usuario reviso el resumen y confirmo:

```text
por el momento lo veo bien
```

## Baseline Aprobada

Archivo aprobado como baseline inicial:

```text
project/product/web-role-screen-matrix.yaml
```

Estado actualizado:

```text
status: APPROVED_BASELINE
```

## Roles Incluidos

- `admin`: administra tenants, usuarios, invernaderos, dispositivos e integraciones.
- `farmer`: consulta estado del cultivo, alertas, tareas y registra observaciones.
- `agronomist`: analiza datos, aprueba/rechaza recomendaciones y deja trazabilidad tecnica.
- `technician`: instala, mantiene y diagnostica sensores, conectividad y dispositivos.
- `owner`: revisa operacion global, adopcion, clientes, reportes y salud del negocio.

## Pantallas Base

- Publicas: `/`, `/login`.
- Compartidas privadas: `/app`, invernadero, alertas, evidencia y Agro Expert Chat.
- Propias por rol: administracion, dashboard agricultor, aprobaciones agronomo, dispositivos tecnico, dashboard owner.

## Reglas De Seguridad

- Toda ruta `/app/**` requiere autenticacion.
- Todo dato privado debe resolverse con `tenant_id` en backend.
- El frontend no es fuente de seguridad.
- Acciones fisicas, cambios sensibles y aprobaciones criticas requieren trazabilidad.

## Trabajo Siguiente

`HU-WEB-IA-001`: definir arquitectura de informacion y navegacion privada sobre esta matriz.
