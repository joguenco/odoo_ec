
## Venv Python (Entorno Virtual de Python) 

***Únicamente*** en el caso, que no se ejecutacen los comandos de Python, se deberán utilizar los siguientes comandos, en una terminal con permisos de **Administrador**
```
Get-ExecutionPolicy
```
```
Get-ExecutionPolicy -List
```
```
Set-ExecutionPolicy  -ExecutionPolicy AllSigned
```
Una vez superados los pasos anteriores se deberá ejecutar el siguiente comando en la ruta: **C:\Users\admin>**
```
pip install virtualenv
```
Para crear los Scripts del proyecto se deberá ejecutar el siguiente comando en la ruta (Ejemplo): **C:\Users\admin\Projects\odoo>** 
```
python -m venv ./venv
```
Una vez ejecutado el comando anterior se crea el siguiente directorio **C:\Users\admin\Projects\odoo\venv\Scripts**

**Entorno virtual de Python**

Para habilitar el ***entorno virtual***, se deberá ejecutar el siguiente comando en un ***terminal con privilegios de Administrador***, en  la ruta (Ejemplo): **C:\Users\admin\Projects\odoo>**
```
.\venv\Scripts\activate
```