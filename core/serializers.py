from rest_framework import serializers
from .models import User, Food, Order, OrderItem
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'phone', 'role', 'password')

    def create(self, validated_data):
        user = User(
            phone=validated_data['phone'],
            role=validated_data.get('role', 'user')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    



class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'




class OrderItemSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)
    food_id = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all(), source='food', write_only=True)
    total_price = serializers.IntegerField(read_only=True)
    class Meta:
        model = OrderItem
        fields = ('id', 'food', 'food_id', 'count', 'total_price')




class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.IntegerField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'manzil', 'status', 'created_at', 'items', 'total_price')

    def create(self, validated_data):
        request = self.context['request']
        items_data = validated_data.pop('items')
        order = Order.objects.create(user=request.user, **validated_data)

        
        for item_data in items_data:
            
            OrderItem.objects.create(
                order=order,
                food=item_data['food'],
                count=item_data['count'],
            )
        return order