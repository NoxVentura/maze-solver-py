import random
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
            seed=None,
    ):
        self._x1 = x1
        self._y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        if seed is not None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

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

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []

            if i + 1 < len(self._cells) and not self._cells[i + 1][j].visited:
                to_visit.append((i + 1, j, "right"))
            if j + 1 < len(self._cells[i]) and not self._cells[i][j + 1].visited:
                to_visit.append((i, j + 1, "bottom"))
            if j - 1 >= 0 and not self._cells[i][j - 1].visited:
                to_visit.append((i, j - 1, "top"))
            if i - 1 >= 0 and not self._cells[i - 1][j].visited:
                to_visit.append((i - 1, j, "left"))

            if not to_visit:
                self._draw_cell(i, j)
                return

            direction = random.randint(0, len(to_visit) - 1)
            selected_cell_index = to_visit[direction]
            selected_cell = self._cells[selected_cell_index[0]][selected_cell_index[1]]
            current_cell = self._cells[i][j]
            selected_direction = selected_cell_index[2]

            if selected_direction == "right":
                current_cell.has_right_wall = False
                selected_cell.has_left_wall = False
            elif selected_direction == "bottom":
                current_cell.has_bottom_wall = False
                selected_cell.has_top_wall = False
            elif selected_direction == "top":
                current_cell.has_top_wall = False
                selected_cell.has_bottom_wall = False
            elif selected_direction == "left":
                current_cell.has_left_wall = False
                selected_cell.has_right_wall = False
            self._break_walls_r(selected_cell_index[0], selected_cell_index[1])

    def _reset_cells_visited(self):
        for column in self._cells:
            for element in column:
                element.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True

        if i == self.num_cols-1 and j == self.num_rows-1:
            return True

        has_left_wall = current_cell.has_left_wall
        has_right_wall = current_cell.has_right_wall
        has_top_wall = current_cell.has_top_wall
        has_bottom_wall = current_cell.has_bottom_wall

        if not has_right_wall and i + 1 < len(self._cells) and not self._cells[i + 1][j].visited:
            selected_cell = self._cells[i + 1][j]
            current_cell.draw_move(selected_cell)
            if self._solve_r(i + 1, j):
                return True
            else:
                current_cell.draw_move(selected_cell, undo=True)
        if not has_bottom_wall and j + 1 < len(self._cells[i]) and not self._cells[i][j + 1].visited:
            selected_cell = self._cells[i][j + 1]
            current_cell.draw_move(selected_cell)
            if self._solve_r(i, j + 1):
                return True
            else:
                current_cell.draw_move(selected_cell, undo=True)
        if not has_top_wall and j - 1 >= 0 and not self._cells[i][j - 1].visited:
            selected_cell = self._cells[i][j - 1]
            current_cell.draw_move(selected_cell)
            if self._solve_r(i, j - 1):
                return True
            else:
                current_cell.draw_move(selected_cell, undo=True)
        if not has_left_wall and i - 1 >= 0 and not self._cells[i - 1][j].visited:
            selected_cell = self._cells[i - 1][j]
            current_cell.draw_move(selected_cell)
            if self._solve_r(i - 1, j):
                return True
            else:
                current_cell.draw_move(selected_cell, undo=True)
        return False
