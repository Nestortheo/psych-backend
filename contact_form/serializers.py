from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    message = serializers.CharField(min_length=10)
    phone = serializers.CharField(required=False, allow_blank=True, max_length=30)
    website = serializers.CharField(required=False, allow_blank=True)  # honeypot