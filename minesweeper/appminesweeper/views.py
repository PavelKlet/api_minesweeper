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
                            data={"error": "Игра завершена"})
        if mine_sweeper.field[row][col] != " ":
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"error": "Уже открытая ячейка"})

        handlers = {
           "X": [obj_minesweeper.handle_mine, (mine_sweeper, open_field)],
           0: [obj_minesweeper.handle_zero, (row, col, open_field)],
           int: [obj_minesweeper.handle_number, (field, open_field, row, col)]
        }

        if open_field[row][col] in handlers:
            handler, params = handlers.get(open_field[row][col])
        elif isinstance(open_field[row][col], int):
            handler, params = handlers.get(int)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Произошла непредвиденная ошибка"}
            )

        mine_sweeper.field = handler(*params)

        if not mine_sweeper.completed:
            check_result = obj_minesweeper.check_win(
                mine_sweeper,
                mine_sweeper.field,
                open_field
            )
            if check_result:
                mine_sweeper.field = check_result

        mine_sweeper.save()
        serializer = MineSweeperSerializer(mine_sweeper)
        return Response(serializer.data)

