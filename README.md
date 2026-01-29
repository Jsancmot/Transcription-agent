# 🎤 AI Transcription Agent

Aplicación de transcripción de audio con API REST y **Groq LLM**. Gestiona automáticamente un historial de transcripciones.

## ✨ Features

- 🤖 **Agente inteligente con Function Calling** - Entiende lenguaje natural sin comandos específicos
- 🎯 **Transcripción precisa** con Deepgram API - Modelos de última generación (Nova-2)
- 🚀 **LLM ultrarrápido** usando Groq API (gratuito, 14,400 requests/día)
- 💬 **Comprensión natural** - Habla como quieras, el agente te entiende
- 📊 **Historial automático** de todas las transcripciones en CSV
- 🌍 **API REST** con FastAPI para integración
- 🌐 **Multi-idioma nativo** - Funciona en español, inglés, francés, etc. sin configuración
- 🔧 **Extensible sin código** - Agrega herramientas con descripciones, sin modificar lógica
- 🐳 **Docker listo** para producción

## 📋 Prerrequisitos

- Python 3.11+ o Docker
- API Keys:
  - Groq API key (100% gratuita) - Para el agente LLM
  - Deepgram API key (gratuita con $200 crédito) - Para transcripción de audio

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd Modulo2-1
```

### 2. Configurar API Keys

1. **Groq API** (gratuito):
   - Visita [https://console.groq.com](https://console.groq.com)
   - Crea cuenta gratuita
   - Genera API key
   - 14,400 requests por día gratis

2. **Deepgram API** (gratuita con crédito):
   - Visita [https://console.deepgram.com/signup](https://console.deepgram.com/signup)
   - Crea cuenta gratuita
   - Recibe $200 en créditos de inicio
   - Genera API key en el dashboard

3. Configurar variables de entorno:

```bash
# Copiar configuración
cp .env.example .env

# Editar .env con tus API keys:
# GROQ_API_KEY=tu_groq_key
# DEEPGRAM_API_KEY=tu_deepgram_key
```

## ⚡ Prueba Rápida

Después de iniciar el servidor, prueba el agente inteligente:

```bash
# Verificar que el servidor está corriendo
curl http://localhost:8000/health

# Probar el agente con diferentes mensajes naturales
curl -X POST http://localhost:8000/agent -F "message=qué puedes hacer?"
curl -X POST http://localhost:8000/agent -F "message=dame el historial"
curl -X POST http://localhost:8000/agent -F "message=show me the last 3 transcriptions"
curl -X POST http://localhost:8000/agent -F "message=cuántas transcripciones hay?"
```

**¡Nota!** El agente entiende lenguaje natural - no necesitas comandos específicos. Ver sección [💬 Guía Completa](#-guía-completa-de-uso-del-agente-inteligente) para más ejemplos.

## 🎯 Uso

### Opción 1: Docker (Recomendado)

#### Construir imagen
```bash
docker build -t transcription-api .
```

#### Iniciar servidor
```bash
docker run -d -p 8000:8000 --env-file .env -v "$(pwd)/data/audio/uploads":/app/data/audio/uploads -v "$(pwd)/data/transcriptions":/app/data/transcriptions --name transcription-api-server transcription-api
```

#### Scripts automáticos
```bash
# Linux/Mac
./start_server.sh

# Windows
start_server.bat
```

#### Detener servidor
```bash
# Linux/Mac
./stop_server.sh

# Windows
stop_server.bat
```

### Opción 2: Local

#### Instalar dependencias
```bash
pip install -r requirements.txt
```

#### Iniciar servidor
```bash
python src/api_server.py
```

## 📝 Uso de la API

### 🤖 Endpoint Inteligente con Function Calling (Recomendado)

El agente usa **function calling nativo** para entender tu intención en lenguaje natural. **No necesitas comandos específicos** - simplemente describe lo que quieres hacer.

#### Transcribir audio adjunto
```bash
curl -X POST http://localhost:8000/agent \
  -F "message=Por favor transcribe este archivo de audio" \
  -F "file=@tu_archivo.mp3"
