from django.contrib import admin
from .models import Presentation, Guide, Practical, Test, Question, Choice, TestAttempt, Answer


@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'description')
    ordering = ('order',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Practical)
class PracticalAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published')
    prepopulated_fields = {'slug': ('title',)}



class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'is_published', 'created_at')
    search_fields = ('title',)
    # include question inline so questions can be edited when editing a Test
    inlines = [QuestionInline]
    # keep Test visible as the single test entry in admin


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'order', 'points', 'allow_multiple')
    search_fields = ('text', 'test__title')
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    search_fields = ('text', 'question__text')


try:
    admin.site.unregister(TestAttempt)
except Exception:
    pass

try:
    admin.site.unregister(Answer)
except Exception:
    pass



# Uzbek admin branding
admin.site.site_header = "Muhandislik kompyuter grafikasi — Admin"
admin.site.site_title = "MCG Admin"
admin.site.index_title = "Boshqaruv paneli"

