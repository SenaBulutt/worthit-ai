from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    STATUS_CHOICES = (
        ('student', 'Öğrenci'),
        ('worker', 'Çalışan'),
        ('both', 'Öğrenci ve Çalışan'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    weekly_work_hours = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='student')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profiller"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"


class PurchaseCheck(models.Model):
    RISK_CHOICES = (
        ('low', 'Düşük'),
        ('medium', 'Orta'),
        ('high', 'Yüksek'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_need = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)

    income_ratio = models.FloatField(default=0)
    work_hours_needed = models.FloatField(default=0)
    similar_category_count = models.PositiveIntegerField(default=0)
    risk_level = models.CharField(max_length=20, choices=RISK_CHOICES, default='low')
    ai_comment = models.TextField(blank=True, null=True)
    worthit_score = models.PositiveIntegerField(default=50)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name

    class Meta:
        verbose_name = "Harcama Analizi"
        verbose_name_plural = "Harcama Analizleri"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    message = models.TextField()
    rating = models.PositiveIntegerField(
    default=5,
    validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ]
)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Geri Bildirim"
        verbose_name_plural = "Geri Bildirimler"