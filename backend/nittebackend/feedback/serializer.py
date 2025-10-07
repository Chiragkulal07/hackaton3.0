# quiz/serializers.py
from rest_framework import serializers

class FeedbackSerializer(serializers.Serializer):
    score = serializers.IntegerField()
    feedback_message = serializers.CharField()
