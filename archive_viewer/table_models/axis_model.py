from pydm.widgets.axis_table_model import BasePlotAxesModel


class ArchiverAxisModel(BasePlotAxesModel):
    """The data model for the axes tab in the properties section. Acts
    as a go-between for the axes in a plot, and QTableView items.
    """
    def __init__(self, plot, parent=None):
        super().__init__(plot, parent)
        self.checkable_col = {self.getColumnIndex("Enable Auto Range"),
                              self.getColumnIndex("Log Mode")}

    def flags(self, index):
        flags = super().flags(index)
        if index.column() in self.checkable_col:
            flags = Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable
        return flags

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        elif role == Qt.CheckStateRole and index.column() in self.checkable_col:
            value = super().data(index, Qt.DisplayRole)
            return Qt.Checked if value else Qt.Unchecked
        elif index.column() not in self.checkable_col:
            return super().data(index, role)
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return QVariant()
        elif role == Qt.CheckStateRole and index.column() in self.checkable_col:
            return super().setData(index, value, Qt.EditRole)
        elif index.column() not in self.checkable_col:
            return super().setData(index, value, role)
        return None

    def append(self, name: str = "") -> None:
        """Add an empty row to the end of the table model.

        Parameters
        ----------
        name : str
            The name for the new axis item. If none is passed in, the
            axis is named "New Axis <row_count>".
        """
        if not name:
            axis_count = self.rowCount() + 1
            name = f"New Axis {axis_count}"
            while name in self._plot.plotItem.axes:
                axis_count += 1
                name = f"New Axis {axis_count}"

        super().append(name)
