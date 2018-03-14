#!/usr/bin/python3

import webapp
import csv

dicc_acortadas = {}
dicc_completas = {}

#with open('fich.txt', 'r') as myfile:
#	line = csv.reader(myfile)
#	for row in line:
#		print(row)
#		llave = row[0]
#		valor = row[1]
#		dicc_acortadas[llave] = valor
#		dicc_completas[valor] = llave
#myfile.close()	
	

formulario = """
 <form action="" method="POST">
  Url:<br>
  <input type="text" name="url" value=""><br>
  <input type="submit" value="Acortar">
</form> 
"""

def devuelve_urls(dicc_acortadas):
	urls = ""
	for key,value in dicc_acortadas.items():
		url_acortada = '<a href=' + "http://localhost:4567" + key + '>' + key + '</a>'
		url = '<a href=' + value + '>' + value + '</a>'
		urls += (url_acortada + " --> " + url+ "<br>")
	return urls

class contentApp(webapp.webApp):
	def parse(self, request):
		return (request.split()[0], request.split()[1], request)

	def process(self, parsedRequest): 
		metodo, recurso, peticion = parsedRequest

		if metodo == "GET":
			if recurso == "/":

				respuesta = devuelve_urls(dicc_acortadas)
				return("200 OK", "<html>Introduce tu url para acortarla!!<br>" + formulario + "Urls acortadas y sin acortar:" + 						
						"<br>" + respuesta + '</html>')
			else:

				if recurso in dicc_acortadas:
					url = dicc_acortadas[recurso]
					return("307 Redirect" + "\n" + "Location: " + url, "")
				else:
					respuesta = "Recurso no disponible"
					return("404 Not Found", "<html>" + respuesta + '</html>')
		

		if metodo == "POST":
			url = peticion.split('\r\n\r\n',1)[1].split('=')[1]
			if url == "":
				respuesta = "ERROR. Introduce una url"
				return("200 OK", "<html>Introduce tu url para acortarla!!<br>" + formulario + "Urls acortadas y sin acortar:" + 						
						"<br>" + respuesta + '</html>')

			if (url.find("http%3A%2F%2F") == 0) or (url.find("https%3A%2F%2F") == 0):
				url = url.split("%3A%2F%2F")[0] + "://"  + url.split("%3A%2F%2F")[1]
			else:
				url = "http://" + url

			if url in dicc_completas:
				respuesta = devuelve_urls(dicc_acortadas)
				return("200 OK", "<html>Introduce tu url para acortarla!!<br>" + formulario + "Urls acortadas y sin acortar:" + 						
						"<br>" + respuesta + '</html>')
			else:

				#new_url = '/' + str(len(dicc_acortadas)) + ',' + url + "\r\n"
				#print(new_url)	

				# Añado al dicc:
				dicc_acortadas['/' + str(len(dicc_acortadas))] = url
				dicc_completas[url] = '/' + str(len(dicc_acortadas))

 				# Añado al fichero:
				#with open('fich.txt', 'w') as myfile:
				#	writer = csv.writer(myfile)
				#	for key, value in dicc_acortadas.items():
				#		linea = key + ',' + value + '\r\n'
				#		writer.writerow(linea)
				#myfile.close()	


				respuesta = devuelve_urls(dicc_acortadas)	
				return("200 OK", "<html>Introduce tu url para acortarla!!<br>" + formulario + "Urls acortadas y sin acortar:" + 						
				"<br>" + respuesta + '</html>')
		
		try:
			print(dicc_acortadas)
			print(recurso)
			return("200 OK", dicc_acortadas[recurso])
		except KeyError:
			return("200 OK", "<html>Introduce tu url para acortarla!!<br>" + formulario + '</html>')

if __name__ == "__main__":
	testWebApp = contentApp("localhost", 4567)
