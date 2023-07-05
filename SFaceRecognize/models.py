from django.db import models
from student.models import CustomUser, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, \
    LeaveReportStudent, FeedBackStudent, StudentResult


# Create your models here.
class Detected(models.Model):
    std_id = models.ForeignKey(Students, on_delete=models.CASCADE, null=True)
    time_stamp = models.DateTimeField()
    photo = models.ImageField(upload_to='detected/', default='SFaceRecognize/FRStream/detected/opencv_frame_0.png')

    def __str__(self):
        stdd = Students.objects.get(id=self.std_id.id)
        return f"{stdd.admin.username} {self.time_stamp}"

    def ImageUrl(self):
        if self.photo:
            return self.photo.url
        else:
            return ""
