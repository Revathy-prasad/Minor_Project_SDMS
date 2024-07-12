from django.db import models

# Create your models here.

class Courses(models.Model):
    Course_name = models.TextField()

class Semester(models.Model):
    Courses = models.ForeignKey(Courses,on_delete=models.CASCADE,default=None)
    Semester_name = models.CharField(max_length = 5)

class Batches(models.Model):
    Courses = models.ForeignKey(Courses,on_delete=models.CASCADE,default=None)
    Semester = models.ForeignKey(Semester,on_delete=models.CASCADE,default=None)
    Batch_name = models.CharField(max_length = 15)


class Subjects(models.Model):
    Courses = models.ForeignKey(Courses,on_delete=models.CASCADE,default=None)
    Semester = models.ForeignKey(Semester,on_delete=models.CASCADE,default=None)
    Subject_code = models.CharField(max_length = 6)
    Subject_name = models.CharField(max_length = 75)


class Students(models.Model):
    Batches = models.ForeignKey(Batches,on_delete=models.CASCADE,default=1)
    Username = models.CharField(max_length = 30, default = 'null')
    Pass = models.CharField(max_length = 255, default = 'null')
    KTUID = models.CharField(max_length = 15)
    Admnno = models.CharField(max_length = 15)
    Rollno = models.CharField(max_length = 3)
    Name = models.CharField(max_length = 30)
    Religion = models.CharField(max_length = 15)
    Category = models.CharField(max_length = 30)
    Gender = models.CharField(max_length = 12)
    Dob = models.CharField(max_length = 12)
    Address = models.TextField()
    PhoneNumber = models.CharField(max_length = 10)
    Personalmail = models.EmailField(max_length = 30)
    RITmail = models.EmailField(max_length = 30)
    Nationality = models.CharField(max_length = 20)
    Aadharno = models.CharField(max_length = 12)
    Blood_group = models.CharField(max_length = 15)
    Year_of_admission = models.IntegerField(default=1) 
    Status = models.CharField(max_length = 15)
    Guardian_name = models.CharField(max_length = 30)
    Guardian_contact_no = models.CharField(max_length = 10)

class Electives(models.Model):
    Subjects = models.ForeignKey(Subjects,on_delete=models.CASCADE,default=None)

class ElectiveChoices(models.Model):
    Students = models.ForeignKey(Students,on_delete=models.CASCADE,default=None)
    Electives = models.ForeignKey(Electives,on_delete=models.CASCADE,default=None)

class Faculties(models.Model):
    Username = models.CharField(max_length = 30, default = 'null')
    Pass = models.CharField(max_length = 255, default = 'null')
    Emp_no = models.CharField(max_length = 15)
    Faculty_name = models.CharField(max_length = 15)

# class Usersstudent(models.Model):
#     Students = models.ForeignKey(Students,on_delete=models.CASCADE,default=1)
#     Username = models.CharField(max_length = 30)
#     Password = models.CharField(max_length = 15)

# class UsersFaculty(models.Model):
#     Faculties = models.ForeignKey(Faculties,on_delete=models.CASCADE,default=1)
#     Username = models.CharField(max_length = 30)
#     Password = models.CharField(max_length = 15)

class Admin(models.Model):
    Username = models.CharField(max_length = 30, default = 'admin')
    Password = models.CharField(max_length = 255, default = 'admin')

class Advisors(models.Model):
    Faculties = models.ForeignKey(Faculties,on_delete=models.CASCADE,default=None)
    Batches = models.ForeignKey(Batches,on_delete=models.CASCADE,default=None)
    
class FacultySubjects(models.Model):
    Faculties = models.ForeignKey(Faculties,on_delete=models.CASCADE,default=None)
    Subjects = models.ForeignKey(Subjects,on_delete=models.CASCADE,default=None)
    Batches = models.ForeignKey(Batches,on_delete=models.CASCADE,default=None)

class Attendance(models.Model):
    Students = models.ForeignKey(Students,on_delete=models.CASCADE,default=1)
    Faculties = models.ForeignKey(Faculties,on_delete=models.CASCADE,default=None)
    Subjects = models.ForeignKey(Subjects,on_delete=models.CASCADE,default=None)
    Batches = models.ForeignKey(Batches,on_delete=models.CASCADE,default=None)
    Date = models.DateField()
    Hour = models.IntegerField()
    Status = models.CharField(max_length = 7,default='P')

class SeriesExamMarks(models.Model):
    Students = models.ForeignKey(Students,on_delete=models.CASCADE,default=None)
    Subjects = models.ForeignKey(Subjects,on_delete=models.CASCADE,default=None)
    SeriesExamNo = models.IntegerField()
    Marks = models.FloatField()

class AssignmentMarks(models.Model):
    Students = models.ForeignKey(Students,on_delete=models.CASCADE,default=None)
    Subjects = models.ForeignKey(Subjects,on_delete=models.CASCADE,default=None)
    AssignmentNo = models.IntegerField()
    Marks = models.FloatField()

class InternalMarks(models.Model):
    Students = models.ForeignKey(Students,on_delete=models.CASCADE,default=None)
    FacultySubjects = models.ForeignKey(FacultySubjects,on_delete=models.CASCADE,default=None)
    SeriesExamMarks = models.ForeignKey(SeriesExamMarks,on_delete=models.CASCADE,default=None)
    AssignmentMarks = models.ForeignKey(AssignmentMarks,on_delete=models.CASCADE,default=None)
    Attendancemarks = models.IntegerField()
    Total = models.IntegerField()

class GradeCards(models.Model):
    Students = models.ForeignKey(Students,on_delete=models.CASCADE,default=None)
    Subjects = models.ForeignKey(Subjects,on_delete=models.CASCADE,default=None)
    Semester = models.CharField(max_length = 5)
    Subject_code = models.CharField(max_length = 5)
    Subject_name = models.TextField()
    Credit = models.IntegerField()
    Month_and_year = models.CharField(max_length = 15)
    Grade = models.CharField(max_length = 5)
    SGPA = models.FloatField()
    Status = models.BooleanField(default=False)

class LeaveRequests(models.Model):
    Students = models.ForeignKey(Students,on_delete=models.CASCADE,default=None)
    Faculties = models.ForeignKey(Faculties,on_delete=models.CASCADE,default=None)
    Subjects = models.ForeignKey(Subjects,on_delete=models.CASCADE,default=None)
    Date = models.DateField()
    Hour = models.IntegerField()
    LeaveType = models.CharField(max_length = 15)
    Reason = models.TextField()
    DL_upload = models.FileField(upload_to='pdf_files/')
    Adv_approval = models.BooleanField(default=0)
    Fac_approval = models.BooleanField(default=0)
    Status = models.CharField(max_length = 15)
class pdfconvert(models.Model):
    name_candidate=models.CharField(max_length=300,default="")
    regno=models.CharField(max_length=300,default="")
    clgname=models.CharField(max_length=300,default="")
    branch=models.CharField(max_length=300,default="")
    sem=models.CharField(max_length=300,default="")
    pgm=models.CharField(max_length=300,default="")
    coursname=models.CharField(max_length=3000,default="")
    code=models.CharField(max_length=300,default="")
    grade=models.CharField(max_length=300,default="")
    credits=models.CharField(max_length=300,default="")
    mnthyearofexam=models.CharField(max_length=300,default="")
    totcrd=models.IntegerField(default="1")
    sgpa=models.FloatField(default="1.0")
    def __str__(self):
        return self.name_candidate
