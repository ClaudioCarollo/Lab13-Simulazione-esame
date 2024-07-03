import flet as ft
from geopy import distance


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def filldd(self):
        mappa = self._model.getAllYears()
        for k, v in mappa.items():
            self._view.ddyear.options.append(ft.dropdown.Option(str(str(k)+"-"+str(v))))
            self._view.update_page()


    def handle_analizza(self, e):
        self._view.txt_result.controls.clear()
        self._view.update_page()
        selected_node = self._view.ddstate.value
        if selected_node is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona un Nodo!", color='red'))
            self._view.update_page()
        else:
            node = self._model.idMap[selected_node.lower()]
            self._view.txt_result.controls.append(ft.Text(f"Stati precedenti al nodo {node.id}:"))
            self._view.update_page()
            predecessori = self._model.grafo.predecessors(node)
            for p in predecessori:
                self._view.txt_result.controls.append(ft.Text(f"{p.id}"))
                self._view.update_page()
            successori = self._model.grafo.successors(node)
            self._view.txt_result.controls.append(ft.Text(f"Stati successivi al nodo {node.id}:"))
            self._view.update_page()
            for s in successori:
                self._view.txt_result.controls.append(ft.Text(f"{s.id}"))
                self._view.update_page()
            componente_connessa = self._model.getComponenteConnessa(node)
            self._view.txt_result.controls.append(ft.Text(f"Nodi raggiungibili dal nodo {node.id}: {len(componente_connessa)}"))
            self._view.txt_result.controls.append(
                ft.Text(f"I nodi sono:"))
            self._view.update_page()
            for c in componente_connessa:

                self._view.txt_result.controls.append(
                    ft.Text(f"{c.id}"))
            self._view.update_page()


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        self._view.update_page()
        selected_year = self._view.ddyear.value[0:4]
        if selected_year is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona un Anno valido!", color='red'))
            self._view.update_page()
        try:
            selected_year = int(selected_year)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Seleziona un Anno intero!", color='red'))
            self._view.update_page()

        self._model.buildGraph(selected_year)
        if self._model.grafo:
            self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente con {len(self._model.grafo.nodes)} nodi e {len(self._model.grafo.edges)} archi", color='green'))
            self._view.update_page()
            stati = self._model.grafo.nodes
            for n in stati:
                self._view.ddstate.options.append(ft.dropdown.Option(str(n.id)))
            self._view.update_page()

    def handle_path(self, e):
        self._view.txtOut2.controls.clear()
        self._view.update_page()
        selected_node = self._view.ddstate.value
        if selected_node is None:
            self._view.txtOut2.controls.append(ft.Text("Seleziona un Nodo!", color='red'))
            self._view.update_page()
        else:
            node = self._model.idMap[selected_node.lower()]
            percorso = self._model.getPath(node)
            self._view.txtOut2.controls.append(ft.Text(f"Cammino più lungo di avvistamenti successivi, lunghezza {len(percorso)}"))
            self._view.update_page()
            for n in percorso:
                self._view.txtOut2.controls.append(
                    ft.Text(f"C{n.id}"))
                self._view.update_page()




