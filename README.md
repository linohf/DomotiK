# DomotiK

Prueba local de Home Assistant Container en Ubuntu con Docker Engine y Compose.
Google Home continúa siendo el centro de voz existente. Esta instalación no
importa automáticamente los dispositivos vinculados a Google Home.

## Abrir y configurar

En este PC: <http://localhost:8123>.
Desde un teléfono en la misma red: `http://IP_DEL_PC:8123`.
Consulta la dirección Wi-Fi/Ethernet actual con `ip -brief address`.

1. Selecciona **Crear mi hogar** y crea tu usuario administrador y contraseña.
2. Revisa la ubicación y la zona horaria (America/Santiago).
3. En **Ajustes → Dispositivos y servicios → Añadir integración**, conecta
   primero un equipo y comprueba su funcionamiento.
4. Configura respaldos en **Ajustes → Sistema → Copias de seguridad**. Descarga
   una copia y el kit de emergencia con la clave de cifrado fuera de este PC.

El servicio comparte la red del PC para facilitar el descubrimiento local.
Escucha en el puerto 8123 de sus interfaces, incluidas las VPN que tenga el PC,
sujeto al firewall. No se configura publicación en internet ni se cambia el router.
El PC debe permanecer encendido, sin suspensión y conectado a la red doméstica.

## Equipos de la prueba

| Ecosistema | Cómo probarlo |
| --- | --- |
| Eye4 / cámaras | ONVIF o Generic Camera con RTSP, si el modelo lo admite. Usar la cuenta local de la cámara; no asumir que coincide con la de Eye4. |
| eWeLink / interruptores | SonoffLAN v3.13.2 está preparado como integración comunitaria. Buscar **Sonoff** en Añadir integración y vincular la cuenta eWeLink. La compatibilidad y el control local dependen del modelo. |
| Domotikapp / estufas | Confirmar modelo y compatibilidad con Tuya/Smart Life. No reiniciar ni cambiar su vinculación solo por usar esa aplicación. |
| Tuya / alarma | Añadir Tuya mediante el QR de la aplicación y comprobar qué funciones expone la central. |
| Tuya / chapa | La integración oficial no soporta la plataforma lock; no asumir que abrir/cerrar estará disponible. |
| SmartThings | Solo importa equipos expuestos por SmartThings, no todos los de Google Home. Revisar condiciones actuales de acceso a su API. |

Las cuentas se vinculan desde la interfaz; no guardar contraseñas en Compose
ni en este repositorio. La primera prueba de alarma/chapa será comprobar estados.
Todavía no hay automatizaciones de apertura, desarmado ni calefacción.

## Operación

Ejecutar desde la carpeta de este proyecto:

```bash
docker compose up -d
docker compose ps
docker compose logs --tail=100 homeassistant
docker compose stop
docker compose start
```

`docker compose down` elimina el contenedor, pero conserva `data/homeassistant`.
No borrar esa carpeta: contiene la instalación, usuarios, integraciones y respaldos locales.
El reinicio automático se aplica cuando arranca Docker, salvo que hayas detenido
el contenedor explícitamente.

La versión está fijada en `compose.yaml` para no actualizar accidentalmente.
Para actualizar: crear un respaldo, revisar las notas de la versión, cambiar
la etiqueta de imagen y ejecutar:

```bash
docker compose pull
docker compose up -d
```

Una vuelta a una versión anterior puede necesitar restaurar el respaldo previo
a la actualización. No hay actualizaciones automáticas configuradas.

## Reproducir en una instalación nueva

Requiere Linux con Docker Engine y Docker Compose; puerto 8123 disponible.
Crear `data/homeassistant` y copiar `configuration.example.yaml` como
`data/homeassistant/configuration.yaml` solo si no existe configuración activa.
Crear también `automations.yaml` y `scenes.yaml` con `[]`, y `scripts.yaml` con `{}`,
dentro de esa carpeta. Después ejecutar `docker compose up -d`.

Para preparar también SonoffLAN antes del primer arranque:

```bash
python3 scripts/install-sonoff.py
```

El script descarga la versión fijada desde el repositorio del autor y no
sobrescribe instalaciones existentes. Si Home Assistant ya estaba iniciado,
reiniciarlo después con `docker compose restart homeassistant`.
SonoffLAN se mantiene manualmente; no se instala HACS ni se modifica el firmware.

La configuración inicial guarda siete días de histórico. Los logs de Docker
rotan en tres archivos de 10 MB. No se configura grabación de cámaras.
Revisar espacio con `df -h .`: históricos y respaldos pueden crecer.

Esta prueba usa dispositivos de red: no monta USB ni D-Bus y no ejecuta el
contenedor con `privileged`. Bluetooth y radios Zigbee/Z-Wave requerirán
configuración adicional. Container no incluye el gestor de apps de Home Assistant OS.
Los servicios se declaran explícitamente en `configuration.example.yaml`, sin
`default_config`, para evitar el arranque de Bluetooth/USB. Al actualizar, revisar
si interesa incorporar nuevos servicios que añada la configuración predeterminada.

## Migración

Crear un respaldo desde Home Assistant, descargarlo junto con su kit de emergencia,
instalar Home Assistant OS en el equipo de destino y restaurar durante el inicio.
Revisar direcciones IP, integraciones y radios. Apagar la instancia anterior antes
de activar automatizaciones en el destino para evitar ejecuciones duplicadas.

## Referencias

- [Instalación oficial en Linux](https://www.home-assistant.io/installation/linux/)
- [SonoffLAN: instalación y compatibilidad](https://github.com/AlexxIT/SonoffLAN)
- [Tuya](https://www.home-assistant.io/integrations/tuya/)
- [ONVIF](https://www.home-assistant.io/integrations/onvif/)
- [Generic Camera](https://www.home-assistant.io/integrations/generic/)
- [Respaldos y migración](https://www.home-assistant.io/common-tasks/general/backups/)
