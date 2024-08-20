# views.py
from django.shortcuts import render
from .models import Users,QuestionPapers, PaperSections, Questions,QuestionPaperQuestions,Subjects,Categories,QuestionImage,MainQuestions,AnswerImage,TinyMCEAPIKey
from django.db.models import Sum
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
import random
from django.db.models import Q



def question_paper_preview(request, question_paper_id):
    if request.user.is_authenticated:
        question_paper = QuestionPapers.objects.get(pk=question_paper_id)
        sections = PaperSections.objects.filter(PaperID=question_paper_id)
        qpq=QuestionPaperQuestions.objects.filter(QuestionPaperID=question_paper_id)
        # Fetch main questions and their sub-questions for each section
        main_questions = MainQuestions.objects.filter(PaperID=question_paper_id)
        question_images = QuestionImage.objects.all()

        print(main_questions)
        for mainquestion in main_questions:
            print(mainquestion)
            
        for i in qpq:
            print(i)
            print(i.QuestionID)
        questions = []
        for paper_question in qpq:
            questions.append(paper_question.QuestionID)
        print(question_paper)
        print(questions)
        context = {
            'question_paper': question_paper,
            'sections': sections,
            'questions': questions,
            'qpq':qpq,
            'mainquestions': main_questions,
            'question_images':question_images,
        }
        return render(request, 'html/question_paper_preview.html', context)
    else:
        return redirect('/')

'''
def create_question_paper(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Extract form data
            category_name = request.POST.get('category')
            subject_name = request.POST.get('subject')
            paper_name = request.POST.get('paper-name')
            paper_code = request.POST.get('paper-code')
            exam_date = request.POST.get('exam-date')
            exam_time = request.POST.get('exam-time')
            department = request.POST.get('dept')
            semester = request.POST.get('sem')
            num_sections = int(request.POST.get('num-sections'))

            # Get or create the Category instance
            category, _ = Categories.objects.get_or_create(Name=category_name)

            # Get or create the Subject instance
            subject, _ = Subjects.objects.get_or_create(Name=subject_name)

            print(subject)
            default_user_id = 1  # Example ID of the default user
            default_user = User.objects.get(pk=default_user_id)
            print(request.user)

            # Create a new QuestionPaper instance with creation time
            question_paper = QuestionPapers.objects.create(
                PaperName=paper_name, TotalMarks=0, Category=category, Subject=subject,
                PaperCode=paper_code, ExamDate=exam_date, ExamTime=exam_time,
                Department=department, Semester=semester, Faculty=default_user,
                CreatedDate=timezone.now().date()  # Add creation time
            )

            # Iterate over sections
            for i in range(1, num_sections + 1):
                section_name = request.POST.get(f'Section {i}')
                num_questions = int(request.POST.get(f'num-questions-{i}'))
                total_section_marks = 0  # Initialize total marks for the section

                # Create a new PaperSections instance for each section
                section = PaperSections.objects.create(
                    PaperID=question_paper, SectionNumber=i, SectionName=section_name,
                    NumQuestions=num_questions, TotalMarksInSection=0
                )

                # Iterate over questions in the section
                for j in range(1, num_questions + 1):
                    question_text = request.POST.get(f'question-{i}-{j}')
                    marks = int(request.POST.get(f'marks-{i}-{j}'))
                    question_type = request.POST.get(f'question-type-{i}-{j}')
                    bloom_level = request.POST.get(f'bloom-level-section-{i}-{j}')
                    unit=request.POST.get(f'unit-{i}-{j}')

                    # Initialize additional fields
                    answer = None
                    option_a, option_b, option_c, option_d = None, None, None, None
                    correct_option = None

                    
                    # Get the image(s) for the question
                    images = request.FILES.getlist(f'image-upload-{i}-{j}')
                    
                    print(images)
                    # Additional processing based on question type
                    if question_type == 'Descriptive':
                        # Get answer for descriptive question
                        answer = request.POST.get(f'answer-{i}-{j}')

                    elif question_type == 'MCQ':
                        # Get options and correct option for MCQ
                        option_a = request.POST.get(f'option-text-{i}-{j}-1')
                        option_b = request.POST.get(f'option-text-{i}-{j}-2')
                        option_c = request.POST.get(f'option-text-{i}-{j}-3')
                        option_d = request.POST.get(f'option-text-{i}-{j}-4')
                        correct_option = request.POST.get(f'option-{i}-{j}')

                    elif question_type == 'FillInTheBlank':
                        # Get answer for fill-in-the-blank question
                        answer = request.POST.get(f'answer-{i}-{j}')

                    elif question_type == 'TrueOrFalse':
                        # Treat true or false as options
                        option_a = 'True'
                        option_b = 'False'
                        correct_option = request.POST.get(f'truefalse-{i}-{j}')  # Get selected option

                    # Check if the question already exists
                    existing_question = Questions.objects.filter(QuestionText=question_text, Type=question_type).first()

                    if existing_question:
                        question = existing_question
                    else:
                        # Create a new Questions instance for each question
                        question = Questions.objects.create(
                            QuestionText=question_text, Marks=marks, Type=question_type,
                            SubjectID=subject, FacultyID=request.user,
                            OptionA=option_a, OptionB=option_b, OptionC=option_c, OptionD=option_d,
                            CorrectOption=correct_option,Unit=unit,Answer=answer,BloomTaxonomyID=bloom_level
                        )

                    # Associate images with the question
                    for image in images:
                        print(image)
                        question_image = QuestionImage.objects.create(
                            Question=question, Image=image
                        )

                    # Add the question to the PaperQuestions table
                    QuestionPaperQuestions.objects.create(QuestionPaperID=question_paper, QuestionID=question, SectionNumber=i)

                    # Add marks of current question to the total marks of the section
                    total_section_marks += marks

                # Update the total marks for the section
                section.TotalMarksInSection = total_section_marks
                section.save()

            # Calculate total marks for the question paper
            total_marks = PaperSections.objects.filter(PaperID=question_paper).aggregate(total_marks=Sum('TotalMarksInSection'))['total_marks']
            question_paper.TotalMarks = total_marks or 0
            question_paper.save()
            
            return redirect('preview', question_paper_id=question_paper.pk)

        # If the request method is not POST, render the form template
        return render(request, 'html/create-question-paper.html')
    else:
        return redirect('/')'''



