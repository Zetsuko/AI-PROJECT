# Instrucciones de instalación del proyecto

### Dentro de la carpeta donde este el proyecto crear un entorno virtual:
```
Windows: python -m vevn .venv
Unix/macOS: python3 -m venv .venv
```
>_**Un entorno virtual permite instalar las dependencias en un entorno aparte de nuestra computadora**_

---

### Activar el venv:
```
Windows: .venv/Scripts/Activate.ps1
Unix/macOS: source .venv/bin/activate
```

### Desactivar venv:
```
Windows/Unix/macOS: deactivate
```
---

### Instalar requerimientos _( el venv debe estar activo )_:
```
pip install -r requerimientos.txt
```
> **En caso de que se agreguen más dependencias este es el comando para agregarlas al archivo ( el venv debe estar activo ):**
```
Windows: py -m pip freeze > requerimientos.txt
Unix/macOS: python3 -m pip freeze > requerimientos.txt
```

> Si quieren revisar las dependencias que tienen instaladas en el venv, el comando es
```
pip list
```
---