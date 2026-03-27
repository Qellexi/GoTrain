from django.db import models


class TrainType(models.Model):
    name = models.CharField(max_length=100)
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
    places_in_cargo = models.PositiveIntegerField()

    @property
    def total_places(self):
        return self.cargo_num * self.places_in_cargo

    def __str__(self):
        return f"Train {self.name} | {self.train_type}"
