
from django.shortcuts import get_object_or_404
from .models import *
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import JsonResponse, HttpResponseNotFound
from django.db.models import Count
import os
from django.http import FileResponse
# import io
import tabula

import PyPDF2

from PyPDF2 import PdfReader
# import PyPDF2
# from PyPDF2 import PdfReader

import pdfplumber
import re

def generate_pdf(request):
    attendance = get_attendance_data()
    table = AttendanceTable(attendance)
    
def view_uploaded_pdf(request, pdf_id):
    # Retrieve the LeaveRequests instance
    leave_request = LeaveRequests.objects.get(id=pdf_id)

    # Retrieve the path to the uploaded PDF file
    pdf_path = leave_request.DL_upload.path

    # Open the PDF file in binary mode
    with open(pdf_path, 'rb') as f:
        response = HttpResponse(f, content_type='application/pdf')

    return response
def bases(request) :
    return render(request,"base.html",{})

def loginpage(request):
    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            usertype = request.POST.get('usertype')
            
            if(usertype=="Admin"):
                aobj = Admin.objects.get(Username = username)
                
                if aobj.Password == password:
                    try:
                        batches = Batches.objects.annotate(num_students=Count('students'))
                        fac = Faculties.objects.count()
                        context={
                        'batches':batches,
                        'fac':fac
                        }
                        return render(request,'index_admin.html',context)
                    except:
                        return render(request,"login.html",{})
                    
            elif(usertype=="Faculty"):
                fobj = Faculties.objects.get(Username = username)
                if fobj.Pass == password:
                    try:
                        request.session['loginfac']=fobj.id

                        return render(request,'indexfaculty.html')
                    except:
                        return render(request,"login.html",{})
                    
            elif(usertype=="Student"):
                
                sobj = Students.objects.get(Username = username)
                if sobj.Pass == password:
                    try:
                        request.session['loginstu']=sobj.id
                        return render(request,'index.html',{})
                    except:
                        return render(request,"login.html",{})
            elif(usertype=="Advisor"):
                fobj = Faculties.objects.get(Username=username)
                # context={
                #     'fobj':fobj
                # }
                if fobj.Pass == password:
                    try:
                        adobj = Advisors.objects.get(Faculties_id = fobj.id)
                        request.session['loginadvisor']=adobj.id
                        return render(request,'indexadvisor.html')
                    except:
                        return render(request,"login.html",{})
                    
            
    return render(request,"login.html",{})

def proj(request) :
    batches = Batches.objects.annotate(num_students=Count('students'))
    fac = Faculties.objects.count()
    context={
    'batches':batches,
    'fac':fac 
    
    }

    return render(request,"index_admin.html",context)



def regstudent(request) :
    if request.method == 'POST':

        stuname1 = request.POST.get('stuname')
        stuuser1 = request.POST.get('stuuser')
        stupassword1 = request.POST.get('stupassword')
        stuadmn1 = request.POST.get('stuadmn')
        stuktu1 = request.POST.get('stuktu')
        stuyofadmn1 = request.POST.get('stuyofadmn')
        batchid = request.POST.get('selbatch')
        batchid1 = int(batchid)
        courseid = request.POST.get('selcourse')
        courseid1 = int(courseid)

        objstudent = Students()
        objstudent.Name = stuname1
        objstudent.Username = stuuser1
        objstudent.Pass = stupassword1
        objstudent.Admnno= stuadmn1
        objstudent.KTUID = stuktu1
        objstudent.Year_of_admission = stuyofadmn1
        objstudent.Courses_id = courseid1
        objstudent.Batches_id = batchid1
        objstudent.save()
        request.session['stu']=objstudent.id
        messages.success(request,"Student Registered")
    selectbatch = Batches.objects.all()
    selectcourse = Courses.objects.all()
    context = {
        'selectbatch':selectbatch,
        'selectcourse':selectcourse
    }
    return render(request,"regstudent.html",context)

def regfaculty(request) :
    if request.method == 'POST':

        facname1 = request.POST.get('facname')
        facuser1 = request.POST.get('facuser')
        facpassword1 = request.POST.get('facpassword')
        facid1 = request.POST.get('facid')

        objfaculty = Faculties()
        objfaculty.Faculty_name = facname1
        objfaculty.Username = facuser1
        objfaculty.Pass = facpassword1
        objfaculty.Emp_no= facid1
        objfaculty.save()
        request.session['fac']=objfaculty.id
        messages.success(request,"Faculty Registered")
    return render(request,"regfaculty.html",{})

def assignsubject(request) :
    if request.method == 'POST':
        selected_course_id = request.POST.get('selcourse')
        selected_semester_id = request.POST.get('selsemester')

        # Perform further processing or database operations with the selected values
        
    else:
        selectfacname = Faculties.objects.all()
        selectempno = Faculties.objects.all()
        selectcourse = Courses.objects.all()
        selectbatch = Batches.objects.all()
        selectsemester = Semester.objects.all()

        selectsubject = Subjects.objects.all()
        selectsubjectcode = Subjects.objects.all()
        # cr = Courses.objects.all()
        # sem= Semester.objects.all()
        context = {
        'selectfacname':selectfacname,
        'selectempno':selectempno,
        'selectcourse':selectcourse,
        'selectbatch':selectbatch,
        'selectsemester':selectsemester,
        'selectsubject':selectsubject,
        'selectsubjectcode':selectsubjectcode,
        }
        return render(request,"assign_subject.html",context)
def saveassignsubject(request):
    if request.method == 'POST':
        facname = request.POST.get('selfacname')
        facname1 = int(facname)
        empno = request.POST.get('selempno')
        empno1 = int(empno)
        courseid=request.POST.get('selcourse')
        courseid1 = int(courseid)

        batchid = request.POST.get('selbatch')
        batchid1 = int(batchid)
        semesterid = request.POST.get('selsemester')
        semesterid1 = int(semesterid)
        subjectname = request.POST.get('selsubject')
        subjectname1 = int(subjectname)
        subjectcode = request.POST.get('selsubjectcode')
        subjectcode1 = int(subjectcode)

        objfacsub = FacultySubjects()
        objfacsub.Faculties_id = facname1
        objfacsub.Faculties_id = empno1
        objfacsub.Courses_id = courseid1
        objfacsub.Batches_id = batchid1
        objfacsub.Semester_id = semesterid1

        objfacsub.Subjects_id = subjectname1
        objfacsub.Subjects_id = subjectcode1
        request.session['loginfac']=objfacsub.Batches_id
        objfacsub.save()
        messages.success(request,"Subject assigned for Faculty")
    # selectfacname = Faculties.objects.all()
    # selectempno = Faculties.objects.all()
    # selectcourse = Courses.objects.all()
    # selectbatch = Batches.objects.all()
    # selectsemester = Semester.objects.all()

    # selectsubject = Subjects.objects.all()
    # selectsubjectcode = Subjects.objects.all()
   
    # context = {
    #     'selectfacname':selectfacname,
    #     'selectempno':selectempno,
    #     'selectcourse':selectcourse,
    #     'selectbatch':selectbatch,
    #     'selectsemester':selectsemester,
    #     'selectsubject':selectsubject,
    #     'selectsubjectcode':selectsubjectcode,
        
    # }
    return render(request,"assign_subject.html",{})

