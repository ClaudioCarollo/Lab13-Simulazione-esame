import flet as ft
from geopy import distance


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = self._model.getAllYears()

    def fillDD(self):
        for a in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(str(a)))
        self._view.update_page()


    def fillddShape(self, e):
        selected_year = self._view.ddyear.value
        try:
            selected_year = int(selected_year)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Inserisci un Anno valido!", color='red'))
            self._view.update_page()
        forme = self._model.getAllShapes(selected_year)
        for f in forme:
            if f != "":
                self._view.ddshape.options.append(ft.dropdown.Option(str(f)))
        self._view.update_page()


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        selected_shape = self._view.ddshape.value
        selected_year = self._view.ddyear.value
        if selected_shape is None:
            self._view.txt_result.controls.append(ft.Text("Inserisci una forma dal menù", color='red'))
            self._view.update_page()
        if selected_year is None:
            self._view.txt_result.controls.append(ft.Text("Inserisci un anno dal menù", color='red'))
            self._view.update_page()
        else:
            self._model.buildGraph(selected_shape, selected_year)
            if self._model.grafo:
                self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente", color='green'))
                self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {len(self._model.grafo.nodes)} nodi e {len(self._model.grafo.edges)} archi"))
                self._view.update_page()
            else:
                self._view.txt_result.controls.append(
                    ft.Text("Grafo non creato", color = "red"))
                self._view.update_page()
            for n in self._model.grafo.nodes:
                peso = 0
                vicini = self._model.grafo.neighbors(n)
                for v in vicini:
                    peso += self._model.grafo[n][v]["weight"]
                self._view.txt_result.controls.append(
                    ft.Text(f"Nodo {n.id}, somma pesi su archi = {peso}"))
                self._view.update_page()



    def handle_path(self, e):
        cammino = self._model.getPath()
        self._view.txtOut2.controls.append(
            ft.Text(f"Peso cammino massimo :{cammino[1]}"))
        self._view.update_page()
        for i in range(0, len(cammino[0])-1):
            self._view.txtOut2 .controls.append(
                ft.Text(f"{cammino[0][i].id}-->{cammino[0][i+1].id}, peso: {self._model.grafo[cammino[0][i]][cammino[0][i+1]]["weight"]}, distance: {distance.distance((cammino[0][i].Lat, cammino[0][i].Lng), (cammino[0][i+1].Lat, cammino[0][i+1].Lng))}"))
            self._view.update_page()