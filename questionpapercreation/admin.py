from django.contrib import admin
from .models import Users, Categories, Subjects, BloomsTaxonomy, QuestionPapers,AnswerImage
from .models import PaperSections, Questions, QuestionPaperQuestions,QuestionImage,MainQuestions,TinyMCEAPIKey

# Register your models here.

admin.site.register(Users)
admin.site.register(Categories)
admin.site.register(Subjects)
admin.site.register(BloomsTaxonomy)
admin.site.register(QuestionPapers)
admin.site.register(PaperSections)
admin.site.register(MainQuestions)
admin.site.register(Questions)
admin.site.register(QuestionPaperQuestions)
admin.site.register(QuestionImage)
admin.site.register(AnswerImage)
admin.site.register(TinyMCEAPIKey)