def assignadvisor(request) :
    if request.method == 'POST':
        courseid = request.POST.get('selcourse')
        courseid1 = int(courseid)
        batchid = request.POST.get('selbatch')
        batchids = int(batchid)
        facname = request.POST.get('selfacname')
        facnames = int(facname)
        empno = request.POST.get('selempno')
        empno1 = int(empno)
        # adv = request.session['loginadvisor']
        objadvisor = Advisors()
        objadvisor.Courses_id = courseid1
        objadvisor.Batches_id = batchids
        objadvisor.Faculties_id = facnames
        objadvisor.Faculties_id = empno1
        objadvisor.save()
        messages.success(request,"Advisor successfully assigned")

    selectcourse = Courses.objects.all()
    selectbatch = Batches.objects.all()
    selectfacname = Faculties.objects.all()
    selectempno = Faculties.objects.all()
    context = {
        'selectcourse':selectcourse,
        'selectbatch':selectbatch,
        'selectfacname':selectfacname,
        'selectempno':selectempno
    }
    return render(request,"assign_advisor.html",context)

def editadvisor(request):
    if request.method == 'POST':
        courseid = request.POST.get('selcourse')
        courseid1 = int(courseid)
        batchid = request.POST.get('selbatch')
        batchids = int(batchid)
        facname = request.POST.get('selfacname')
        facnames = int(facname)
        empno = request.POST.get('selempno')
        empno1 = int(empno)
        # adv = request.session['loginadvisor']
        objadvisor = Advisors.objects.get(Faculties_id = facnames)
        objadvisor.Courses_id = courseid1
        objadvisor.Batches_id = batchids
        objadvisor.Faculties_id = facnames
        objadvisor.Faculties_id = empno1
        objadvisor.save()
        messages.success(request,"Advisor successfully edited")

    selectcourse = Courses.objects.all()
    selectbatch = Batches.objects.all()
    selectfacname = Faculties.objects.all()
    selectempno = Faculties.objects.all()
    context = {
        'selectcourse':selectcourse,
        'selectbatch':selectbatch,
        'selectfacname':selectfacname,
        'selectempno':selectempno
    }
    return render(request,"editadvisor.html",context)

# def updatestudent(request) :
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         admnno = request.POST.get('stuadmn')
#         name = request.POST.get('stuname')

#         objstu = Students.objects.filter(Admnno=admnno)
#     return render(request, 'update_student.html',{})
#     # else:
#     #     return render(request,"update_student.html")

def delstudent(request) :
    
       
    return render(request,"del_student.html",{})
def delstudsave(request) :
    if request.method=='POST':
        
        admn=request.POST.get('inputAdmissionNo5')
        stud=Students.objects.get(Admnno=admn)
        stud.delete()
        messages.success(request,"Deleted!")
       
    else:
        return render(request,"del_student.html",{})

def delfaculty(request) :
    return render(request,"del_faculty.html",{})
def delfacultysave(request) :
    if request.method=='POST':
        
        facno=request.POST.get('inputFacultyID6')
        fac=Faculties.objects.get(Emp_no=facno)
        fac.delete()
        return HttpResponse('Deleted!')
        # messages.success(request,"Delete Faculty!")  
    else:
        return render(request,"del_faculty.html",{})

def semupdation(request) :
    if request.method == 'POST':
        batchid = request.POST.get('selbatch')
        batchid1 = int(batchid)
        courseid = request.POST.get('selcourse')
        courseid1 = int(courseid)
        semesterid = request.POST.get('selsemester')
        semesterid1 = int(semesterid)
        psemesterid = request.POST.get('selsemester')
        psemesterid1 = int(psemesterid)
        objupsem = Batches.objects.get(id = batchid1)
        objupsem.Semester_id = psemesterid1
        objupsem.save()
        messages.success(request,"Semester updated")
    selectbatch = Batches.objects.all()
    selectcourse = Courses.objects.all()
    selectsemester = Semester.objects.all()
    context = {
        'selectbatch':selectbatch,
        'selectcourse':selectcourse,
        'selectsemester':selectsemester
    }
    
    return render(request,"sem_updation.html",context)


def selectelective(request):
    if request.method == 'POST':
        selected_semester_id = request.POST.get('selsemester')
        selected_subject_id = request.POST.get('selsubject')

        # Perform further processing or database operations with the selected values
        
    else:
        semesters = Semester.objects.all()
        subjects = Subjects.objects.all()
        context = {
            'sem': semesters,
            'sub': subjects
        }
        return render(request, 'select_elective.html', context)
def saveelective(request):
    if request.method == 'POST':

        sub=request.POST.get('selsubject')
        
        obj=Electives()
        obj.Subjects_id=sub
       
      

        obj.save()
        
        messages.success(request,"Elective Subject Assigned!!")
        return render(request,"select_elective.html",{})
    else:
        return render(request,"select_elective.html",{})
    

def electivestudent(request):
    return render(request,"electivestudent.html",{})
def addbatch(request):
    if request.method == 'POST':
        selected_course_id = request.POST.get('selcourse')
        selected_semester_id = request.POST.get('selsemester')

        # Perform further processing or database operations with the selected values
        
    else:
        cr = Courses.objects.all()
        sem= Semester.objects.all()
        context = {
            'cr': cr,
            'sem': sem
        }
        return render(request,"add_batch.html",context)
def batchdrop(request) :
    if request.method == 'POST':
        addbatch1 = request.POST.get('addbatch')
        courseid = request.POST.get('selcourse')
        courseid1 = int(courseid)
        semesterid = request.POST.get('selsemester')
        semesterid1 = int(semesterid)
        objbatch = Batches()
        objbatch.Batch_name = addbatch1
        objbatch.Courses_id = courseid1
        objbatch.Semester_id = semesterid1
        objbatch.save()
        messages.success(request,"Batch added")
        return render(request,"add_batch.html")
    # selectcourse = Courses.objects.all()
    # selectsemester = Semester.objects.all()
    # context = {
    #     'selectcourse':selectcourse,
    #     'selectsemester':selectsemester
    # }
    return render(request,"add_batch.html")

def addcourse(request) :
    if request.method == 'POST':
        addcourse1 = request.POST.get('addcourse')

        objcourse = Courses()
        objcourse.Course_name = addcourse1
        objcourse.save()
        messages.success(request,"Course Added!!")

		# messages.success(request,'Course Added!!')
		# return render(request,'add_course.html')
    
    return render(request,'add_course.html')

def addsemester(request) :
    if request.method == 'POST':
        courseid = request.POST.get('selcourse')
        courseid1 = int(courseid)
        addsemester1 = request.POST.get('addsemester')

        objsemester = Semester()
        
        objsemester.Courses_id = courseid1
        objsemester.Semester_name = addsemester1
        objsemester.save()
        request.session['sem']=objsemester.id
        messages.success(request,"Semester added")
        
    selectcourse = Courses.objects.all()
    context = {
    'selectcourse':selectcourse
    }
    
    return render(request,"add_semester.html",context)
    # else:
    #     return render(request,"add_semester.html")

def addsubject(request) :
    if request.method == 'POST':
        selected_course_id = request.POST.get('selcourse')
        selected_semester_id = request.POST.get('selsemester')

        # Perform further processing or database operations with the selected values
        
    else:
        cr = Courses.objects.all()
        sem= Semester.objects.all()
        context = {
            'cr': cr,
            'sem': sem
        }
        return render(request,"add_subject.html",context)

