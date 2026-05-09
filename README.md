# Laboratorio 03 – Funciones PRIMERO y SIGUIENTE

Este proyecto implementa el cálculo de las funciones PRIMERO (FIRST) y SIGUIENTE (FOLLOW) a partir de una gramática libre de contexto.

Estas funciones son fundamentales en la construcción de analizadores sintácticos, ya que permiten determinar:

* Qué símbolos pueden aparecer al inicio de una derivación (FIRST)
* Qué símbolos pueden aparecer después de un no terminal (FOLLOW)

---

## Funcionalidades

El programa permite:

* Ingresar una gramática manualmente
* Utilizar gramáticas predefinidas
* Identificar:

  * Símbolos terminales
  * Símbolos no terminales
* Calcular:

  * Conjuntos FIRST
  * Conjuntos FOLLOW
* Mostrar resultados de forma clara y estructurada

---

## Estructura del programa

El código incluye:

* Cálculo de conjuntos FIRST
* Cálculo de conjuntos FOLLOW
* Parser para interpretar gramáticas ingresadas como texto
* Conversión de gramáticas desde formato diccionario
* Menú interactivo para facilitar pruebas
* Formateo de salida para mejor lectura

---

## Ejecución

### Requisitos

* Python 3.x

### Ejecución

```bash
python primero_y_siguiente.py
```

---

## Uso del programa

Al ejecutar el programa, se muestra un menú con opciones para:

* Seleccionar ejemplos predefinidos
* Ingresar una gramática manualmente
* Salir del programa

---

## Restricciones

* No se utilizaron librerías externas para calcular FIRST o FOLLOW
* Los algoritmos fueron implementados manualmente

---

##  Video

<p align="center">
  <a href="https://youtu.be/3I0bdvyO5yU">
    <img src="https://img.youtube.com/vi/3I0bdvyO5yU/0.jpg" alt="Video demostración" width="600"/>
  </a>
</p>

<p align="center">
  ▶️ Haz clic en la imagen o accede directamente aquí:
</p>

<p align="center">
  🔗 https://youtu.be/3I0bdvyO5yU
</p>


En el video se demuestra:

* Ejecución del programa
* Uso con al menos dos gramáticas diferentes
* Explicación del funcionamiento del algoritmo

---

##  Conclusión

El programa cumple con los objetivos del laboratorio al implementar correctamente los algoritmos de FIRST y FOLLOW, permitiendo analizar gramáticas libres de contexto de manera clara y estructurada.

---

## Integrantes

-   **Alejandro Antón** - [Anton17303](https://github.com/Anton17303)
-   **Ruth de Léon** - [Anaru03](https://github.com/Anaru03)


