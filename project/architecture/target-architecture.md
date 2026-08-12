# Arquitectura objetivo candidata — MVP

SENSORS / ACTUATORS
→ ESP32/XIAO nodes
→ WiFi / RS485 where applicable
→ MQTT
→ Raspberry Pi 5 Edge
   - Mosquitto
   - ingestion
   - PostgreSQL + TimescaleDB
   - API
   - rules/events
→ Web UI

VISION:
UGREEN cameras → Lenovo vision server → local images/YOLO → metadata REST → Raspberry/API

Principios:
- offline resilience;
- no imágenes por MQTT;
- datos contextualizados;
- fail-safe;
- configuración sobre hardcoding;
- observabilidad;
- control físico progresivo;
- contratos existentes se evolucionan.
