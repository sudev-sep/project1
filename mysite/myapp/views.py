from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponseForbidden
from django.urls import reverse
from .models import User, Teacher, Student
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404






def home(request):
    return render(request,'home.html')

def student_register(request):
    if request.method == "POST":
        FIRSTNAME = request.POST['FIRSTNAME']
        LASTNAME = request.POST['LASTNAME']
        EMAIL = request.POST['EMAIL']
        ADDRESS = request.POST['ADDRESS']
        PHONE_NUMBER = request.POST['PHONE_NUMBER']
        guardian = request.POST['GUARDIAN']
        USERNAME = request.POST['USERNAME']
        PASSWORD = request.POST['PASSWORD']

        new_user = User.objects.create_user(
            first_name=FIRSTNAME,
            last_name=LASTNAME,
            email=EMAIL,
            username=USERNAME,
            password=PASSWORD,
            address=ADDRESS,
            phone_number=PHONE_NUMBER,
            usertype='student',
            is_active=False   
        )
        new_user.save()

        x = Student.objects.create(student_id=new_user, guardian=guardian)
        x.save()
        return HttpResponse( "<script> alert('Registration successful');window.location.href='/login';</script>")
    
    else:
        return render(request, 'student_register.html')


def teacher_register(request):
    if request.method == "POST":
        FIRSTNAME = request.POST['FIRSTNAME']
        LASTNAME = request.POST['LASTNAME']
        EMAIL = request.POST['EMAIL']
        ADDRESS = request.POST['ADDRESS']
        PHONE_NUMBER = request.POST['PHONE_NUMBER']
        USERNAME = request.POST['USERNAME']
        PASSWORD = request.POST['PASSWORD']
        SALARY = request.POST['SALARY']
        EXPERIENCE = request.POST['EXPERIENCE']

        new_user = User.objects.create_user(
            first_name=FIRSTNAME,
            last_name=LASTNAME,
            email=EMAIL,
            username=USERNAME,
            password=PASSWORD,
            address=ADDRESS,
            phone_number=PHONE_NUMBER,
            usertype='teacher',
            is_active=True,
            is_staff=True,
        )
        new_user.save()
        x = Teacher.objects.create(teacher_id=new_user, salary=SALARY, experience=EXPERIENCE)
        x.save()

        return HttpResponse( "<script> alert('Registration successful');window.location.href='/admin_h';</script>")
    
    else:
        return render(request, 'teacher_register.html')


def login_view(request):
     if request.method=="POST":
        USERNAME=request.POST['USERNAME']
        PASSWORD=request.POST['PASSWORD']
        userpass=authenticate(request,username=USERNAME,password=PASSWORD)
        if userpass is not None and userpass.is_superuser==1:
            return redirect('admin_h')
        elif userpass is not None and userpass.is_staff==1:
            login(request,userpass)
            request.session['teach_id']=userpass.id
            return redirect('teacher_h')
        elif userpass is not None and userpass.is_active==1:
            login(request,userpass)
            request.session['stud_id']=userpass.id
            return redirect('student_h')
        else:
            return HttpResponse('invalid login')
     else:
        return render(request, 'login.html')
     

def student_h(request):
    student = get_object_or_404(Student, student_id=request.user)
    if not request.user.usertype != student:  
        return HttpResponseForbidden("Access denied. Teachers only.")
    return render(request,'student_h.html',{'student': student})


def teacher_h(request):
    teacher = get_object_or_404(Teacher, teacher_id=request.user)
    if not request.user.is_staff:  
        return HttpResponseForbidden("Access denied. Teachers only.")
    students = Student.objects.all()
    return render(request, 'teacher_h.html', {
        'students': students,
        'teacher': teacher
    })

def admin_h(request):
    return render(request, 'admin_h.html')


def student_admin(request):
    students =Student.objects.select_related('student_id').all()
    return render(request, 'student_admin.html', {
        'students': students,
    })

