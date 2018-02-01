# ForensicDROID

ForensicDROID es una herramienta para asistir a en analisis forense en android.
Coloca el nombre del paquete, El programa automaticamente descargara las APK, datas, permisos de archivos, manifest, bases de datos y logs.
es facil de usar y de interactuar con las opciones !


## Instalacion
Simplemente clonar el repositorio de github

### Dependencias

#### Python
-	python >= 2.6 o mayor(version 2.x)
-	[Python-magic](https://github.com/ahupp/python-magic/)

#### SDK
-	aapt
-	adb
-	hprof-conv

#### Otros
-	dispositivo rooteado
-	sqlite3	

## Modo de Uso
	1) Mostrar mensaje de ayuda
		./androick.py -h

	2) Mostrar Informacion
		./androick.py -a

	3) seleccionar dispositivo a usar
		./androick.py -D serial_number PACKAGE_NAME_1 PACKAGE_NAME_2 ETC...
		./androick.py --device serial_number PACKAGE_NAME_1 PACKAGE_NAME_2 ETC...

	4) buscar por nombre de paquete
		./androick.py [-v] -f <Part of package name>

	5) descargar todo lo necesario de la aplicacion
		./androick.py [-v] -A PACKAGE_NAME_1 PACKAGE_NAME_2 ETC...
	
	6) seleccionar solo lo necesario a extraer
		./androick.py [-v] [-d --datas] [-s --sql] [-m --manifest] [-p --permissions] [-m --memory-dump]  [-l --logs] [--keyLogs="keywords"] PACKAGE_NAME_1 PACKAGE_NAME_2 ETC...

	7) como usar la opcion  --keyLogs
			--keyLogs="key1,key2,key3"
		si es mas de un paquete
			--keyLogs="key1_P1,key2_P1|key1_P2|key1_P3,key2_P3,key3_P3"
		
		Ejemplo :
			./androick.py -l --keyLogs="antivirus,protection|music,licence" com.package.antivirus com.music.player
	
	/!\ La funcioon memory dump no funciona correctamente en builds recientes

## Autor
Axel Vásquez
-Torland.Axel-

## Licencia
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
