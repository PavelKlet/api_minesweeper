import random


class MineSweepers(object):

    def __init__(self, width, height, mines_count, field=None):
        self.width = width
        self.height = height
        self.mines_count = mines_count
        self.field = [[" " for _ in range(self.width)]
                      for _ in range(self.height)] if not field else field

    def lay_mines(self):
        flat_field = [cell for row in self.field for cell in row]
        mines_indices = random.sample(range(len(flat_field)), self.mines_count)

        for i in mines_indices:
            flat_field[i] = "X"

        updated_field = [flat_field[i:i+self.width]
                         for i in range(0, len(flat_field), self.width)]

        for row in range(len(updated_field)):
            for col in range(len(updated_field[row])):
                if updated_field[row][col] != "X":
                    updated_field[row][col] = self.count_mines(row, col,
                                                               updated_field)

        return updated_field

    def count_mines(self, x, y, current_field):
        count = 0
        neighbors = ((x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1),
                     (x - 1, y - 1), (x - 1, y + 1),
                     (x + 1, y + 1), (x + 1, y - 1))

        for nx, ny in neighbors:
            if 0 <= nx < self.height and 0 <= ny < self.width:
                if current_field[nx][ny] == "X":
                    count += 1
        return count

    def count_zero(self, x, y, current_field):
        stack = [(x, y)]
        visited = set()

        while stack:
            found_zero = False
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))

            if current_field[x][y] == 0:
                self.field[x][y] = 0
                found_zero = True

            for nx, ny in ((x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1),
                           (x - 1, y - 1), (x - 1, y + 1),
                           (x + 1, y + 1), (x + 1, y - 1)):
                if 0 <= nx < self.height and 0 <= ny < self.width:
                    if current_field[nx][ny] == 0 and (nx, ny) not in visited:
                        stack.append((nx, ny))
                    if isinstance(current_field[nx][ny], int):
                        self.field[nx][ny] = current_field[nx][ny]
            if not found_zero:
                break
        return self.field