def savesub(request):
    if request.method == 'POST':
        addsubject1 = request.POST.get('addsubject')
        addsubjectcode1 = request.POST.get('addsubjectcode')
        courseid = request.POST.get('selcourse')
        courseid1 = int(courseid)
        semesterid = request.POST.get('selsemester')
        semesterid1 = int(semesterid)
    #     # electivechoice = request.POST.get('selelective')
        objsubject = Subjects()
        objsubject.Subject_name = addsubject1
        objsubject.Subject_code = addsubjectcode1
        objsubject.Courses_id = courseid1
        objsubject.Semester_id = semesterid1
        objsubject.save()
        # if electivechoice == 'Yes':
        #     objelective = Electives()
        #     objelective.Subjects_id = objsubject.Subject_name
        #     objelective.save()
        # messages.success(request,"Subject added")
    return render(request,"add_subject.html",{})
    # else:
        # return render(request,"add_subject.html",{})


    # selectcourse = Courses.objects.all()
    # selectsemester = Semester.objects.all()
    # context = {
    #     'selectcourse':selectcourse,
    #     'selectsemester':selectsemester
    # }
    
    

def viewcourse(request):
    
    coursedata = Courses.objects.all()
    context = {
        'coursedata':coursedata
    }
    return render(request,"viewcourse.html",context)

def viewbatch(request):
    if request.method == 'POST':
        courseid = request.POST.get('selcourse')
        courseid1 = int(courseid)
    selectcourse = Courses.objects.all()
    context = {
        'selectcourse':selectcourse,
    }
    return render(request,"viewbatch.html",context)

def btnviewbatch(request):
    if request.method == 'POST':
        courseid = request.POST.get('selcourse')
        courseid1 = int(courseid)
        batchdata = Batches.objects.filter(Courses_id=courseid1)
        context={
            'batchdata':batchdata
        }
        return render(request,"batch.html",context)
    else:
        return render(request,"batch.html")

def viewsemester(request):
    if request.method == 'POST':
        courseid = request.POST.get('selcourse')
        courseid1 = int(courseid)
    selectcourse = Courses.objects.all()
    
    context = {
        'selectcourse':selectcourse,
    }
    return render(request,"viewsemester.html",context)

def btnviewsem(request):
    if request.method == 'POST':
        courseid = request.POST.get('selcourse')
        courseid1 = int(courseid)
        semesterdata = Semester.objects.filter(Courses_id=courseid1)
        context={
            'semesterdata':semesterdata
        }
        return render(request,"semester.html",context)
    else:
        return render(request,"semester.html")

def viewsubject(request):
    if request.method == 'POST':
        courseid = request.POST.get('selcourse')
        courseid1 = int(courseid)
        semesterid = request.POST.get('selsemester')
        
        semesterid1 = int(semesterid)
        # sm=request.session['semesterid1']
    
    
    selectcourse = Courses.objects.all()
    selectsemester = Semester.objects.all()
    # semesteridm = request.session['sem']
    # subjectdata = Subjects.objects.filter(Semester_id=semesterid1)  
    context = {
        'selectcourse':selectcourse,
        'selectsemester':selectsemester,
        # 'subjectdata':subjectdata
    }
    return render(request,"viewsubject.html",context)

def btnview(request):
    if request.method == 'POST':
        courseid = request.POST.get('selcourse')
        courseid1 = int(courseid)
        semesterid = request.POST.get('selsemester')
        semesterid1 = int(semesterid)
        subjectdata = Subjects.objects.filter(Courses_id=courseid1,Semester_id=semesterid1)
        context={
            'subjectdata':subjectdata
        }
        return render(request,"subject.html",context)
    else:
        return render(request,"subject.html")


def deletecourse(request):
    Course_name=Courses.objects.all()
    context={
    'Course_name':Course_name
    }
    return render(request,"deletecourse.html",context)
def savedeletecourse(request):
    if request.method=='POST':
        crname=request.POST.get('cr_name')
        c=Courses.objects.get(id=crname)
        c.delete()
        messages.success(request,"Deleted!")
        return render(request,"deletecourse.html")
    else:
        return render(request,"deletecourse.html")

def deletebatch(request):
    cname=Courses.objects.all()
    btch=Batches.objects.all()
    context={
    'btch':btch,
    'cname':cname
    }
    return render(request,"deletebatch.html",context)
def savedeletebatch(request):
    if request.method=='POST':
        c_name=request.POST.get('crname')
        b_name=request.POST.get('btn')
        c=Batches.objects.get(id=b_name)
        c.delete()
        messages.success(request,"Delete Batch!")
        return render(request,"deletebatch.html")
    else:
        return render(request,"deletebatch.html")

def deletesemester(request):
    if request.method == 'POST':
        selected_course_id = request.POST.get('selcourse')
        selected_semester_id = request.POST.get('selsemester')

        # Perform further processing or database operations with the selected values
        
    else:
        cr = Courses.objects.all()
        sem= Semester.objects.all()
        context = {
            'cr': cr,
            'sem': sem
        }
        return render(request,"deletesemester.html",context)
def savedeletesem(request):
    if request.method=='POST':
        
        b_name=request.POST.get('selsemester')
        c=Semester.objects.get(id=b_name)
        c.delete()
        messages.success(request,"Successfully Deleted Semester")
        return render(request,"deletesemester.html")
    else:
        return render(request,"deletesemester.html")
def deletesubject(request):
    if request.method == 'POST':
        selected_course_id = request.POST.get('selcourse')
        selected_semester_id = request.POST.get('selsem')

        # Perform further processing or database operations with the selected values
        
    else:
        cr = Courses.objects.all()
        sem= Semester.objects.all()
        sub=Subjects.objects.all()
        context = {
            'cr': cr,
            'sem': sem,
            'sub':sub
        }
    return render(request,"deletesubject.html",context)
def savesubdel(request):
    if request.method=='POST':
        
        sname=request.POST.get('selsub')
        c=Subjects.objects.get(id=sname)
        c.delete()
        messages.success(request,"Successfully Deleted Subject")
        return render(request,"deletesubject.html")
        
    else:
        return render(request,"deletesubject.html")


def index_faculty(request):
    lvr=LeaveRequests.objects.select_related('Students','Faculties','Subjects').all()

    return render(request,"indexfaculty.html",{'lvr':lvr})

def upload_attendance(request):
   
    if request.method == 'POST':
        selected_course_id = request.POST.get('selcourse')
        selected_semester_id = request.POST.get('selsemester')
        batch_id = request.POST.get('selbatch')
        studdt=Students.objects.filter(Batches_id=batch_id)
       

        return render(request,"uploadattendance1.html",{'studdt':studdt})
        
    else:
        # facid=request.session['loginfac']
   
        bat=Batches.objects.all()
        st=Students.objects.all()
        cr = Semester.objects.all()
        sem= Subjects.objects.all()
        context = {
        # 'facid':facid,
        'st':st,
        'bat':bat,   
        'cr': cr,
        'sem': sem
        }
        return render(request,"uploadattendance1.html",context)

def batch_students(request):
    if request.method == 'POST':
        batch_id = request.POST.get('selbatch')
        s = Students.objects.filter(batch_id=batch_id)
        return render(request, 'uploadattendance1.html', {'s': s})

    b = Batches.objects.all()
    return render(request, 'uploadattendance1.html', {'b': b})
def save_attendance(request):
    if request.method == 'POST':
        batch_id = request.POST.get('selbatch')
        semester_id = request.POST.get('selsem')
        subject_id = request.POST.get('selsub')
        hour = request.POST.get('selhour')
        date = request.POST.get('seldate')
        facid=request.session['loginfac']

        # Get the list of selected students and their attendance status
        student_list = request.POST.getlist('table_data')
        attendance_status_list = request.POST.getlist('stat')

        # Iterate over the student list and save their attendance
        for student_id, status in zip(student_list, attendance_status_list):
            attendance = Attendance.objects.create(
                Students_id=student_id,
                Faculties_id=facid,  # Assuming you have an authenticated faculty user
                Subjects_id=subject_id,
                Batches_id=batch_id,
                Date=date,
                Hour=hour,
                Status=status
            )
            attendance.save()

        # Optionally, you can add a success message to be displayed in the template
        # messages.success(request, 'Attendance saved successfully.')

        # att=Attendance()
        # att.Batches_id=btid
        # att.Students_id=studid
        # att.Subjects_id=sub
        # att.Faculties_id=facid
        # att.Hour=hour
        # att.Date=attdate
        # att.Status=st
        # # request.session['batchid']=att.Batches_id
        # att.save()
        messages.success(request,"Attendance Marked")
        return render(request,"uploadattendance1.html")
    else:
        return render(request,"uploadattendance1.html",{})
