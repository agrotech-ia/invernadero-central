# Follow-ups de HUs Cerradas Con Limitaciones

Fecha: 2026-09-24

## Regla de cierre

Una HU puede quedar en `DONE` si cumple su alcance y criterios de aceptacion para MVP. Si el resultado es `PASS_WITH_LIMITATIONS`, cada limitacion relevante debe quedar registrada como una HU nueva, bug o hardening.

## Follow-ups creados

| ID | Origen | Motivo |
| --- | --- | --- |
| `HU-FW-HARDEN-NODE-FAMILY-LAB-001` | `HU-FW-MQTT-RESILIENCE-ALL-001` | El patron MQTT compila en SHT40/exterior, pero falta prueba fisica broker off/on por familia de nodo. |
| `HU-FW-CONFIG-PORTAL-ALL-001` | `HU-FW-CONFIG-001`, `HU-FW-CONFIG-PORTAL-001` | El cambio WiFi/MQTT sin USB quedo probado en suelo; falta portar/validar en SHT40 y exterior. |
| `HU-FW-RESET-REASON-HARDENING-001` | `HU-FW-WATCHDOG-001` | `reset_reason=unknown` es aceptable para MVP, pero no es suficiente para diagnostico fino de campo. |
| `HU-FW-DURABLE-OFFLINE-RETENTION-001` | `HU-FW-OFFLINE-RETENTION-001` | La retencion offline actual es volatil; no sobrevive perdida de energia del nodo. |
| `HU-SOIL-CALIBRATION-HARDENING-001` | `HU-SOIL-001` | Falta cerrar modelo exacto, verificacion formal electrica y calibracion contra referencia independiente. |

## Interpretacion

Estas HUs no reabren las historias cerradas. Las historias cerradas quedan aceptadas para el alcance MVP ya validado; estos follow-ups son el camino para pasar de "funciona para MVP" a "robusto para campo/productivo".