```

#### Transcribir audio que ya está en la carpeta uploads
```bash
# Si ya tienes un archivo en data/audio/uploads/podcast.mp3
curl -X POST http://localhost:8000/agent \
  -F "message=transcribe el archivo podcast.mp3 que está en uploads" \
  -F "file=@data/audio/uploads/podcast.mp3"

# O de forma más natural
curl -X POST http://localhost:8000/agent \
  -F "message=pasa a texto el podcast.mp3" \
  -F "file=@data/audio/uploads/podcast.mp3"
```

#### Consultar historial
```bash
curl -X POST http://localhost:8000/agent \
  -F "message=dame el historial de transcripciones"
```

#### Buscar contenido específico
```bash
curl -X POST http://localhost:8000/agent \
  -F "message=busca transcripciones que mencionen proyecto"
```

### Endpoints Legacy (Directos)
Para cuando sabes exactamente qué necesitas:

#### Transcribir archivo
```bash
curl -X POST "http://localhost:8000/upload?language=es" -F "file=@data/audio/uploads/tu_archivo.mp3"
```

#### Ver historial
```bash
curl -X GET http://localhost:8000/history
```

#### Descargar CSV
```bash
curl -X GET http://localhost:8000/download -o transcripciones.csv
```

#### Ver estado
```bash
curl http://localhost:8000/health
```

## 💬 Guía Completa de Uso del Agente Inteligente

El agente usa **function calling nativo de LangChain** para entender lenguaje natural. Esto significa:
- ✅ **No necesitas comandos específicos** - habla naturalmente
- ✅ **Funciona en múltiples idiomas** - español, inglés, etc.
- ✅ **Extrae parámetros automáticamente** - entiende números, términos de búsqueda, etc.
- ✅ **Sin palabras clave rígidas** - múltiples formas de pedir lo mismo

### 📋 Consultar Historial de Transcripciones

El agente entiende muchas variaciones naturales:

```bash
# Español formal
curl -X POST http://localhost:8000/agent -F "message=dame el historial de transcripciones"

# Español casual
curl -X POST http://localhost:8000/agent -F "message=muéstrame qué transcripciones tienes guardadas"

# Inglés
curl -X POST http://localhost:8000/agent -F "message=show me the transcription history"

# Muy casual
curl -X POST http://localhost:8000/agent -F "message=qué has transcrito?"

# Pregunta directa
curl -X POST http://localhost:8000/agent -F "message=cuántas transcripciones hay?"

# Una sola palabra también funciona
curl -X POST http://localhost:8000/agent -F "message=historial"
```

### 🔢 Con Límites Específicos

El LLM **extrae automáticamente** el número del mensaje:

```bash
# Las últimas 3
curl -X POST http://localhost:8000/agent -F "message=muéstrame las últimas 3 transcripciones"

# Las 5 más recientes
curl -X POST http://localhost:8000/agent -F "message=enséñame las 5 transcripciones más recientes"

# Solo 2
curl -X POST http://localhost:8000/agent -F "message=dame solo 2 del historial"

# Las 10 más nuevas
curl -X POST http://localhost:8000/agent -F "message=lista las 10 más nuevas"
```

### 🔍 Búsquedas con Filtros

El LLM **extrae el término de búsqueda** automáticamente:

```bash
# Buscar por palabra clave
curl -X POST http://localhost:8000/agent -F "message=busca transcripciones que mencionen reunión"

# Buscar contenido específico
curl -X POST http://localhost:8000/agent -F "message=encuentra transcripciones sobre proyecto"

# Búsqueda casual
curl -X POST http://localhost:8000/agent -F "message=hay algo transcrito sobre inteligencia artificial?"

# Con comillas para frases exactas
curl -X POST http://localhost:8000/agent -F "message=busca reunión importante"
```

### 🎧 Transcribir Audio

#### Con archivo adjunto nuevo

```bash
# Formal
curl -X POST http://localhost:8000/agent \
  -F "message=transcribe este archivo de audio" \
  -F "file=@mi_audio.mp3"

# Casual
curl -X POST http://localhost:8000/agent \
  -F "message=pásame esto a texto porfa" \
  -F "file=@podcast.wav"

# Inglés
curl -X POST http://localhost:8000/agent \
  -F "message=convert this audio to text" \
  -F "file=@interview.m4a"

