from rest_framework import serializers
from .models import MineSweeper


class MineSweeperSerializer(serializers.ModelSerializer):
    class Meta:
        model = MineSweeper
        fields = ["game_id", "width", "height", "mines_count", "completed", "field"]

    def validate_width(self, value):
        if value > 30:
            raise serializers.ValidationError(
                "Ширина должна быть" " меньше или равна 30."
            )
        return value

    def validate_height(self, value):
        if value > 30:
            raise serializers.ValidationError(
                "Длина должна " "быть меньше или равна 30."
            )
        return value

    def validate_mines_count(self, value):
        width = self.initial_data.get("width")
        height = self.initial_data.get("height")
        if value > width * height - 1:
            raise serializers.ValidationError(
                "Количество мин должно быть " "меньше или равно " "ширина * высота - 1."
            )
        return value
