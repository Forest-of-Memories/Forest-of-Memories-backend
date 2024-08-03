from rest_framework import serializers
from .models import CommonQuestion, PersonalQuestion, Family, Memory, Feed

# 공통 질문
class CommonQuestionSerializer(serializers.ModelSerializer):
    class Meta:
      model = CommonQuestion
      fields = '__all__'

class PersonalQuestionSerializer(serializers.ModelSerializer):
    class Meta:
      model = PersonalQuestion
      fields = ['prsn_qst_no', 'prsn_qst_txt']

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
      model = Feed
      fields = '__all__'

class MemorySerializer(serializers.ModelSerializer):
    class Meta:
      model = Memory
      fields = '__all__'
  