# Muy directo
curl -X POST http://localhost:8000/agent \
  -F "message=transcribe" \
  -F "file=@meeting.mp3"

# Con contexto
curl -X POST http://localhost:8000/agent \
  -F "message=necesito transcribir esta reunión importante" \
  -F "file=@reunion-enero.mp3"
```

#### Con archivo que ya está en uploads

Si ya tienes archivos en `data/audio/uploads/`:

```bash
# Referencia directa al archivo
curl -X POST http://localhost:8000/agent \
  -F "message=transcribe el archivo podcast-ep1.mp3" \
  -F "file=@data/audio/uploads/podcast-ep1.mp3"

# Forma más natural
curl -X POST http://localhost:8000/agent \
  -F "message=pasa a texto el archivo entrevista.wav que tengo en uploads" \
  -F "file=@data/audio/uploads/entrevista.wav"

# Muy directo
curl -X POST http://localhost:8000/agent \
  -F "message=transcribe reunión-2024.mp3" \
  -F "file=@data/audio/uploads/reunión-2024.mp3"

# Con contexto adicional
curl -X POST http://localhost:8000/agent \
  -F "message=necesito transcribir el audio conferencia.m4a que subí antes" \
  -F "file=@data/audio/uploads/conferencia.m4a"
```

### 🌍 Multi-idioma (Sin Cambiar Código)

El agente entiende múltiples idiomas automáticamente:

```bash
# Español
curl -X POST http://localhost:8000/agent -F "message=dame el historial"

# Inglés
curl -X POST http://localhost:8000/agent -F "message=give me the history"

# Francés
curl -X POST http://localhost:8000/agent -F "message=montre-moi l'historique"

# Portugués
curl -X POST http://localhost:8000/agent -F "message=mostre-me o histórico"

# Mezcla de idiomas (code-switching)
curl -X POST http://localhost:8000/agent -F "message=show me las últimas transcripciones"
```

### 🎯 Ejemplos de Extracción Automática de Parámetros

El LLM entiende contexto y extrae valores sin necesidad de formato específico:

```bash
# Extrae limit=10 automáticamente
curl -X POST http://localhost:8000/agent -F "message=muéstrame las 10 últimas transcripciones"

# Extrae search=AI automáticamente
curl -X POST http://localhost:8000/agent -F "message=busca transcripciones que hablen de AI"

# Extrae limit=5 y entiende recientes
curl -X POST http://localhost:8000/agent -F "message=dame las 5 más nuevas"

# Extrae search=proyecto y busca
curl -X POST http://localhost:8000/agent -F "message=hay transcripciones sobre el proyecto?"

# Combinación de parámetros
curl -X POST http://localhost:8000/agent -F "message=muéstrame las últimas 3 que mencionen reunión"
```

### 💬 Conversaciones Naturales

El agente maneja preguntas abiertas e informales:

```bash
# Pregunta abierta
curl -X POST http://localhost:8000/agent -F "message=qué puedes hacer?"

# Exploración
curl -X POST http://localhost:8000/agent -F "message=tengo audios para transcribir"

# Contexto informal
curl -X POST http://localhost:8000/agent -F "message=hola, necesito ver qué he transcrito antes"

# Instrucción directa
curl -X POST http://localhost:8000/agent -F "message=lista todo lo que tienes"

# Sin mencionar transcripción
curl -X POST http://localhost:8000/agent -F "message=qué archivos has procesado?"

# Pregunta indirecta
curl -X POST http://localhost:8000/agent -F "message=recuerdas qué has transcrito?"

# Contexto implícito
curl -X POST http://localhost:8000/agent -F "message=enséñame lo que tienes guardado"
```

### 🧪 Flujo Completo de Ejemplo

```bash
# 1. Transcribir un nuevo archivo
curl -X POST http://localhost:8000/agent \
  -F "message=transcribe este podcast" \
  -F "file=@mi_podcast.mp3"

# Respuesta:
# "Transcripción completada:
#  Archivo: mi_podcast.mp3
#  Duración: 125.34 segundos
#  Transcripción: [texto transcrito...]"

