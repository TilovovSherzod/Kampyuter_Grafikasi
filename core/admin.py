from django.contrib import admin
import nested_admin
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



class ChoiceInline(nested_admin.NestedTabularInline):
    """Variantlarni savolni ichida ko'rsatish uchun"""
    model = Choice
    extra = 1
    fields = ('text', 'is_correct')
    verbose_name_plural = "Javob variantlari"
    readonly_fields = ()
    can_delete = True  # O'chirish imkoniyatini berish
    
    class Media:
        css = {
            'all': ('admin_choice_inline.css',)
        }
        js = ('admin_choice_inline.js',)


class QuestionInline(nested_admin.NestedTabularInline):
    """Savollarni test ichida ko'rsatish uchun"""
    model = Question
    extra = 1
    fields = ('text', 'order', 'points', 'allow_multiple')
    ordering = ('order',)
    verbose_name_plural = "Savollar"
    inlines = [ChoiceInline]  # Savolning ichida variantlar
    can_delete = True  # O'chirish imkoniyatini berish


@admin.register(Test)
class TestAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'file', 'is_published', 'created_at')
    search_fields = ('title',)
    list_filter = ('is_published',)
    fieldsets = (
        (None, {'fields': ('title', 'description', 'file')}),
        ('Sozlamalar', {'fields': ('is_published', 'time_limit', 'allow_manual_review')}),
    )
    inlines = [QuestionInline]  # Testning ichida savollar, savolning ichida variantlar


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'order', 'points', 'allow_multiple')
    list_filter = ('test', 'allow_multiple')
    search_fields = ('text', 'test__title')
    fieldsets = (
        ('Savol ma\'lumotlari', {'fields': ('test', 'text', 'order', 'points')}),
        ('Variantlar', {'fields': ('allow_multiple',), 'description': 'Bir nechta to\'g\'ri javob bo\'lsa, "Bir nechta variantga ruxsat berish" ni belgilang'}),
    )
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct', 'question__test')
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

