from TwoThree import TwoThree
from jikanpy import Jikan
from AVL import AVL
from ABB import ABB
import qprompt


jikan = Jikan()
# action = jikan.genre(type='anime', genre_id=43)
#Numero maximo de genero: 43

genre = qprompt.ask_int("Ingrese el ID del genero que desea ver")
if genre in range(1, 44):

	data = jikan.genre(type='anime', genre_id=genre)

	while True:
		qprompt.echo("Genero seleccionado: {}\n".format(data["mal_url"]["name"]))
		menu = qprompt.Menu()
		menu.add("A", "ABB")
		menu.add("B", "AVL")
		menu.add("C", "2-3")
		menu.add("D", "Salir")
		qprompt.echo("Elija en que estructura desea guardar la información")
		choice = menu.show()
		if choice == "A":
			info = ABB(data["mal_url"]["name"], data["anime"])
		elif choice == "B":
			info = AVL(data["mal_url"]["name"], data["anime"])
		elif choice == "C":
			info = TwoThree(data["mal_url"]["name"], data["anime"])
		elif choice == "D":
			break
		else:
			qprompt.echo("\nIngrese una opción valida porfavor")

		#Consultas
		consultar = True
		while consultar:
			conslt = qprompt.Menu()
			conslt.add("A", "Insertar")
			conslt.add("B", "Buscar anime por puntuación")
			conslt.add("C", "Eliminar")
			conslt.add("D", "Imprimir Arbol")
			conslt.add("E", "Mejor Anime")
			conslt.add("F", "Peor Anime")
			conslt.add("G", "Volver")
			qprompt.echo("\nElija una de las consultas disponibles")
			choice = conslt.show()

			#Insert
			if choice == "A":
				title = ""
				while title.strip() == "":
					title = qprompt.ask_str("Ingrese el titulo del anime que desea agregar")
				score = qprompt.ask_float("Ingrese el score del anime que desea agregar")
				info.insert(info.root, title, score)
				qprompt.echo("\nSe ha agregado el anime {} de forma exitosa\n".format(title))

			#Serch
			elif choice == "B":
				score = qprompt.ask_float("Ingrese el score del anime que desea buscar")
				node = info.find(info.root, score)
				if not node:
					qprompt.echo("No se ha encontrado ningun anime con ese puntaje\n")
				else:
					for anime in node.titles:
						qprompt.echo("Title: {}, Score: {}".format(anime, node.score))

			#Delete
			elif choice == "C":
				score = qprompt.ask_float("Ingrese el score del anime que desea eliminar")
				node = info.find(info.root, score)
				if not node:
					qprompt.echo("No se ha encontrado ningun anime con ese puntaje\n")
				else:
					to_delete = qprompt.Menu()
					i = 1
					for anime in node.titles:
						to_delete.add(str(i), anime)
						i += 1
					qprompt.echo("\nElige uno de los siguientes animes para eliminar")
					choice = to_delete.show()
					info.delete_title(node, int(choice)-1)

			#Summary
			elif choice == "D":
				info.print_tree(info.root)

			#Best
			elif choice == "E":
				node = info.max(info.root)
				if len(node.titles) != 1:
					qprompt.echo("Los animes mejor punteados son:")
					for title in node.titles:
						qprompt.echo("Title: {}, Score: {}".format(title, node.score))
				else:
					qprompt.echo("El anime mejor punteado es:")
					qprompt.echo("Title: {}, Score: {}".format(node.titles[0], node.score))

			#Worst
			elif choice == "F":
				node = info.min(info.root)
				if len(node.titles) != 1:
					qprompt.echo("Los animes peor punteados son:")
					for title in node.titles:
						qprompt.echo("Title: {}, Score: {}".format(title, node.score))
				else:
					qprompt.echo("El anime peor punteado es:")
					qprompt.echo("Title: {}, Score: {}".format(node.titles[0], node.score))

			#Volver
			elif choice == "G":
				consultar = False

			#Input invalido
			else:
				qprompt.echo("Ingrese una opción valida porfavor\n")

else:
	qprompt.echo("Ingrese una opción valida porfavor, los ID van del 1 al 43")