# 2. Ver el historial
curl -X POST http://localhost:8000/agent \
  -F "message=muéstrame qué has transcrito"

# Respuesta:
# "Historial de transcripciones recientes:
#  📄 mi_podcast.mp3
#  📅 2026-01-29 15:30:00
#  📝 [primeras 100 palabras...]"

# 3. Buscar contenido específico
curl -X POST http://localhost:8000/agent \
  -F "message=busca transcripciones que mencionen inteligencia artificial"

# Respuesta:
# "Se encontraron 2 transcripciones que contienen 'inteligencia artificial':
#  [resultados filtrados...]"

# 4. Ver solo las últimas 2
curl -X POST http://localhost:8000/agent \
  -F "message=dame las 2 más recientes"

# Respuesta:
# "Últimas 2 transcripciones:
#  1. mi_podcast.mp3 - 2026-01-29 15:30:00
#  2. [anterior]..."
```

### 🎨 Variaciones Creativas que Funcionan

Gracias al function calling, estas variaciones **todas funcionan**:

```bash
# Coloquial
curl -X POST http://localhost:8000/agent -F "message=a ver qué tengo por aquí"

# Formal
curl -X POST http://localhost:8000/agent -F "message=por favor proporcione el registro histórico"

# Pregunta
curl -X POST http://localhost:8000/agent -F "message=cuántos audios he transcrito ya?"

# Imperativo suave
curl -X POST http://localhost:8000/agent -F "message=podrías mostrarme el historial"

# Con urgencia
curl -X POST http://localhost:8000/agent -F "message=necesito urgentemente ver las transcripciones anteriores"

# Técnico
curl -X POST http://localhost:8000/agent -F "message=dump del historial"

# Muy simple
curl -X POST http://localhost:8000/agent -F "message=lista"
```

### ⚡ Por Qué Funciona Esto

**Antes** (sistemas con palabras clave):
- ❌ Solo funcionaba: "historial", "show history"
- ❌ Fallaba con: "qué has transcrito?", "muéstrame todo"
- ❌ Requería comandos exactos
- ❌ No entendía contexto ni variaciones

**Ahora** (con function calling nativo):
- ✅ Entiende **intención**, no solo palabras exactas
- ✅ Extrae **parámetros automáticamente** del mensaje
- ✅ Funciona en **múltiples idiomas**
- ✅ Maneja **variaciones naturales** del lenguaje
- ✅ **Sin condicionales** `if/elif` en el código
- ✅ **Extensible**: agregar herramientas no requiere cambiar lógica

### 🔧 Cómo Funciona Internamente

```python
# El usuario escribe en lenguaje natural
"dame las últimas 5 transcripciones"

# El LLM analiza el mensaje + descripciones de herramientas
# y genera automáticamente un tool_call:
{
  "name": "query_history",
  "args": {"limit": 5}
}