def upload_internalmark(request):
    if request.method == 'POST':
        
        batch_id = request.POST.get('selbatch')
        studdt=request.POST.get('selstudname')
    
    else:
        
        bat=Batches.objects.all()
        st=Students.objects.all()
        facid=request.session['loginfac']
        factsub=FacultySubjects.objects.select_related('Subjects').filter(Faculties_id=facid)
        # cr = Semester.objects.all()
        # sem= Subjects.objects.all()
        context = {
        'factsub':factsub,
        'st':st,
        'bat':bat, 
        'facid':facid
        }
        return render(request,"uploadinternalmark1.html",context)

def saveinteralmark(request):   
    if request.method == 'POST':
        batch_id = request.POST.get('selbatch')
        student_id = request.POST.get('selstudname')
        faculty_subject_id = request.POST.get('selfacsub')
        assignment1_mark = request.POST.get('makasgn1')
        assignment2_mark = request.POST.get('makasgn2')
        series1_mark = request.POST.get('seriesmm')
        series2_mark = request.POST.get('seriesmm2')
        attendance_mark = request.POST.get('inputatt1')
        assgnn1=request.POST.get('asgn1')
        assgnn2=request.POST.get('asgn2')
        seriesn1=request.POST.get('series1')
        seriesn2=request.POST.get('series2')

        student = Students.objects.get(id=student_id)
        faculty_subject = FacultySubjects.objects.get(id=faculty_subject_id)

        # Create AssignmentMarks objects
        assignment1 = AssignmentMarks.objects.create(Students=student, Subjects=faculty_subject.Subjects, AssignmentNo=assgnn1, Marks=assignment1_mark)
        assignment2 = AssignmentMarks.objects.create(Students=student, Subjects=faculty_subject.Subjects, AssignmentNo=assgnn2, Marks=assignment2_mark)

        # Create SeriesExamMarks objects
        series1 = SeriesExamMarks.objects.create(Students=student, Subjects=faculty_subject.Subjects, SeriesExamNo=seriesn1, Marks=series1_mark)
        series2 = SeriesExamMarks.objects.create(Students=student, Subjects=faculty_subject.Subjects, SeriesExamNo=seriesn2, Marks=series2_mark)

        # Create InternalMarks object
        internal_marks = InternalMarks.objects.create(Students=student, FacultySubjects=faculty_subject,
                                                      SeriesExamMarks=series1, AssignmentMarks=assignment1,
                                                      Attendancemarks=attendance_mark, Total=0)
        internal_marks1 = InternalMarks.objects.create(Students=student, FacultySubjects=faculty_subject,
                                                      SeriesExamMarks=series2, AssignmentMarks=assignment2,
                                                      Attendancemarks=attendance_mark, Total=0)

        total_marks = float(assignment1_mark)+float(assignment2_mark)+float(series1_mark)+float(series2_mark)+int(attendance_mark)
        internal_marks.Total = total_marks
        internal_marks.save()
        internal_marks1.Total=total_marks
        internal_marks1.save()
        messages.success(request,"Intermark Uploaded")
        return render(request,"uploadinternalmark1.html")
    else:
        return render(request,"uploadinternalmark1.html",{})

def dutymed_leave(request):
    # lvapprove = LeaveRequests.objects.select_related('Students','Faculties','Subjects').all()
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('status_'):
                leave_id = key.split('_')[1]
                status = value
                leave_request = LeaveRequests.objects.get(id=leave_id)
                leave_request.Fac_approval = status
                leave_request.save()

    lvr=LeaveRequests.objects.select_related('Students','Faculties','Subjects').filter(Adv_approval=1)
    return render(request,"dutymedleave1.html",{'lvr':lvr})

def contact1(request):
    return render(request,"contact1.html",{})

def indexes(request):
    # st=request.session['loginstu']
    # lev=LeaveRequests.objects.select_related('Subjects').filter(id=st).all()
    # internal_marks = InternalMarks.objects.filter(Students_id=st)
   
    # context={
    # 'lev':lev,
    # 'internal_marks':internal_marks,
    # }
    return render(request,"index.html")

def edit(request):
    stud1=request.session['loginstu']
    stud = Students.objects.get(id=stud1)
    context = {
        'stud':stud
    }
    return render(request,"editpersonaldetails.html",context)

def edit_personaldetails(request):
    if request.method == 'POST':
        stud1=request.session['loginstu']
        # student session
        # stuname1 = request.POST.get('stuname')
        # stuuser1 = request.POST.get('stuuser')
        # stupassword1 = request.POST.get('stupassword')
        # stuadmn1 = request.POST.get('stuadmn')
        # stuktu1 = request.POST.get('stuktu')
        # stuyofadmn1 = request.POST.get('stuyofadmn')
        # batchid = request.POST.get('selbatch')
        rollno = request.POST.get('sturoll')
        religion = request.POST.get('stureligion')
        category = request.POST.get('stucat')
        gender = request.POST.get('stugen')
        dob = request.POST.get('studob')
        phone = request.POST.get('stuphone')
        pmail = request.POST.get('stumail')
        rmail = request.POST.get('sturitmail')
        address = request.POST.get('stuadd')
        nationality = request.POST.get('stunation')
        bloodgroup = request.POST.get('stublood')
        aadhar = request.POST.get('stuaadhar')
        status = request.POST.get('stustatus')
        guardianname = request.POST.get('stugname')
        guardianphone = request.POST.get('stugphone')

        objstudent = Students.objects.get(id = stud1)
        objstudent.Rollno = rollno
        objstudent.Religion = religion
        objstudent.Category = category
        objstudent.Gender = gender
        objstudent.Dob = dob
        objstudent.Address = address
        objstudent.Nationality = nationality
        objstudent.Aadharno = aadhar
        objstudent.Personalmail = pmail
        objstudent.RITmail =rmail
        objstudent.PhoneNumber = phone
        objstudent.Blood_group = bloodgroup
        objstudent.Status = status
        objstudent.Guardian_name = guardianname
        objstudent.Guardian_contact_no = guardianphone
        objstudent.save()

    return render(request,"editpersonaldetails.html",{})


def view_personaldetails(request):
    stud1=request.session['loginstu']
    stud = Students.objects.get(id=stud1)
    context = {
        'stud':stud
    }
    return render(request,"viewpersonaldetails.html",context)

def internalmark(request):
    stid=request.session['loginstu']
    stud = Students.objects.get(id=stid)
    stbatch_id = stud.Batches_id
    sub=FacultySubjects.objects.select_related('Subjects').filter(Batches_id=stbatch_id)
    # internal=InternalMarks.objects.select_related('Students','AssignmentMarks','SeriesExamMarks').filter(Students_id=stid)
    # internalassign=InternalMarks.objects.select_related('AssignmentMarks')filter(Students_id=stid)
    # interalseries=InternalMarks.objects.select_related('SeriesExamMarks')filter(Students_id=stid)
    


    context={
    # 'internal':internal,
   'sub':sub,
    }
    return render(request,"viewinternalmark.html",context)


