from django import forms
from .models import Guide, Video, Practical, Lab, Test


class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ["title", "description", "file", "is_published"]


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "description", "file", "url", "is_published"]


class PracticalForm(forms.ModelForm):
    class Meta:
        model = Practical
        fields = ["title", "description", "files", "is_published"]


class LabForm(forms.ModelForm):
    class Meta:
        model = Lab
        fields = ["title", "description", "files", "is_published"]


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["title", "description", "file", "time_limit", "allow_manual_review", "is_published"]
