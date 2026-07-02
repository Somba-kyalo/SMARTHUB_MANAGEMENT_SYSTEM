from django.db import models
from django.contrib.auth.hashers import make_password


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)

    dob = models.DateField()
    gender = models.CharField(max_length=20)

    nationality = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    address = models.TextField()
    county = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    course = models.CharField(max_length=100)

    admission_number = models.CharField(max_length=50)

    year_of_study = models.CharField(max_length=20)
    study_mode = models.CharField(max_length=20)

    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=20)

    personal_email = models.EmailField()

    institution_email = models.EmailField(unique=True)

    username = models.CharField(max_length=100, unique=True)

    profile_photo = models.ImageField(
        upload_to='students/',
        blank=True,
        null=True
    )

    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class Unit(models.Model):
    unit_code = models.CharField(max_length=20)
    unit_name = models.CharField(max_length=200)
    course = models.CharField(max_length=100)
    year = models.CharField(max_length=20)
    semester = models.CharField(max_length=20)
    credit_hours = models.IntegerField()

    def __str__(self):
        return f"{self.unit_code} - {self.unit_name}"


class UnitRegistration(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE
    )

    registered_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student} - {self.unit}"
    



class Result(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE
    )

    cat = models.FloatField()
    exam = models.FloatField()

    total = models.FloatField(
        blank=True,
        null=True
    )

    grade = models.CharField(
        max_length=2,
        blank=True
    )

    remark = models.CharField(
        max_length=100,
        blank=True
    )

    semester = models.CharField(max_length=20)

    def save(self, *args, **kwargs):

        self.total = self.cat + self.exam

        if self.total <= 39:
            self.grade = "F"
            self.remark = "Supplementary Required"

        elif self.total <= 59:
            self.grade = "C"
            self.remark = "Average Performance"

        elif self.total <= 69:
            self.grade = "B"
            self.remark = "Good Performance"

        else:
            self.grade = "A"
            self.remark = "Excellent Performance"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.unit}"
    



class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Candidate(models.Model):
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE
    )

    position = models.CharField(max_length=100)

    student_name = models.CharField(max_length=200)

    manifesto = models.TextField()

    photo = models.ImageField(
        upload_to='candidates/',
        blank=True,
        null=True
    )

    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.student_name
    


class Vote(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )

    voted_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('student', 'candidate')


class Announcement(models.Model):
    title = models.CharField(max_length=200)

    message = models.TextField()

    posted_by = models.CharField(
        max_length=100,
        default="Administration"
    )

    important = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Lecturer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Venue(models.Model):
    name = models.CharField(max_length=100)
    building = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Timetable(models.Model):

    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE
    )

    lecturer = models.ForeignKey(
        Lecturer,
        on_delete=models.CASCADE
    )

    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE
    )

    day = models.CharField(
        max_length=20
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    semester = models.CharField(
        max_length=20
    )

    def __str__(self):
        return f"{self.unit} - {self.day}"
    

class Fee(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    total_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    semester = models.CharField(
        max_length=20
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        self.balance = (
            self.total_fee -
            self.amount_paid
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.student)
    

class LecturerEvaluation(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    lecturer_name = models.CharField(max_length=200)

    unit_code = models.CharField(max_length=20)

    teaching_rating = models.CharField(max_length=20)

    communication_rating = models.CharField(max_length=20)

    punctuality_rating = models.CharField(max_length=20)

    remarks = models.TextField()

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student} - {self.lecturer_name}"