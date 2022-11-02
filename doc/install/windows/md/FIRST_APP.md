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

El path de la ubicación de los **addons**, se encuentra generalmente en la siguiente ruta:  **C:\Projects\odoo\addons**

El directorio o carpeta del nuevo **custom-addons**, debe residir dentro de la carpeta **odoo**:  **C:\Projects\odoo\custom-addons**<br>

**Comando para añadir un addons-path**   
```
python odoo-bin --addons-path="/home/odoo/projects/odoo/custom-adons" -c odoo.conf --save --stop
```
Con la utilización de este comando, generalmente suelen borrarse los **paths** del archivo **./odoo.conf**, por lo que es recomendable agregar la nueva ruta **addons**, editando el archivo **./odoo.conf**    

**Comando para añadir un módulo con sus directorios (esqueleto de directorios), utilizando**  **scaffold**   
```
python odoo-bin scaffold mi_modulo ./custom-addons
```
**Para la instalación del nuevo Módulo, se deberá utilizar el siguiente comando:**
```
python odoo-bin -c odoo.conf -i mi_modulo
```
Con la opción **-i**, se pueden instalar varios módulos separados por una **coma ,** para la **actualización del Módulo**, se deberá utilizar el siguiente comando:
```
python odoo-bin -c odoo.conf -u mi_modulo
```
## 5. Creando una nueva aplicación

**Agregar un Item al menu principal**

En el caso, de iniciar Odoo sin datos demostrativos (**datos de prueba**), se debería ejecutar el siguiente comando:     
```
python odoo-bin -d odoo15 -r Juan -w mi_password --without-demo=all --stop-after-init
```
En el directorio **/views** se crea el archivo: library_menu.xml, el elemento **<menuitem>**, es una instrucción para escribir un registro en el modelo:**ir.ui.menu**:
```
<odoo>
    <!-- Library App Menu -->
    <menuitem id="menu_library" name="Library" />
</odoo>
```
En el archivo: __manifest__.py, se deberá agregar el siguiente código:
```
"data": [
    "views/library_menu.xml",
],
```
**Agregar Grupos de Seguridad**

En el archivo **__manifest__.py** se deberá agregar la categoría :
```
"category": "Services/library"
```
Una vez asignado el ID XML **(Services/library)**, al módulo categoría **(category)**, se genera automaticamente el prefijo del nombre de la categoría, para este caso tendríamos:
```
base.module_category_services_library  ("category": "Services/library")
```
Se deberá crear el archivo: **/security/library_security.xml**, y agregar el siguiente contenido:
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
  </data>
</odoo>
```
Los XML's (name, category_id y implied_ids), son agregados en un registro al modelo **res.groups**
Se deberá editar el archivo: **/security/library_security.xml**, y agregar el siguiente contenido:
```
<odoo>
  <data>
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
</odoo>
```
El archivo **__manifest.py__**, debería tener las siguientes instrucciones:
```
"data": [
    "security/library_security.xml",
    "views/library_menu.xml",
],
```
La instrucción **"security/library_security.xml",**, siempre deberá estar antes de **"views/library_menu.xml",** 

## 6. Agregar Test Automatizados

Se debe agregar en el directorio **/tests** el archivo **tests/__init__.py**, con el siguiente código: 
```
from . import test_book
```
En el directorio **/tests**, se debe agregar el archivo **tests/test_book.py**, con el siguiente código:
Las funciones **test** deberán iniciar con la siguiente expresión: **test_**

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

Con el siguiente comando se arrancan los test: 
```
python odoo-bin -c odoo.conf -u library_module --test-enable
```
**Probando (Testing) la lógica del negocio**

En el archivo **tests/test_book.py**, agregaremos las siguientes líneas de código, después de **test_book_create()**

```
    def test_check_isbn(self):
        "Check valid ISBN"
        self.assertTrue(self.book1._check_isbn)
```
**Probando (Testing) la seguridad de acceso**

Se debe agregar dos líneas en la función **def setUp(self,*args,**kwargs)**, la primera busca el registro del usuario **admin** usando XML ID, la segunda línea modifica el ambiente utilizado para arrancar el test **self.env**,cambiando del **usuario activo** al **usuario administrador** 

```
user_admin = self.env.ref("base.user_admin")
self.env = self.env(user=user_admin)
```
Finalmente el código, quedaría de la siguiente manera:

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

## 7. Implementando la capa del modelo

**Creando un data model**

En el archivo __init__.py se deberá agregar:
```
from . import models
```
Se deberá crear el archivo **models/__init__.py**, y agregar la siguiente línea de código:

```
from . import library_book
```
Crear el archivo **models/library_book.py**, y agregar las siguientes líneas de código:
```
from odoo import fields, models

class Book(models.Model):
    _name = "library.book"
    _description = "Book"

    name = fields.Char("Title", required=True)
    isbn = fields.Char("ISBN")
    active = fields.Boolean("Active?", default=True)
    date_published = fields.Date()
    image = fields.Binary("Cover")
    publisher_id = fields.Many2one("res.partner", string="Publisher")
    author_ids = fields.Many2many("res.partner", string="Authors")
