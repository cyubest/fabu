from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from rest_framework import response
from .models import Student, Room, Exam, Course, UserInformation
from .forms import StudentFORM, CourseForm, RoomForm, UserProfileForm, update_examData, update_CourseForm, update_RoomForm, ExamForm
from .filters import ExamFilter, CourseFilter, RoomFilter
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime
from django.views.generic import ListView
from django.contrib.auth import get_user_model
# imports for report
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import ExamFilter
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users, student_only
from django.contrib.auth.decorators import login_required

# API rest_frameWork imports
from rest_framework.parsers import JSONParser
from .serializers import ExamSerializers, UserInformationSerializers, UserSerializer, LoginUserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
# Token imports to be used
import jwt
import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status
from rest_framework import permissions, generics, status
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth.models import Group
#  API rest_frameWork views


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        # let set our token to the cookies
        response.set_cookie(key='jwt', value=token, httponly=True)
        # we don't want the front-end to access the token(we use cookies) and the only purpose of token is to be sent to the back-end
        response.data = {
            'jwt': token
        }

        return response


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True,)
        user = serializer.validated_data['user']
        user_id_main = user.id
        user_name = user.username
        user_firstName = user.first_name
        user_lastName = user.last_name
        print(user_id_main, user_name)
        user_details = ({"id": user_id_main, "username": user_name,
                        "FirstName": user_firstName, "LastName": user_lastName})
        login(request, user)
        login_details = super(LoginAPI, self).post(request, format=None)
        login_deta = super(LoginAPI, self).post(request, format=None)
        login_deta.data = user_details
        # login_details.data = user_details
        return Response({"data": login_details.data, "user": login_deta.data, "status": status.HTTP_200_OK})


class RegisterView(generics.GenericAPIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# class LoginView(APIView):
#     def post(self, request):
#         username = request.data['username']
#         password = request.data['password']

#         user = User.objects.filter(username=username).first()

#         if user is None:
#             raise AuthenticationFailed('User not found!')

#         if not user.check_password(password):
#             raise AuthenticationFailed('incorrect password!')

#         payload = {
#             'id': user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.utcnow()
#         }

#         token = jwt.encode(payload, 'secret', algorithm='HS256')

#         response = Response()
#         # let set our token to the cookies
#         response.set_cookie(key='jwt', value=token, httponly=True)
#         # we don't want the front-end to access the token(we use cookies) and the only purpose of token is to be sent to the back-end
#         response.data = {
#             'jwt': token
#         }

#         return response


class userView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }

        return response


class ExamAPIView(viewsets.ModelViewSet):
    serializer_class = ExamSerializers

    def get_queryset(self):
        exams = Exam.objects.all()
        return Response(exams)

    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        print(params['pk'])
        exam_std = Exam.objects.filter(students=params['pk'])
        serializer = ExamSerializers(exam_std, many=True)
        return Response({"results": serializer.data})


class UserInfoAPIView(viewsets.ModelViewSet):
    serializer_class = UserInformationSerializers

    def get_queryset(self):
        info = UserInformation.objects.all()
        return Response(info)

    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        print(params['pk'])
        users_info = UserInformation.objects.filter(user=params['pk'])
        print(users_info)
        serializer = UserInformationSerializers(users_info, many=True)
        return Response({"results": serializer.data})


@api_view(['GET'])
def get_student_examTimetable(request, std_Id):
    exams = Exam.objects.get(id=std_Id)
    serializer = ExamSerializers(exams, many=True)
    return Response(serializer.data)


# views for application

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def add_Exam(request):
    form = ExamForm(request.POST or None)

    if form.is_valid():
        time = form.cleaned_data['time']
        date = form.cleaned_data['date']
        rooms = form.cleaned_data['rooms']
        program = form.cleaned_data['program']
        datas = form.cleaned_data['course']
        student_List = Student.objects.filter(course_id=datas)
        print(student_List)
        student_Lists = Student.objects.filter(
            course_id=datas).count()
        exam_date = Exam.objects.filter(date=date, time=time).exists()
        exam_time = Exam.objects.filter(time=time).exists()
        room_seats = Room.objects.get(roomName=rooms)
        floors = Room.objects.get(roomName=rooms)
        floor = floors.floor
        room_s = room_seats.seats
        seats = 0
        students = []
        if exam_date:
            messages.add_message(request, messages.SUCCESS,
                                 "There is an exam on the same date and time please try to add on other date and time")
        else:

            for stdNumber in student_List:
                students.append(stdNumber)

            for std in students:
                students = std
                print(students)
                if student_Lists < room_s:
                    seats += 1
                exam = Exam.objects.create(
                    course=datas, students=students, rooms=rooms, date=date, time=time, program=program, floor=floor, seats=seats)
            exam.save()
            messages.add_message(request, messages.SUCCESS,
                                 "The Exam was added successfully. You may add another Exam below.")
            return redirect('add_exam')
    context = {
        'form': form
    }
    return render(request, 'add_Exams.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def add_Courses(request):
    form = CourseForm(request.POST or None)
    if request.method == 'POST':
        form = form.save(commit=False)
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             "The Exam was added successfully. You may add another Exam below.")
        return redirect('add_course')
    context = {

    }
    return render(request, 'add_Course.html')

