from rest_framework.views import APIView, Request, Response
from rest_framework import status

from .models import MineSweeper
from .serializers import MineSweeperSerializer
from .minesweeper import MineSweepers


class MineSweeperNewAPIView(APIView):
    def post(self, request: Request) -> Response:
        MineSweeper.objects.filter(completed=True).delete()
        serializer = MineSweeperSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            mine_sweeper = serializer.save()
            obj_minesweeper = MineSweepers(width=mine_sweeper.width,
                                           height=mine_sweeper.height,
                                           mines_count=mine_sweeper.mines_count,
                                           )
            mine_sweeper.field = obj_minesweeper.field
            mine_sweeper.open_field = obj_minesweeper.lay_mines()
            mine_sweeper.save()

        return Response(serializer.data)


class MineSweeperTurnAPIView(APIView):
    def post(self, request: Request) -> Response:
        game_id = request.data.get("game_id")
        col = request.data.get("col")
        row = request.data.get("row")
        mine_sweeper = MineSweeper.objects.get(game_id=game_id)
        field = mine_sweeper.field
        open_field = mine_sweeper.open_field
        obj_minesweeper = MineSweepers(mine_sweeper.width,
                                       mine_sweeper.height,
                                       mine_sweeper.mines_count, field=field)

        if mine_sweeper.completed:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"error": "Произошла непредвиденная ошибка"})
        if mine_sweeper.field[row][col] != " ":
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"error": "Уже открытая ячейка"})

        if open_field[row][col] == 0:
            mine_sweeper.field = obj_minesweeper.count_zero(row, col, open_field)
        elif open_field[row][col] == "X":
            mine_sweeper.field = open_field
            mine_sweeper.completed = True
            mine_sweeper.save()
            serializer = MineSweeperSerializer(mine_sweeper)
            return Response(data=serializer.data)
        elif isinstance(open_field[row][col], int):
            mine_sweeper.field[row][col] = open_field[row][col]

        win = True
        for cells in range(len(mine_sweeper.field)):
            for cell in range(len(mine_sweeper.field[cells])):
                if (mine_sweeper.field[cells][cell] == " "
                        and mine_sweeper.open_field[cells][cell] != "X"):
                    win = False
                    break

        if win:
            mine_sweeper.field = open_field
            for cells in mine_sweeper.field:
                for cell in cells:
                    if cell == "X":
                        cells[cells.index(cell)] = "M"
            mine_sweeper.completed = True

        mine_sweeper.save()
        serializer = MineSweeperSerializer(mine_sweeper)
        return Response(serializer.data)
