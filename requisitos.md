# Requisitos y Funcionalidades del Proyecto PixMatch 

## Funcionalidades Principales

### 1. Configuración y Personalización del Juego
- **Selección de Nivel de Dificultad**: El usuario puede elegir entre tres niveles de dificultad (Fácil, Medio, Duro), que afectan la complejidad del juego y el intervalo de tiempo para las acciones automáticas.
- **Entrada de Datos del Jugador**: Posibilidad de ingresar el nombre del jugador y el país, lo cual es utilizado para personalizar la experiencia y registrar puntuaciones en el tablero de líderes.

### 2. Dinámica del Juego
- **Interfaz de Usuario Interactiva**: Utilización de botones dinámicos y elementos visuales para interactuar con el usuario.
- **Autorefresco y Regeneración de Contenidos**: Funcionalidad de autorefresco que actualiza los elementos del juego basados en el tiempo definido por la dificultad seleccionada.
- **Manejo de Estado del Juego**: Uso de `st.session_state` para mantener el estado del juego a través de diferentes sesiones y eventos.

### 3. Sistema de Puntuación
- **Puntuación Basada en Acciones**: El sistema de puntuación incrementa o decrementa basado en las respuestas correctas o incorrectas del jugador.
- **Visualización de Puntuación**: Se muestra la puntuación actual del jugador de manera continua en la barra lateral.

### 4. Ranking
- **Registro de Puntuaciones Altas**: Implementación de un ranking que guarda las puntuaciones más altas junto con los nombres de los jugadores y sus países.
- **Visualización del Tablero de Líderes**: Capacidad para leer y mostrar el tablero de líderes dentro del juego.

## Futuras Mejoras Propuestas
- **Integración de nuevos modos de juego**: Considero que se podrían colocar otros modos de juego, por ejemplo un modo contrareloj en el que la partida durara la mitad y se buscara la máxima puntuación
- **Ranking de usuarios extendido**: Una pestaña aparte que incluya un ranking más detallado de disntintos usuarios.

