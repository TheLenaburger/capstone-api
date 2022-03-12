from django.urls import path
from .views.user_views import SignUpView, SignInView, SignOutView, ChangePasswordView
from .views.question_views import QuestionsView, QuestionsCreateView, QuestionDetailView
# from .views.answer_views import AnswersView

urlpatterns = [
  	# Restful routing
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('sign-out/', SignOutView.as_view(), name='sign-out'),
    path('change-pw/', ChangePasswordView.as_view(), name='change-pw'),
    path('questions/', QuestionsView.as_view(), name='questions'),
    path('questions/create/', QuestionsCreateView.as_view(), name='question_create'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('questions/<int:pk>/edit/', QuestionDetailView.as_view(), name='question_update')
    # path('answers/<int:pk>/', AnswersView.as_view(), name='answer_detail')

]
