# ⚔️ Presentación de Proyecto: Dragons & IA

## 📝 Guía para la IA de Diseño de Presentaciones
Este documento contiene la esencia estratégica, comercial y técnica de **Dragons & IA**. El objetivo es proporcionar contexto suficiente para que una IA pueda generar una presentación de impacto (Pitch Deck), enfocándose en la propuesta de valor, la innovación y la experiencia del usuario.

---

## 🚀 1. Concepto General (The Elevator Pitch)
**Dragons & IA** es una plataforma de juegos de rol (RPG) por texto donde la Inteligencia Artificial no es solo un asistente, sino el **Dungeon Master (DM)**. 

A diferencia de los juegos con opciones predefinidas, Dragons & IA ofrece una narrativa emergente en tiempo real, permitiendo que el jugador escriba cualquier acción y reciba una respuesta coherente, creativa y mecánicamente justa, integrando las reglas de D&D 5e.

**Slogan Sugerido:** *"Tu imaginación es la única limitación; la IA es quien narra la leyenda."*

---

## 💎 2. Propuesta de Valor (Value Propositions)

### A. Libertad Narrativa Absoluta
El usuario no elige entre "Opción A" u "Opción B". Puede intentar convencer a un guardia, quemar una taberna o negociar con un dragón. La IA procesa la intención y adapta la historia dinámicamente.

### B. Democratización de la IA (Soberanía del Modelo)
El proyecto es agnóstico al modelo. El usuario decide qué "cerebro" usar:
- **Máxima Calidad:** Claude (Anthropic) o modelos masivos en la nube.
- **Privacidad y Costo Cero:** Modelos locales vía Ollama (Llama 3.2, etc.).
- **Equilibrio:** Ollama Cloud.
Esto convierte al juego en una herramienta flexible para distintos perfiles de usuarios.

### C. Fusión de Mecánica y Narrativa
No es solo un "chat con IA". Es un sistema de juego:
- **Reglas D&D 5e:** Gestión de stats, HP y XP.
- **Azar Real:** Sistema de dados interactivos (d4-d20) que impactan el resultado de la narración.
- **Inmersión Visual:** Tipografías y temas que cambian según el mundo seleccionado (Fantasía, Sci-Fi, Isekai, Dark Fantasy).

---

## 🛠️ 3. Pilares del Producto (Key Features)

### 🧠 El Motor de Inteligencia
- **Dungeon Master Autónomo:** Genera escenas, describe entornos y reacciona a los jugadores.
- **Multi-LLM:** Integración vía LiteLLM para cambiar de modelo sin fricción.
- **Estado de IA en Tiempo Real:** Indicadores visuales que informan al usuario sobre la salud y respuesta de la IA.

### 🎲 El Sistema de Juego
- **Creación de Personaje:** Implementación de *Point Buy* y cálculo automático de salud por clase.
- **Dados Críticos:** Feedback visual impactante en Natural 20 (Éxito Crítico) y Natural 1 (Fallo Crítico).
- **Ciclo de Juego:** Acciones rápidas (Atacar, Defender, Huir) para agilizar la experiencia sin perder la profundidad del texto.

### 🌌 Mundos y Atmósfera
- **Sistemas Temáticos:** Cada mundo (ej. *Orbitron* para Sci-Fi, *Crimson Text* para Fantasía Oscura) altera la estética del juego para sumergir al jugador en la ambientación.
- **Persistencia:** Sistema de guardado de partidas con historial completo, permitiendo retomar aventuras épicas en cualquier momento.

---

## 📈 4. Perfil del Usuario (Target Audience)
1. **Entusiastas de los TTRPG (Tabletop RPG):** Jugadores de D&D que no siempre tienen un grupo disponible o un DM humano.
2. **Early Adopters de IA:** Personas interesadas en probar las capacidades narrativas de los últimos LLMs.
3. **Gamers Casuales:** Usuarios que buscan una experiencia de "elige tu propia aventura" pero con esteroides tecnológicos.

---

## 🛡️ 5. Calidad Técnica (The "Under the Hood" Trust)
Para una presentación, es vital resaltar que el proyecto no es un prototipo inestable, sino una aplicación robusta:
- **Arquitectura Moderna:** FastAPI (Python) + PostgreSQL + SQLAlchemy Async.
- **Seguridad:** Autenticación JWT con auto-logout y gestión de claves de API solo en el lado del cliente (localStorage).
- **Estabilidad Probada:** Suite de 62 tests automatizados (Backend y Frontend) con 100% de tasa de éxito.
- **Despliegue Profesional:** Dockerizado y optimizado para Render.com.

---

## 🎬 6. Estructura Sugerida para la Presentación (Slide Deck Flow)

1. **Portada:** Nombre, logo y slogan impactante.
2. **El Problema:** La dificultad de coordinar grupos de RPG o la rigidez de los juegos de rol tradicionales.
3. **La Solución:** Presentación de Dragons & IA como el DM definitivo impulsado por IA.
4. **Cómo Funciona (Demo/Flujo):** Creación de personaje $\rightarrow$ Elección de mundo $\rightarrow$ Acción $\rightarrow$ Tirada de dados $\rightarrow$ Narrativa de la IA.
5. **El Diferenciador (Soberanía de IA):** Mostrar la flexibilidad de elegir entre Claude, Ollama Cloud y Local.
6. **Inmersión y Mecánicas:** Mostrar los mundos temáticos y la integración de reglas D&D 5e.
7. **Robustez Técnica:** Resumen del stack y la calidad de los tests (confianza en el producto).
8. **Visión Futura:** Posibles expansiones (multijugador, generación de imágenes de escenas, etc.).
9. **Cierre:** Call to action y enlace a la demo.
