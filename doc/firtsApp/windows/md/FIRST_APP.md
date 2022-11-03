## Mi primera aplicación con Odoo 15.0

## 1. Comando de ejecución de Odoo con un archivo .conf
```
python odoo-bin -c ./odoo.conf --save --stop 
``` 
Donde el archivo **./odoo.conf**, contiene las configuraciones de arranque del servidor, todos los parámetros podrían ser editados: <br>

 **dbname**= odoo15 <br>
 **dbpassword**= mi_password <br>
 **dbuser**= Juan <br>

## 2. Comando de Odoo con un archivo .conf y el puerto http
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

El path de la ubicación de los **addons**, se encuentra generalmente en la siguiente ruta:  **C:\Projects\odoo\addons** y el nuevo directorio **custom-addons**, debe residir en la ruta **C:\Projects\odoo\custom-addons**<br>

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
En el directorio **/views** se crea el archivo: [**library_menu.xml**](../docs/ch03/library_app/views/library_menu.xml), el elemento **&#60;menuitem&#62;**, creará un registro en el modelo: **ir.ui.menu**:

En el archivo: **&#95;&#95;manifest&#95;&#95;.py**, en la sección **data : [ ]** se deberá agregar el siguiente código: [**"data": ["views/library_menu.xml",],**](../../../firtsApp/windows/docs/ch03/library_app/__manifest__.py)
<br> <br>
**Agregar Grupos de Seguridad**

&#9655; En el archivo **&#95;&#95;manifest&#95;&#95;.py** se deberá agregar en la sección **categoría** :  [**"category": "Services/library"**](../../../firtsApp/windows/docs/ch03/library_app/__manifest__.py)

&#9655; Se deberá crear el archivo: [**/security/library_security.xml**](../../../firtsApp/windows/docs/ch03/library_app/security/library_security.xml), con los xml's (**name**, **category_id** y **implied_ids**)

&#9655; El archivo [**&#95;&#95;manifest&#95;&#95;.py**](../../../firtsApp/windows/docs/ch03/library_app/__manifest__.py), debería tener las siguientes instrucciones: **"data":** **["security/library_security.xml", "views/library_menu.xml",],**

La instrucción **"security/library_security.xml",** siempre deberá estar antes de **"views/library_menu.xml",** 

## 6. Agregar Test Automatizados

&#9655; Se debe agregar en el directorio **/tests** el archivo [**tests/__init__.py**](../../../firtsApp/windows/docs/ch03/library_app/tests/__init__.py), con el siguiente código: **from . import test_book**

&#9655; En el directorio **/tests**, se debe agregar el archivo [**tests/test_book.py**](../../../firtsApp/windows/docs/ch03/library_app/tests/test_book.py), las funciones **test** siempre deberán iniciar con la expresión: **test_**

**Arrancando los tests**
```
python odoo-bin -c odoo.conf -u library_module --test-enable
```
**Probando (Testing) la lógica del negocio**

En el archivo [**tests/test_book.py**](../../../firtsApp/windows/docs/ch03/library_app/tests/test_book.py), agregaremos las siguientes líneas de código, después de **test_book_create()**
<br>
~~~
def test_check_isbn(self):
 "Check valid ISBN"
 self.assertTrue(self.book1._check_isbn)
~~~
**Probando (Testing) la seguridad de acceso**

