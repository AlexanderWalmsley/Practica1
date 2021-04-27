# Herramienta para graficar datos meteorológicos
El funcionamiento de esta herramienta esta dividido en 2 funciones principales:
- Un programa para generar gráficos a partir de multiples datasets, configurable a través de un archivo .json que recibirá los parámetros.
- Un programa para realizar operaciones sobre los datos para modificar sus variables o añadir nuevas.


## Instrucciones de uso
### Graficador (plotter.py)
Este programa esta configurado para recorrer una carpeta que contenga configuracionnes en archivos .json y generar a partir de estos varios graficos segun el rango de tiempo definido
las configuraciones de ejemplo se encuentran en Practica1/FIGURES/configs

Es necesario activar un ambiente con todas sus dependencias. }

A continuación se adjuntará un archivo de configuración y se comentará la utilidad e importancia de cada campo:

```javascript
{   //El archivo posee 2 secciones
    //esta primera sección definirá configuraciones generales para el mapa
    "map_settings" : {    
         //se define la proyeccion a utilizar, de momento están implementadas Orthographic, Mercator y PlateCarree
        "projection": "Mercator", 
        //latitud y longitud central, en caso de que alguno no sea necesaria para la proyeccion elegida, dejar en 0     
        "central latitude": 0,           
        "central longitude": 0,
        //seccion del mapa que quiere graficarse, formato: [LatMax,LatMin,LonMax,LonMin]
        "extent": [-60, -100, -50, -20],  
         //Densidad de pixeles, mas alta generará un gráfico con mayor resolucián pero considerablemente mas pesado
        "dpi": 100,  
        "timeframe": [0,32,4],     //período de tiempo a gráficar [start, stop, step]                    
        "coastline_color": "black",       //color para dibujar las lineas costales
        "coastline_res": "10m"            //resolucion en metros de las costas

    },
//la segunda seccion consiste de una lista de diccionarios, aqui se configura cada una de las variables a graficar

"data" : [ 

    {  //identificador de la variable. La carpeta generada para guardar los graficos 
        //consistirá de la concatenación de todos estos valores separados por _
        "id": "cape",      
         //Nombre de la variablew que aparecerá como leyenda en el gráfico                                  
        "name": "MUCAPE",
        //Dataset del cual se tomara la variable a gráficar  
        "file": "ERA-5_MAY2019/cape_slp_twp_era5_may2019.nc",  
         //si este campo es true la variable será graficada, de lo contrario no lo será, 
         //esto existe para poder activar y desactivar variables rapidamente
        "plot?": true,            
         //Variable a referenciar del dataset, debe coincidir con su nombre en este.                                 
        "vars": ["cape"],  
        //Formato al graficar, dividida en 5 tipos: contornos, sombreado, barbas, vectores, y estrellas.        
        "type": "contour",        
         //altura en la cual se seleccionara la variable, si el dataset no contiene alturas,  dejar como null
        "level": null,   ]
        //rango de selección de la variable formato [begin, end, step]
        "range": [0, 3000, 100],
        "sigma": 1,              // nivel de suavización de la curva
        "colors": "b"             //color a utilizar para la variable

    },

    {   //la definicion de barbas y vectores es sumamente similar, reciben parámetros idénticos, a excepcion de "type".
        "id": "wind",
        "name": "Wind",
        "file": "ERA-5_MAY2019/wind_era5_may2019.nc",
        "plot?": true,
        "vars": ["u", "v"],        //solo para graficar barbas y vectores, deben definirse 2 variables en este campo
        "type": "barbs",         //el tipo puede ser referenciado por su nombre en ingles o español
        "length": 7,           //largo de las flechas o vectores
        "level": 850,                       
        "density": 8,       //separación entre las barbas, a mas alto el numero, mayoer separación
        "colors": "k"             

    },

    {
        "id": "tmp",
        "name": "Temperature [F]", 
        "file": "ERA-5_MAY2019/temp_era5_may2019.nc",
        "plot?": true,
        "vars": ["t"],
        "type": "shading",
        "level": 500,
        "range": [-36.67, 35.33, 1.8],  
        "sigma": 1,

       // campo opcional que permite realizar operaciones matemáticas simples
        "conversions": [["subtract", 273.15], ["multiply", 1.8]["add", 32]]  
        "colors":"cmo.thermal"    //para utilizar colormaps del paquete cmocean, cmo.<colormap>
    }
]
}
```
El campo "conversions" que puede ser añadido a cualquiera de los diccionarios que definen una variable a graficar debe tener la siguiente firma: 
```python
array[array[str, float]]
```
Es decir un arreglo de largo indefinido, que contiene arreglos de largo 2 en cada índice. 
Estos arreglos pequeños deben consistir cada uno de un par (operación, valor), de esta forma se aplicará cada operación con el valor que tiene asignado.
Estas operaciones se realizarán secuencialmente, es decir NO respetan el orden algebraico automáticamente, si una suma se encuentra antes que una multipicacón, la suma se realizara primero!

