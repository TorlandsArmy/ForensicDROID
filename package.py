#!/usr/bin/python
# -*- coding: utf8 -*-

from subprocess import Popen, PIPE, STDOUT
import os
import sys
import datetime
import time
import fnmatch
import magic

from general import *

class Package():
	def __init__(self, package, device):
		self.device 	= device
		self.package 	= package

	# find packages
	def find(self):
		cmd = "adb "+ self.device +" shell pm list packages " + self.package
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		stdout, stderr = process.communicate()
		if stdout == "":
			return False
		else:
			return stdout.replace("package:", "").split()
	
	# check if package exist
	def exist(self):
		print "\nVerificando que el paquete'" + self.package + "' Exista"
		
		result = self.find()
		if result and self.package in result:
			if self.verbose:
				print "Paquete encontrado\n"
			return True
		
		print "Paquete "+ self.package +" No encontrado"
		return False
	
	# extract datas
	def extract(self, verbose, datas, sql, keyLogs, manifest, permissions, memoryDump):
		self.verbose = verbose
		
		if not self.exist():
			return False
		
		self.externalStorage = self.getExternalStorage()
		
		self.createDirectories()
		self.getAPK()
		
		if datas:
			self.getDatas()
			self.getExternalDatas()
			self.getExternalDatasSD()
			self.getLib()
		
		if sql:
			self.getSQL()
		
		if manifest:
			self.getManifest()		
		
		if permissions:
			self.getPermissions()
		
		if memoryDump:
			self.getMemoryDump()
		
		if len(keyLogs) > 0:
			self.getLogs(keyLogs)
		
		return True
		
	def createDirectories(self):
		#create directories
		try:
			self.path = "output/"+ self.package
			if os.path.exists (self.path):
				self.path = "output/"+ self.package +"-"+ datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
			
			self.pathData = self.path + "/data"
			self.pathDataSD = self.path + "/dataSD"
			self.pathDataExternalSD = self.path + "/dataExternalSD"
			self.pathLib = self.path + "/lib"
			self.pathSQL = self.path + "/SQL"
			self.pathLogs = self.path + "/Logs"
			
			if not self.verbose:
				print "Creando directorios ..."
			
			if self.verbose:
				print "Creando directorio : "+ self.pathData
			os.makedirs(self.pathData)
			if self.verbose:
				print "Creando directorio : "+ self.pathDataSD
			os.makedirs(self.pathDataSD)
			if self.verbose:
				print "Creando directorio : "+ self.pathDataExternalSD
			os.makedirs(self.pathDataExternalSD)
			if self.verbose:
				print "Creando directorio : "+ self.pathLib
			os.makedirs(self.pathLib)
			if self.verbose:
				print "Creando directorio : "+ self.pathSQL
			os.makedirs(self.pathSQL)
			if self.verbose:
				print "Creando directorio : "+ self.pathLogs +"\n"
			os.makedirs(self.pathLogs)
		except OSError as e:
			print "Folder " + e.filename +" no creado"
			print "Eroor : "+ e.strerror
	
	def getAPK(self):
		if self.verbose:
			print "Obteniendo ubicacion del APK..."
		#getting apk path
		cmd = "adb "+ self.device +" shell pm path "+ self.package
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		stdout, stderr = process.communicate()
		self.pathToApk = stdout.replace("package:", "")
		if self.verbose:
			print "Ubicaciom del APK : " + self.pathToApk
		
		#pull apk to computer
		print "Descargando APK..."
		cmd = "adb pull "+ self.pathToApk +" "+ self.path + "/" + self.package + ".apk"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		if self.verbose:
			printVerbose (process)
		else:
			process.communicate()
		
		cmd = "adb pull "+ self.pathToApk.replace(".apk", ".odex") +" "+ self.path + "/" + self.package + ".odex"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		if self.verbose:
			printVerbose (process)
		else:
			process.communicate()
		
		print ""
	
	def getDatas(self):
		print "Descargando Datas ..."
			
		if self.verbose:
			print "Creando Directorio temporal"
		cmd = "adb "+ self.device +" shell su -c rm -rf /sdcard/androick/*;mkdir -p /sdcard/androick/"+ self.package
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		process.communicate()
		
		if self.verbose:
			print "Copiando datas al directorio temporal"
		cmd = "adb "+ self.device +" shell su -c cp -r /data/data/"+ self.package +" /sdcard/androick/"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		process.communicate()
		
		if self.verbose:
			print "COlocando datas en la pc"
		cmd = "adb "+ self.device +" pull /sdcard/androick/"+ self.package +" "+ self.pathData
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		if self.verbose:
			printVerbose (process)
		else:
			process.communicate()
		
		if self.verbose:
			print "Eliminando directorio temporal"
		cmd = "adb "+ self.device +" shell rm -rf /sdcard/androick"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE, stdin=PIPE)
		process.communicate()
		print ""
	
	# find external sd storage path
	def getExternalStorage(self):
		if self.verbose:
			print "Buscando ubicacion de tarjeta externa..."
			
		cmd = "adb "+ self.device +" shell echo $EXTERNAL_STORAGE"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		stdout, stderr = process.communicate()
		if stdout == "":
			if self.verbose:
				print "directorio de externa no encontrado\n"
			return False
		else:
			if self.verbose:
				print "Directorio encontrado : " + stdout
			return stdout.replace("\n", "").replace("\r", "")
	
	# download external datas
	def getExternalDatas(self):
		print "Descargando DAtas Externas..."
		
		cmd = "adb "+ self.device +" pull /sdcard/Android/data/"+ self.package +" "+ self.pathDataSD
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		
		if self.verbose:
			printVerbose (process)
		else:
			process.communicate()
		print ""
	
	# download external SD card datas
	def getExternalDatasSD(self):
		print "Descargando datar externas de la SD..."
		
		if self.externalStorage:
			cmd = "adb "+ self.device +" pull "+ self.externalStorage + "/Android/data/"+ self.package +" "+ self.pathDataExternalSD
			process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
			
			if self.verbose:
				printVerbose (process)
			else:
				process.communicate()
		print ""
	
	# download libraries (only for applications who are stored in external SD card)
	def getLib(self):
		if self.pathToApk.find("/data/data/", 0, 11) is -1:
			print "Descargando Librerias..."
			
			cmd = "adb "+ self.device +" pull "+ self.pathToApk.replace("pkg.apk", "lib") +" "+ self.pathLib
			process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
			
			if self.verbose:
				printVerbose (process)
			else:
				process.communicate()
		print ""
	
	# extract databases in csv format
	def getSQL(self):
		print "Buscando Archivos de  Base de datos..."
		mime = magic.Magic()
		for root, dirnames, filenames in os.walk(self.path):
		  for filename in fnmatch.filter(filenames, "*"):
		  	try:
			  	typeFile = mime.from_file(root +"/"+ filename)
				if typeFile is not None and typeFile.find("SQLite", 0, 6) is not -1:
				  	if self.verbose:
				  		print "Base de datos encontrada : "+ root +"/"+ filename
				  	
				  	os.makedirs(self.pathSQL + "/" + filename)
				  	
				  	cmd = "sqlite3 "+ root +"/"+ filename +" .tables"
				  	process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
				  	stdout, stderr = process.communicate()

				  	cmd = "sqlite3 "+ root +"/"+ filename
					process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE, stdin=PIPE)
					process.stdin.write(".headers on\n")
					process.stdin.write(".mode csv\n")
				  	for table in stdout.split():
				  		if self.verbose:
				  			print "\tExtrayendo tabla : "+ table
						process.stdin.write(".output "+ self.pathSQL +"/"+ filename +"/"+ table +".csv\n")
						process.stdin.write("select * from "+ table +";\n")
					process.stdin.write(".quit\n")
					stdout, stderr = process.communicate()
			except IOError:
				continue
			except OSError as e:
				print "Directorio " + e.filename +" no creada "
				print "Error : "+ e.strerror
		print ""
	
	def getManifest(self):
		print "Generando manifest..."
		cmd = "aapt d badging " + self.path + "/" + self.package + ".apk"
		writeResultToFile(cmd, self.path + "/informations", self.verbose)
		
		cmd = "aapt d xmltree " + self.path + "/" + self.package + ".apk" + " AndroidManifest.xml"
		writeResultToFile(cmd, self.path + "/manifest", self.verbose)
		print ""
	
	def getPermissions(self):
		print "Obteniendo permisos sobre archivos..."
		cmd = "adb " + self.device + " shell su -c ls -aRl /data/data/" + self.package + " /sdcard/Android/data/" + self.package
		if self.externalStorage:
			cmd += " " + self.externalStorage + "/Android/data/"+ self.package
		writeResultToFile(cmd, self.path + "/permissions", self.verbose)
		print ""
	
	def getMemoryDump(self):
		print "Obteniendo un heap dump de memoria..."
		
		if self.verbose:
			print "Imprimir la columna y numeros de PID´s..."
		cmd = "adb " + self.device + " shell su -c ps | head -n 1 | awk -F' ' '{for (i = 1; i <= NF; i++) if ($i == \"PID\") print i}'"
		process = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
		column, stderr = process.communicate()
		column = column.replace("\n", "").replace("\r", "")

		try:
			column = int(column)
		except ValueError:
			print "Error : PID  no se ha encontrado la columna y no se puede imprimir el dump de memoria.\n"
			return False

		if self.verbose:
			print "Abriendo la aplicacion (no cerrar hasta que el programa acabe ...)"
		cmd = "adb shell monkey -p " + self.package + " -v 1"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE, stdin=PIPE)
		process.communicate()
		
		if self.verbose:
			print "Buscando PID de la aplicacion..."
		cmd = "adb " + self.device + " shell su -c ps | awk -F' ' '{if ($NF == \"" + self.package + "\r\") print $" + str(column) +"}'"
		process = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
		pid, stderr = process.communicate()
		pid = pid.replace("\n", "").replace("\r", "")
		
		try:
			pid = int(pid)
		except ValueError:
			print "Error : PID no encontrado. no se puede obtener el dump de memoria.\n"
			return False
		
		if self.verbose:
			print "Generando dump de memoria..."
		cmd = "adb " + self.device + " shell su -c am dumpheap " + str(pid) + " /sdcard/androick-memory-heap-dump"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE, stdin=PIPE)
		stdout, stderr = process.communicate()

		if len(stdout) > 1 or stderr is not None:
			print "Error : No se ah podido generar un dump de memoria.\n"
			return False
		
		if self.verbose:
			print "colocando dump de memoria en la computadora..."
		cmd = "adb "+ self.device +" pull /sdcard/androick-memory-heap-dump " + self.path + "/memory-heap-dump"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		process.communicate()
		
		if self.verbose:
			print "eliminando dump de memoria del telefono..."
		cmd = "adb "+ self.device +" shell rm /sdcard/androick-memory-heap-dump"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		process.communicate()
		
		if self.verbose:
			print "convirtiendo dump de memoria a formato hprof..."
		cmd = "hprof-conv " + self.path + "/memory-heap-dump " + self.path + "/memory-heap-dump.hprof"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		process.communicate()
		
		cmd = "rm " + self.path + "/memory-heap-dump"
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		process.communicate()
		print ""		
		
	def getLogs(self, keyLogs):
		print "Obteniendo Logs"
		for key in keyLogs:
			if self.verbose:
				print "Obteniendo Logs Correspondientes de : " + key
			
			cmd = "adb " + self.device + " logcat -d | grep " + key
			writeResultToFile(cmd, self.pathLogs + "/" + key, self.verbose)
	
