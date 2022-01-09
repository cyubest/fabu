from django.urls import path
from django.urls.conf import include
from . import views
from .views import (ExamAPIView, UserInfoAPIView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers
from .views import UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('exam_list', ExamAPIView, basename='exam_list')
router.register('user_info', UserInfoAPIView, basename='user_info')

urlpatterns = [
    path('main/', views.main_dash, name='main_dash'),
    path('addExam', views.add_Exam, name='add_exam'),
    path('addStudent', views.add_Student, name='add_student'),
    path('addCourse', views.add_Courses, name='add_course'),
    path('addRoom', views.add_Room, name='add_room'),
    path('dashboard/', views.dashboard_lay, name='dashboard_layout'),
    path('reportpdf/', views.generate_pdf, name='reportpdf'),
    path('report_page/', views.generate_pdf, name='report_page'),
    path('student_exam/',
         ExamAPIView.as_view, name='student_exam'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('api_login/', views.userView.as_view(), name='api_login'),
    path('api_logout/', views.LogoutView.as_view(), name='api_logout'),
    path('login_page/', views.login_page, name='login_page'),
    path('logout/', views.logoutUser, name='logout'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('errorPage/', views.error_Page, name='errorPage'),
    path('exams/', views.viewExam, name='exams'),
    path('profile/', views.userProfile, name="user_profile"),
    path('view_course/', views.viewCourse, name='view_course'),
    path('view_room/', views.viewRoom, name='view_room'),
    path('update_exam/<int:id>/', views.update_exam, name='update_exam'),
    path('update_course/<slug:slug>/', views.update_course, name='update_course'),
    path('update_room/<int:id>/', views.update_room, name='update_room'),
    path('', views.newLandingPage, name='home'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh-token', TokenRefreshView.as_view(), name='refreshtoken'),
    path('test-view/', views.exam_render_pdf_view, name='test-view'),
    path('ajax/load-courses/', views.load_courses, name='ajax_load_courses'),
    path('ajax/load-students/', views.load_students, name='ajax_load_students'),
    path('ajax/load-rooms/', views.load_room, name='ajax_load_rooms'),
    path('', include(router.urls))


]
