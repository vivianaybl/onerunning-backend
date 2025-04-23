
# 📘 Documentación Técnica - Prueba Backend

## 🎯 Objetivo de la prueba

Implementar un backend en Django REST Framework que permita:
- Registrar dispositivos con validación personalizada.
- Sincronizar entrenamientos en segundo plano usando Celery.
- Exponer endpoints RESTful para Device y Training.
- Validar la lógica con pruebas automatizadas.
- Organizar el código de forma modular y escalable.

---

## 🧱 Estructura del Proyecto

```
one_running_test/
├── devices/
│   ├── models.py          # Modelos Device y Training
│   ├── serializers.py     # Serializadores DRF
│   ├── views.py           # Vistas DRF + endpoints personalizados
│   ├── tasks.py           # Tareas en segundo plano con Celery
│   ├── tests.py           # Pruebas unitarias
│   ├── urls.py            # Enrutamiento local
├── config/
│   ├── settings.py        # Configuración del proyecto
│   ├── celery.py          # Configuración de Celery
│   └── __init__.py        # Inicializa la app Celery
```

---

## 🔌 Endpoints de la API

| Método | Endpoint                     | Acción                             |
|--------|------------------------------|------------------------------------|
| GET    | /devices/                    | Listar dispositivos                |
| POST   | /devices/                    | Crear dispositivo                  |
| POST   | /api/devices/authorize/      | Autorizar dispositivo              |
| POST   | /api/trainings/sync/         | Iniciar sincronización (Celery)    |
| GET    | /trainings/                  | Listar entrenamientos              |
| POST   | /trainings/                  | Crear entrenamiento                |

---

## ⚙️ Tareas en Segundo Plano (Celery)

La tarea `sync_trainings` recorre los dispositivos autorizados y crea entrenamientos ficticios.

Configuración en `settings.py`:

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'America/Bogota'
```

---

## 🧪 Pruebas

```bash
python manage.py test devices
```

Casos cubiertos:
- Autorización de dispositivo
- Prevención de duplicados
- Disparo de tareas Celery
- Creación de entrenamientos

---

## 🚀 Cómo ejecutar el proyecto desde GitHub

### 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/repositorio.git
cd repositorio
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar base de datos

Modificar `settings.py` con tus credenciales de MySQL.

```bash
python manage.py migrate
```

### 4. Ejecutar el servidor

```bash
python manage.py runserver
```

### 5. Ejecutar Celery

Asegúrate de que Redis esté corriendo, luego:

```bash
celery -A config worker --loglevel=info
```

---

## ✅ Verificación

- Revisar los endpoints con Postman o navegador.
- Disparar sincronización con: `POST /api/trainings/sync/`
- Verificar logs de tareas en la terminal de Celery.

---
