## Mi primera aplicación con Odoo 15.0

## 1. Comando de ejecución de Odoo con un archivo .conf 
El comando de arranque de Odoo puede ser ejecutado de la siguiente manera:
```
python odoo-bin -c ./odoo.conf --save --stop 
``` 
Donde el archivo **./odoo.conf**, contiene las configuraciones de arranque del servidor, todos los parámetros podrian ser editados: <br>

 **dbname**= odoo15 <br>
 **dbpassword**= mi_password <br>
 **dbuser**= Juan <br>

## 2. Comando de Odoo con un archivo .conf y el puerto http 

El comando de arranque de Odoo puede ser ejecutado con el puerto de la http:
```
python odoo-bin -c ./odoo.conf --http-port=8081 
```
## 3. Gestión de los mensajes Log del Servidor 

En el archivo **./odoo.conf**, se pueden configurar los niveles de información : **warn/error/critical**.  <br>

**log_db**= False  <br>
**log_db_level**= warning <br>
**log_hanler**=:INFO <br>
**log_level**= info   warn/error/critical <br>
**logfile**= **./mylog.log** <br>  

## 4. Creación de un nuevo módulo addons

El path de la ubicación de los **addons**, se encuentra generalmente en la siguiente ruta:  **C:\Projects\odoo\addons** y el directorio nuevo **custom-addons**, debe residir en la ruta **C:\Projects\odoo\custom-addons**<br>

**Comando para añadir un addons-path**   
```
python odoo-bin --addons-path="/home/odoo/projects/odoo/custom-adons" -c odoo.conf --save --stop
```
Con la utilización de este comando, generalmente suelen borrarse los **addons path** del archivo **./odoo.conf**, por lo que es recomendable agregar la nueva ruta **addons**, editando el archivo **./odoo.conf**    

**Comando para añadir un módulo con sus directorios (esqueleto de directorios), utilizando**  **scaffold**   
```
python odoo-bin scaffold mi_modulo ./custom-addons
```
**Para la instalación del nuevo Módulo, se deberá utilizar el siguiente comando:**
```
python odoo-bin -c odoo.conf -i mi_modulo
```
Con la opción **-i**, se pueden instalar varios módulos separados por una **coma ,** para la **Actualización del Módulo**, se debería utilizar:
```
python odoo-bin -c odoo.conf -u mi_modulo
```
## 5. Creando una nueva aplicación

**Agregar un Item al menu principal**

En el caso, de iniciar Odoo sin datos demostrativos (**datos de prueba**), se debería ejecutar el siguiente comando:     
```
python odoo-bin -d odoo15 -r Juan -w mi_password --without-demo=all --stop-after-init
```
En el directorio **/views** se crea el archivo: [**library_menu.xml**](../docs/ch03/library_app/views/library_menu.xml), el elemento **menuitem**, creará un registro en el modelo: **ir.ui.menu**:

En el archivo: **__manifest__.py**, en la sección **data : [ ]** se deberá agregar el siguiente código: [**"data": ["views/library_menu.xml",],**](../docs/ch03/library_app/__manifest__.py)
<br> <br>
**Agregar Grupos de Seguridad**

&#9655; En el archivo **__manifest__.py** se deberá agregar en la sección **categoría** :  [**"category": "Services/library"**](../docs/ch03/library_app/__manifest__.py)

&#9655; Se deberá crear el archivo: [**/security/library_security.xml**](../docs/ch03/library_app/security/library_security.xml), con los xml's (**name**, **category_id** y **implied_ids**)

&#9655; El archivo [**__manifest.py__**](../docs/ch03/library_app/__manifest__.py), debería tener las siguientes instrucciones: **"data":** **["security/library_security.xml", "views/library_menu.xml",],**

La instrucción **"security/library_security.xml",** siempre deberá estar antes de **"views/library_menu.xml",** 

## 6. Agregar Test Automatizados

&#9655; Se debe agregar en el directorio **/tests** el archivo [**tests/__init__.py**](../docs/ch03/library_app/tests/__init__.py), con el siguiente código: **from . import test_book**

&#9655; En el directorio **/tests**, se debe agregar el archivo [**tests/test_book.py**](../docs/ch03/library_app/tests/test_book.py). Las funciones **test** deberán iniciar con la siguiente expresión: **test_**

**Arrancando los tests**
```
python odoo-bin -c odoo.conf -u library_module --test-enable
```
**Probando (Testing) la lógica del negocio**

