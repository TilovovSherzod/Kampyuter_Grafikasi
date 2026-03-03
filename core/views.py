from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .utils import teacher_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Presentation, Guide, Video, Practical, Lab, Test, Question, Choice, TestAttempt, Answer
from .serializers import PresentationSerializer, GuideSerializer, VideoSerializer
from .forms import GuideForm, VideoForm, PracticalForm, LabForm
from django.utils import timezone
from datetime import timedelta
import uuid

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.urls import reverse


def home(request):
    """Render main landing page."""
    context = {"title": "Muhandislik kompyuter grafikasi"}
    return render(request, "index.html", context)


@api_view(["GET"])
def api_presentations(request):
    if not request.user or not request.user.is_authenticated:
        return Response({'detail': 'Authentication required'}, status=403)
    qs = Presentation.objects.filter(is_published=True).order_by('order', '-created_at')
    serializer = PresentationSerializer(qs, many=True, context={"request": request})
    return Response(serializer.data)


@login_required
def presentations_list(request):
    qs = Presentation.objects.filter(is_published=True).order_by('order', '-created_at')
    return render(request, 'core/presentations_list.html', {'items': qs})


@login_required
def presentation_download(request, pk):
    pres = get_object_or_404(Presentation, pk=pk)
    if not pres.file:
        raise Http404("Fayl topilmadi")
    path = pres.file.path
    if not os.path.exists(path):
        raise Http404("Fayl topilmadi")
    return FileResponse(open(path, 'rb'), as_attachment=True, filename=os.path.basename(path))


@api_view(["GET"])
def api_guides(request):
    if not request.user or not request.user.is_authenticated:
        return Response({'detail': 'Authentication required'}, status=403)
    qs = Guide.objects.filter(is_published=True).order_by('-created_at')
    serializer = GuideSerializer(qs, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
def api_videos(request):
    if not request.user or not request.user.is_authenticated:
        return Response({'detail': 'Authentication required'}, status=403)
    qs = Video.objects.filter(is_published=True).order_by('-created_at')
    serializer = VideoSerializer(qs, many=True, context={"request": request})
    return Response(serializer.data)


# Frontend CRUD views for Guides
@login_required
def guides_list(request):
    qs = Guide.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'core/guides_list.html', {'guides': qs})


@login_required
def guide_detail(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    return render(request, 'core/guide_detail.html', {'guide': guide})


@login_required
def guide_download(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    if not guide.file:
        raise Http404("Fayl topilmadi")
    path = guide.file.path
    if not os.path.exists(path):
        raise Http404("Fayl topilmadi")
    return FileResponse(open(path, 'rb'), as_attachment=True, filename=os.path.basename(path))


@teacher_required
def guide_create(request):
    if request.method == 'POST':
        form = GuideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('core:guides_list')
    else:
        form = GuideForm()
    return render(request, 'core/guide_form.html', {'form': form})


# Videos
@login_required
def videos_list(request):
    qs = Video.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'core/videos_list.html', {'videos': qs})


@login_required
def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    return render(request, 'core/video_detail.html', {'video': video})


@login_required
def video_download(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if not video.file:
        raise Http404("Fayl topilmadi")
    path = video.file.path
    if not os.path.exists(path):
        raise Http404("Fayl topilmadi")
    return FileResponse(open(path, 'rb'), as_attachment=True, filename=os.path.basename(path))


@teacher_required
def video_create(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('core:videos_list')
    else:
        form = VideoForm()
    return render(request, 'core/video_form.html', {'form': form})


# Practicals
@login_required
def practicals_list(request):
    qs = Practical.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'core/practicals_list.html', {'items': qs})


@login_required
def practical_detail(request, pk):
    item = get_object_or_404(Practical, pk=pk)
    return render(request, 'core/practical_detail.html', {'item': item})


@login_required
def practical_download(request, pk):
    item = get_object_or_404(Practical, pk=pk)
    if not item.files:
        raise Http404("Fayl topilmadi")
    path = item.files.path
    if not os.path.exists(path):
        raise Http404("Fayl topilmadi")
    return FileResponse(open(path, 'rb'), as_attachment=True, filename=os.path.basename(path))


@teacher_required
def practical_create(request):
    if request.method == 'POST':
        form = PracticalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('core:practicals_list')
    else:
        form = PracticalForm()
    return render(request, 'core/practical_form.html', {'form': form})


# Labs
@login_required
def labs_list(request):
    qs = Lab.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'core/labs_list.html', {'items': qs})


@login_required
def lab_detail(request, pk):
    item = get_object_or_404(Lab, pk=pk)
    return render(request, 'core/lab_detail.html', {'item': item})


@login_required
def lab_download(request, pk):
    item = get_object_or_404(Lab, pk=pk)
    if not item.files:
        raise Http404("Fayl topilmadi")
    path = item.files.path
    if not os.path.exists(path):
        raise Http404("Fayl topilmadi")
    return FileResponse(open(path, 'rb'), as_attachment=True, filename=os.path.basename(path))


@teacher_required
def lab_create(request):
    if request.method == 'POST':
        form = LabForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('core:labs_list')
    else:
        form = LabForm()
    return render(request, 'core/lab_form.html', {'form': form})


# Tests (placeholder)
def tests_list(request):
    qs = Test.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'core/tests_list.html', {'items': qs})


