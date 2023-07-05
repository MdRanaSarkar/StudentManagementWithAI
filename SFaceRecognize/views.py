from django.shortcuts import render
import datetime
import cv2
from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import  reverse
from .FRStream.click import click
from .FRStream.ModelTrain import trainer
from .FRStream.SCvideoStream import stream
from  .FRStream.faceauthenticating import identify_faces
from student.models import CustomUser, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, StudentResult

# Create your views here.
def TakePhotos(request,id):
    cam=cv2.VideoCapture(0)
    std_info=get_object_or_404(Students,id=id)
    click(std_info.admin.username,std_info.id,cam)
    return HttpResponseRedirect(reverse('manage_student'))

def train_model(request):
    trainer()
    return HttpResponseRedirect(reverse('admin_home'))


def InitialQuiz(request):
    # std_info=Students.objects.all()
    # context={
    #     std_info:std_info
    # }
    return render(request,'QuizInitial.html')


def CheckStudentWithVideoStream(request):
    stream()
    return HttpResponseRedirect(reverse('quizeinitial'))

def FaceAuthenticate(request):
    std_info = Students.objects.get(admin=request.user.id)
    videocap = cv2.VideoCapture(0)
    identify_faces(videocap,std_info)
    return HttpResponseRedirect(reverse('QuizData'))