En el archivo [**tests/test_book.py**](../docs/ch03/library_app/tests/test_book.py), agregaremos las siguientes líneas de código, después de **test_book_create()**
<br>
~~~
def test_check_isbn(self):
 "Check valid ISBN"
 self.assertTrue(self.book1._check_isbn)
~~~
**Probando (Testing) la seguridad de acceso**

En el archivo [**tests/test_book.py**](../docs/ch03/library_app/tests/test_book.py), se debe agregar dos líneas en la función **def setUp(self,*args,**kwargs)**, la primera busca el registro del usuario **admin** usando XML ID, la segunda línea modifica el ambiente utilizado para arrancar el test **self.env**,cambiando del **usuario activo** al **usuario administrador** 
~~~
user_admin = self.env.ref("base.user_admin")
self.env = self.env(user=user_admin)
~~~

## 7. Implementando la capa del modelo

**Creando un data model**

En el archivo [**__init__.py**](../docs/ch03/library_app/__init__.py) del **root** se deberá agregar: **from . import models**

Se deberá crear el archivo [**models/__init__.py**](../docs/ch03/library_app/models/__init__.py), y agregar la siguiente línea de código: **from . import library_book**

Se crea el archivo [**models/library_book.py**](../docs/ch03/library_app/models/library_book.py)

Ahora para ejecutar los cambios, se debe efectuar la **actualización** del módulo **library_module**, con el siguiente comando:   
```
python odoo-bin -c odoo.conf -u library_module
```
## 8. Configurando la seguridad de acceso

**Seguridad en el Control de Acceso**

Para acceder a las reglas de acceso del modelo, podemos navegar en la aplicación web en el apartado: **Settings|Technical|Security|Access Rights**. Se podría otorgar acceso completo al **Administrador de la Librería**, y a los **usuarios** permisos para **leer**, **escribir** y **crear** libros.
Estos permisos de acceso pueden ser proporcionados por el archivo: [**security/ir.model.access.csv**](../docs/ch03/library_app/security/ir.model.access.csv).
En el archivo **__manifest__.py**, se debería agregar la siguiente línea de código: **security/ir.model.access.csv**.
```
    "data": [
        "security/library_security.xml",
        "security/ir.model.access.csv",
        "views/library_menu.xml",
    ],
```
Para la actualización del Módulo, se deberá utilizar el siguiente comando:
```
python odoo-bin -c odoo.conf -u library_module --test-enable
```
**Reglas de acceso a nivel de fila**

En el archivo: [**security/library-security.xml**](../docs/ch03/library_app/security/library_security.xml), sección **&#60;data&#62;** antes del tag **&#60;&#92;odoo&#62;**, se deben agregar algunas líneas de código

La regla de registro residente en el elemento **&#60;data noupdate="1"&#62;**, determina que estos registros se **crearán en la instalación del módulo**, pero **no se reescribirán en las actualizaciones** del módulo.


## 9. Implementando la capa de vista de backend

**Agregar elementos de menú**

Se crea el archivo [**views/library_menu.xml**](../docs/ch03/library_app/views/library_menu.xml), este archivo de datos describe dos registros de la siguiente manera:
<br><br>
&#9655;El elemento **&#60;record&#62;**  define una acción de ventana del lado del cliente, para abrir el Modelo Library.Book con las vistas de árbol y formulario habilitadas, en ese orden.
<br>
&#9655;El elemento **&#60;menuitem&#62;**, ejecutando la acción **action_library_book**

**Creación de una vista de formulario**

&#9655;Las **vistas** son registros de datos almacenados en la base de datos del modelo **ir.ui.view**, las cuales se almacenan con el elemento **&#60;record&#62;**, descrito en la vista [**views/book_view.xml**](../docs/ch03/library_app/views/book_view.xml)

**Vistas de formulario de documentos del Negocio**

&#9655;En el archivo [**views/book_view.xml**](../docs/ch03/library_app/views/book_view.xml), se detalla el contenido de los elementos **&#60;header&#62;** y **&#60;sheet&#62;**

**Agregar Boton de Acción**

&#9655;En el archivo [**views/book_view.xml**](../docs/ch03/library_app/views/book_view.xml), se detalla el contenido del elemento **<header>** 
<br>
<br>
En el archivo: [**__manifest__.py**](../docs/ch03/library_app/__manifest__.py) del root,  se deberá, agregar la línea de código: **views/book_view.xml**, en el elemento **"data" :[]**


