import flet as ft
from model.model import Model

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def handle_anno(self, e):
        anno = self._view.txtInYear.value
        if anno is None:
            self._view.txt_result.controls.append(ft.Text("Inserisci un anno!", color='red'))
            self._view.update_page()
        else:
            try:
                anno = int(anno)
            except ValueError:
                self._view.txt_result.controls.append(ft.Text("Inserisci un anno intero!", color='red'))
                self._view.update_page()
            if anno <= 2014 and anno >= 1910:
                shapes = self._model.getShapes(anno)
                for s in shapes:
                    if s != "":
                        self._view.ddshape.options.append(ft.dropdown.Option(str(s)))
                self._view.update_page()
            else:
                self._view.txt_result.controls.append(ft.Text("Inserisci un anno compreso tra 1910 e 2014!", color='red'))
                self._view.update_page()


    def handle_graph(self, e):
        anno = self._view.txtInYear.value
        shape = self._view.ddshape.value
        if shape is None:
            self._view.txt_result.controls.append(ft.Text("Inserisci una forma", color='red'))
            self._view.update_page()
        else:
            self._model.buildGraph(shape, anno)
            if self._model.grafo:
                self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente con {len(self._model.grafo.nodes)} nodi e {len(self._model.grafo.edges)} archi", color='green'))
                self._view.update_page()
            for n1 in self._model.grafo.nodes:
                peso = 0
                for n2 in self._model.grafo.neighbors(n1):
                    peso+=self._model.grafo[n1][n2]["weight"]
                self._view.txt_result.controls.append(ft.Text(f"Nodo {n1.id}, peso archi incidenti: {peso}"))
                self._view.update_page()