Solo pueden ser operados valores constantes, si es necesario operar entre variables de los datos, será necesario el uso del programa aparte para operar entre los datos.
En el código de ejemplo se muestra una conversión de temperaturas desde Kelvin a Farenheit.


### Operador de Datos (dataoperator.py)

El operador de datos es un programa aparte para realizar operaciones de mayor complejidad, ya sea entre variables de un mismo dataset, o de 2 datasets distintos.

Debido a las limitaciones de los archivos NetCDF y por seguridad esto tiene una restricciones importantes:

- El programa NO modificará variables existentes, ni tampoco puede eliminarlas. Si la variable existe AUNQUE ESTE VACÍA, el programa se saltará la asignación de valores a esa variable, esto es importante porque en caso de algun error en las declaraciones creadas en el archivo .json, se debe empezar con un dataset fresco, o cambiar el nombre de la varible, dado que no encontrará el error hasta después de creada esta variable.

Esto significa que el programa solo puede crear variables nuevas y rellenarlas con el resultado de la operación entre ambos valores.

El programa opera de manera similar a el graficador, recorriendo una carpeta de archivos .json, los cuales pueden contener 1 o mas operaciones dentro de sí, a continuación se mostrará un archivo de ejemplo
```javascript
{   \\es importante que la lista de operaciones se llame "operations", el programa accede a ella a partir de este nombre.
    "operations" : [{
        "new_var_id": "ushear",         \\id de la nueva variable
        "new_var_name": "U Windshear",   \\nombre largo de la nueva variable
        "units": "m s**-1",              \\unidades de la nueva variable                                   
        "file1": "datasets/wind_era5_may2019.nc",   \\el primer archivo 
        "var1": "u",                      \\variable a tomar del primer archivo para la operación
        "file2": "datasets/swind_era5_may2019.nc", \\el segundo archivo (puede ser el mismo que el primero!)
        "var2": "u10",                    \\variable a tomar del segundo archivo

   \\altura a la cual tomar la variable en cada archivo, si alguno no posee el campo de altura, dejarlo como null es importante
        "levels": [850, null],          
        "operation": "subtract",    \\operación a realizar sobre las 2 variables definidas
        "output_file": "datasets/wind_era5_may2019.nc" \\ archivo en el cual se almacenará la nueva variable
    },
        {
        "new_var_id": "vshear",
        "new_var_name": "V Wind Shear",
        "units": "m s**-1",
        "file1": "datasets/wind_era5_may2019.nc",
        "var1": "v",
        "file2": "datasets/swind_era5_may2019.nc",
        "var2": "v10",
        "levels": [850, null],
        "operation": "subtract",
        "output_file": "datasets/wind_era5_may2019.nc"
    
        }]
} 
\\este input resta el viento superficial al viento en altura 850 hPa para generar el sisalle
```


Para añadir una nueva operación al programa es necesario modificar 2 de sus partes:

Primero, en el contstructor de Operator, agregar al diccionario self.ops un par "llave": operación(), 
con el nombre que se usará para invocarla operación desde el archivo .json en la llave.

Segundo, deberá definirse la operación, dado que aún no esta implementada la herencia para la selección de variables, debe verse de esta forma:

```python
    def add(self):
        for i in range(0, len(self.dataset1["time"])):
            if self.settings["levels"][0] is not None:
                var0 = self.dataset1[self.settings["var1"]].sel(level=self.settings["levels"][0]).isel(time=i).values
            else:
                var0 = self.dataset1[self.settings["var1"]].isel(time=i).values
            if self.settings["levels"][1] is not None:
                var1 = self.dataset2[self.settings["var2"]].sel(level=self.settings["levels"][1]).isel(time=i).values
            else:
                var1 = self.dataset2[self.settings["var2"]].isel(time=i).values
            self.var[i, :, :] = (var0 + var1)

        return
```
Donde sólo la ultima linea define la operación con la que se irá rellenando la nueva variable, el resto es la selección de las variables a tomar para la operación, puede ser copiado entre operaciones, e idealmente se implementará que nod eba ser escrita usando herencia.