**Usando Grupos para la organización de Formularios**

En el archivo **views/book_view.xml**,citado anteriormente, se organizan los elementos **<group>**
```
<sheet>
  <group name="group_top">
    <group name="group_left">
      <field name="name" /> 
      <field name="author_ids" widget="many2many_tags" /> 
      <field name="publisher_id" /> 
      <field name="date_published" /> 
    </group>
    <group name="group_right">
      <field name="isbn" /> 
      <field name="active" /> 
      <field name="image" widget="image" /> 
    </group>
  </group>
</sheet>
```
**Agregando Listas y Vistas de busqueda**

El elemento **<tree>** deberá contener los campos que se presentarán como columnas, nuevamente se edita el archivo **views/book_view.xml**, agregando el siguiente código antes del elemento **</odoo>**
```
  <record id="view_tree_book" model="ir.ui.view">
    <field name="name">Book List</field>
    <field name="model">library.book</field>
    <field name="arch" type="xml">
      <tree>
        <field name="name"/>
        <field name="isbn"/>
        <field name="author_ids" widget="many2many_tags"/>
        <field name="publisher_id"/>
          <!--<field name="date_published"/>-->
      </tree>
    </field>
  </record>
  
  <record id="view_search_book" model="ir.ui.view">
    <field name="name">Book Filters</field>
    <field name="model">library.book</field>
    <field name="arch" type="xml">
      <search>
        <field name="publisher_id"/>
        <filter name="filter_inactive"
                string="Inactive"
                domain="[('active','=',False)]"/>
        <filter name="filter_active"
                string="Active"
                domain="[('active','=',True)]"/>
      </search>
    </field>
    </record>
    ...
  </odoo>  
```
Finalmente el código del archivo **views/book_view.xml**, quedaría de la siguiente manera :

```
<odoo> 
  <record id="view_form_book" model="ir.ui.view"> 
    <field name="name">Book Form</field> 
    <field name="model">library.book</field> 
    <field name="arch" type="xml"> 
  
      <form string="Book">
        <header>
          <button name="verify_isbn" type="object"
            string="Check ISBN" />
        </header>
        <sheet>
          <group name="group_top">
            <group name="group_left">
              <field name="name" /> 
              <field name="author_ids" widget="many2many_tags" /> 
              <field name="publisher_id" /> 
              <field name="date_published" /> 
            </group>
            <group name="group_right">
              <field name="isbn" /> 
              <field name="active" /> 
              <field name="image" widget="image" /> 
            </group>
        </group>
        </sheet>
      </form> 
    </field> 
  </record>
  
  <record id="view_tree_book" model="ir.ui.view">
    <field name="name">Book List</field>
    <field name="model">library.book</field>
    <field name="arch" type="xml">
      <tree>
        <field name="name"/>
        <field name="isbn"/>
        <field name="author_ids" widget="many2many_tags"/>
        <field name="publisher_id"/>
          <!--<field name="date_published"/>-->
      </tree>
    </field>
  </record>
  
  <record id="view_search_book" model="ir.ui.view">
    <field name="name">Book Filters</field>
    <field name="model">library.book</field>
    <field name="arch" type="xml">
      <search>
        <field name="publisher_id"/>
        <filter name="filter_inactive"
                string="Inactive"
                domain="[('active','=',False)]"/>
        <filter name="filter_active"
                string="Active"
                domain="[('active','=',True)]"/>
      </search>
    </field>
  </record>
  
</odoo>

```
## 10. Implementación de la capa lógica del negocio  

**Agregar la lógica en la capa del negocio**

Ahora el archivo **models/library_book.py**, agregando el **Validador de errores** quedaría de la siguiente manera: 

```
from odoo import fields, models
from odoo.exceptions import ValidationError

class Book(models.Model):
    """
    Describes a Book catalogue.
    """
    _name = "library.book"
    _description = "Book"

    name = fields.Char("Title", required=True)
    isbn = fields.Char("ISBN")
    active = fields.Boolean("Active?", default=True)
    date_published = fields.Date()
    image = fields.Binary("Cover")
    publisher_id = fields.Many2one("res.partner", string="Publisher")
    author_ids = fields.Many2many("res.partner", string="Authors")

    def _check_isbn(self):
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3] * 6
            terms = [a * b for a, b in zip(digits[:12], ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check

    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise ValidationError("Please provide an ISBN for %s" % book.name)
            if book.isbn and not book._check_isbn():
                raise ValidationError("%s ISBN is invalid" % book.isbn)
        return True
```

