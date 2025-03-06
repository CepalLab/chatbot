# Chatbot de la CEPAL

Este repositorio contiene el código fuente para un chatbot experimental desarrollado para la Comisión Económica para América Latina y el Caribe (CEPAL).  El chatbot está construido utilizando Streamlit para la interfaz de usuario y se integra con un modelo de lenguaje grande (LLM) a través de la API de Groq.

## Funcionalidades

El chatbot proporciona información sobre la CEPAL, respondiendo preguntas sobre su historia, misión, estructura y actividades.  Sus principales características son:

* **Interfaz Conversacional:**  Interactúa con el usuario a través de una interfaz de chat intuitiva en español.
* **Respuestas Informativas:** Ofrece respuestas concisas y precisas basadas en la información disponible sobre la CEPAL.
* **Sugerencias de Preguntas:**  Proporciona sugerencias de preguntas adicionales para profundizar en la conversación.
* **Manejo de Contexto:**  Mantiene el contexto de la conversación para ofrecer respuestas más relevantes.
* **Gestión de Errores:**  Indica al usuario cuando no cuenta con la información solicitada.


## Tecnologías Utilizadas

* **Streamlit:** Para la creación de la interfaz de usuario.
* **Groq:**  Para la integración con el modelo de lenguaje grande.
* **Atomic Agents:** Librería para la gestión de agentes conversacionales.
* **Python:** Lenguaje de programación principal.
* **Pydantic:** Para la validación de datos.


## Instalación y Ejecución

Para ejecutar este chatbot, necesitarás:

1. **Clonar el repositorio:** `git clone https://github.com/CepalLab/chatbot.git`
2. **Instalar las dependencias:** `pip install -r requirements.txt`
3. **Configurar la API Key de Groq:**  Crea un archivo llamado `secrets.toml` en la raíz del proyecto con la siguiente estructura:

```toml
[secrets]
GROQ_API_KEY = "TU_API_KEY"
# Reemplaza "TU_API_KEY" con tu clave de API de Groq.
```
4. **Ejecutar la aplicación:** `streamlit run app.py`

## Estructura del Proyecto
- `app.py`: Contiene el código principal de la aplicación Streamlit.
- `secrets.toml`: Archivo de configuración con la clave de API de Groq (no se debe subir a repositorios públicos).
- `requirements.txt`: Lista de las dependencias del proyecto.

## Contribuciones
Las contribuciones son bienvenidas. Si encuentras algún error o tienes sugerencias para mejorar el chatbot, por favor, abre un issue o un pull request en este repositorio.

## Autores
Alejandro Bustamante, Laboratorio de Prospectiva, Innovación e Inteligencia Artificial
alejandro.bustamante@un.org 