En el archivo [**tests/test_book.py**](../../../firtsApp/windows/docs/ch03/library_app/tests/test_book.py), se deben agregar dos líneas de código en la función **def setUp(self,&#42;args,&#42;&#42;kwargs)**, la primera busca el registro del usuario **admin** usando XML ID, y la segunda línea modifica el ambiente utilizado para arrancar el **test self.env**, cambiando del **usuario activo** al **usuario administrador** 
~~~
user_admin = self.env.ref("base.user_admin")
self.env = self.env(user=user_admin)
~~~

## 7. Implementando la capa del modelo

**Creando un data model**

En el archivo [**&#95;&#95;init&#95;&#95;.py**](../../../firtsApp/windows/docs/ch03/library_app/__init__.py) del **root** se deberá agregar: **from . import models**

Se deberá crear el archivo [**models/&#95;&#95;init&#95;&#95;.py**](../../../firtsApp/windows/docs/ch03/library_app/models/__init__.py), y agregar la siguiente línea de código: **from . import library_book**

Se crea el archivo [**models/library_book.py**](../../../firtsApp/windows/docs/ch03/library_app/models/library_book.py), y se debe efectuar **actualizar** el módulo **library_module**   
```
python odoo-bin -c odoo.conf -u library_module
```
## 8. Configurando la seguridad de acceso

**Seguridad en el Control de Acceso**

Para administrar las reglas de acceso del modelo, se podría ingresar a la aplicación web en el apartado: **Settings|Technical|Security|Access Rights**. Donde se otorgaría acceso completo al **Administrador de la Librería**, y a los **usuarios** permisos para **leer**, **escribir** y **crear** libros.
Estos permisos de acceso pueden ser configurados en el archivo: [**security/ir.model.access.csv**](../../../firtsApp/windows/docs/ch03/library_app/security/ir.model.access.csv).
En el archivo **&#95;&#95;manifest&#95;&#95;.py** del **root**, se debería agregar la siguiente línea de código: **security/ir.model.access.csv**.
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

En el archivo: [**security/library-security.xml**](../../../firtsApp/windows/docs/ch03/library_app/security/library_security.xml), sección **&#60;data&#62;** antes del tag **&#60;&#92;odoo&#62;**, la regla de registro residente en el elemento **&#60;data noupdate="1"&#62;**, determina que estos registros se **crearán en la instalación del módulo**, pero **no se reescribirán en las actualizaciones** del módulo.


## 9. Implementando la capa de vista de backend

**Agregar elementos de menú**

Se crea el archivo [**views/library_menu.xml**](../../../firtsApp/windows/docs/ch03/library_app/views/library_menu.xml), que describe la información de dos registros:

&#9655;El elemento **&#60;record&#62;**  define una acción de ventana del lado del cliente, con las vistas de árbol y formulario habilitadas

&#9655;El elemento **&#60;menuitem&#62;**, ejecuta la acción **action_library_book**

**Creación de una vista de formulario**

&#9655;Las vistas son registros almacenados en el modelo **ir.ui.view**, con el elemento **&#60;record&#62;**, descrito en la vista [**views/book_view.xml**](../../../firtsApp/windows/docs/ch03/library_app/views/book_view.xml)

&#9655;**Vistas de formulario de documentos del Negocio**, descritas en los elementos [**&#60;header&#62;**](../../../firtsApp/windows/docs/ch03/library_app/views/book_view.xml) y [**&#60;sheet&#62;**](../../../firtsApp/windows/docs/ch03/library_app/views/book_view.xml)

&#9655;**Agregar Boton de Acción**, descrito en el elemento [**&#60;header&#62;**](../../../firtsApp/windows/docs/ch03/library_app/views/book_view.xml) 

&#9655;**Usando Grupos para la organización de Formularios**, organizados en los elementos [**&#60;group&#62;**](../../../firtsApp/windows/docs/ch03/library_app/views/book_view.xml)

&#9655;**Agregando Listas y Vistas de busqueda**, el elemento [**&#60;tree&#62;**](../../../firtsApp/windows/docs/ch03/library_app/views/book_view.xml) contiene los campos que se presentarán como columnas
<br> <br>
En el archivo: [**&#95;&#95;manifest&#95;&#95;.py**](../../../firtsApp/windows/docs/ch03/library_app/__manifest__.py) del root,  se deberá, agregar la línea de código: **views/book_view.xml**, en el elemento **"data" :[ ]**

## 10. Implementación de la capa lógica del negocio  

**Agregar la lógica en la capa del negocio**

Ahora en el archivo [**models/library_book.py**](../../../firtsApp/windows/docs/ch03/library_app/models/library_book.py), se le agrega un **Validador de errores**  


## 11. Implementación de la Interfaz de Usuario del WebSite

**Agregar el Controlador EndPoint**

Se deberá agregar en el archivo: [**library_app/&#95;&#95;init&#95;&#95;.py**](../../../firtsApp/windows/docs/ch03/library_app/__init__.py) las siguientes líneas de código:

```
from . import models
from . import controllers
```
En el archivo : [**library_app/controllers/&#95;&#95;init&#95;&#95;.py**](../../../firtsApp/windows/docs/ch03/library_app/controllers/__init__.py), se deberá agregar la siguiente línea de código: **from . import main**

En el archivo : [**library_app/controllers/main.py**](../../../firtsApp/windows/docs/ch03/library_app/controllers/main.py), se deberá agregar el siguiente código:

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
La anotación **@http.route**, declara que el extremo de la URL está enlazado: a **/books**. La instrucción **http.request.render()** procesa el **library_app**, para que la plantilla **index_template** genere el **HTML** de salida 

**Agregando un QWeb Template**

Se crea el archivo: [**(views/book_list_template.xml)**](../../../firtsApp/windows/docs/ch03/library_app/views/book_list_template.xml) 

&#9655;El elemento **&#60;template&#62;**  declara la existencia de una plantilla **QWeb**

&#9655;El atributo **&#60;t-foreach&#62;** se utiliza para recorrer los elementos de la variable **books**, disponibles para la plantilla **QWeb**  

&#9655;El atributo **&#60;t-field&#62;** se encarga de representar correctamente el contenido de un campo de registro de la plantilla.

&#9655;La plantilla **&#60;QWeb&#62;** [**(views/book_list_template.xml)**](../../../firtsApp/windows/docs/ch03/library_app/views/book_list_template.xml), debe declararse en el archivo [**&#95;&#95;manifest&#95;&#95;.py**](../../../firtsApp/windows/docs/ch03/library_app/__manifest__.py) en el apartado **data[ ]**, como un archivo XML

Una vez realizada la actualización del módulo, la página web, debería de trabajar en la url **http://localhost:8069/library/books**, donde sin la necesidad de loguearse, se deberían de listar los libros disponibles  

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