## 11. Implementación de la Interfaz de Usuario del WebSite

**Agregar el Controlador EndPoint**

Se deberá agregar en el archivo:**library_app/__init__.py** las siguientes líneas de código:

```
from . import models
from . import controllers
```
En el archivo : **library_app/controllers/__init__.py**, se deberá agregar la siguiente línea de código:
```
from . import main
```
En el archivo : **library_app/controllers/main.py**, se deberá agregar el siguiente código:

```
from odoo import http

class Books(http.Controller):

    @http.route("/library/books")
    def list(self, **kwargs):
        Book = http.request.env["library.book"]
        books = Book.search([])
        return http.request.render(
            "library_app.book_list_template",
            {"books": books}
        )
```
La anotación **@http.route** es importante ya que declara que el extremo de la URL está enlazado: a **/books** 

El paso final es usar **http.request.render()** para procesar el **library_app**, para que la plantilla QWeb **index_template** genere el HTML de salida 

**Agregando un QWeb Template**

El archivo de datos de plantilla **QWeb** debe declararse en el **__manifest__.py** del módulo, como cualquier otro archivo de datos XML, para que se cargue y pueda estar disponible.

En el archivo **/__manifest__.py**, se deberá agregar la línea de código: **views/book_list_template.xml**, en el apartado **data[]**, quedando de la siguiente manera:

```
{
    "name": "Library Management",
    "summary": "Manage library catalog and book lending.",
    "author": "Daniel Reis",
    "license": "AGPL-3",
    "website": "https://github.com/PacktPublishing"
               "/Odoo-15-Development-Essentials",
    "version": "15.0.1.0.0",
    "category": "Services/Library",
    "depends": ["base"],
    "data": [
        "security/library_security.xml",
        "security/ir.model.access.csv",
        "views/book_view.xml",
        "views/library_menu.xml",
        "views/book_list_template.xml",
        ],
    "application": True,
}

```
Se deberá crear el archivo: **views/book_list_template.xml**. 

El elemento **template**  declara una plantilla **QWeb**. Es un atajo para un **ir.ui.view** record, el modelo base donde se almacenan las plantillas.

El atributo **t-foreach** se utiliza para recorrer los elementos de la variable **books**, disponibles para la plantilla mediante la llamada **http.request.render()** del controlador. 

El atributo **t-field** se encarga de representar correctamente el contenido de un campo de registro Odoo.

A continuación se deberán agregar las siguientes líneas de código:

```
<odoo>

<template id="book_list_template" name="Book List">
  <div id="wrap" class="container">
    <h1>Books</h1>
      <t t-foreach="books" t-as="book">
        <div class="row">
          <span t-field="book.name" />,
          <span t-field="book.date_published" />,
          <span t-field="book.publisher_id" />
        </div>
      </t>
  </div>
</template>

</odoo>
```

Después de la declaración del archivo **"views/book_list_template.xml"**, en el **__manifest__.py** y realizado la actualización del módulo. 
La página web, debería de trabajar en la url **http://localhost:8069/library/books**, donde sin la necesidad de loguearse, se deberían de listar los libros disponibles  

## Seguridad de Acceso

```
Access security

Internal system models are listed here:
 • res.groups: groups—relevant fields: name, implied_ids, users
 • res.users: users—relevant fields: name, groups_id
 • ir.model.access: Access Control—relevant fields: name, model_id, group_
   id, perm_read, perm_write, perm_create, perm_unlink
 • ir.access.rule: Record Rules—relevant fields: name, model_id, groups,
   domain_force

XML IDs for the most relevant security groups are listed here:
 • base.group_user: internal user—any backend user
 • base.group_system: Settings—the Administrator belongs to this group
 • base.group_no_one: technical feature, usually used to make features not
   visible to users
 • base.group_public: Public, used to make features accessible to web
   anonymous users
XML IDs for the default users provided by Odoo are listed here:
 • base.user_root: The root system superuser, also known as OdooBot.
 • base.user_admin: The default user, by default named Administrator.
 • base.default_user: The template used for new backend users. It is a template
   and is inactive, but can be duplicated to create new users.
 • base.default_public user: The template used to create new portal users.
```



