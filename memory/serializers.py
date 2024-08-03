from rest_framework import serializers
######### LSH ##################
from .models import CommonQuestion, PersonalQuestion, Family, Feed, Memory
######### KHS ##################
from .models import CommonComment, PersonalComment

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

# # 피드 대표사진 3개 변경
# class FeedUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Feed
#         fields = ['feed_img']

class CommonCommentSerializer(serializers.ModelSerializer):
   class Meta:
      model = CommonComment
      fields = '__all__'

class PersonalCommentSerializer(serializers.ModelSerializer):
   class Meta:
      model = PersonalComment
      fields = '__all__'

class MemorySerializer(serializers.ModelSerializer):
    class Meta:
      model = Memory
      fields = '__all__'
  