def studinternalv(request):
    if request.method=='POST':
        stid=request.session['loginstu']

        sb=request.POST.get('inputsubject')
        sbname = FacultySubjects.objects.get(id=sb)
        stbatch_id = sbname.Subjects_id
        assgn=AssignmentMarks.objects.filter(Students_id=stid,Subjects=stbatch_id)
        seri=SeriesExamMarks.objects.filter(Students_id=stid,Subjects=stbatch_id)
        internal = InternalMarks.objects.select_related('FacultySubjects').filter(Students_id=stid,FacultySubjects_id=sb).values('Attendancemarks','Total').distinct()  
        itrn = InternalMarks.objects.filter(Students_id=stid).distinct()
        
        context={
        'stbatch_id':stbatch_id,
        'internal':internal,
        'sb':sb,
        'assgn':assgn,
        'seri':seri,
        'itrn':itrn
        }
        return render(request,"studinternalmview.html",context)

def attendance(request):

    stud1=request.session['loginstu']
    st=Students.objects.get(id=stud1)
    stbtachid=st.Batches_id
    stsub=FacultySubjects.objects.select_related('Subjects').filter(Batches_id=stbtachid)
    studd=Attendance.objects.select_related('Students','Subjects').filter(Students_id=stud1)
    context={
    'stbtachid':stbtachid,
    'stsub':stsub,
    }
    return render(request,"viewattendance.html",context)
from django.db.models import Sum

def  attendancesubdt(request):
   
    if request.method=='POST':
        stud1=request.session['loginstu']
        selected_subject_id=request.POST.get('inputsubject')
        selected_subject = Subjects.objects.get(id=selected_subject_id)
        total_hours_presented = Attendance.objects.filter(Subjects=selected_subject, Students=stud1).aggregate(Sum('Hour'))['Hour__sum']

        total_hours = Attendance.objects.filter(Subjects=selected_subject, Students=stud1).count()

        total_subject_hours = Attendance.objects.filter(Subjects=selected_subject).aggregate(Sum('Hour'))['Hour__sum']

        attendance_percentage = (total_hours_presented / total_subject_hours) * 100 if total_subject_hours else 0
        studd=Attendance.objects.select_related('Students','Subjects').filter(Students_id=stud1)
    context = {
        'studd':studd,
        'total_subject_hours':total_subject_hours,
        'total_hours_presented': total_hours_presented,
        'attendance_percentage': attendance_percentage
    }
    
    return render(request,"attendancesubsel.html",context)
def duty_leave(request):
    if request.method == 'POST':
        selected_sub_id = request.POST.get('selsubject')
        selected_semester_id = request.POST.get('selsem')

        # Perform further processing or database operations with the selected values
        
    else:
        sub = Subjects.objects.all()
        sem= Semester.objects.all()
        stud1=request.session['loginstu']
        st = Students.objects.get(id=stud1)
        stbatch_id = st.Batches_id
        fac=FacultySubjects.objects.select_related('Faculties').all()
        # btid=Students.objects.get()
        # fac=FacultySubjects.objects.select_related('Faculties','Subjects').filter(Batches_id=stbatch_id)
        context = {
        'fac':fac,
        'sub': sub,
        'sem': sem
        }
        return render(request,"dutyleave.html",context)
    # if request.method == 'POST':
    #     stulogin = request.session['stu']

    #     leave = request.POST.get('reqdutyleave')
    #     subjectname = request.POST.get('selsubject')
    #     facname = request.POST.get('selfacname')
    #     date = request.POST.get('seldate')
    #     hour = request.POST.get('selhour')
    #     reason1 = request.POST.get('reason')
    #     leavefile = request.FILES['DL_upload']
        
    #     objleave = LeaveRequests()
    #     objleave.LeaveType = leave
    #     objleave.Subjects_id = subjectname
    #     objleave.Faculties_id = facname
    #     objleave.Date = date
    #     objleave.Hour = hour
    #     objleave.Reason = reason1
    #     objleave.DL_upload = leavefile
    #     objleave.save()
    # stulogin = request.session['stu']
    # student = Students.objects.get(id=stulogin)
    # sub=FacultySubjects.objects.get(Batches_id=student.Batches_id)
    
    # subb=Subjects.objects.get(id=sub.Subjects_id)

    # # batch = student.Batches_id
    # # subjects=FacultySubjects.objects.filter(Batches_id=batch)
    #     # faculties=FacultySubjects.objects.filter(Batches_id=batch)
    # context = {
    #         # 'subjects':subjects,
    #         'student':student,
    #         'sub':sub,
    #         'subb':subb
    #         # 'faculties':faculties
    # }
    # return render(request,"dutyleave.html",context)
    # else:
    
def saveleave(request):
    if request.method == 'POST':
        stulogin = request.session['loginstu']

        leave = request.POST.get('reqdutyleave')
        subjectname = request.POST.get('selsubject')
        facname = request.POST.get('selfacname')
        date = request.POST.get('seldate')
        hour = request.POST.get('selhour')
        reason1 = request.POST.get('reason')
        leavefile = request.FILES['certificates']
        # 
        objleave = LeaveRequests()
        objleave.Students_id=stulogin
        objleave.LeaveType = leave
        objleave.Subjects_id = subjectname
        objleave.Faculties_id = facname
        objleave.Date = date
        objleave.Hour = hour
        objleave.Reason = reason1
        objleave.DL_upload = leavefile
        objleave.save()
        messages.success(request,"Leave Request Submited")
        return render(request,"dutyleave.html",{})
    return render(request,"dutyleave.html",{})
def update_status(request):
    if request.method == 'POST':
        selected_status = request.POST.get('status')
        LeaveRequests.objects.update(Adv_approval=selected_status)
        messages.success(request,"Leave Request Updated")
        return render(request,"dutyleave.html") 
    
def upload_gradecard(request):
    # stulogin = request.session['loginstu']
    sm=Semester.objects.all()

    return render(request,"uploadgradecard.html",{'sm':sm})
from django.db import transaction
def process_pdf(request):
    if request.method == 'POST' and 'pdf_file' in request.FILES:
        pdf_file = request.FILES['pdf_file']
        pdf = PdfReader(pdf_file)

        # Extract relevant information from the PDF
        page = pdf.pages[0]
        text = page.extract_text()
        candidate_name = text.split('Name of Candidate')[1].split('Register No')[0].strip()
        register_no = text.split('Register No')[1].split('Name of College')[0].strip()
        college_name = text.split('Name of College')[1].split('Branch')[0].strip()
        branch = text.split('Branch')[1].split('Semester')[0].strip()
        semester = text.split('Branch')[1].split('Program')[0].strip()
        s = semester.split('Semester')[1].split('Program')[0].strip()
        program = text.split('Program')[1].split('Course Name')[0].strip()
        tot = text.split('Total Earned Credits')[1].split('SGPA')[0].strip()
        sgpa = text.split('SGPA')[1].split()[-31].strip()
        
        course_rows = text.split('\n')[12:-3]  # Exclude the header and footer

        coursename = ""
        code = ""
        grade = ""
        credits = ""
        exam_date = ""
        # code_count = 0  # Counter for the number of codes found
        for row in course_rows:
            row_data = row.split()

            # Check if the row has enough elements
            if len(row_data) >= 4:
               
                code = row_data[-4]
                grade = row_data[-3]
                credits = row_data[-2]
                exam_date = row_data[-1]

                # Create a new pdfconvert instance and save it
                result = pdfconvert(
                    name_candidate=candidate_name,
                    regno=register_no,
                    clgname=college_name,
                    branch=branch,
                    sem=s,
                    pgm=program,
                    # coursname=course_rows,
                    code=code,
                    grade=grade,
                    credits=credits,
                    mnthyearofexam=exam_date,
                    totcrd=int(tot),
                    sgpa=float(sgpa)
                    # Assign values to other fields as necessary
                )
                result.save()

                # code_count += 1

        return render(request, 'uploadgradecard.html')
    else:
        return render(request, 'uploadgradecard.html')