```
Ahora para ejecutar los cambios, se debe efectuar la **actualización** del módulo **library_module**, con el siguiente comando:   

```
python odoo-bin -c odoo.conf -u library_module
```
## 8. Configurando la seguridad de acceso

**Seguridad en el Control de Acceso**

Para acceder a las reglas de acceso del modelo, podemos navegar en la aplicación web en el apartado: **Settings|Technical|Security|Access Rights** 

Se podría otorgar accesos a los usuarios de la biblioteca para leer, escribir, crear libros y otorgar acceso completo al **administrador** de la biblioteca.

Estos permisos de acceso pueden ser proporcionados por un archivo de datos de módulo, cargando los registros en el **ir.model**

En el directorio **/security**, se debe agregar el archivo **security/ir.model.access.csv**, con el siguiente contenido:
```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_book_user,BookUser,model_library_book,library_group_user,1,1,1,0
access_book_manager,BookManager,model_library_book,library_group_manager,1,1,1,1
```
En el archivo **__manifest__.py**, se debería agregar la siguiente línea de código: **security/ir.model.access.csv**, de manera que el archivo deberá quedar de la siguiente manera:
```
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'views/library_menu.xml',
    ],
```
Para la actualización del Módulo, se deberá utilizar el siguiente comando:
```
python odoo-bin -c odoo.conf -u library_module --test-enable
```
**Reglas de acceso a nivel de fila**

En el archivo: **security/library-security.xml**, sección <data> antes de el tag </odoo>, se deben agregar las siguientes líneas de código:
```
<odoo>
  ...
  <data noupdate="1">
    <record id="book_user_rule" model="ir.rule">
      <field name="name">Library Book User Access</field>
      <field name="model_id" ref="model_library_book"/>
      <field name="domain_force">
        [('active', '=', True)]
      </field>
      <field name="groups" eval="[(4, 
        ref('library_group_user'))]"/>
    </record>
  </data>

</odoo>
```
La regla de registro está dentro de un elemento **<data noupdate="1">**, lo que significa que esos
registros se crearán en la instalación del módulo, pero no se reescribirán en las actualizaciones del módulo.

Finalmente el archivo: **security/library-security.xml**, quedaría de la siguiente manera: 

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
      <field name="groups" eval="[(4, 
        ref('library_group_user'))]"/>
    </record>
  </data>
  
</odoo>
```

## 9. Implementando la capa de vista de backend

**Agregar elementos de menú**

El archivo **views/library_menu.xml**, deberá contener el siguiente código: 
```
<odoo>

  <!-- Action to open the Book list -->
  <record id="action_library_book" model="ir.actions.act_window">
    <field name="name">Library Books</field>
    <field name="res_model">library.book</field>
    <field name="view_mode">tree,form</field>
  </record>
  
  <!-- Menu item to open the Book list -->
  <menuitem id="menu_library_book"
    name="Books"
    parent="menu_library"
    action="action_library_book"
  />

</odoo>
```

Este archivo de datos describe dos registros de la siguiente manera:

• El elemento <record>  define una acción de ventana del lado del cliente, para abrir el Modelo Library.Book con las vistas de árbol y formulario habilitadas, en ese orden.
• El elemento <menuitem> for Books, ejecutando la acción **action_library_book**

**Creación de una vista de formulario**

Las Vistas son registros de datos almacenados en la base de datos en el modelo **ir.ui.view**, las cuales se almacenan con el elemento **<record>**, descrito en la vista **views/book_view.xml**

Se crea el archivo **views/book_view.xml**, el cuál deberá tener el siguiente código:

```
<odoo> 
  <record id="view_form_book" model="ir.ui.view"> 
    <field name="name">Book Form</field> 
    <field name="model">library.book</field> 
    <field name="arch" type="xml"> 
      <form string="Book">
        <group>
          <field name="name" /> 
          <field name="author_ids" widget="many2many_tags" /> 
          <field name="publisher_id" /> 
          <field name="date_published" /> 
          <field name="isbn" /> 
          <field name="active" /> 
          <field name="image" widget="image" /> 
        </group>
      </form> 
    </field> 
  </record>
    
</odoo>
```
En el archivo: **__manifest__.py** del root,  se deberá, agregar la línea de código: **views/book_view.xml**, en el elemento **"data" :[]**

```
    'name': "library_module",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Esta es una descripcion extendida
        de mi nuevo modulo
        para aprender odoo
    """,

    'author': "Jorge Luis",
    'website': "http://mestizos.dev",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Library',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'views/book_view.xml',
        'views/library_menu.xml',
        'views/book_list_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
```
**Vistas de formulario de documentos del Negocio**

En el archivo **views/book_view.xml**, se agregan los elementos **<header>** y **<sheet>**
```
<odoo>  
  <form>
    <header>
    </header>
    <sheet>
      <group>
        <field name="name" /> 
        <field name="author_ids" widget="many2many_tags" /> 
        <field name="publisher_id" /> 
        <field name="date_published" /> 
            
        <field name="isbn" /> 
        <field name="active" /> 
        <field name="image" widget="image" />
      </group>
    </sheet>
  </form>
</odoo>
```
**Agregar Boton de Acción**

En el archivo **views/book_view.xml**, citado anteriormente, se agregará el siguiente código, en el elemento **<header>** 

```
<header>
   <button name="verify_isbn" type="object" string="Check ISBN" />
</header>
```
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