def test_detail(request, pk):
    item = get_object_or_404(Test, pk=pk)
    return render(request, 'core/test_detail.html', {'item': item})


@staff_member_required
# Test creation is managed via admin. Frontend create view removed.


# --- Test taking views ---
def test_take(request, pk):
    test = get_object_or_404(Test, pk=pk, is_published=True)
    questions = test.questions.prefetch_related('choices').all()
    # Start attempt flow: if AJAX start, create attempt and set expiry if time_limit set
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Create attempt (or return existing active attempt for this user and test)
        user = request.user if request.user.is_authenticated else None
        # check for existing active attempt
        attempt = None
        if user:
            attempt = TestAttempt.objects.filter(test=test, user=user, finished_at__isnull=True).first()
        if not attempt:
            attempt = TestAttempt.objects.create(test=test, user=user)
            # set expiry
            if test.time_limit and test.time_limit > 0:
                attempt.expires_at = attempt.started_at + timedelta(seconds=test.time_limit)
                attempt.save()
        data = {
            'attempt_id': attempt.pk,
            'expires_at': attempt.expires_at.isoformat() if attempt.expires_at else None,
        }
        return JsonResponse(data)

    return render(request, 'core/test_take.html', {'test': test, 'questions': questions})


@api_view(['POST'])
def attempt_save(request, attempt_pk):
    """Save progress for an attempt (partial). Expects POST with q_<id>=choice ids[]"""
    attempt = get_object_or_404(TestAttempt, pk=attempt_pk)
    # check expiry
    now = timezone.now()
    if attempt.expires_at and now > attempt.expires_at:
        attempt.is_timed_out = True
        attempt.save()
        return Response({'detail': 'Time expired'}, status=400)

    # Save answers (replace existing answers for attempt)
    for key, vals in request.data.lists():
        if not key.startswith('q_'):
            continue
        qid = int(key.split('_', 1)[1])
        q = get_object_or_404(Question, id=qid)
        # ensure answer exists
        ans, _ = Answer.objects.get_or_create(attempt=attempt, question=q)
        # set choices
        chosen_ids = [int(x) for x in vals]
        ans.choices.set(Choice.objects.filter(id__in=chosen_ids))
    return Response({'detail': 'saved'})


