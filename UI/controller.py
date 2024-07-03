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



    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        selected_year = self._view.txtInYear.value
        selected_day = self._view.txtxG.value
        try:
            selected_year = int(selected_year)
            selected_day = int(selected_day)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Inserisci un anno e un numero di giorni interi", color='red'))
            self._view.update_page()
        if selected_day<1 or selected_day>180:
            self._view.txt_result.controls.append(
                ft.Text("Inserisci un numero di giorni compreso tra 1 e 180", color='red'))
            self._view.update_page()
        if selected_year<1906 or selected_year>2014:
            self._view.txt_result.controls.append(
                ft.Text("Inserisci un anno tra il 1906 e il 2014", color='red'))
            self._view.update_page()
        else:
            self._model.buildGraph(selected_year, selected_day)
            if self._model.grafo:
                self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente con {len(self._model.grafo.nodes)} nodi e {len(self._model.grafo.edges)} archi", color='green'))
                self._view.update_page()
                pesi = self._model.getPesiAdiacenti()
                for k,v in pesi.items():
                    self._view.txt_result.controls.append(ft.Text(f"{k}-> somma pesi archi adiacenti: {v}"))
                self._view.update_page()