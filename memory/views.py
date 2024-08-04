# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
######### ALL ##################
from .models import *
from .serializers import *


from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CommonQuestion, PersonalQuestion, User, Family
from .serializers import CommonQuestionSerializer, PersonalQuestionSerializer

class CommonQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommonQuestion.objects.all().order_by('cmn_qst_no')
    serializer_class = CommonQuestionSerializer

    # def list(self, request):
    #     family_id = request.query_params.get('family_id')
    #     liked_questions = []

    #     if not family_id:
    #         return Response({"error": "Family ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    #     try:
    #         family = Family.objects.get(family_id=family_id)
    #     except Family.DoesNotExist:
    #         return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)
        
    #     users = User.objects.filter(family=family)
    #     if users.exists():
    #         liked_questions = [
    #             int(q) for user in users
    #             if user.liked_cmn_qst_no for q in user.liked_cmn_qst_no.split(',')
    #         ]

    #     cmn_qst_no = family.cmn_qst_no.cmn_qst_no
    #     questions = CommonQuestion.objects.filter(cmn_qst_no__lte=cmn_qst_no)
    #     serializer = CommonQuestionSerializer(questions, many=True)

    #     response_data = {
    #         "questions": [{"index": q['cmn_qst_no'], "content": q['cmn_qst_txt']} for q in serializer.data],
    #         "likes": liked_questions
    #     }
    #     return Response(response_data)


class PersonalQuestionViewSet(viewsets.ViewSet):
    serializer_class = PersonalQuestionSerializer

    def get_queryset(self):
        family_id = self.kwargs.get('family_id')
        if family_id:
            return PersonalQuestion.objects.filter(family_id=family_id)
        return PersonalQuestion.objects.all()

    def list(self, request, *args, **kwargs):
        family_id = kwargs.get('family_id')
        if family_id:
            try:
                family = Family.objects.get(family_id=family_id)
                questions = PersonalQuestion.objects.filter(family=family)
                serializer = PersonalQuestionSerializer(questions, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Family.DoesNotExist:
                return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = self.get_queryset()
            serializer = PersonalQuestionSerializer(queryset, many=True)
            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

class MemoryViewSet(viewsets.ModelViewSet):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer
        

class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
        
class CommonCommentList(APIView):

    def get(self, request, family_id, format=None):
        try:
            family = Family.objects.get(family_id=family_id)
            comments = CommonComment.objects.filter(family=family)
            serializer = CommonCommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)
        except CommonComment.DoesNotExist:
            return Response({"error": "Comments not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, family_id, format=None):
        try:
            family = Family.objects.get(family_id=family_id)
            request.data['cmn_qst'] = family.cmn_qst_no.cmn_qst_no
            request.data['family'] = family_id
            serializer = CommonCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)

class PersonalCommentList(APIView):

    def get(self, request, family_id, format=None):
        try:
            family = Family.objects.get(family_id=family_id)
            comments = PersonalComment.objects.filter(prsn_qst__family=family)
            serializer = PersonalCommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, family_id, format=None):
        try:
            family = Family.objects.get(family_id=family_id)
            request.data['prsn_qst'] = family.cmn_qst_no.cmn_qst_no
            request.data['family'] = family_id
            serializer = PersonalCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)

class FamilyListView(ListAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer

class FamilyDetailView(APIView):

    def get(self, request, family_id, format=None):
        try:
            family = Family.objects.get(family_id=family_id)  # URL에서 받은 family_id 사용
            serializer = FamilySerializer(family)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)

class WaterUpdateView(APIView):

    def post(self, request, family_id, format=None):
        try:
            family = Family.objects.get(family_id=family_id)  # URL에서 받은 family_id 사용
            serializer = WaterSerializer(family, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)
        
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