from datetime import date

def create_question_paper(request):
    if request.user.is_authenticated:
        api_key_obj, _ = TinyMCEAPIKey.objects.get_or_create(id=1)  # Ensure one row exists
        current_api_key = api_key_obj.api_key
        # Check if the API key is expired or expiring today
        current_date = date.today()
        is_api_key_expired = api_key_obj.expected_expiration and api_key_obj.expected_expiration <= current_date
        if request.method == 'POST':
            # Extract form data
            category_name = request.POST.get('exam')
            subject_name = request.POST.get('subject')
            paper_name = "Default"
            paper_code = request.POST.get('paper-code')
            exam_date = request.POST.get('exam-date')
            exam_time = request.POST.get('exam-time')
            department = request.POST.get('dept')
            semester = request.POST.get('sem')
            num_sections = int(request.POST.get('num-sections'))
            total_marks= int(request.POST.get('total_marks'))

            # Get or create the Category instance
            category, _ = Categories.objects.get_or_create(Name=category_name)

            # Get or create the Subject instance
            subject, _ = Subjects.objects.get_or_create(Name=subject_name)

            # Get the current authenticated user
            faculty = request.user

            # Create a new QuestionPaper instance with creation time
            question_paper = QuestionPapers.objects.create(
                PaperName=paper_name, TotalMarks=0, Category=category, Subject=subject,
                PaperCode=paper_code, ExamDate=exam_date, ExamTime=exam_time,
                Department=department, Semester=semester, Faculty=faculty,
                CreatedDate=timezone.now()  # Add creation time
            )

            # Iterate over sections
            for i in range(1, num_sections + 1):
                section_name = request.POST.get(f'section-name-{i}')
                num_main_questions = int(request.POST.get(f'num-main-questions-{i}'))
                total_section_marks = 0  # Initialize total marks for the section

                # Create a new PaperSections instance for each section
                section = PaperSections.objects.create(
                    PaperID=question_paper, SectionNumber=i, SectionName=section_name,
                    NumMainQuestions=num_main_questions, TotalMarksInSection=0
                )

                # Iterate over main questions in the section
                for j in range(1, num_main_questions + 1):
                    num_sub_questions = int(request.POST.get(f'num-sub-questions-{i}-{j}'))
                    total_main_question_marks = 0  # Initialize total marks for the main question

                    # Create a new MainQuestions instance for each main question
                    main_question = MainQuestions.objects.create(
                       PaperID=question_paper, Section=section, MainQuestionNumber=j, NumSubQuestions=num_sub_questions
                    )

                    # Iterate over sub-questions in the main question
                    for k in range(1, num_sub_questions + 1):
                        question_text = request.POST.get(f'question-{i}-{j}-{k}')
                        marks = int(request.POST.get(f'marks-{i}-{j}-{k}'))
                        question_type = request.POST.get(f'question-type-{i}-{j}-{k}')
                        bloom_level = request.POST.get(f'bloom-level-{i}-{j}-{k}')
                        unit = request.POST.get(f'unit-{i}-{j}-{k}')

                        # Additional processing based on question type
                        answer = None
                        option_a, option_b, option_c, option_d = None, None, None, None
                        correct_option = None

                        # Get the image(s) for the question
                        question_images = request.FILES.getlist(f'image-upload-{i}-{j}-{k}')
                        answer_images = request.FILES.getlist(f'answer-image-upload-{i}-{j}-{k}')

                        if question_type == 'Descriptive':
                            # Get answer for descriptive question
                            answer = request.POST.get(f'answer-{i}-{j}-{k}')

                        elif question_type == 'MCQ':
                            # Get options and correct option for MCQ
                            option_a = request.POST.get(f'option-text-{i}-{j}-1')
                            option_b = request.POST.get(f'option-text-{i}-{j}-2')
                            option_c = request.POST.get(f'option-text-{i}-{j}-3')
                            option_d = request.POST.get(f'option-text-{i}-{j}-4')
                            correct_option = request.POST.get(f'option-{i}-{j}')

                        elif question_type == 'FillInTheBlank':
                            # Get answer for fill-in-the-blank question
                            answer = request.POST.get(f'answer-{i}-{j}-{k}')

                        elif question_type == 'TrueOrFalse':
                            # Treat true or false as options
                            option_a = 'True'
                            option_b = 'False'
                            correct_option = request.POST.get(f'truefalse-{i}-{j}-{k}')  # Get selected option

                        # Check if the question already exists
                        existing_question = Questions.objects.filter(QuestionText=question_text, Type=question_type).first()

                        if existing_question:
                            question = existing_question
                        else:
                            # Create a new Questions instance for each question
                            question = Questions.objects.create(
                                QuestionText=question_text, Marks=marks, Type=question_type,Answer=answer,
                                SubjectID=subject, FacultyID=faculty,
                                OptionA=option_a, OptionB=option_b, OptionC=option_c, OptionD=option_d,
                                CorrectOption=correct_option, Unit=unit, BloomTaxonomyID=bloom_level
                            )

                        # Associate question images with the question
                        for image in question_images:
                            question_image = QuestionImage.objects.create(
                                Question=question, Image=image
                            )

                        # Associate answer images with the question
                        for image in answer_images:
                            answer_image = AnswerImage.objects.create(
                                Question=question, Image=image
                            )

                        # Add the question to the PaperQuestions table
                        QuestionPaperQuestions.objects.create(
                            QuestionPaperID=question_paper, QuestionID=question, SectionNumber=i, MainQuestionsID=main_question
                        )

                        # Add marks of current question to the total marks of the main question
                        total_main_question_marks += marks

                    # Add the total marks of the main question to the total marks of the section
                    total_section_marks += total_main_question_marks

                # Update the total marks for the section
                section.TotalMarksInSection = total_section_marks
                section.save()

            # Calculate total marks for the question paper
            #total_marks = PaperSections.objects.filter(PaperID=question_paper).aggregate(total_marks=Sum('TotalMarksInSection'))['total_marks']
            question_paper.TotalMarks = total_marks or 0
            question_paper.save()

            return redirect('preview', question_paper_id=question_paper.pk)

        # If the request method is not POST, render the form template
        return render(request, 'html/create-question-paper-sub.html',{'current_api_key': current_api_key,'is_api_key_expired': is_api_key_expired})
    else:
        return redirect('/')



