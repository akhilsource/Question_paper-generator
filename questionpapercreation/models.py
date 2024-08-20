from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Users(models.Model):
    UserID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)
    Role = models.CharField(max_length=50)

class Categories(models.Model):
    CategoryID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)

class Subjects(models.Model):
    SubjectID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)

class BloomsTaxonomy(models.Model):
    TaxonomyID = models.CharField(max_length=2, primary_key=True)
    LevelName = models.CharField(max_length=50, unique=True)

class QuestionPapers(models.Model):
    QuestionPaperID = models.AutoField(primary_key=True)
    
    PaperName = models.CharField(max_length=255)
    PaperCode = models.CharField(max_length=255)  # Add this field
    ExamDate = models.DateField()  # Add this field
    ExamTime = models.TimeField()  # Add this field
    Department = models.CharField(max_length=255, null=False)  # Add this field
    Semester = models.CharField(max_length=255, null=False)  # Add this field
    TotalMarks = models.IntegerField()
    Faculty = models.ForeignKey(User, on_delete=models.CASCADE)
    Subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    Category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"QuestionPaperID-{self.QuestionPaperID}"


class PaperSections(models.Model):
    PaperID = models.ForeignKey(QuestionPapers, on_delete=models.CASCADE)
    SectionNumber = models.IntegerField()
    SectionName = models.CharField(max_length=255)
    NumMainQuestions = models.IntegerField()
    TotalMarksInSection = models.IntegerField()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['PaperID', 'SectionNumber'], name='unique_paper_section')
        ]
    def __str__(self):
        return f"Section {self.SectionNumber} - {self.SectionName}"

class MainQuestions(models.Model):
    PaperID = models.ForeignKey(QuestionPapers, on_delete=models.CASCADE)
    MainQuestionNumber = models.IntegerField()
    MainQuestionID = models.AutoField(primary_key=True)
    Section = models.ForeignKey(PaperSections, on_delete=models.CASCADE)
    NumSubQuestions = models.IntegerField()

    def __str__(self):
        return f"Main Question ID: {self.MainQuestionID}, Section: {self.Section.SectionName}, NumSubQuestions: {self.NumSubQuestions}"

class Questions(models.Model):
    QuestionID = models.AutoField(primary_key=True)
    QuestionText = models.TextField()
    Answer = models.TextField(null=True, blank=True)
    OptionA = models.CharField(max_length=255, null=True, blank=True)
    OptionB = models.CharField(max_length=255, null=True, blank=True)
    OptionC = models.CharField(max_length=255, null=True, blank=True)
    OptionD = models.CharField(max_length=255, null=True, blank=True)
    CorrectOption = models.CharField(max_length=255, null=True, blank=True)
    Unit = models.CharField(max_length=7, null=True, blank=True)
    SubjectID = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    FacultyID = models.ForeignKey(User, on_delete=models.CASCADE)
    Marks = models.IntegerField()
    Type = models.CharField(max_length=50)
    BloomTaxonomyID = models.CharField(max_length=2)
    class Meta:
        unique_together = ('QuestionText', 'Type')
    def __str__(self):
        return f"Question ID: {self.QuestionID}, Text: {self.QuestionText}, Type: {self.Type}"

class QuestionImage(models.Model):
    Question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='question_images')
    Image = models.ImageField(upload_to='question_images/')

class AnswerImage(models.Model):
    Question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='answer_images')
    Image = models.ImageField(upload_to='answer_images/')

class QuestionPaperQuestions(models.Model):
    QuestionPaperID = models.ForeignKey(QuestionPapers, on_delete=models.CASCADE)
    QuestionID = models.ForeignKey(Questions, on_delete=models.CASCADE)
    SectionNumber = models.IntegerField()
    MainQuestionsID = models.ForeignKey(MainQuestions, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('QuestionPaperID', 'QuestionID')

    def __str__(self):
        return f"QuestionPaperID: {self.QuestionPaperID}, QuestionID: {self.QuestionID}"

class TinyMCEAPIKey(models.Model):
    api_key = models.CharField(max_length=100, blank=True, null=True)  # Store the TinyMCE API key
    expected_expiration = models.DateField(blank=True, null=True)  # Store the expected expiration date
    last_updated = models.DateTimeField(auto_now=True)  # Track the last update time

    def __str__(self):
        return self.api_key if self.api_key else 'No API Key'

    class Meta:
        verbose_name = 'TinyMCE API Key'
        verbose_name_plural = 'TinyMCE API Keys'
