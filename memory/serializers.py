from rest_framework import serializers
######### ALL ##################
from .models import *

# 공통 질문
class CommonQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonQuestion
        fields = ['cmn_qst_no', 'cmn_qst_txt']

class PersonalQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalQuestion
        fields = ['prsn_qst_no', 'prsn_qst_txt']

class FeedSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Feed
        fields = '__all__'

# # 피드 대표사진 3개 변경
# class FeedUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Feed
#         fields = ['feed_img']
class FeedUpdateSerializer(serializers.ModelSerializer):
    first_feed = serializers.PrimaryKeyRelatedField(queryset=Feed.objects.all(), required=False)
    second_feed = serializers.PrimaryKeyRelatedField(queryset=Feed.objects.all(), required=False)
    third_feed = serializers.PrimaryKeyRelatedField(queryset=Feed.objects.all(), required=False)

    class Meta:
        model = Family
        fields = ['first_feed', 'second_feed', 'third_feed']

    def validate_first_feed(self, value):
        if value and not Feed.objects.filter(feed_id=value.feed_id).exists():
            raise serializers.ValidationError("Invalid first_feed")
        return value

    def validate_second_feed(self, value):
        if value and not Feed.objects.filter(feed_id=value.feed_id).exists():
            raise serializers.ValidationError("Invalid second_feed")
        return value

    def validate_third_feed(self, value):
        if value and not Feed.objects.filter(feed_id=value.feed_id).exists():
            raise serializers.ValidationError("Invalid third_feed")
        return value
    
  ##############################

class CommonCommentSerializer(serializers.ModelSerializer):
   user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
   class Meta:
      model = CommonComment
      fields = '__all__'

class PersonalCommentSerializer(serializers.ModelSerializer):
   user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
   class Meta:
      model = PersonalComment
      fields = '__all__'

class MemorySerializer(serializers.ModelSerializer):
    class Meta:
      model = Memory
      fields = '__all__'
  
class FamilySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='family_id')
    exp = serializers.IntegerField(source='tree_exp')
    date = serializers.DateField(source='tree_start_date')
    feed_id_1 = serializers.IntegerField(source='first_feed_id')
    feed_id_2 = serializers.IntegerField(source='second_feed_id')
    feed_id_3 = serializers.IntegerField(source='third_feed_id')
    skin = serializers.CharField(source='tree_skin')
    water = serializers.IntegerField(source='wrt_strg')

    class Meta:
        model = Family
        fields = ['id', 'exp', 'date', 'feed_id_1', 'feed_id_2', 'feed_id_3', 'skin', 'water']

class WaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ['wrt_strg']

    def validate_wrt_strg(self, value):
        if value < 0 or value > 3:
            raise serializers.ValidationError("Water must be between 0 and 3")
        return value

class ShopItemSerializer(serializers.ModelSerializer):
      class Meta:
            model = ShopItem
            fields = '__all__'

class PurchaseItemSerializer(serializers.ModelSerializer):
    family_id=serializers.IntegerField()
    item_id=serializers.IntegerField()