# El agente ejecuta la herramienta sin if/elif
result = tools["query_history"]._run(limit=5)
```

**Documentación técnica completa**: Ver `docs/architecture.md` para detalles sobre la implementación del function calling.

## 🌐 Documentación

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📁 Estructura del Proyecto

```
Modulo2-1/
├── src/                    # Código fuente principal
│   ├── api_server.py      # Servidor API FastAPI
│   ├── agent.py           # Agente principal con LangChain
│   ├── __init__.py
│   ├── __main__.py
│   ├── prompts/           # Plantillas de prompts
│   │   └── agent_prompt.md
│   └── tools/             # Herramientas del agente
│       ├── __init__.py
│       ├── transcriber.py # Transcripción con Whisper
│       └── history.py     # Gestión de historial
├── data/                  # Datos de la aplicación
│   ├── audio/            # Archivos de audio
│   │   └── uploads/      # Subidas de usuario
│   └── transcriptions/   # Resultados
│       └── output/
│           └── history.csv
├── tests/                # Pruebas unitarias
├── Dockerfile
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── .dockerignore
├── .env.example
├── start_server.sh
├── stop_server.sh
├── start_server.bat
├── stop_server.bat
└── README.md
```

## 🎵 Formatos de Audio Soportados

- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- OGG (.ogg)
- FLAC (.flac)
- MP4 (.mp4) - solo audio

## 🧠 Modelos de Deepgram

| Modelo | Velocidad | Precisión | Costo | Recomendado para |
|--------|-----------|-----------|-------|------------------|
| nova-2 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Bajo | **Uso general** ✅ (Última generación) |
| nova | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Bajo | Buena relación calidad-precio |
| base | ⭐⭐⭐⭐ | ⭐⭐⭐ | Muy bajo | Transcripción básica |
| enhanced | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Alto | Máxima precisión |

**Recomendación**: Usa `nova-2` para mejor rendimiento y precisión (modelo por defecto).

**Características de Nova-2**:
- 🚀 Velocidad ultrarrápida (tiempo real)
- 🎯 Mayor precisión que modelos anteriores
- 🌍 Soporte para 100+ idiomas
- 💰 Mejor costo-beneficio

## 📊 Formato CSV del Historial

El historial se guarda automáticamente en `data/transcriptions/output/history.csv`:

```csv
timestamp,filename,duration_seconds,model,transcription_text
2026-01-29 10:30:00,podcast.mp3,3.45,deepgram-nova-2,"Texto transcrito..."
2026-01-29 11:45:00,interview.wav,2.87,deepgram-nova-2,"Otra transcripción..."
```

**Nota**: `duration_seconds` representa el tiempo de procesamiento de la API (generalmente < 5 segundos).

## 🔧 Configuración Avanzada

### Cambiar modelo de Deepgram

En `src/tools/transcriber.py`, modifica el valor por defecto:

```python
model: str = Field(
    default="nova-2",  # Opciones: nova-2, nova, base, enhanced
    description="Deepgram model to use..."
)
```

O especifica el modelo en la llamada al agente:
```bash
curl -X POST http://localhost:8000/agent \
  -F "message=transcribe este audio usando el modelo enhanced" \
  -F "file=@audio.mp3"
```

### Cambiar modelo de Groq LLM

En `src/agent.py`, línea del modelo:

```python
model_name="llama-3.3-70b-versatile",  # Opciones: llama-3.3-70b-versatile, llama-3.1-8b-instant, mixtral-8x7b-32768
```

**Nota**: El modelo debe soportar **function calling** para que el agente funcione correctamente.

## 🐛 Troubleshooting

### Error: "GROQ_API_KEY not configured"

- Asegúrate de haber creado el archivo `.env`
- Verifica que tu API key esté correctamente copiada
- No incluyas comillas alrededor de la API key

### Error: "DEEPGRAM_API_KEY not configured"

- Obtén tu API key en [https://console.deepgram.com](https://console.deepgram.com)
- Agrégala al archivo `.env`:
  ```bash
  DEEPGRAM_API_KEY=tu_deepgram_key_aqui
  ```
- Verifica que tengas créditos disponibles en tu cuenta

### Error de Deepgram API

```bash
# Verificar que la API key funciona
curl -X GET "https://api.deepgram.com/v1/projects" \
  -H "Authorization: Token TU_DEEPGRAM_API_KEY"
```

### Audio no se transcribe correctamente

- Verifica que el formato sea compatible (mp3, wav, m4a, ogg, flac, mp4)
- Usa un modelo de mayor calidad (`enhanced` o `nova-2`)
- Especifica el idioma si es necesario:
  ```bash
  curl -X POST http://localhost:8000/agent \
    -F "message=transcribe este audio en español" \
    -F "file=@audio.mp3"
  ```

### Transcripción lenta o timeout

- Deepgram API es muy rápida (generalmente < 5 segundos)
- Si experimentas lentitud, verifica tu conexión a internet
- Revisa el status de Deepgram: [https://status.deepgram.com](https://status.deepgram.com)

## 🧠 ¿Qué es Function Calling?

Function calling es una capacidad nativa de los LLMs modernos donde el modelo puede **generar estructuras de llamada a funciones** basándose en descripciones semánticas.

### ❌ Antes (Sistemas tradicionales con palabras clave)
```python
if "transcribe" in message or "transcribir" in message:
    use_transcribe_tool()
elif "historial" in message or "history" in message:
    use_history_tool()
