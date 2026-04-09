from django.db import models


class TrainType(models.Model):
    name = models.CharField(max_length=100)
    average_speed = models.PositiveIntegerField(default=120)

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(
        max_length=100,
    )
    train_type = models.ForeignKey(
        TrainType,
        on_delete=models.CASCADE,
    )
    cargo_num = models.PositiveIntegerField()

    first_class_places = models.PositiveIntegerField(default=0)
    second_class_places = models.PositiveIntegerField(default=0)
    economy_places = models.PositiveIntegerField(default=0)

    @property
    def places_in_cargo(self):
        return self.first_class_places + self.second_class_places + self.economy_places

    @property
    def total_places(self):
        return self.cargo_num * self.places_in_cargo

    def __str__(self):
        return f"Train {self.name} | {self.train_type}"