def automatic_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Extract form data
            category_name = request.POST.get('exam')
            subject_name = request.POST.get('subject')
            paper_name = "Default"
            paper_code = request.POST.get('paper-code')
            exam_date = request.POST.get('exam-date')
            exam_time = request.POST.get('exam-time')
            department = request.POST.get('dept')
            semester = request.POST.get('sem')
            num_sections = int(request.POST.get('num-sections'))

            # Get or create the Category instance
            category, _ = Categories.objects.get_or_create(Name=category_name)

            # Get or create the Subject instance
            subject, _ = Subjects.objects.get_or_create(Name=subject_name)

            # Get the current authenticated user
            faculty = request.user

            # Create a new QuestionPaper instance with creation time
            question_paper = QuestionPapers.objects.create(
                PaperName=paper_name, TotalMarks=0, Category=category, Subject=subject,
                PaperCode=paper_code, ExamDate=exam_date, ExamTime=exam_time,
                Department=department, Semester=semester, Faculty=faculty,
                CreatedDate=timezone.now()  # Add creation time
            )

            # Iterate over sections
            for i in range(1, num_sections + 1):
                section_name = request.POST.get(f'Section {i}')
                num_main_questions = int(request.POST.get(f'num-main-questions-{i}'))
                total_section_marks = 0  # Initialize total marks for the section

                # Create a new PaperSections instance for each section
                section = PaperSections.objects.create(
                    PaperID=question_paper, SectionNumber=i, SectionName=section_name,
                    NumMainQuestions=num_main_questions, TotalMarksInSection=0
                )

                # Iterate over main questions in the section
                for j in range(1, num_main_questions + 1):
                    num_sub_questions = int(request.POST.get(f'num-sub-questions-{i}-{j}'))
                    total_main_question_marks = 0  # Initialize total marks for the main question

                    # Create a new MainQuestions instance for each main question
                    main_question = MainQuestions.objects.create(
                        PaperID=question_paper, Section=section, MainQuestionNumber=j, NumSubQuestions=num_sub_questions
                    )

                    # Iterate over sub-questions in the main question
                    for k in range(1, num_sub_questions + 1):
                        # Retrieve BloomTaxonomyID, Unit, Type, and Marks for each sub-question
                        bloom_level = request.POST.get(f'bloom-level-{i}-{j}-{k}')
                        unit = request.POST.get(f'unit-{i}-{j}-{k}')
                        question_type = request.POST.get(f'question-type-{i}-{j}-{k}')
                        marks = int(request.POST.get(f'marks-{i}-{j}-{k}'))

                        # Initialize a set to keep track of selected question IDs to avoid repetition
                        selected_question_ids = set()

                        # Retrieve questions based on criteria until a unique question is found
                        while True:
                            # Get a random question based on the specified criteria
                            questions = Questions.objects.filter(
                                SubjectID=subject, BloomTaxonomyID=bloom_level, Unit=unit, Type=question_type, Marks=marks
                            ).exclude(QuestionID__in=selected_question_ids)

                            # If there are no more available questions that meet the criteria, break the loop
                            if not questions.exists():
                                break

                            # Select a random question from the filtered queryset
                            question = random.choice(questions)

                            # If the question ID is not in the set of selected question IDs, break the loop
                            if question.QuestionID not in selected_question_ids:
                                selected_question_ids.add(question.QuestionID)
                                QuestionPaperQuestions.objects.create(
                                    QuestionPaperID=question_paper, QuestionID=question, SectionNumber=i, MainQuestionsID=main_question
                                )
                                break

                        # Add the selected question to the PaperQuestions table
                        

                        total_main_question_marks += marks

                    # Add the total marks of the main question to the total marks of the section
                    total_section_marks += total_main_question_marks

                # Update the total marks for the section
                section.TotalMarksInSection = total_section_marks
                section.save()

            # Calculate total marks for the question paper
            total_marks = PaperSections.objects.filter(PaperID=question_paper).aggregate(total_marks=Sum('TotalMarksInSection'))['total_marks']
            '''
            if category_name in ['Assignment-1', 'Assignment-2']:
                question_paper.TotalMarks = 10
            elif category_name in ['Mid-term Examination-1', 'Mid-term Examination-2']:
                question_paper.TotalMarks = 35
            elif category_name in ['Supplementary','Sem End Examination']:
                question_paper.TotalMarks = 70
            else:
                question_paper.TotalMarks = 0  # Default value'''
        
            
            #question_paper.TotalMarks = total_marks or 0
            question_paper.save()

            return redirect('preview', question_paper_id=question_paper.pk)

        # If the request method is not POST, render the form template
        return render(request, 'html/Automatic_Question_Paper_Generation_sub.html')
    else:
        return redirect('/')
    