# def result(request):
#     data = []

#     # Fetch all pdfconvert objects from the database
#     pdfconvert_objects = pdfconvert.objects.all()

#     # Extract the required fields and append to the data list
#     for obj in pdfconvert_objects:
#         name = obj.name_candidate
#         reg = obj.regno
#         bnch = obj.branch
#         code = obj.code
#         grade = obj.grade
#         credits = obj.credits
#         total = obj.totcrd
#         sg = obj.sgpa

#         if len(code) >= 5 and len(grade) == 1 and grade.isalpha():
#             try:
#                 float_credits = float(credits)
#                 extracted_code = code[-6:]
#                 data.append({
#                     'name': name,
#                     'reg':reg,
#                     'bnch':bnch,
#                     'extracted_code': extracted_code,
#                     'grade': grade,
#                     'credits': credits,
#                     'total':total,
#                     'sg':sg

#                 })
#             except ValueError:
#                 pass

#     context = {
#         'data': data
#     }
   
#     return render(request,"result.html",context) 
#     # ithum athupole cheyane

def result(request):
    return render(request, "result.html")



   
def resultview(request):
    if request.method == 'POST':
        semester = request.POST.get('semno')
        student_data = pdfconvert.objects.filter(sem=semester)
        code_values = set([obj.code for obj in student_data if len(obj.code) >= 6 and obj.code[-3:].isdigit() and obj.code[-6:-3].isalpha()])
        student_data_list = []
        code_suffix = ""
        
        for code in code_values:
            students = student_data.filter(code=code)
            if len(code) >= 6 and code[-3:].isdigit() and code[-6:-3].isalpha():
                code_suffix = code[-6:]  # Split the last 6 characters

            student_data_dict = {
                'code': code_suffix,
                'students': students.values('regno', 'name_candidate', 'grade', 'sgpa')
            }
            student_data_list.append(student_data_dict)

        context = {
           'code_values':code_values,
            'semester': semester,
            'student_data': student_data_list
        }

        return render(request, 'resultanalysis.html', context)

    return render(request, 'resultanalysis.html')

def indexadvisor(request):
    advisor_id=request.session['loginadvisor']
    advisor = Advisors.objects.get(id=advisor_id)
    batch_id = advisor.Batches_id

    leave = LeaveRequests.objects.filter(Students__Batches=batch_id).distinct() 
    # Count the number of students in the advisor's batch
    students_count = Students.objects.filter(Batches_id=batch_id).count()

    context ={'students_count': students_count,
    'leave':leave
    }
    return render(request,"indexadvisor.html",context)

def advisorpdview(request):
    # if request.method=='POST':
        # stname=request.POST.get('selstudent')
        # advid=request.session['loginadvisor']
        # advisor = get_object_or_404(Advisors, id=advid)
        # batch = advisor.Batches
        # stud = Students.objects.filter(Batches=batch,Name=stname)
        # context={
            # 'stud':stud
        # }
    # facid=request.session['fac']
    # stud=Students.objects.filter()
    # context={
    # 'facid':facid
    # }
    # if request.method == 'POST':
    #     student1 = request.POST.get('selstudent')
    #     stud1=request.session['stu']
    #     stud = Students.objects.get(id=student1)
    #     context = {
    #         'stud':stud
    #     }
    #     return render(request,"advisorpdview.html",context)
    # else:
    return render(request,"advisorpdview.html")

def viewpersonalinfo(request):
    if request.method=='POST':
         stname=request.POST.get('selstudent')
         advid=request.session['loginadvisor']

         advisor = get_object_or_404(Advisors, id=advid)

    # Retrieve the batch for the advisor
         batch = advisor.Batches

    # Retrieve the student details for the batch
         studd= Students.objects.filter(Batches=batch,Name=stname)
         # studd=Students.objects.all()
         context={
            'studd':studd
            }
         return render(request,"viewpersonalinfo.html",context)


def advisorviewstudperdt(request):
    advid=request.session['loginadvisor']
    # advbt=Advisors.objects.filter()
    # Retrieve the advisor instance
    advisor = get_object_or_404(Advisors, id=advid)

    # Retrieve the batch for the advisor
    batch = advisor.Batches
    student_details = StudentDetails.objects.filter(Batches=batch)
def adviewinternalmark(request):
    if request.method == 'POST':
        sub_id = request.POST.get('inputsubject')
        advisor_id = request.session['loginadvisor']
        advisor = get_object_or_404(Advisors, id=advisor_id)
        batch_id = advisor.Batches_id
        students = Students.objects.filter(Batches_id=batch_id)
        internal_marks = InternalMarks.objects.filter(Students__Batches=batch_id, FacultySubjects__Subjects__id=sub_id)

        context = {
            'sub_id': sub_id,
            'students': students,
            'internal_marks': internal_marks
        }
        return render(request, "tableadviewinternmark.html", context)

    else:
        advid = request.session['loginadvisor']
        advisor = get_object_or_404(Advisors, id=advid)
        batch = advisor.Batches
        subjects = FacultySubjects.objects.filter(Batches=batch).select_related('Subjects').values('Subjects__id', 'Subjects__Subject_name').distinct()

        context = {
            'subjects': subjects
        }
        return render(request, "adviewinternalmark.html", context)
    # if request.method == 'POST':
    #     advid=request.session['loginadvisor']
    #     advisor = get_object_or_404(Advisors, id=advid)

    #     batch = advisor.Batches
    #     facsub=FacultySubjects.objects.select_related('Batches','Students','Subjects').filter(Batches_id=batch)
    #     context={
    #     # 'batch':batch,
    #     'advid':advid,
    #     'facsub':facsub
    #     }
    #     return render(request,"adviewinternalmark.html",context)

    # else:
    #     advid=request.session['loginadvisor']
    #     advisor = get_object_or_404(Advisors, id=advid)
    #     batch = advisor.Batches
    #     facsub=FacultySubjects.objects.select_related('Batches','Subjects').filter(Batches_id=batch)

    #     att= InternalMarks.objects.select_related('Students').all()
    #     sub=Subjects.objects.all()
    #     context={
    #     'facsub':facsub,

    #     'sub':sub,
    #     'att':att
    #     }

        # return render(request,"adviewinternalmark.html")
def adviewsub(request):
    if request.method == 'POST':
        sub_id = request.POST.get('inputsubject')
        advisor_id = request.session['loginadvisor']
        advisor = get_object_or_404(Advisors, id=advisor_id)
        batch_id = advisor.Batches_id
        students = Students.objects.filter(Batches_id=batch_id)
        internal_marks = InternalMarks.objects.filter(Students__Batches=batch_id, FacultySubjects__Subjects_id=sub_id)

        context = {
            'sub_id': sub_id,
            'students': students,
            'internal_marks': internal_marks
        }
        return render(request, "tableadviewinternmark.html", context)

    else:
        advid = request.session['loginadvisor']
        advisor = get_object_or_404(Advisors, id=advid)
        batch = advisor.Batches
        sub = FacultySubjects.objects.select_related('Subjects').filter(Batches_id=batch).distinct()

        context = {
            'sub': sub
        }
        return render(request, "adviewinternalmark.html", context)
        # return render(request,"tableadviewinternmark.html",context)
    
