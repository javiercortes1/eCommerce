from .models import Product, Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    # category_name = serializers.CharField(read_only=True, source="category.name")
    # category = CategorySerializer(read_only=True)
    # category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source="category")
    # name = serializers.CharField(required=True, min_length=3)

    def validate_name(self, value):
        exists = Product.objects.filter(name__iexact=value).exists()

        if exists:
            raise serializers.ValidationError("Este producto ya existe")
        return value

    class Meta:
        model = Product
        fields = '__all__'