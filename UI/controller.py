import copy

import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model



    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        shape = self._view.ddshape.value
        if not shape:
            self._view.txt_result1.controls.append(
                ft.Text("Selezionare una forma dal menu a tendina.", color="red")
            )
            self._view.update_page()
            return

        year = self._view.ddyear.value
        if not year:
            self._view.txt_result1.controls.append(
                ft.Text("Selezionare un anno dal menu a tendina.", color="red")
            )
            self._view.update_page()
            return
        self._model.buildGraph(shape, int(year))
        nodes, edges =  self._model.getGraphDetails()
        self._view.txt_result1.controls.append(
            ft.Text(f"Numero di vertici: {len(nodes)}\nNumero di archi: {len(edges)}", color="green")
        )
        lenCompConn, maxCompConn = self._model.getComponentsGraph()
        self._view.txt_result1.controls.append(
            ft.Text(f"Il grafo ha {lenCompConn} componenti connesse")
        )
        self._view.txt_result1.controls.append(
            ft.Text(f"La componente connessa più grande è costituita da {len(maxCompConn)} nodi: ")
        )
        for node in maxCompConn:
            self._view.txt_result1.controls.append(
                ft.Text(node)
            )
        self._view.update_page()


    def fillDdYears(self):
        years = self._model.getAllYears()
        for year in years:
            self._view.ddyear.options.append(
                ft.dropdown.Option(year)
            )

    def fillDdShapes(self):
        shapes = self._model.getAllShapes()
        for shape in shapes:
            self._view.ddshape.options.append(
                ft.dropdown.Option(shape)
            )

    def handle_path(self, e):
        pass
