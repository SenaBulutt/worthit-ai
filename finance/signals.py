from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name != "finance":
        return

    from .models import Category

    default_categories = [
    "Giyim",
    "Teknoloji",
    "Yemek",
    "Ulaşım",
    "Eğlence",
    "Eğitim",
    "Abonelik",
    "Sağlık",
    "Kişisel Bakım",
    "Diğer",
]

    for category_name in default_categories:
        Category.objects.get_or_create(name=category_name)