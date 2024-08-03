# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
######### LSH ##################
from .models import CommonQuestion, User, PersonalQuestion, Family, Memory, Feed, ShopItem
from .serializers import CommonQuestionSerializer, PersonalQuestionSerializer, MemorySerializer, FeedSerializer, ShopItemSerializer
######### KHS ##################
from .models import CommonComment, PersonalComment

from .serializers import CommonCommentSerializer, PersonalCommentSerializer


from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CommonQuestion, PersonalQuestion, User, Family
from .serializers import CommonQuestionSerializer, PersonalQuestionSerializer

class CommonQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommonQuestion.objects.all()
    serializer_class = CommonQuestionSerializer

    def list(self, request):
        family_id = request.query_params.get('family_id')
        liked_questions = []

        if not family_id:
            return Response({"error": "Family ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            family = Family.objects.get(family_id=family_id)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)
        
        users = User.objects.filter(family=family)
        if users.exists():
            liked_questions = [
                int(q) for user in users
                if user.liked_cmn_qst_no for q in user.liked_cmn_qst_no.split(',')
            ]

        cmn_qst_no = family.cmn_qst_no.cmn_qst_no
        questions = CommonQuestion.objects.filter(cmn_qst_no__lte=cmn_qst_no)
        serializer = CommonQuestionSerializer(questions, many=True)

        response_data = {
            "questions": [{"index": q['cmn_qst_no'], "content": q['cmn_qst_txt']} for q in serializer.data],
            "likes": liked_questions
        }
        return Response(response_data)


class PersonalQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PersonalQuestionSerializer

    def list(self, request):
        family_id = request.query_params.get('family_id')
        liked_questions = []

        if not family_id:
            return Response({"error": "Family ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            family = Family.objects.get(family_id=family_id)
            users = User.objects.filter(family=family)
            liked_questions = [
                int(q) for user in users
                if user.liked_psn_qst_no for q in user.liked_psn_qst_no.split(',')
            ]
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)

        questions = PersonalQuestion.objects.filter(family=family)
        serializer = PersonalQuestionSerializer(questions, many=True)

        response_data = {
            "questions": [{"index": q['prsn_qst_no'], "content": q['prsn_qst_txt']} for q in serializer.data],
            "likes": liked_questions
        }
        return Response(response_data)
    

class MemoryViewSet(viewsets.ModelViewSet):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer
        

class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
        
class CommonCommentViewSet(ModelViewSet):
    queryset = CommonComment.objects.all()
    serializer_class = CommonCommentSerializer

class PersonalCommentViewSet(ModelViewSet):
    queryset = PersonalComment.objects.all()
    serializer_class = PersonalCommentSerializer

class ShopItemViewSet(viewsets.ModelViewSet):
    queryset = ShopItem.objects.all()
    serializer_class = ShopItemSerializer

class PurchaseItemViewSet(viewsets.ViewSet):
    def create(self, request):
        family_id = request.data.get('family_id')
        item_id = request.data.get('item_id')

        if not family_id or not item_id:
            return Response({"error": "Family ID and Item ID are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            family = Family.objects.get(family_id=family_id)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            item = ShopItem.objects.get(item_id=item_id)
        except ShopItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        if family.item_list:
            family.item_list = f"{family.item_list},{item_id}"
        else:
            family.item_list = str(item_id)
        
        family.save()

        return Response({"id": family_id, "item_id": item_id}, status=status.HTTP_201_CREATED)