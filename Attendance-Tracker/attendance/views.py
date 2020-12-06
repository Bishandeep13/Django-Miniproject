from django.shortcuts import render
from .models import Subject
from .forms import SubjectForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    return render(request, 'attendance/index.html')

def homePage(request):
    print(request.user)
    count=0
    totalAttended=0.0
    if str(request.user)=='AnonymousUser':
        return HttpResponseRedirect('/accounts/login/')
    subjects=Subject.objects.filter(userid__exact=request.user)
    
    if request.method =='POST':
        form = SubjectForm(request.POST)
        instance=form.save(commit=False)
        instance.userid=request.user
        instance.save()
    form = SubjectForm()
    studentAttendance=[]
    for subject in subjects:
        studentAttendance.append(subject)
        totalAttended+=subject.attendance
    
    count=len(studentAttendance)
    if count!=0:
        totalAttended=totalAttended/count
    context = {
        'studentAttendance': studentAttendance, 
        'form': form,
        'totalAttendance':totalAttended,
    }
    return render(request, 'attendance/home.html', context)

def deleteSub(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    subject.delete()
    return HttpResponseRedirect('/home/')


def updateAttendance(request, subject_id, attended):
    subject =Subject.objects.get(id=subject_id)

    subject.undo_attendance=subject.attendance
    subject.undo_attended=subject.attended
    subject.undo_total=subject.total

    if attended==0:
        subject.attended=subject.attended+1
        subject.total=subject.total+1
    else:
        subject.total=subject.total+1
    if subject.total!=0:
        subject.attendance='{0:.2f}'.format((subject.attended/subject.total)*100)

    subject.save()
    return HttpResponseRedirect('/home/')


def undoAttendance(request, subject_id):
    subject =Subject.objects.get(id=subject_id)
    subject.attendance=subject.undo_attendance
    subject.attended=subject.undo_attended
    subject.total=subject.undo_total
    subject.save()
    return HttpResponseRedirect('/home/')
