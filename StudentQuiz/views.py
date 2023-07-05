from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from student.models import CustomUser, Staffs, Courses, Subjects, Students
from SFaceRecognize.FRStream.recordScreen import record_screen
# Create your views here.
from StudentQuiz.models import Quiz,Question,Answer,FinalResult

@login_required(login_url='doLogin')
def QuizQuestion(request):
    student_obj = Students.objects.get(admin=request.user.id)
    allquiz=list(Quiz.objects.filter(course=student_obj.course_id))
    context={"allquiz":allquiz}
    return render(request,'quiz.html',context)

def CreateQuize(request):
    courses = Courses.objects.all()
    context={"courses":courses}
    return render(request,'HOD_CreateQuiz.html',context)

def CreateQuizSave(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('createquiz')
    else:
        quizname = request.POST.get('quizname')
        quiztopic = request.POST.get('quiztopic')
        questionumber = request.POST.get('questionumber')
        quiztime = request.POST.get('quiztime')
        quizscore = request.POST.get('quizscore')
        quizDifficulty = request.POST.get('quizDifficulty')
        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)
        try:
            quizall = Quiz(name=quizname,topic=quiztopic,number_of_questions=questionumber,
                           time=quiztime,required_score_to_pass=quizscore,difficulty=quizDifficulty,course=course,)
            quizall.save()
            messages.success(request, "Quiz Created Successfully!")
            return redirect('createquiz')
        except:
            messages.error(request, "Failed to Add Subject!")
            return redirect('createquiz')


def ManageQuiz(request):
    mangquiz=Quiz.objects.all()[::-1]
    context={
        "mangquiz":mangquiz
    }
    return render(request,'managequiz.html',context)


def CreateQuestion(request):
    allquiz=Quiz.objects.all()
    context={"quiz":allquiz}
    return  render(request,'HOD_CreateQuestions.html',context)

def CreateQuestionSave(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('createquestion')
    else:
        questiontext = request.POST.get('questiontext')
        quiz_id = request.POST.get('existquiz')
        quiz = Quiz.objects.get(id=quiz_id)
        # answertext=request.POST.get('answertext')
        # answercheck=request.POST.get('answercheck')
        # question=request.POST.get('question')
        try:
            # answer=Answer(text="answertext",correct=False,question=question)
            # answer.save()
            questionall = Question(text=questiontext, quiz=quiz)
            questionall.save()
            messages.success(request, "Questions  Created Successfully!")
            return redirect('createquestion')
        except:
            messages.error(request, "Failed to Add Questions !")
            return redirect('createquestion')

@login_required(login_url='doLogin')
def AllQuestionShow(request):
    allquests=Question.objects.all()[::-1]
    context={
        "allquests":allquests
    }
    return render(request,"allquestionsList.html",context)


@login_required(login_url='doLogin')
def AnswerCreate(request):
    allq=Question.objects.all()[::-1]
    context={
        "allq":allq
    }
    return render(request,"answerquestion.html",context)

def answerQuestionSave(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('answerquestion')
    else:
        ques_id= request.POST.get('question')
        question=Question.objects.get(id=ques_id)
        answer = request.POST.get('answer')
        check = request.POST.get('check')
        checkfinal=""
        if check=="on":
            checkfinal=True
        else:
            checkfinal=False
        try:
            answerall=Answer(text=answer,correct=checkfinal,question=question)
            answerall.save()
            messages.success(request, "Answer Created Successfully!")
            return redirect('answerquestion')
        except:
            messages.error(request, "Failed to Add Answer !")
            return redirect('answerquestion')



@login_required(login_url='doLogin')
def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'particularquiz.html', {'obj': quiz})

@login_required(login_url='doLogin')
def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        print(q)
        for a in q.get_answer():
            answers.append(a.text)
        questions.append({str(q): answers})
    print(questions)
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
        
    })
    record_screen()
    
    
    
@login_required(login_url='doLogin')
def save_quiz_view(request, pk):
    # print(request.POST)
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key:', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        score_ = score * multiplier
        FinalResult.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})

        