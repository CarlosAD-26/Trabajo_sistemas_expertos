# Proyecto grupal - Sistemas Expertos

## 1. Integrantes del grupo

- Adrián Chao
- Carlos Alvarez
- Alejandro Colchero
- Pablo Picón

## 2. Estructura del proyecto

En este proyecto se implementa un sistema experto basado en reglas, haciendo uso de lógica difusa mediante el método Mamdani.

El proyecto sigue la siguiente estructura:

* motor.py
* reglas.py
* logica_difusa.py
* main.py
* app.py
* Readme.md
* informe_grupo_X_s02.pdf

## 3. Instalación de dependencias

Primero que todo, necesitaremos tener instalado Python en nuestro equipo, para ello, nos vamos a su página oficial y nos descargamos la version mas reciente y estable (https://www.python.org/downloads/).

Las dependencias que necesitamos para este proyectos son las siguientes:

1. Numpy
2. Matplotlib
3. Streamlit

Para poder descargar dichas dependencias es muy simple, nos vamos a nuestra terminal en VS Code y escribimos:

__pip install numpy__

Esperamos a que termine la instalación y continuamos con el siguiente comando:

__pip install matplotlib__

Hacemos lo mismo, esperamos a que acabe de descargarse y lanzamos el último comando de descarga:

__pip install streamlit__

Este último es algo pesado debido a que necesita descargar bastantes cosas, nosotros esperaremos y ya tendríamos nuestras dependencias instaladas.

__*ATENCIÓN: Deberás tener en tu VS Code las extensiones necesarias sobre Python instaladas para asegurarnos de una experiencia más comoda y segura, para ello abre el apartado de extensiones en tu VS Code e instala Python, después se instalará todo lo necesario de forma automática*__

## 4. Cómo ejecutar la aplicación 

Este último paso es bastante sencillo, pero hay que tener en cuenta si queremos ejecutar nuestro programa con Streamlit o en Consola

### Ejecutar con Streamlit

Para ejecutar nuestro programa con esta libreria es bastante sencillo, solo tendremos que abrir nuestra terminal y lanzar el siguiente comando:

__python -m streamlit run app.py__

Una vez lanzado este comando nos saldrá una ventana en la que nos pedirá introducir un correo electrónico, el cual vamos a ignorar dandole a __Enter__ y una vez hecho esto se nos abrirá nuestro navegador web bajo el enlace de _http://localhost:8501/_ nuestro sistema experto previamente diseñado.


## Ejecutar con la Consola

Para ello es muy sencillo, solo deberemos lanzar el siguiente comando:

__py mi_programa.py__ (Sustituimos "mi_programa por el nombre de nuestro programa")

Con esto se nos abriría nuestra terminal con el programa lanzado.

