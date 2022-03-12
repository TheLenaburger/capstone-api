from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.question import Question
from ..serializers import QuestionSerializer, QuestionReadSerializer

class QuestionsView(generics.ListCreateAPIView):
  permission_classes=(IsAuthenticated,)
  serializer_class = QuestionSerializer

  def get(self, request):
    """Index request"""
    questions = Question.objects.all()[:15]
    data = QuestionSerializer(questions, many=True).data
    return Response({ 'questions': data })

  def post(self, request):
    """Create request"""
    request.data['question']['owner'] = request.user.id

    question = QuestionSerializer(data=request.data['question'])

    if question.is_valid():
      question.save()
      return Response({ 'question': question.data }, status=status.HTTP_201_CREATED)

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
  permission_classes=(IsAuthenticated,)
  def get(self, request, pk):
    """Show request"""
    question = get_object_or_404(Question, pk=pk)
    data = QuestionReadSerializer(question).data
    return Response({ 'question': data })

  def partial_update(self, request, pk):
    """Update Request"""
    question = get_object_or_404(Question, pk=pk)

    if request.user != question.owner:
      raise PermissionDenied("Cannot edit; you didn't ask this question.")

    request.data['question']['owner'] = request.user.id
    data = QuestionSerializer(question, data=request.data['question'], partial=True)

    if data.is_valid():
      data.save()
      return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    """Delete request"""
    question = get_object_or_404(Question, pk=pk)

    if request.user != question.owner:
      raise PermissionDenied("Cannot delete; you didn't ask this question.")

    question.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
