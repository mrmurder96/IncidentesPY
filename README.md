# Sistema de Gestión de Incidencias - Cordillera

Aplicación de escritorio en **Python** para registrar y gestionar incidencias técnicas con vistas por rol:
- Administrador
- Agente
- Técnico

## Características principales

- Inicio de sesión con validación de usuarios.
- Registro y visualización de incidencias.
- Interfaces diferenciadas por perfil de usuario.
- Carga de datos desde archivos (`.csv` y `.json`).
- Interfaz gráfica con recursos visuales en la carpeta `Imagenes/`.

## Estructura del proyecto

- `Login.py`: pantalla de acceso al sistema.
- `FrameMarca.py`: componentes de interfaz y estructura principal.
- `ventana_incidencias_admin.py`: vista para administrador.
- `ventana_incidencias_agente.py`: vista para agente.
- `ventana_incidencias_tecnico.py`: vista para técnico.
- `cargar_archivos.py`: utilidades de carga de archivos.
- `informacion.csv`: datos de incidencias/información base.
- `user_data.json`: datos de usuarios.
- `Imagenes/`: íconos e imágenes de la aplicación.

## Requisitos

- Python 3.10 o superior (recomendado)
- Librerías usadas por la interfaz (según tu implementación)

> Si al ejecutar aparece algún error de dependencias, instala los paquetes faltantes con `pip install <paquete>`.

## Ejecución

1. Clona el repositorio:

```bash
git clone https://github.com/mrmurder96/IncidentesPY.git
cd IncidentesPY
```

2. Instala dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación principal:

```bash
python Login.py
```

## Flujo general

1. El usuario inicia sesión en `Login.py`.
2. Según el rol, el sistema abre la ventana correspondiente.
3. Se consultan y gestionan incidencias según permisos.

## Autor

Proyecto académico de la materia **Algoritmos**.

## Licencia

Uso académico/educativo.
