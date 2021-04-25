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
        "name": "Temperature [K]", 
        "file": "ERA-5_MAY2019/temp_era5_may2019.nc",
        "plot?": true,
        "vars": ["t"],
        "type": "shading",
        "level": 500,
        "range": [235, 275, 1],
        "colors":"RdYlBu_r"    //para el sombreado, se recomienda escoger un colormap en vez de un color simple
    }

]
}
```
