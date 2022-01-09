from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Room, Course, Exam
from django.forms import ModelForm, Textarea, TextInput, Select, DateTimeInput, DateTimeField, MultipleChoiceField
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime


# class DateTimeInput(forms.DateTimeInput):
#     input_type = "datetime-local"

#     def __init__(self, **kwargs):
#         kwargs["format"] = "%Y-%m-%dT%H:%M"
#         super().__init__(**kwargs)


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam

        fields = [
            'course',
            'rooms',
            'program',
            'date',
            'time'
        ]

        widgets = {
            'course': Select(attrs={'class': 'form-control'}),
            'rooms':  Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={
                'class': 'form-control',
            }),
            'date': DateInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'time': TimeInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

    #      date_time_input = forms.DateField(widget=AdminSplitDateTime())
    #         def clean_name(self):
    #           name = self.cleaned_data['name']
    #             if myModel.objects.filter(name=name).exists():
    #               raise forms.ValidationError('The name [%s] already exists' % name)
    #         return name


class StudentFORM(forms.ModelForm):
    class Meta:
        model = Student

        fields = [

            'std_Id',
            'firstName',
            'lastName',
            'course_id',
        ]
        widgets = {

            'course_id': forms.Select(attrs={
                'class': 'form-control',
            }),
            'firstName': forms.TextInput(attrs={
                'class': 'form-control',

            }),
            'lastName': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'name'
            }),

            'std_Id': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'course_Id',
            'courseName',
        ]
        widgets = {
            'course_Id': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'courseName': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'name'
            }),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'roomName',
            'floor',
            'seats',
        ]
        widgets = {

            'seat_id': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'roomName': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'roomName',
            }),
            'floor': Select(attrs={
                'class': 'form-control',
                'placeholder': 'floor'
            }),
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['readonly'] = True
        self.fields['last_name'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['is_active'].widget.attrs['readonly'] = True


class update_examData(forms.ModelForm):
    class Meta:
        model = Exam
        fields = [
            'course',
            'rooms',
            'program',
            'date',
            'time'
        ]

        widgets = {
            'course': forms.TextInput(attrs={
                'class': 'form-control',

            }),

            'rooms': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'program': forms.Select(attrs={
                'class': 'form-control',

            }),
            'date': DateInput(
                attrs={
                    'class': 'form-control',

                }
            ),
            'time': TimeInput(
                attrs={
                    'class': 'form-control',

                }
            ),
        }


class update_CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'course_Id',
            'courseName',
        ]
        widgets = {
            'course_Id': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'courseName': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'name'
            }),
        }


class update_RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'roomName',
            'floor',
            'seats',
        ]
        widgets = {

            'seat_id': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'roomName': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'roomName',
            }),
            'floor': Select(attrs={
                'class': 'form-control',
                'placeholder': 'floor'
            }),
        }