def question_papers(request):
    if request.user.is_authenticated:
        # Fetch question papers created by the currently logged-in user
        subjects = Subjects.objects.all()
        user = request.user
        question_papers = QuestionPapers.objects.filter(Faculty=user)
        # Adjusting CreatedDate by subtracting 5.5 hours
        search_query = request.GET.get('search')
        if search_query:
            question_papers = question_papers.filter(Subject__Name__icontains=search_query)
        for paper in question_papers:
            paper.CreatedDate += timedelta(hours=5, minutes=30)  # Subtracting 5.5 hours
        context = {'question_papers': question_papers,'subjects': subjects}
        return render(request, 'html/question_papers.html', context) 
    else:
        return redirect('/')   
    

def notesgeneration(request):
    if request.user.is_authenticated:
        subject_name = request.GET.get('subject')
        question_type = request.GET.get('type')
        unit = request.GET.get('unit')
        if (question_type or subject_name or unit) and subject_name != "All Subjects" or question_type=='' or question_type:
            query = Q()
            if subject_name and subject_name != "All Subjects":
                # Assuming SubjectID is the foreign key to the Subject model
                query &= Q(SubjectID__Name=subject_name)
            if question_type:
                query &= Q(Type=question_type)
            if unit:
                query &= Q(Unit=unit)
            
            questions = Questions.objects.filter(query)
            # Now you have filtered questions based on the selected subject and type
            # Proceed to generate notes
            return render(request, 'html/notes_template.html', {'questions': questions,'subject':subject_name,'questiontype':question_type,'unit':unit})
        if subject_name == "All Subjects":
            subject_name=None
            questions = Questions.objects.all()
            return render(request, 'html/notes_template.html', {'questions': questions,'subject':subject_name,'questiontype':question_type,'unit':unit})
        else:  
            # Handle when no subject or type is selected
            # Redirect or render an appropriate response
            subjects = Subjects.objects.all()
            context = {'subjects': subjects}
            return render(request, 'html/notes_generation.html',context)
    else:
        return redirect('/')
    
def apihelp(request):
    if request.user.is_authenticated:
        api_key_obj, _ = TinyMCEAPIKey.objects.get_or_create(id=1)  # Ensure one row exists
        # Check if the API key is expired or expiring today
        current_date = date.today()
        is_api_key_expired = api_key_obj.expected_expiration and api_key_obj.expected_expiration <= current_date

        if request.method == 'POST':
            # Get the API key from the form data
            new_api_key = request.POST.get('api_key', '').strip()  # Retrieve the submitted API key
            expected_expiration = request.POST.get('expected_expiration')
            api_key_obj.api_key = new_api_key  # Update the model
            api_key_obj.expected_expiration = expected_expiration
            api_key_obj.save()  # Save the changes
            return redirect('/create')  # Redirect to avoid form re-submission
        return render(request, 'html/help.html',{'api_key_obj': api_key_obj,'is_api_key_expired': is_api_key_expired})
    else:
        return redirect('/')