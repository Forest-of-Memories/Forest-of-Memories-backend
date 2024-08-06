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

class GoogleLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GoogleUserSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user_id')
            email = serializer.validated_data.get('email')

            if User.objects.filter(user_id=user_id).exists():
                return Response({"error": "User with this user_id already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(email=email).exists():
                return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            return Response({"message": "User created successfully", "user": GoogleUserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommonQuestionViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        user_name = request.query_params.get('user_name')

        if not user_name:
            return Response({"error": "User name is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(user_name=user_name)
            family = user.family  # 사용자 패밀리 객체 가져오기
            family_cmn_qst_no = family.cmn_qst_no.cmn_qst_no  # 패밀리의 cmn_qst_no 가져오기
            liked_cmn_qst_nos = user.liked_cmn_qst_no.split(',') if user.liked_cmn_qst_no else []
            liked_questions = CommonQuestion.objects.filter(cmn_qst_no__in=liked_cmn_qst_nos)

            # Family의 cmn_qst_no 이하의 질문들만 가져오기
            questions = CommonQuestion.objects.filter(cmn_qst_no__lte=family_cmn_qst_no)
            questions_data = [{"index": q.cmn_qst_no, "content": q.cmn_qst_txt} for q in questions]
            liked_questions_data = [q.cmn_qst_no for q in liked_questions]

            return Response({
                'questions': questions_data,
                'likes': liked_questions_data
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PersonalQuestionViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        user_name = request.query_params.get('user_name')

        if not user_name:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(user_name=user_name)
            family = user.family  # 사용자 패밀리 객체 가져오기
            # family_prsn_qst_no = family.prsn_qst_no.prsn_qst_no  # 패밀리의 prsn_qst_no 가져오기
            liked_prsn_qst_nos = user.liked_psn_qst_no.split(',') if user.liked_psn_qst_no else []
            liked_questions = PersonalQuestion.objects.filter(prsn_qst_no__in=liked_prsn_qst_nos)

            questions = PersonalQuestion.objects.all()
            questions_data = [{"index": q.prsn_qst_no, "content": q.prsn_qst_txt} for q in questions]
            liked_questions_data = [q.prsn_qst_no for q in liked_questions]

            return Response({
                'questions': questions_data,
                'likes': liked_questions_data
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MemoryViewSet(viewsets.ModelViewSet):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer
        

class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    lookup_field = 'feed_id'
        
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
            user_name = request.data.get('user')
            if not user_name:
                return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.get(user_name=user_name)
            request.data['user'] = user.user_name  # Ensure the user ID is correctly set
            
            serializer = CommonCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

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
            # family = Family.objects.get(family_id=family_id)
            # prsn_qest_no = request.data.get('prsn_qst_no')
            # request.data['family'] = family_id
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

class FeedUpdateView(APIView):

    def get(self, request, family_id, format=None):
        try:
            family = Family.objects.get(family_id=family_id)
            serializer = FeedUpdateSerializer(family)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, family_id, format=None):
        try:
            family = Family.objects.get(family_id=family_id)
            serializer = FeedUpdateSerializer(family, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)
        

class WaterUpdateView(APIView):

    def get(self, request, family_id, format=None):
        try:
            family = Family.objects.get(family_id=family_id)  # URL에서 받은 family_id 사용
            serializer = WaterSerializer(family)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)
    
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

class CommonAnswerList(APIView):

    def get(self, request, family_id, format=None):
        try:
            family = Family.objects.get(family_id=family_id)
            comments = CommonAnswer.objects.filter(family=family)
            serializer = CommonAnswerSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)
        except CommonAnswer.DoesNotExist:
            return Response({"error": "Answer not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, family_id, format=None):
        try:
            user_name = request.data.get('user')
            if not user_name:
                return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.get(user_name=user_name)
            request.data['user'] = user.user_name  # Ensure the user ID is correctly set
            
            serializer = CommonAnswerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class PersonalAnswerList(APIView):
    def get(self, request, family_id, format=None):
        try:
            family = Family.objects.get(family_id=family_id)
            comments = PersonalAnswer.objects.filter(prsn_qst__family=family)
            serializer = PersonalAnswerSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, family_id, format=None):
        try:
            # family = Family.objects.get(family_id=family_id)
            # request.data['prsn_qst'] = family.cmn_qst_no.cmn_qst_no
            # request.data['family'] = family_id
            serializer = PersonalAnswerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)