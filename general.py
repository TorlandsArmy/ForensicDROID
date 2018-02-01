#!/usr/bin/python
# -*- coding: utf8 -*-

from subprocess import Popen, PIPE, STDOUT
import sys

def about():
	print "####################################################"
	print "#	@author		Axel Vásquez		              #"
	print "#	@company	Getbyte			   				  #"
	print "#	@mail		axelvasquez924@gmail.com	 	  #"
	print "#	@mail		java924@gmail.com		 	 	  #"
	print "#	@version	2.0	(Español) 					  #"
	print "#	@licence	GNU GPL v3		   				  #"
	print "#	@dateCreation	27/03/2013		  			  #"
	print "#	@lastModified	01/02/2018		 			  #"
	print "####################################################"
	print ""
	print "ForensicDROID es una conjunto de herramientas para forensia sobre android."

def help():
	print "Modo de uso : "+ sys.argv[0] +" [OPCION] NOMBREDEPAQUETE1 [NOMBREDEPAQUETE2 etc...]"
	print "-a --about : Mas informacion acerca de este programa"
	print "-h --help : Mostrar este mensaje"
	print "-v --verbose : modo vervose "
	print "-D --device : Numero de serie del dispositivo"
	print "-A --all : activar todas las opciones"
	print "-d --datas : obtener los paquetes data de las aplicaciones"
	print "-s --sql : buscar y exportar todas las bases de datos a formato CSV (para usarlo debe de contener el argumento  -d)"
	print "-m --manifest : generar un pequeño archivo manifest"
	print "-p --permissions : Obtener Todos los permisos para los archivos de las aplicaciones"
	print "-M --memory-dump : extraer la informacion en memoria"
	print "  => en la mayoria no funciona en builds recien producidas"
	print "-l --logs : obtener logs de la aplicacion"
	print "--keyLogs : Escoje los keylogs de la aplicacion (default : PACKAGE_NAME, debe de ser usado con argummento -l)"
	print "\tEjemplo : --keyLogs=\"key1,key2,key3\""
	print "  si hay más de un paquete, puede elegir palabras clave para cada paquete haciendo : "
	print "\t--keyLogs=\"key1_P1,key2_P1|key1_P2|key1_P3,key2_P3,key3_P3\" etc..."
	print "-f --find : Encontrar el paquete"
	print ""
	print ""
	print "1) Mostrar Mensaje de ayuda"
	print "\t./ForensicDROID.py -h"
	print ""
	print "2) Mostrar informacion"
	print "\t./ForensicDROID.py -a"
	print ""
	print "3) Seleccionar el dispositivo a usar"
	print "\t./ForensicDROID.py -D serial_number PACKAGE_NAME_1 PACKAGE_NAME_2 ETC..."
	print "\t./ForensicDROID.py --device serial_number PACKAGE_NAME_1 PACKAGE_NAME_2 ETC..."
	print ""
	print "4) Buscar paquete: "
	print "\t./ForensicDROID.py [-v] -f <Parte del nombre del paquete>"
	print ""
	print "5) Descargar todas las cosas relacionadas a la aplicación"
	print "\t./ForensicDROID.py [-v] -A PACKAGE_NAME_1 PACKAGE_NAME_2 ETC..."
	print ""
	print "6) Seleccionar Solo las cosas que quieras extraer"
	print "\t./ForensicDROID.py [-v] [-d --datas] [-s --sql] [-m --manifest] [-p --permissions] [-M --memory-dump] [-l --logs] [--keyLogs=\"keywords\"] PACKAGE_NAME_1 PACKAGE_NAME_2 ETC..."
	print ""
	print "7) Ejemplo con la opcion --keyLogs"
	print "\t./ForensicDROID.py -l --keyLogs=\"antivirus,protection|music,licence\" com.package.antivirus com.music.player"
	
def printVerbose (process):
	while process.poll() is None:
		print process.stdout.readline().replace("\n", "").replace("\r", "")
	process.communicate()


def writeResultToFile (cmd, filename, verbose):
	try:
		f = open(filename, "w")
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		
		while True:
			line = process.stdout.readline()
			if not line:
				break
			
			f.write(line)
			
			if verbose:
				print line.replace("\n", "").replace("\r", "")
		
		process.communicate()
		f.close()
		
		return True
	except IOError as e:
		print "Archivo " + e.filename +" no fue creado"
		print "Error : "+ e.strerror
