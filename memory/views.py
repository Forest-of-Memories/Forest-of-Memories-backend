# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
######### ALL ##################
from .models import *
from .serializers import *

class CommonQuestionViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            liked_cmn_qst_nos = user.liked_cmn_qst_no.split(',')
            liked_questions = CommonQuestion.objects.filter(cmn_qst_no__in=liked_cmn_qst_nos)

            queryset = CommonQuestion.objects.all()
            serializer = CommonQuestionSerializer(queryset, many=True)
            liked_questions_serializer = CommonQuestionSerializer(liked_questions, many=True)
            
            return Response({
                'common_questions': serializer.data,
                'liked_cmn_qst_no': liked_questions_serializer.data
            }, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PersonalQuestionViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            liked_prsn_qst_nos = user.liked_psn_qst_no.split(',')
            liked_questions = PersonalQuestion.objects.filter(prsn_qst_no__in=liked_prsn_qst_nos)

            queryset = PersonalQuestion.objects.all()
            serializer = PersonalQuestionSerializer(queryset, many=True)
            liked_questions_serializer = PersonalQuestionSerializer(liked_questions, many=True)
            
            return Response({
                'personal_questions': serializer.data,
                'liked_prsn_qst_no': liked_questions_serializer.data
            }, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class MemoryViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            family = Family.objects.get(id=user.family_id)
            memories = Memory.objects.filter(family=family)
            
            queryset = Memory.objects.all()
            serializer = MemorySerializer(queryset, many=True)
            
            return Response({
                'memories': serializer.data
            }, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
        
class CommonCommentList(APIView):

    def get(self, request, format=None):
        comments = CommonComment.objects.all()
        serializer = CommonCommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommonCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonalCommentViewSet(ModelViewSet):
    queryset = PersonalComment.objects.all()
    serializer_class = PersonalCommentSerializer

class FamilyDetailView(APIView):

    def get(self, request, format=None):
        try:
            family = Family.objects.get(family_id=1)  # 가정 예시로 id=1을 사용
            serializer = FamilySerializer(family)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)

class WaterUpdateView(APIView):

    def post(self, request, format=None):
        try:
            family = Family.objects.get(family_id=1)  # 가정 예시로 family_id=1을 사용
            serializer = WaterSerializer(family, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Family.DoesNotExist:
            return Response({"error": "Family not found"}, status=status.HTTP_404_NOT_FOUND)
