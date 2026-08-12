# Invernadero Inteligente — Baseline local V1

Este repositorio materializa la planificación recuperada y completada hasta HU-009.

## Estado

- HU-001..HU-007: copias recuperadas completas de los archivos originales.
- HU-008: original recuperado + cierre con inventario físico V2 y correcciones aprobadas.
- HU-009: completada y congelada con Gap Analysis, V&V, agentes, mercado y backlog inicial.
- DEC-001..DEC-085: registro generado desde las HU recuperadas y decisiones de cierre.
- n8n: definido como orquestador local.
- Git: fuente de verdad.

## No usar

El ZIP `invernadero-inteligente-bootstrap.zip` anterior queda invalidado.

## Primer trabajo local

1. Inicializar Git.
2. Revisar `project/baselines/`.
3. Revisar `project/inventory/master-inventory-v2.yaml`.
4. Levantar EN-AGENT-001 en n8n.
5. Ejecutar el caso de prueba del sensor de suelo.
6. Continuar desde `project/backlog/master-backlog.yaml`.

## Regla de baseline

Una HU FROZEN no se edita silenciosamente. Todo cambio posterior debe quedar como nueva decisión,
enmienda explícita o nueva historia.
