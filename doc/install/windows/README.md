## Mi primera Aplicación con Oddo 15.0

### 1. Comando de Odoo con un archivo .conf 
El comando de Odoo puede ser ejecutado de la siguiente manera:
```
(venv) C:\odoo\odoo>python odoo-bin -c ./myfile.conf --save --stop 
``` 
Donde el archivo ./myfile.conf, contiene las configuraciones de arranque del servidor 

Por ejemplo los parametros: dbname, dbuser y dbpassword pueden ser editados
```
 dbname= odoo15
 dbuser= juan
 dbpassword= ***
```
### 2. Comando de Odoo con un archivo .conf y puerto http 
El comando de Odoo puede ser ejecutado con el puerto de la dirección Http:
```
(venv) C:\odoo\odoo>python odoo-bin -c ./myfile.conf --http-port=8081 
```
### 3. Gestión de los mensajes Log del Servidor 
Los niveles de información pueden tener los siguientes niveles de información: **warning/error/critical**

En el archivo ./myfile.conf, se pueden configurar los siguientes parámetros: 
```
log_db= False
log_db_level= warning
log_hanler=:INFO
log_level= info   warning/error/critical
logfile= ./mylog.log   
```
### 4. Creación de un nuevo módulo addons

El path de la ubicación addons, se encuentra generalmente dentro de la carpeta **odoo**, tal como se muestra a continuación:
```
C:\Projects\odoo\addons
```
El directorio o carpeta del nuevo **custom-addons**, debe residir dentro de la carpeta **odoo** 
```
C:\Projects\odoo\custom-addons
```
Comando para añadir un **addons-path**   
```
(venv) C:\Projects\odoo> odoo --addons-path="/home/odoo/projects/odoo/custom-adons" -c odoo.conf --save --stop
```
Comando para añadir un módulo con sus directorios, utilizando  **scaffold**   
```
(venv) C:\Projects\odoo> odoo scaffold mi_modulo ./custom-addons
```
Comando para añadir una base de datos, sin datos demostrativos (**datos de prueba**)     
```
(venv) C:\Projects\odoo> odoo -d odoo15 -r graham -w *** --without-demo=all --stop-after-init
```
Para la instalación del Nuevo Módulo, se deberá utilizar el siguiente comando:
```
(venv) C:\Projects\odoo> odoo -c odoo.conf (-d nombre_bd) -i library_module
```
La expresión encerrada entre parentesis es opcional, selecciona la base de datos

Para la actualización del Módulo, se deberá utilizar el siguiente comando:
```
(venv) C:\Projects\odoo> odoo -c odoo.conf (-d nombre_bd) -u library_module
```
La expresión encerrada entre parentesis es opcional, selecciona la base de datos

### 5. Creando una nueva Aplicación

**Agregar un Item al menu principal**

En el directorio **/views** se crea el archivo: library_menu.xml y deberá tener el siguiente contenido:
```
<odoo>
    <!-- Library App Menu -->
    <menuitem id="menu_library" name="Library" />
</odoo>
```
En el archivo: __manifest__.py, se deberá agregar el siguiente contenido:
```
"data": [
    "views/library_menu.xml",
],
```
**Agregar Grupos de Seguridad**

En el subdirectorio **/security** se debe crear el archivo: **/security/library_security.xml**

En el subdirectorio **/Services/Library** se debe crear el archivo: **/Services/library/base.module_category_services_library**

En el archivo: **/security/library_security.xml**, se deberá agregar el siguiente contenido:
```
<odoo>

  <data>
  <!-- Library User Group -->
  <record id="library_group_user" model="res.groups">
    <field name="name">User</field>
    <field name="category_id"
           ref="base.module_category_services_library"/>
    <field name="implied_ids"
           eval="[(4, ref('base.group_user'))]"/>
  </record>

  <!-- Library Manager Group -->
  <record id="library_group_manager" model="res.groups">
    <field name="name">Manager</field>
    <field name="category_id"
           ref="base.module_category_services_library"/>
    <field name="implied_ids"
           eval="[(4, ref('library_group_user'))]"/>
    <field name="users"
           eval="[(4, ref('base.user_root')),
                  (4, ref('base.user_admin'))]"/>
  </record>

  </data>
  <data noupdate="1">
    <record id="book_user_rule" model="ir.rule">
      <field name="name">Library Book User Access</field>
      <field name="model_id" ref="model_library_book"/>
      <field name="domain_force">
        [('active', '=', True)]
      </field>
      <field name="groups" eval="[(4, ref('library_group_user'))]"/>
    </record>
  </data>

</odoo>
```
En el archivo **__manifest.py__**, debería tener las siguientes instrucciones:
```
"data": [
    "security/library_security.xml",
    "views/library_menu.xml",
],
```
### 6. Agregar Test Automatizados

Se debe agregar en el directorio **/tests** el archivo **tests/__init__.py**, con el siguiente código: 
```
from . import test_book
```
En el directorio **/tests**, se debe agregar el archivo **tests/test_book.py**, con el siguiente código:

```
from odoo.tests.common import TransactionCase

class TestBook(TransactionCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.Book = self.env["library.book"]
        self.book1 = self.Book.create({
            "name": "Odoo Development Essentials",
            "isbn": "879-1-78439-279-6"})

    def test_book_create(self):
        "New Books are active by default"
        self.assertEqual(
            self.book1.active, True
        )
```
**Arrancando los tests**

Con el siguiente comando se arrancan los test 
```
(venv) C:\Projects\odoo> odoo -c odoo.conf -u library_module --test-enable
```
**Probando (Testing) la lógica del negocio**

En el archivo **tests/test_book.py**, agregaremos las siguientes lineas de código, después de **test_book_create()**

```
    def test_check_isbn(self):
        "Check valid ISBN"
        self.assertTrue(self.book1._check_isbn)
```
**Probando (Testing) la seguridad de acceso**

Finalmente el codigo, quedaría de la siguiente manera:

```
from odoo.tests.common import TransactionCase

class TestBook(TransactionCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        user_admin = self.env.ref("base.user_admin")
        self.env = self.env(user=user_admin)
        self.Book = self.env["library.book"]
        self.book1 = self.Book.create({
            "name": "Odoo Development Essentials",
            "isbn": "879-1-78439-279-6"})

    def test_book_create(self):
        "New Books are active by default"
        self.assertEqual(
            self.book1.active, True
        )

    def test_check_isbn(self):
        "Check valid ISBN"
        self.assertTrue(self.book1._check_isbn)
```

### 7. Implementando la capa del modelo

**Creando un data model**




### 8. Creación de un nuevo módulo addons
### 9. Instalación de herramientas de línea de comandos (wkhtmltopdf)
### 10. Instalación de herramientas de línea de comandos (wkhtmltopdf)
### 11. Instalación de herramientas de línea de comandos (wkhtmltopdf)
### 12. Instalación de herramientas de línea de comandos (wkhtmltopdf)









