from django.db import models
from django.utils.text import slugify
import uuid


class BaseResource(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, db_index=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug from title when missing.

        This ensures new resources get a reasonable slug without requiring a manual fill.
        It avoids strict DB-level uniqueness to keep the migration low-risk, but will
        attempt to make slugs human-friendly and avoid collisions by appending a short
        random suffix when necessary.
        """
        if not getattr(self, 'slug', None) and self.title:
            base = slugify(self.title)[:200] or 'item'
            slug = base
            Model = self.__class__
            # Avoid infinite loop but try to find a unique-ish slug
            attempt = 0
            while Model.objects.filter(slug=slug).exists() and attempt < 5:
                slug = f"{base}-{uuid.uuid4().hex[:6]}"
                attempt += 1
            # final fallback
            if Model.objects.filter(slug=slug).exists():
                slug = f"{base}-{uuid.uuid4().hex[:6]}"
            self.slug = slug
        super().save(*args, **kwargs)


class Presentation(BaseResource):
    file = models.FileField(upload_to='presentations/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Taqdimot"
        verbose_name_plural = "Taqdimotlar"


class Guide(BaseResource):
    file = models.FileField(upload_to='guides/')

    class Meta:
        verbose_name = "Qo'llanma"
        verbose_name_plural = "Qo'llanmalar"


class Video(BaseResource):
    # support local files or external URL
    file = models.FileField(upload_to='videos/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videolar"


class Practical(BaseResource):
    files = models.FileField(upload_to='practicals/', blank=True, null=True)

    class Meta:
        verbose_name = "Amaliy mashg'ulot"
        verbose_name_plural = "Amaliy mashg'ulotlar"


class Lab(BaseResource):
    files = models.FileField(upload_to='labs/', blank=True, null=True)

    class Meta:
        verbose_name = "Laboratoriya"
        verbose_name_plural = "Laboratoriyalar"


class Test(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='tests/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # time limit in seconds (0 = no limit)
    time_limit = models.PositiveIntegerField(default=0)
    # allow teacher manual review / override
    allow_manual_review = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Testlar"


class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=1)
    allow_multiple = models.BooleanField(default=False)

    class Meta:
        ordering = ('order', 'id')
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"

    def __str__(self):
        return f"{self.test.title} - {self.text[:50]}"


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Javob varianti"
        verbose_name_plural = "Javob variantlari"


class TestAttempt(models.Model):
    test = models.ForeignKey(Test, related_name='attempts', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    score = models.FloatField(default=0)
    max_score = models.FloatField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    manual_score = models.FloatField(null=True, blank=True)
    is_reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey('auth.User', null=True, blank=True, related_name='reviewed_attempts', on_delete=models.SET_NULL)
    # expiry/timer
    expires_at = models.DateTimeField(null=True, blank=True)
    is_timed_out = models.BooleanField(default=False)

    def __str__(self):
        return f"Attempt #{self.pk} for {self.test.title}"

    class Meta:
        verbose_name = "Test urinish"
        verbose_name_plural = "Test urinishlar"


class Answer(models.Model):
    attempt = models.ForeignKey(TestAttempt, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice, blank=True)

    def __str__(self):
        return f"Answer q={self.question_id} attempt={self.attempt_id}"

    class Meta:
        verbose_name = "Javob"
        verbose_name_plural = "Javoblar"