# ... más condicionales ...
```

**Problemas**:
- Solo funciona con palabras específicas
- No escala (cada herramienta = más condicionales)
- No entiende variaciones del lenguaje
- Difícil de mantener

### ✅ Ahora (Function Calling nativo)
```python
# 1. Vincular herramientas al LLM con descripciones
llm_with_tools = llm.bind_tools([
    TranscribeAudioTool(),  # "Transcribes audio files..."
    QueryHistoryTool(),     # "Queries transcription history..."
])

# 2. El LLM decide automáticamente
response = llm_with_tools.invoke(user_message)

# 3. Ejecutar sin condicionales
if response.tool_calls:
    result = tools[response.tool_calls[0]['name']]._run(**response.tool_calls[0]['args'])
```

**Ventajas**:
- ✅ Entiende intención, no solo palabras
- ✅ Funciona en múltiples idiomas automáticamente
- ✅ Extrae parámetros del mensaje del usuario
- ✅ Agregar herramientas no requiere cambiar código

**📖 Documentación completa**: Ver `docs/architecture.md` para análisis técnico detallado sobre la implementación del function calling.

## 📚 Recursos

- [Groq Documentation](https://console.groq.com/docs)
- [Deepgram API](https://developers.deepgram.com/)
- [OpenAI's Whisper](https://github.com/openai/whisper)
- [LangChain Function Calling](https://python.langchain.com/docs/modules/model_io/chat/function_calling)
- [FastAPI](https://fastapi.tiangolo.com/)

## 🧪 Testing

### Probar herramientas individuales

```bash
python tests/test_tools.py
```

Con pytest (recomendado):
```bash
pip install pytest
pytest tests/
```

### Probar servidor local

```bash
python src/api_server.py
curl http://localhost:8000/health
```

## 🏗️ Arquitectura Técnica

```
┌─────────────────────────────────────────────────┐
│              API FastAPI                        │
│           (Servidor REST)                       │
└────────────────────┬────────────────────────────┘
                     │
                     │ Mensaje del usuario
                     ▼
┌─────────────────────────────────────────────────┐
│     Agente Inteligente (Function Calling)      │
│  ┌──────────────────────────────────────────┐  │
│  │  LLM (Groq Llama 3.3 70B)                │  │
│  │  • Lee descripciones de herramientas     │  │
│  │  • Genera tool_calls automáticamente     │  │
│  │  • Extrae parámetros del mensaje         │  │
│  └──────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
┌──────────────┐ ┌──────────┐ ┌─────────────┐
│ Transcriber  │ │  Query   │ │    Save     │
│   Tool       │ │ History  │ │ Transcribe  │
│              │ │   Tool   │ │    Tool     │
│ • Deepgram   │ │          │ │             │
│   Nova-2 API │ │          │ │             │
└──────────────┘ └────┬─────┘ └──────┬──────┘
                      │               │
                      └───────┬───────┘
                              ▼
                   ┌──────────────────────┐
                   │   CSV Historial      │
                   │  (Pandas + CSV)      │
                   └──────────────────────┘
```

### Stack Tecnológico

- **API**: FastAPI + Uvicorn
- **LLM**: Groq (Llama 3.3 70B Versatile) - 14,400 peticiones/día gratis
- **Transcripción**: Deepgram API (Nova-2) - $200 en créditos iniciales
- **Framework**: LangChain con **Function Calling nativo**
- **Agent Pattern**: Inteligencia basada en descripciones semánticas, sin condicionales
- **Persistencia**: Pandas + CSV
- **Configuración**: python-dotenv

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para detalles.

---

## 🎯 Resumen

Este proyecto implementa un **agente de IA verdaderamente inteligente** que entiende lenguaje natural gracias a **function calling nativo**:

- 💬 **Habla naturalmente** - No necesitas comandos específicos
- 🌍 **Multi-idioma automático** - Funciona en cualquier idioma sin configuración
- 🔧 **Extensible sin fricción** - Agrega herramientas con descripciones, sin modificar lógica
- ⚡ **Sin condicionales** - Cero `if/elif` basados en palabras clave
- 🎯 **Extracción inteligente** - El LLM identifica parámetros automáticamente

**📖 Para detalles técnicos completos**: Consulta `docs/architecture.md`

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub
