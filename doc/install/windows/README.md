## Instalación de Odoo 15.0 en Windows 11

## Requerimientos   

 - Python **3.8.10**        
 - VS Build Tools **16.11.4** 
 - Wkhtmltopdf **0.12.5-1**
 - Postgresql **13.4**     
 - Odoo **15.0**           


## 1. Instalación de Python

El **path de python** se encuentrará en la siguiente ubicación: C:\Users\\...\AppData\Local\Programs\Python\Python38

**La ejecución del comando de actualización del pip es opcional** 
```
python -m pip install --upgrade pip 
```

## 2. Instalación de VS Build Tools 

Una vez descargada la versión [**VS Build Tools 3.8.10**](https://visualstudio.microsoft.com/es/downloads/), se deberá instalar, seleccionando las opciones, mostradas en la [***ilustración adjunta***](images/library_.png)  



## 3. Instalación de herramientas de línea de comandos

Se deberán instalar las herramientas de línea de comandos de código abierto [**wkhtmltopdf-0.12.5-1**](https://github.com/wkhtmltopdf/wkhtmltopdf/releases/tag/0.12.5), destinadas a la conversión de **HTML** a **PDF** 

## 4. Instalación de PostgreSQL

Una vez instalado PostgreSql, se deberán  realizar las configuraciones correspondientes citadas en la [**información adjunta**](./INSTALL_POSTGRESQL.md)


## 5. Clonación del Repositorio de Odoo 15.0 

Una vez seleccionada la [**versión 15.0 de Odoo**](https://github.com/odoo/odoo/tree/15.0), se creará un directorio (carpeta), donde se ejecutará el siguiente comando: 
```
git clone https://github.com/odoo/odoo.git --depth=1 -b 15.0 
```
Las expresiones: ***--depth=1 -b 15.0***, corresponden a la última versión de Odoo 15.0, a continuación se deberá ejecutar el siguiente comando:
```
pip install setuptools wheel
```
En el directorio de clonación se deberá de editar el archivo : **requeriments.txt**, de la siguiente manera: <br>

libsass==**0.21.0** <br>
cryptography==**3.4.8** <br>
passlib==**1.7.2** <br>
python-stdnum==**1.16** <br>

## 6. Instalación de ***venv*** Python (Entorno Virtual de Python) 

***Únicamente*** en el caso, que no se ejecutacen los comandos de Python, se deberá utilizar la [**información adjunta**](./VENV_PYTHON.md), y ejecutarla en un terminal con **permisos de Administrador**

Para la instalación de todas las **dependencias del proyecto**, se ejecutará el siguiente comando:
```
pip install -r requirements.txt
```

## 7. Ejecución de Odoo 15.0

Se abrirá un terminal y se ejecutará el siguiente comando:

```
python odoo-bin -d odoo15 -r Juan -w mi_password
```
El parámetro: **-d odoo15**, representa la base de datos, la expresión: **-r Juan**, cita el nombre del Rol y el elemento: **-w mi_password**, define el password otorgado al Rol, todos estos parámetros estan detallados en la **Sección 4. Instalación de PostgreSQL**


En el caso, de iniciar Odoo sin datos demostrativos (**datos de prueba**), se debería ejecutar el siguiente comando:

```
python odoo-bin -d odoo15 -r Juan -w mi_password --without-demo=all --stop-after-init
```

Para Finalizar, si los pasos anteriores se realizaron satisfactoriamente se deberá abrir un navegador web y utilizar la siguiente URL:
```
http://localhost:8069
```