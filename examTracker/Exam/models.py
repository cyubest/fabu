from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, User

# Create your models here.
# class User(AbstractUser):
#     username = models.CharField(max_length=200)
#     password = models.CharField(max_length=255)


class UserInformation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.email


class Course(models.Model):
    courseName = models.CharField(max_length=100)
    course_Id = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return self.courseName


class Student(models.Model):
    std_Id = models.CharField(max_length=100, primary_key=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    course_id = models.ManyToManyField(Course, related_name='courses')

    def __str__(self):
        return str(self.std_Id)


# class StudentCourse(models.Model):
#     student = models.ForeignKey(
#         Student, on_delete=models.CASCADE,)
#     course = models.ForeignKey(
#         Course, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.student.firstName, self.course

# # avoiding to be registered twice in course
#     class Meta:
#         unique_together = [['student', 'course']]

class Room(models.Model):
    FLOOR = (
        ('1stFloor', '1stFloor'),
        ('2ndFloor', '2ndFloor'),
        ('3rdFloor', '3rdFloor'),
    )
    roomName = models.CharField(max_length=100, unique=True)
    floor = models.CharField(max_length=100, choices=FLOOR)
    seats = models.IntegerField(default=0)

    def __str__(self):
        return self.roomName


class Exam(models.Model):

    PROGRAM = (
        ('Day', 'Day'),
        ('Evening', 'Evening')
    )
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    students = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    time = models.TimeField(null=True)
    rooms = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='roomNew',)
    seats = models.IntegerField(default=0)
    floor = models.CharField(max_length=100)
    program = models.CharField(max_length=100, choices=PROGRAM)

    def __str__(self):
        return self.course.courseName

    # def save_exam(self):
    #     if Exam.objects.filter(time=self.time, date=self.date).exists():
    #         print('There is an exam on that time')

    # # avoiding to be registered twice in course and seats and rooms(unique together means no student allowed to register twice in course for exams)
    # class Meta:
    #     unique_together = [['course', 'students']]

    # class Meta:
    #     unique_together = [['rooms', 'seats']]
