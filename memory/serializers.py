from rest_framework import serializers
from .models import CommonQuestion, PersonalQuestion, Family, Feed

# 공통 질문
class CommonQuestionSerializer(serializers.ModelSerializer):
    class Meta:
      model = CommonQuestion
      fields = '__all__'

class PersonalQuestionSerializer(serializers.ModelSerializer):
    class Meta:
      model = PersonalQuestion
      fields = ['prsn_qst_no', 'prsn_qst_txt']

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
      model = Family
      fields = '[family_id, tree_exp, tree_start_date, tree_skin]'

class FeedSerializer(serializers.ModelSerializer):
    class Meta: 
       model = Feed
       fields = ['feed_img']

# # 피드 대표사진 3개 변경
# class FeedUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Feed
#         fields = ['feed_img']