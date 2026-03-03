from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path('accounts/signup/', views.signup, name='signup'),
    path("api/presentations/", views.api_presentations, name="api_presentations"),
    path('presentations/', views.presentations_list, name='presentations_list'),
    path("api/guides/", views.api_guides, name="api_guides"),
    # Guides
    path('guides/', views.guides_list, name='guides_list'),
    path('guides/add/', views.guide_create, name='guide_add'),
    path('guides/<int:pk>/', views.guide_detail, name='guide_detail'),
    path('guides/<int:pk>/download/', views.guide_download, name='guide_download'),
    path('presentations/<int:pk>/download/', views.presentation_download, name='presentation_download'),
    # Practicals
    path('practicals/', views.practicals_list, name='practicals_list'),
    path('practicals/add/', views.practical_create, name='practical_add'),
    path('practicals/<int:pk>/', views.practical_detail, name='practical_detail'),
    path('practicals/<int:pk>/download/', views.practical_download, name='practical_download'),
    # Tests
    path('tests/', views.tests_list, name='tests_list'),
    path('tests/<int:pk>/', views.test_detail, name='test_detail'),
    path('tests/<int:pk>/take/', views.test_take, name='test_take'),
    path('api/attempts/<int:attempt_pk>/save/', views.attempt_save, name='attempt_save'),
    path('api/attempts/<int:attempt_pk>/submit/', views.attempt_submit, name='attempt_submit'),
    path('attempt/<int:pk>/result/', views.test_result, name='test_result'),
    path('my-results/', views.my_results, name='my_results'),
    path('review/attempts/', views.review_attempts, name='review_attempts'),
    path('review/attempts/<int:pk>/', views.review_attempt_detail, name='review_attempt_detail'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
]
