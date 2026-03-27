from rest_framework import serializers

from railway.models.news import News


class NewsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = (
            "title",
            "short_description",
            "created_at"
        )


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = (
            "title",
            "full_description",
            "created_at"
        )


class NewsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "title",
            "short_description",
            "full_description",
            "created_at"
        )

    def to_internal_value(self, data):
        data = data.copy()

        short_description = data.get('short_description')
        full_description = data.get('full_description')

        if full_description and not short_description:
            if len(full_description) > 200:
                data["short_description"] = full_description[:197] + "..."
            else:
                data["short_description"] = full_description

        return super().to_internal_value(data)