# Adjax Querry set for Courses And Students


def load_courses(request):
    courses = Course.objects.all().order_by('courseName')
    print(courses)
    return render(request, 'option/courses_dropdown_list_option.html', {'courses': courses})


def load_students(request):
    courses = request.GET.get('course')

    students = Student.objects.filter(
        course_id=courses).exclude(firstName='--- Select Students ---').order_by('firstName')
    context = {
        'students': students,
    }
    return render(request, 'option/student_dropdown_list_options.html', context)

# Adjax Querry set for Room And Seats


def load_room(request):
    rooms = Room.objects.all().order_by('roomName')
    # print(rooms)
    return render(request, 'option/room_dropdown_list_option.html', {'rooms': rooms})


# You can access the join table that Django automatically  creates for you by doing:

# User.videos.through.objects.all()
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def add_Courses(request):
    form = CourseForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             "The Course was added successfully. You may add another Course below.")
        return redirect('add_course')
    context = {
        'form': form,
    }
    return render(request, 'add_Course.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def add_Student(request):
    form = StudentFORM(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             "The Course was added successfully. You may add another Course below.")
        return redirect('add_student')
    context = {
        'form': form,
    }
    return render(request, 'add_Students.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def add_Room(request):
    form = RoomForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             "The Room was added successfully. You may add another Room below.")
        return redirect('add_room')
    context = {
        'form': form,
    }
    return render(request, 'add_Room.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def main_dash(request):
    current_year = datetime.datetime.now().year
    current_day = datetime.datetime.now().day
    current_month = datetime.datetime.now().month
    courses = Course.objects.all().count()
    rooms = Room.objects.all().count()
    now = datetime.datetime.now().today()
    exams = Exam.objects.filter(date__gt=datetime.datetime.now()).count()

    januaryExam = Exam.objects.filter(
        date__year=current_year).filter(date__month="1").count()
    februaryExam = Exam.objects.filter(
        date__year=current_year).filter(date__month="2").count()
    marchExam = Exam.objects.filter(
        date__year=current_year).filter(date__month="3").count()
    aprilExam = Exam.objects.filter(
        date__year=current_year).filter(date__month="4").count()
    mayExam = Exam.objects.filter(
        date__year=current_year).filter(date__month="5").count()
    juneExam = Exam.objects.filter(
        date__year=current_year).filter(date__month="6").count()
    julyExam = Exam.objects.filter(
        date__year=current_year).filter(date__month="7").count()
    augustExam = Exam.objects.filter(
        date__year=current_year).filter(date__month="8").count()
    septemberExam = Exam.objects.filter(
        date__year=current_year, date__month="9").count()
    octoberExam = Exam.objects.filter(
        date__year=current_year).filter(date__month="10").count()
    novemberExam = Exam.objects.filter(
        date__year=current_year).filter(date__month="11").count()
    decemberExam = Exam.objects.filter(
        date__year=current_year).filter(date__month="12").count()

    context = {
        'exams': exams,
        'courses': courses,
        'rooms': rooms,
        'januaryExam': januaryExam,
        'februaryExam': februaryExam,
        'marchExam': marchExam,
        'aprilExam': aprilExam,
        'mayExam': mayExam,
        'juneExam': juneExam,
        'julyExam': julyExam,
        'augustExam': augustExam,
        'septemberExam': septemberExam,
        'octoberExam': octoberExam,
        'novemberExam': novemberExam,
        'decemberExam': decemberExam,
    }
    return render(request, 'main_dash.html', context)


def dashboard_lay(request):
    context = {
    }
    return render(request, 'dashboard_layout.html', context)


# make report views page

content_type = 'application/pdf'


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type=content_type)
    return None


def generate_pdf(request, *args, **kwargs):
    all_exams = Exam.objects.all()
    my_filter = ExamFilter(request.POST, queryset=all_exams)
    filtered_exams = my_filter.qs
    context = {
        'my_filter': my_filter
    }
    if request.method == 'GET':
        return render(request, 'make_report.html', context)
    else:

        data = {
            'filtered_exams': filtered_exams,
            'title': '',
            'today': datetime.datetime.now(),
            'reporter': request.user.first_name,
            'reporterL': request.user.last_name,
            'number_of_data': len(filtered_exams)
        }
    pdf = render_to_pdf('report_page.html', data)
    return HttpResponse(pdf, content_type=content_type)


def reportPDF(request):
    current_year = datetime.now().year
    current_day = datetime.now().day
    current_month = datetime.now().month
    exams = Exam.objects.all()

    myFilter = ExamFilter(request.GET, queryset=exams)
    exams = myFilter.qs

    context = {
        'exams': exams,
        'myFilter': myFilter,
    }
    return render(request, 'reportPdf.html', context)


def exam_render_pdf_view(request, *args, **kwargs):
    current_year = datetime.now().year
    current_day = datetime.now().day
    current_month = datetime.now().month

    exams = Exam.objects.all()
    myFilter = ExamFilter(request.GET, queryset=exams)
    exams = myFilter.qs

    context = {
        'exams': exams,
        'myFilter': myFilter,
    }
    template_path = 'pdf1.html'
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # if you want to download use the code below:
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if you want to view it before download use this:
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def newLandingPage(request):
    context = {
    }
    return render(request, 'landingPage.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # if user.is_active:
            #     print("The password is valid, but the account has been disabled!")
            return redirect('main_dash')

        else:
            messages.info(request, 'username OR password is incorrect')
            #messages.info(request, 'account yawe irafunze hamagara ababishinzwe')
    context = {

    }
    return render(request, 'login_Page.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def userProfile(request):
    form = request.user
    form = UserProfileForm(instance=form)
    context = {
        'form': form,
    }
    return render(request, 'user_ProfilePage.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def viewExam(request):
    exams = Exam.objects.all()
    myFilter = ExamFilter(request.GET, queryset=exams)
    exams = myFilter.qs

    page = request.GET.get('page', 1)
    paginator = Paginator(exams, 5)

    try:
        examos = paginator.page(page)
    except PageNotAnInteger:
        examos = paginator.page(1)
    except EmptyPage:
        examos = paginator.page(paginator.num_pages)

    context = {
        'examos': examos,
        'myFilter': myFilter,
    }
    return render(request, 'view_exams.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def viewCourse(request):
    course = Course.objects.all()
    myFilter = CourseFilter(request.GET, queryset=course)
    courses = myFilter.qs

    page = request.GET.get('page', 1)
    paginator = Paginator(courses, 5)

    try:
        coursos = paginator.page(page)
    except PageNotAnInteger:
        coursos = paginator.page(1)
    except EmptyPage:
        coursos = paginator.page(paginator.num_pages)

    context = {
        'coursos': coursos,
        'myFilter': myFilter,
    }
    return render(request, 'viewCourse.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def viewRoom(request):
    room = Room.objects.all()
    myFilter = RoomFilter(request.GET, queryset=room)
    rooms = myFilter.qs

    page = request.GET.get('page', 1)
    paginator = Paginator(rooms, 5)

    try:
        roomos = paginator.page(page)
    except PageNotAnInteger:
        roomos = paginator.page(1)
    except EmptyPage:
        roomos = paginator.page(paginator.num_pages)

    context = {
        'roomos': roomos,
        'myFilter': myFilter,
    }
    return render(request, 'viewRoom.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def update_exam(request, id):
    id = Exam.objects.get(id=id)
    form = update_examData(request.POST or None, instance=id)
    if request.method == 'POST':
        form = update_examData(request.POST, instance=id)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "The exam was updated successfully.")
            return redirect('exams')
    context = {
        'form': form,
    }

    return render(request, 'updateExams.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def update_course(request, slug):
    id = Course.objects.get(slug=slug)
    form = update_CourseForm(request.POST or None, instance=slug)
    if request.method == 'POST':
        form = update_CourseForm(request.POST, instance=slug)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "The course info updated successfully.")
            return redirect('view_course')
    context = {
        'form': form
    }

    return render(request, 'updateCourse.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def update_room(request, id):
    id = Room.objects.get(id=id)
    form = update_RoomForm(request.POST or None, instance=id)
    if request.method == 'POST':
        form = update_RoomForm(request.POST, instance=id)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "The room info updated successfully.")
            return redirect('view_room')
    context = {
        'form': form,
    }

    return render(request, 'updateRoom.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login_page')


def sign_up(request):
    context = {
    }
    return render(request, 'sign_Up.html', context)


def error_Page(request):
    context = {
    }
    return render(request, '400_errorPage.html', context)
