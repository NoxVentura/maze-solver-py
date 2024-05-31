import time
from cell import Cell


class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
    ):
        self._x1 = x1
        self._y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self._create_cells()
        self._break_entrance_and_exit()

    def _create_cells(self):
        self._cells = [[Cell(self._win) for element in range(self.num_rows)] for column in range(self.num_cols)]
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self.cell_size_x * i + self._x1
        y1 = self.cell_size_y * j + self._y1
        self._cells[i][j].draw(x1, y1, x1 + self.cell_size_x, y1 + self.cell_size_y)
        self._animate()

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)