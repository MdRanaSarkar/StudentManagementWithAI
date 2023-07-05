from django.urls import path
from StudentQuiz.views import ( QuizQuestion,CreateQuize,CreateQuizSave,
                                ManageQuiz,CreateQuestion,CreateQuestionSave,AllQuestionShow,
                                AnswerCreate,answerQuestionSave,quiz_view,save_quiz_view,quiz_data_view)
urlpatterns=[
path('',QuizQuestion,name="QuizData"),
path('createquiz/',CreateQuize,name="createquiz"),
    path('quizesave/',CreateQuizSave,name="createquizesave"),
    path('managequiz/',ManageQuiz,name='managequiz'),
    path('createquestions/',CreateQuestion,name='createquestion'),
path('questionsave/',CreateQuestionSave,name="CreateQuestionSave"),
    path('allquestions/',AllQuestionShow,name="AllQuestionShow"),
    path('answercreate/',AnswerCreate,name="answerquestion"),
path('answercreatesave/',answerQuestionSave,name="answerquestionsave"),
    path('<pk>/', quiz_view, name='quiz-view'),
    path('<pk>/save/', save_quiz_view, name="save-view"),
    path('<pk>/data/', quiz_data_view, name='quiz-data-view'),

]