from rest_framework import serializers

from railway.models.train import TrainType, Train


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name")


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "train_type",
            "cargo_num",
            "places_in_cargo",
        )


class TrainRetrieveSerializer(TrainSerializer):
    train_type = TrainTypeSerializer(read_only=True)

    total_places = serializers.IntegerField(read_only=True)

    class Meta(TrainSerializer.Meta):
        fields = TrainSerializer.Meta.fields + ("total_places",)
