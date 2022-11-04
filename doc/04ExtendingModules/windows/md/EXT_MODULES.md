## Extendiendo módulos

## 1. Ampliación de la aplicación Biblioteca
Para iniciar se debe crear el directorio [**/library_member**](../../windows/docs/library_member), dentro del mismo se debe crear un archivo [**/&#95;&#95;init&#95;&#95;.py**](../../windows/docs/library_member/__init__.py) que inicialmente deberá estar vacio y una archivo [**/&#95;&#95;manifest&#95;&#95;.py**](../../windows/docs/library_member/__manifest__.py). El directorio [**/library_member**](../../windows/docs/library_member), debe estar al mismo orden jerárquico (junto) al directorio [**/library_app**](../../windows/docs/library_app) 
## 2. Agregar nuevos campos con la extensión del modelo
Para extender un modelo existente, se debera usar una **Python Class** con el atributo **_inherit** que identifica el modelo que se va a ampliar.
Es recomendable tener un archivo Python por cada modelo, así que se debe agregar el archivo [**/library_member/models/&#95;&#95;init&#95;&#95;.py**](../../windows/docs/library_member/models/__init__.py), encargado de ampliar el modelo original    
## 3. Ampliación de modelos utilizando la extensión
## 4. Modelos enbebidos usando herencia de delegación
## 5. Extendiendo Vistas y datos
## 6. Extendiendo Páginas Web

```
python odoo-bin -c ./odoo.conf --save --stop 
``` 

&#9655; En el archivo **&#95;&#95;manifest&#95;&#95;.py** se deberá agregar en la sección **categoría** :  [**"category": "Services/library"**](../../windows/docs/ch03/library_app/__manifest__.py)

&#9655; Se deberá crear el archivo: [**/security/library_security.xml**](../../windows/docs/ch03/library_app/security/library_security.xml), con los xml's (**name**, **category_id** y **implied_ids**)

&#9655; El archivo [**&#95;&#95;manifest&#95;&#95;.py**](../../windows/docs/ch03/library_app/__manifest__.py), debería tener las siguientes instrucciones: **"data":** **["security/library_security.xml", "views/library_menu.xml",],**

La instrucción **"security/library_security.xml",** siempre deberá estar antes de **"views/library_menu.xml",** 

## 6. Agregar Test Automatizados

&#9655; Se debe agregar en el directorio **/tests** el archivo [**tests/&#95;&#95;init&#95;&#95;.py**](../../windows/docs/ch03/library_app/tests/__init__.py), con el siguiente código: **from . import test_book**

&#9655; En el directorio **/tests**, se debe agregar el archivo [**tests/test_book.py**](../../windows/docs/ch03/library_app/tests/test_book.py), las funciones **test** siempre deberán iniciar con la expresión: **test_**

**Arrancando los tests**
**Probando (Testing) la lógica del negocio**

En el archivo [**tests/test_book.py**](../../windows/docs/ch03/library_app/tests/test_book.py), agregaremos las siguientes líneas de código, después de **test_book_create()**
<br>
**Probando (Testing) la seguridad de acceso**

En el archivo [**tests/test_book.py**](../../windows/docs/ch03/library_app/tests/test_book.py), se deben agregar dos líneas de código en la función **def setUp(self,&#42;args,&#42;&#42;kwargs)**, la primera busca el registro del usuario **admin** usando XML ID, y la segunda línea modifica el ambiente utilizado para arrancar el **test self.env**, cambiando del **usuario activo** al **usuario administrador** 
~~~
user_admin = self.env.ref("base.user_admin")
self.env = self.env(user=user_admin)
~~~

## 7. Implementando la capa del modelo

**Creando un data model**

En el archivo [**&#95;&#95;init&#95;&#95;.py**](../../windows/docs/ch03/library_app/__init__.py) del **root** se deberá agregar: **from . import models**

Se deberá crear el archivo [**models/&#95;&#95;init&#95;&#95;.py**](../../windows/docs/ch03/library_app/models/__init__.py), y agregar la siguiente línea de código: **from . import library_book**

Se crea el archivo [**models/library_book.py**](../../windows/docs/ch03/library_app/models/library_book.py), y se debe efectuar **actualizar** el módulo **library_module**   
```
python odoo-bin -c odoo.conf -u library_module
```
## 8. Configurando la seguridad de acceso

**Seguridad en el Control de Acceso**

Para administrar las reglas de acceso del modelo, se podría ingresar a la aplicación web en el apartado: **Settings|Technical|Security|Access Rights**. Donde se otorgaría acceso completo al **Administrador de la Librería**, y a los **usuarios** permisos para **leer**, **escribir** y **crear** libros.
Estos permisos de acceso pueden ser configurados en el archivo: [**security/ir.model.access.csv**](../../windows/docs/ch03/library_app/security/ir.model.access.csv).
En el archivo **&#95;&#95;manifest&#95;&#95;.py** del **root**, se debería agregar la siguiente línea de código: **security/ir.model.access.csv**.
Para la actualización del Módulo, se deberá utilizar el siguiente comando:
```
python odoo-bin -c odoo.conf -u library_module --test-enable
```
**Reglas de acceso a nivel de fila**

En el archivo: [**security/library-security.xml**](../../windows/docs/ch03/library_app/security/library_security.xml), sección **&#60;data&#62;** antes del tag **&#60;&#92;odoo&#62;**, la regla de registro residente en el elemento **&#60;data noupdate="1"&#62;**, determina que estos registros se **crearán en la instalación del módulo**, pero **no se reescribirán en las actualizaciones** del módulo.


## 9. Implementando la capa de vista de backend

**Agregar elementos de menú**

Se crea el archivo [**views/library_menu.xml**](../../windows/docs/ch03/library_app/views/library_menu.xml), que describe la información de dos registros:

&#9655;El elemento **&#60;record&#62;**  define una acción de ventana del lado del cliente, con las vistas de árbol y formulario habilitadas

&#9655;El elemento **&#60;menuitem&#62;**, ejecuta la acción **action_library_book**

**Creación de una vista de formulario**

&#9655;Las vistas son registros almacenados en el modelo **ir.ui.view**, con el elemento **&#60;record&#62;**, descrito en la vista [**views/book_view.xml**](../../windows/docs/ch03/library_app/views/book_view.xml)

&#9655;**Vistas de formulario de documentos del Negocio**, descritas en los elementos [**&#60;header&#62;**](../../windows/docs/ch03/library_app/views/book_view.xml) y [**&#60;sheet&#62;**](../../windows/docs/ch03/library_app/views/book_view.xml)

&#9655;**Agregar Boton de Acción**, descrito en el elemento [**&#60;header&#62;**](../../windows/docs/ch03/library_app/views/book_view.xml) 

&#9655;**Usando Grupos para la organización de Formularios**, organizados en los elementos [**&#60;group&#62;**](../../windows/docs/ch03/library_app/views/book_view.xml)

&#9655;**Agregando Listas y Vistas de busqueda**, el elemento [**&#60;tree&#62;**](../../windows/docs/ch03/library_app/views/book_view.xml) contiene los campos que se presentarán como columnas
<br> <br>
En el archivo: [**&#95;&#95;manifest&#95;&#95;.py**](../../windows/docs/ch03/library_app/__manifest__.py) del root,  se deberá, agregar la línea de código: **views/book_view.xml**, en el elemento **"data" :[ ]**

## 10. Implementación de la capa lógica del negocio  

**Agregar la lógica en la capa del negocio**

Ahora en el archivo [**models/library_book.py**](../../windows/docs/ch03/library_app/models/library_book.py), se le agrega un **Validador de errores**  


## 11. Implementación de la Interfaz de Usuario del WebSite

**Agregar el Controlador EndPoint**

Se deberá agregar en el archivo: [**library_app/&#95;&#95;init&#95;&#95;.py**](../../windows/docs/ch03/library_app/__init__.py) las siguientes líneas de código:

```
from . import models
from . import controllers
```
En el archivo : [**library_app/controllers/&#95;&#95;init&#95;&#95;.py**](../../windows/docs/ch03/library_app/controllers/__init__.py), se deberá agregar la siguiente línea de código: **from . import main**

En el archivo : [**library_app/controllers/main.py**](../../windows/docs/ch03/library_app/controllers/main.py), se deberá agregar el siguiente código:

La anotación **@http.route**, declara que el extremo de la URL está enlazado: a **/books**. La instrucción **http.request.render()** procesa el **library_app**, para que la plantilla **index_template** genere el **HTML** de salida 

**Agregando un QWeb Template**

Se crea el archivo: [**(views/book_list_template.xml)**](../../windows/docs/ch03/library_app/views/book_list_template.xml) 

&#9655;El elemento **&#60;template&#62;**  declara la existencia de una plantilla **QWeb**

&#9655;El atributo **&#60;t-foreach&#62;** se utiliza para recorrer los elementos de la variable **books**, disponibles para la plantilla **QWeb**  

&#9655;El atributo **&#60;t-field&#62;** se encarga de representar correctamente el contenido de un campo de registro de la plantilla.

&#9655;La plantilla **&#60;QWeb&#62;** [**(views/book_list_template.xml)**](../../windows/docs/ch03/library_app/views/book_list_template.xml), debe declararse en el archivo [**&#95;&#95;manifest&#95;&#95;.py**](../../windows/docs/ch03/library_app/__manifest__.py) en el apartado **data[ ]**, como un archivo XML

Una vez realizada la actualización del módulo, la página web, debería de trabajar en la url **http://localhost:8069/library/books**, donde sin la necesidad de loguearse, se deberían de listar los libros disponibles  




