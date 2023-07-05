from django.urls import path
from SFaceRecognize.views import (TakePhotos,train_model,
                                  InitialQuiz,CheckStudentWithVideoStream,
                                  FaceAuthenticate)
urlpatterns = [
    path('takephotos/<int:id>/',TakePhotos,name="studentphotostake"),
    path('trainmodel/',train_model,name="train_model"),
    path('quizinitial/',InitialQuiz,name="quizeinitial"),
    path('checkface/',CheckStudentWithVideoStream,name="checkface"),
    path('faceauthenticate/',FaceAuthenticate,name="studentfaceauthen")
    ]