def viewinternalstudad(request):

    if request.method == 'POST':
        selected_course_id = request.POST.get('selcourse')
        selected_semester_id = request.POST.get('selsemester')
        batch_id = request.POST.get('sub')
        studdt=Students.objects.filter(Batches_id=batch_id)
       

        return render(request,"adviewinternalmark.html",{'studdt':studdt})
        
    else:
        att= InternalMarks.objects.select_related('Students','Subjects').all()
        context = {
       
        'att': att
        }
        return render(request,"adviewinternalmark.html",context)

def attendance(request):

    stud1=request.session['loginstu']
    st=Students.objects.get(id=stud1)
    stbtachid=st.Batches_id
    stsub=FacultySubjects.objects.select_related('Subjects').filter(Batches_id=stbtachid)
    studd=Attendance.objects.select_related('Students','Subjects').filter(Students_id=stud1)
    context={
    'stbtachid':stbtachid,
    'stsub':stsub,
    }
    return render(request,"viewattendance.html",context)
from django.db.models import Sum

def  attendancesubdt(request):
   
    if request.method=='POST':
        stud1=request.session['loginstu']
        selected_subject_id=request.POST.get('inputsubject')
        selected_subject = Subjects.objects.get(id=selected_subject_id)
        total_hours_presented = Attendance.objects.filter(Subjects=selected_subject, Students=stud1).aggregate(Sum('Hour'))['Hour__sum']

        total_hours = Attendance.objects.filter(Subjects=selected_subject, Students=stud1).count()

        total_subject_hours = Attendance.objects.filter(Subjects=selected_subject).aggregate(Sum('Hour'))['Hour__sum']

        attendance_percentage = (total_hours_presented / total_subject_hours) * 100 if total_subject_hours else 0
        studd=Attendance.objects.select_related('Students','Subjects').filter(Students_id=stud1)
    context = {
        'studd':studd,
        'total_subject_hours':total_subject_hours,
        'total_hours_presented': total_hours_presented,
        'attendance_percentage': attendance_percentage
    }
    
    return render(request,"attendancesubsel.html",context)

def adviewattendance(request):
    advisor_id = request.session['loginadvisor']
    advisor = get_object_or_404(Advisors, id=advisor_id)
    batch_id = advisor.Batches_id
    stsub=FacultySubjects.objects.select_related('Subjects').filter(Batches_id=batch_id)
    context={
    'stsub':stsub,
    }
    # students = Students.objects.all()
    # attendance_data = Attendance.objects.values('Students').annotate(
    #     total_hour=Sum('Hour'),
    #     present_hour=Sum(Case(When(Status='P', then=Value(F('Hour'))), default=Value(0), output_field=FloatField()))
    # ).order_by('Students')

    # for student in students:
    #     attendance = attendance_data.filter(Students=student.id).first()
    #     if attendance:
    #         student.total_hour = attendance['total_hour']
    #         student.present_hour = attendance['present_hour']
    #         student.percentage = (attendance['present_hour'] / attendance['total_hour']) * 100
            # student.subject_name = Subjects.objects.get(id=attendance['Subjects_id']).name

    # for student in students:
        # attendance = attendance_data.filter(Students=student.id).first()
        # if attendance:
            # student.total_hour = attendance['total_hour']
            # student.present_hour = attendance['present_hour']
            # student.percentage = (attendance['present_hour'] / attendance['total_hour']) * 100
    return render(request,"adviewattendance.html",context)
def stdtadvattendance(request):
    if request.method=='POST':
        advisor_id = request.session['loginadvisor']
        advisor = get_object_or_404(Advisors, id=advisor_id)
        batch_id = advisor.Batches_id
        students = Students.objects.filter(Batches_id=batch_id)
        selected_subject_id=request.POST.get('inputsubject')
        selected_subject = Subjects.objects.get(id=selected_subject_id)
        total_hours_presented = Attendance.objects.filter(Subjects=selected_subject, Students__in=students).aggregate(Sum('Hour'))['Hour__sum']

        total_hours = Attendance.objects.filter(Subjects=selected_subject,Students__in=students,).count()

        total_subject_hours = Attendance.objects.filter(Subjects=selected_subject).aggregate(Sum('Hour'))['Hour__sum']

        attendance_percentage = (total_hours_presented / total_subject_hours) * 100 if total_subject_hours else 0
        studd=Attendance.objects.select_related('Students','Subjects').filter(Students__in=students)
    context = {
        'studd':studd,
        'total_subject_hours':total_subject_hours,
        'total_hours_presented': total_hours_presented,
        'attendance_percentage': attendance_percentage
    }
    
    return render(request,"tbadvisorattendance.html",context)

def leaveapproval(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('status_'):
                leave_id = key.split('_')[1]
                status = value
                leave_request = LeaveRequests.objects.get(id=leave_id)
                leave_request.Adv_approval = status
                leave_request.save()
        # leave_ids = request.POST.get('leave_id')  # Get the selected leave request IDs
        # status = request.POST.get('status')  # Get the selected status (Approved or Rejected)
        # if status == "Approved":
            # status = True
        # elif status == "Rejected":
            # status = False

        # Update the status of the selected leave requests
        # LeaveRequests.objects.filter(id=leave_ids).update(Adv_approval=status)
     # Update the status of the selected leave requests
        # LeaveRequests.objects.filter(id__in=leave_ids).update(Adv_approval=status)
      # advbt=Advisors.objects.filter()
    # Retrieve the advisor instance
    advid=request.session['loginadvisor']
  
    advisor = get_object_or_404(Advisors, id=advid)

   
    batch = advisor.Batches
    lvapprove = LeaveRequests.objects.select_related('Students','Faculties','Subjects').all()
    return render(request,"leaveapproval.html",{'lvapprove':lvapprove})

def resultanalysis(request):
    return render(request,"resultanalysis.html",{})

def reportgeneration(request):
    return render(request,"reportgeneration.html",{})
def studcount(request):
    stud=Students.objects.select_related('Batches')
    context={
    'stud':stud
    }


# Create your views here.
def view_uploaded_pdf(request, pdf_filename):
    # Construct the file path to the uploaded PDF file
    file_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)

    # Check if the file exists
    if os.path.exists(file_path):
        # Open the file in binary mode
        with open(file_path, 'rb') as pdf_file:
            # Set the appropriate response headers for PDF content
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{pdf_filename}"'
            return response
    else:
        # Return a 404 response if the file does not exist
        return HttpResponse("PDF file not found.", status=404)
def update_status(request):
    if request.method == 'POST':
        leave_ids = request.POST.getlist('leave_id')  # Get the selected leave request IDs
        status = request.POST.get('status')  # Get the selected status (Approved or Rejected)

        # Update the status of the selected leave requests
        for leave_id in leave_ids:
            leave_request = LeaveRequest.objects.get(id=leave_id)
            leave_request.status = status
            leave_request.save()
            return redirect('leaveapproval')
    return render(request,"leaveapproval.html",{})


# def selassign_subject(request):
#     if request.method == 'POST':
#         # Get the selected students' IDs
#         student_ids = request.POST.getlist('students')

#         # Get the selected elective ID
#         elective_id = request.POST.get('elective_id')

#         # Assign the elective to the selected students
#         for student_id in student_ids:
#             elective_choice = ElectiveChoices(Students_id=student_id, Electives_id=elective_id)
#             elective_choice.save()

#         # Redirect to a success page or perform further actions
#         # ...

#     # Get all students
#     students = Students.objects.all()

