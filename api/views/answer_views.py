from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.answer import Answer
from ..serializers import AnswerSerializer

class AnswersView(generics.ListCreateAPIView)
  permission_classes=(IsAuthenticated,)
  serializer_class = AnswerSerializer

  def get(self, request):
    """Index request"""
    answers = Answer.objects.all()[:10]
    data = AnswerSerializer(answers, many=True).data
    return Response({ 'answers': data })

  def post(self, request, pk):
    """Create request"""
    request.data['answer']['owner'] = request.user.id
    # Since we'll be creating comments from the question view URL, we can take the question id from 'pk' in the URL
    request.data['answer']['question'] = pk

    answer = AnswerSerializer(data=request.data['answer'])

    if answer.is_valid():
      answer.save()
      return Response({ 'answer': answer.data }, status=status.HTTP_201_CREATED)

class AnswersDetailView(generics.RetrieveUpdateDestroyAPIView):
  permission_classes=(IsAuthenticated,)
  def get(self, request, pk):
    """Show request"""
    answer = get_object_or_404(Answer, pk=pk)
    data = AnswerSerializer(answer).data
    return Response({ 'answer': data })

  def partial_update(self, request, pk):
    """Update request"""
    answer = get_object_or_404(Answer, pk=pk)
    if request.user != answer.owner:
      raise PermissionDenied("Cannot edit; you didn't write this answer.")

    request.data['answer']['owner'] = request.user.id
    data = AnswerSerializer(answer, data=request.data['answer'], partial=True)

    if data.is_valid():
      data.save()
      return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    """Delete request"""
    answer = get_object_or_404(Answer, pk=pk)

    if request.user != answer.owner:
      raise PermissionDenied("Cannot delete; you didn't write this answer.")

    answer.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