def teacher_admin(request):
    teachers = Teacher.objects.select_related('teacher_id').all()
    return render(request, 'teacher_admin.html', {
        'teachers': teachers,  
    })

def approve_student(request, id):
    stud = Student.objects.select_related('student_id').get(id=id)
    stud.student_id.is_active = True
    stud.student_id.save()
    return redirect('student_admin')

def logout_view(request):
    logout(request)
    return HttpResponse("<script> alert('You have been successfully logged-out!'); window.location.href='/login/';</script>")

def delete_s(request,id):
    x=Student.objects.get(id=id)
    user_id=x.student_id.id
    x.delete()
    user=User.objects.get(id=user_id)
    user.delete()
    return HttpResponse("<script> alert('deleted'); window.location.href='/student_admin';</script>")

def delete_t(request,id):
    x=Teacher.objects.get(id=id)
    user_id=x.teacher_id.id
    x.delete()
    user=User.objects.get(id=user_id)
    user.delete()
    return HttpResponse("<script> alert('deleted'); window.location.href='/teacher_admin';</script>")

def student_edit(request, id):
    student = Student.objects.filter(id=id).first()
    if not student:
        return redirect("student_admin")

    if request.method == "POST":
        student.student_id.first_name = request.POST.get("FIRSTNAME")
        student.student_id.last_name = request.POST.get("LASTNAME")
        student.student_id.email = request.POST.get("EMAIL")
        student.student_id.username = request.POST.get("USERNAME")
        student.student_id.save()

        student.address = request.POST.get("ADDRESS")
        student.phone_number = request.POST.get("PHONE_NUMBER")
        student.guardian = request.POST.get("GUARDIAN")
        student.save()

        return redirect("student_admin")

    return render(request, "student_edit.html", {"student": student})


def student_edit_h(request, id):
    student = get_object_or_404(Student, id=id)

    if request.user != student.student_id and not request.user.is_superuser:
        return HttpResponse("Access denied.")

    if request.method == "POST":
        student.student_id.first_name = request.POST.get("FIRSTNAME")
        student.student_id.last_name = request.POST.get("LASTNAME")
        student.student_id.email = request.POST.get("EMAIL")
        student.student_id.username = request.POST.get("USERNAME")
        student.student_id.save()

        student.address = request.POST.get("ADDRESS")
        student.phone_number = request.POST.get("PHONE_NUMBER")
        student.guardian = request.POST.get("GUARDIAN")
        student.save()
        return redirect("student_h")  

    return render(request, "student_edit.html", {"student": student})





def edit_teacher(request, id):
    teacher = Teacher.objects.filter(id=id).first()
    user = teacher.teacher_id  

    if not teacher:
        return redirect("teacher_admin")   
    if request.method == "POST":
        user.first_name = request.POST["FIRSTNAME"]
        user.last_name = request.POST["LASTNAME"]
        user.email = request.POST["EMAIL"]
        user.address = request.POST["ADDRESS"]
        user.phone_number = request.POST["PHONE_NUMBER"]

        teacher.salary = request.POST["SALARY"]
        teacher.experience = request.POST["EXPERIENCE"]

        user.save()
        teacher.save()

        return redirect("teacher_admin")   

    return render(request, "teacher_edit.html", {"teacher": teacher})


def edit_teacher_h(request, id):
    teacher = Teacher.objects.filter(id=id).first()
    user = teacher.teacher_id  

    if not teacher:
        return redirect("teacher_h")   
    if request.method == "POST":
        user.first_name = request.POST["FIRSTNAME"]
        user.last_name = request.POST["LASTNAME"]
        user.email = request.POST["EMAIL"]
        user.address = request.POST["ADDRESS"]
        user.phone_number = request.POST["PHONE_NUMBER"]

        teacher.salary = request.POST["SALARY"]
        teacher.experience = request.POST["EXPERIENCE"]

        user.save()
        teacher.save()

        return redirect("teacher_h")   

    return render(request, "teacher_edit.html", {"teacher": teacher})