@api_view(['POST'])
def attempt_submit(request, attempt_pk):
    attempt = get_object_or_404(TestAttempt, pk=attempt_pk)
    now = timezone.now()
    if attempt.expires_at and now > attempt.expires_at:
        attempt.is_timed_out = True
        attempt.finished_at = now
        attempt.save()
        return Response({'detail': 'Time expired, attempt closed'}, status=400)


    # parse submitted answers from request.data
    total = 0
    max_total = 0
    questions = attempt.test.questions.prefetch_related('choices').all()
    for q in questions:
        key = f'q_{q.id}'
        selected = request.data.getlist(key) if hasattr(request.data, 'getlist') else request.data.get(key, [])
        # normalize to list
        if isinstance(selected, str):
            selected = [selected]
        chosen_objs = Choice.objects.filter(id__in=[int(x) for x in selected if str(x).isnumeric()])
        # create/replace Answer
        ans, _ = Answer.objects.get_or_create(attempt=attempt, question=q)
        ans.choices.set(chosen_objs)
        # grading with partial credit
        correct_qs = q.choices.filter(is_correct=True)
        correct_ids = set(correct_qs.values_list('id', flat=True))
        chosen_ids = set(chosen_objs.values_list('id', flat=True))
        max_total += q.points
        if not q.allow_multiple:
            # single choice: full if exact match
            if chosen_ids == correct_ids:
                total += q.points
        else:
            # multiple correct: partial credit
            num_correct_total = len(correct_ids)
            if num_correct_total == 0:
                continue
            num_correct_selected = len(chosen_ids & correct_ids)
            num_incorrect_selected = len(chosen_ids - correct_ids)
            # formula: credit = (correct_selected - incorrect_selected) / num_correct_total
            credit_ratio = (num_correct_selected - num_incorrect_selected) / num_correct_total
            if credit_ratio < 0:
                credit_ratio = 0
            if credit_ratio > 1:
                credit_ratio = 1
            total += q.points * credit_ratio

    attempt.score = round(total, 2)
    attempt.max_score = max_total
    attempt.finished_at = now
    attempt.save()
    return Response({'attempt_id': attempt.pk, 'score': attempt.score, 'max_score': attempt.max_score})


@login_required
def my_results(request):
    qs = TestAttempt.objects.filter(user=request.user).order_by('-started_at')
    return render(request, 'core/my_results.html', {'attempts': qs})


@teacher_required
def review_attempts(request):
    qs = TestAttempt.objects.filter(is_reviewed=False).order_by('-finished_at')
    return render(request, 'core/review_attempts.html', {'attempts': qs})


@teacher_required
def review_attempt_detail(request, pk):
    attempt = get_object_or_404(TestAttempt, pk=pk)
    if request.method == 'POST':
        manual = request.POST.get('manual_score')
        if manual:
            try:
                attempt.manual_score = float(manual)
            except ValueError:
                attempt.manual_score = None
            attempt.is_reviewed = True
            attempt.reviewed_by = request.user
            attempt.save()
            return redirect('core:review_attempts')
    return render(request, 'core/review_attempt_detail.html', {'attempt': attempt})


@teacher_required
def teacher_dashboard(request):
    """Simple teacher panel: list resources and recent attempts."""
    tests = Test.objects.all().order_by('-created_at')
    recent_attempts = TestAttempt.objects.order_by('-started_at')[:20]
    return render(request, 'core/teacher_dashboard.html', {'tests': tests, 'recent_attempts': recent_attempts})



def test_result(request, pk):
    attempt = get_object_or_404(TestAttempt, pk=pk)
    # build per-question feedback
    feedback = []
    for ans in attempt.answers.select_related('question').prefetch_related('choices'):
        q = ans.question
        correct_ids = set(q.choices.filter(is_correct=True).values_list('id', flat=True))
        chosen_ids = set(ans.choices.values_list('id', flat=True))
        feedback.append({
            'question': q,
            'chosen': ans.choices.all(),
            'correct': q.choices.filter(is_correct=True).all(),
            'is_correct': correct_ids == chosen_ids,
            'points': q.points,
        })
    return render(request, 'core/test_result.html', {'attempt': attempt, 'feedback': feedback})


def signup(request):
    """Simple user registration view using Django's built-in UserCreationForm.

    After successful signup the user is logged in and redirected to home.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in
            auth_login(request, user)
            # redirect to next if provided, else home
            next_url = request.GET.get('next') or request.POST.get('next') or reverse('core:home')
            return redirect(next_url)
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