#     # Get the IDs of students with elective assignments
#     students_with_elective_ids = ElectiveChoices.objects.values_list('Students_id', flat=True)

#     # Exclude students with elective assignments from the list
#     students_without_elective = students.exclude(id__in=students_with_elective_ids)

#     # Get all available electives
#     electives = Electives.objects.all()

#     context = {
#         'students': students,
#         'electives': electives,
#         'students_without_elective': students_without_elective,
#     }
#     return render(request, 'success.html', context)
    # return render(request, 'success.html', context)

def selassign_subject(request):
    if request.method == 'POST':
        elective_id = request.POST.get('elective_id')
        student_ids = request.POST.getlist('students')
        
       
        elective = Electives.objects.get(pk=elective_id)
        students = Students.objects.filter(pk__in=student_ids)
        
        for student in students:
            ElectiveChoices.objects.create(Students=student, Electives=elective)
        
     
        
        return render(request, 'success.html')
    else:
        student_ids = request.POST.getlist('students')
        unassigned_students = Students.objects.exclude(
            id__in=ElectiveChoices.objects.values_list('Students_id', flat=True)
        )
       
        electives = Electives.objects.all()
        
        context = {
            'electives': electives,
            'unassigned_students': unassigned_students,
        }
        
        return render(request, 'success.html', context)

def facviewinternalmark(request):
   
    if request.method == 'POST':
        selected_course_id = request.POST.get('selcourse')
        selected_semester_id = request.POST.get('selsemester')
        batch_id = request.POST.get('selbatch')
        studdt=Students.objects.filter(Batches_id=batch_id)
       

        return render(request,"facviewattendance.html",{'studdt':studdt})
        
    else:
        # facid=request.session['loginfac']
   
        bat=Batches.objects.all()
        st=Students.objects.all()
        cr = Semester.objects.all()
        sem= Subjects.objects.all()
        context = {
        # 'facid':facid,
        'st':st,
        'bat':bat,   
        'cr': cr,
        'sem': sem
        }
        return render(request,"facviewattendance.html",context)

def facviewsub(request):
    if request.method == 'POST':
        sub_id = request.POST.get('inputsubject')
        facid=request.session['loginfac']
        factsub=FacultySubjects.objects.select_related('Subjects').filter(Faculties_id=facid)
        batch_id = request.POST.get('selbatch')
        students = Students.objects.filter(Batches_id=batch_id)
        internal_marks = InternalMarks.objects.filter(Students__Batches=batch_id, FacultySubjects__Subjects_id=sub_id)

        context = {
            'facsub':facsub,
            'sub_id': sub_id,
            'students': students,
            'internal_marks': internal_marks
        }
        return render(request, "tablefacviewinternmark.html", context)

    else:
        facid=request.session['loginfac']
        batch = advisor.Batches
        sub = FacultySubjects.objects.select_related('Subjects').filter(Batches_id=batch).distinct()

        context = {
            'sub': sub
        }
        return render(request, "facviewinternalmark.html", context)
        # return render(request,"tableadviewinternmark.html",context)


def facviewattendance(request):
   
    if request.method == 'POST':
        selected_course_id = request.POST.get('selcourse')
        selected_semester_id = request.POST.get('selsemester')
        batch_id = request.POST.get('selbatch')
        studdt=Students.objects.filter(Batches_id=batch_id)
       

        return render(request,"facviewattendance.html",{'studdt':studdt})
        
    else:
        # facid=request.session['loginfac']
   
        bat=Batches.objects.all()
        st=Students.objects.all()
        cr = Semester.objects.all()
        sem= Subjects.objects.all()
        context = {
        # 'facid':facid,
        'st':st,
        'bat':bat,   
        'cr': cr,
        'sem': sem
        }
        return render(request,"facviewattendance.html",context)

def stdtfacattendance(request):
    if request.method=='POST':
        facid=request.session['loginfac']
        factsub=FacultySubjects.objects.select_related('Subjects').filter(Faculties_id=facid)
        batch_id = request.POST.get('selbatch')
        students = Students.objects.filter(Batches_id=batch_id)
        selected_subject_id=request.POST.get('inputsubject')
        selected_subject = Subjects.objects.get(id=selected_subject_id)
        total_hours_presented = Attendance.objects.filter(Subjects=selected_subject, Students__in=students).aggregate(Sum('Hour'))['Hour__sum']

        total_hours = Attendance.objects.filter(Subjects=selected_subject,Students__in=students,).count()

        total_subject_hours = Attendance.objects.filter(Subjects=selected_subject).aggregate(Sum('Hour'))['Hour__sum']

        attendance_percentage = (total_hours_presented / total_subject_hours) * 100 if total_subject_hours else 0
        studd=Attendance.objects.select_related('Students','Subjects').filter(Students__in=students)
    context = {
        'facsub':facsub,
        'studd':studd,
        'total_subject_hours':total_subject_hours,
        'total_hours_presented': total_hours_presented,
        'attendance_percentage': attendance_percentage
    }
    
    return render(request,"tbfacattendance.html",context)


# import PyPDF2

# def extract_pdf_data(pdf_file_path):
#     with open(pdf_file_path, 'rb') as f:
#         reader = PyPDF2.PdfFileReader(f)
#         page = reader.getPage(0)

#         # Extract values from the first table
#         name_candidate = page.extract_text().split("Name of Candidate")[1].strip()
#         regno = page.extract_text().split("Register No")[1].strip()
#         clgname = page.extract_text().split("Name of College")[1].strip()
#         branch = page.extract_text().split("Branch")[1].strip()
#         sem = page.extract_text().split("Semester")[1].strip()
#         pgm = page.extract_text().split("Program")[1].strip()

#         # Create an instance of PdfConvert and save the extracted values
#         pdf_obj = PdfConvert.objects.create(
#             name_candidate=name_candidate,
#             regno=regno,
#             clgname=clgname,
#             branch=branch,
#             sem=sem,
#             pgm=pgm
#         )

#         # Extract values from the second table
#         course_table = page.extract_text().split("Course Name Code Grade Credits Month & Year of Examination")[1]
#         course_rows = course_table.strip().split('\n')

#         for row in course_rows:
#             values = row.split()
#             coursname = ' '.join(values[:-4])
#             code = values[-4]
#             grade = values[-3]
#             credits = values[-2]
#             mnthyearofexam = values[-1]

#             # Create an instance of PdfConvert for each course and save the values
#             PdfConvert.objects.create(
#                 name_candidate=name_candidate,
#                 regno=regno,
#                 clgname=clgname,
#                 branch=branch,
#                 sem=sem,
#                 pgm=pgm,
#                 coursname=coursname,
#                 code=code,
#                 grade=grade,
#                 credits=credits,
#                 mnthyearofexam=mnthyearofexam
#             )

#         # Extract Total Earned Credits and SGPA
#         total_earned_credits = page.extract_text().split("Total Earned Credits")[-1].strip()
#         sgpa = page.extract_text().split
# from django.shortcuts import render
# import os

# def upload_pdf(request):
#     if request.method == 'POST':
#         pdf_file = request.FILES['pdf_file']
#         upload_dir = 'path/to/your/directory/uploads/'
#         pdf_file_path = os.path.join(upload_dir, pdf_file.name)

#         with open(pdf_file_path, 'wb') as f:
#             f.write(pdf_file.read())

#         # Call the function to extract data from the PDF
#         extract_pdf_data(pdf_file_path)

#         success_message = "PDF uploaded and processed successfully."

#         return render(request, 'upload_pdf.html', {'success_message': success_message})

#     return render(request, 'upload_pdf.html')