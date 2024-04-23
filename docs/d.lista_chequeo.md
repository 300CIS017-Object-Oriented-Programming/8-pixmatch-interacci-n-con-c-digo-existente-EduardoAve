Diligencie la siguiente lista de chequeo a partir del estudio del código fuente
### Lista de chequeo de revisión del código actual
X = No aplica
✔ = aplica


#### Claridad y Estructura
- [ ✔ ] **Flujo Confuso:** El código no sigue un flujo lógico, haciendo difícil seguir la secuencia de operaciones. _Ejemplo: Funciones que realizan saltos abruptos entre tareas sin relación aparente._ (parece código espageti)
- [ ✔ ] **Documentación Insuficiente o Ausente:** Falta de comentarios claros o documentación, especialmente en partes complicadas del código. _Ejemplo: Código con bucles y condicionales complejos sin explicaciones sobre su propósito._ (el código no está muy bien documentado)
- [ X ] **Nombres de Variables No Descriptivos:** Uso de nombres genéricos o confusos que no reflejan la función o el contenido de la variable. _Ejemplo: Variables nombradas con una sola letra o nombres no intuitivos como `data1`, `xyz`._ (El autor hizo buen trabajo nombrando las variables. )

#### Complejidad
- [ ✔ ] **Estructuras de Control Anidadas Profundamente:** Uso excesivo de bucles y condicionales anidados que complica la lectura. _Ejemplo: Tres o más niveles de bucles o condicionales dentro de una función._ (el código original es complicadisimo de leer.)
- [ X ] **Código separable:** Funciones que intentan hacer demasiado, complicando su uso y mantenimiento. Se podrían dividir tareas complejas en funciones más pequeñas con una única responsabilidad _Ejemplo: Una función que carga datos, realiza cálculos y además genera gráficos._
- [ X ] **Código Duplicado:** Presencia de bloques de código muy similares en diferentes partes del programa. _Ejemplo: Múltiples funciones que contienen las mismas líneas de código para procesar datos._
- [ ✔ ] **Falta de estructura:** Sería beneficioso definir nuevos tipos de datos (o clases) para representar entidades complejas dentro del código. (posiblemente)

#### Cohesión y Organización
- [ ✔ ] **Baja Cohesión:** Módulos o funciones que tienen múltiples responsabilidades no relacionadas. _Ejemplo: Se pueden identificar secciones de código que podrían convertirse en funciones o módulos independientes_
- [✔ ] **Modularidad Pobre:** Falta de separación clara entre distintas funcionalidades, dificultando la reutilización de código. _Ejemplo: Un script monolítico sin funciones definidas, donde todo el código está en el nivel superior._

#### Acoplamiento y Dependencias
- [ X ] **Alto Acoplamiento:** Cambios en una parte del código requieren ajustes frecuentes en otras partes. _Ejemplo: Modificar una estructura de datos que requiere cambios en múltiples funciones que dependen directamente de esa estructura._ (por lo general se puede hacer desde las variables de estado)
- [ ✔ ] **Dependencia de Detalles Internos:** Funciones que dependen de los detalles internos de otras, violando el principio de encapsulamiento. _Ejemplo: Acceso directo a campos de datos de un objeto desde fuera de la clase, en lugar de usar métodos de acceso._ (para agregar una nueva funcionalidad se deben corregir varias funciones)
- [ X  ] **Uso de variables globales:** Las variables globales generan dependencias por lo que es difícil que el estado del programa sea gestionado de forma previsible y controlada. No se encapsulan las variables globales dentro de funciones o clases donde sea posible para minimizar efectos secundarios

#### Mantenibilidad y Escalabilidad
- [ ✔ ] **Dificultad de Extensión:** Es difícil añadir nuevas características debido a la estructura actual del código? La estructura de código dificulta la adición de nuevas funcionalidades sin extensas modificaciones. _Ejemplo: Código tan rígido que cualquier nueva funcionalidad requiere una reescritura significativa._ (Es difícil, el código es muy confuso y para agregar cualquier función de debe de modificar varias cosas anteriormente)
- [ ✔ ] **Pruebas Complicadas:** Estructura de código que hace difícil escribir y mantener pruebas. _Ejemplo: Funciones con alto acoplamiento y dependencias externas complejas que requieren configuraciones extensas para pruebas._ (Es cierto, mi aplicación tira un error cuando se pierde la partida y aún no sé por qué.)
- [ ✔ ] **Diseño orientado a objetos:** ¿Podría un diseño orientado a objetos mejorar la escalabilidad y la flexibilidad para futuros cambios? (Seguramente)

#### Separación de Intereses
- [✔  ] **Mezcla de Lógica de Negocio y Presentación:** Lógica de negocio y operaciones de I/O o presentación visual entrelazadas en el mismo bloque de código. _Ejemplo: Código que calcula resultados y al mismo tiempo actualiza una interfaz gráfica._ (Sí, se mezclan funciones de streamlit con actualizaciones de variables y archivos)

#### Pruebas y Validaciones
- [ ✔ ] **Falta de Pruebas Automáticas:** Ausencia de pruebas unitarias o de integración que verifiquen el comportamiento y la corrección del código. _Ejemplo: Módulo complejo sin pruebas asociadas, donde cualquier cambio puede introducir errores inadvertidamente._ (Intenté agregar lo de perder la partida y ahora me imprime un error en la pantalla final junto al game over. )

#### Documentación y Estilo de Código
- [ ✔ ] **Inconsistencia en el Estilo de Código:** No sigue un estilo de codificación consistente que cumpla con las guías de estilo PEP 8. _Ejemplo: Mezcla de estilos de CamelCase para variables cuando se debe usar el estilo de `nombre_variable`