from django import forms
from .models import Profile, PurchaseCheck, Feedback


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["monthly_income", "weekly_work_hours", "status"]
        widgets = {
    "monthly_income": forms.NumberInput(attrs={
        "min": "0"
    }),

    "weekly_work_hours": forms.NumberInput(attrs={
        "min": "0",
        "max": "168"
    }),
}
        labels = {
            "monthly_income": "Aylık Gelir",
            "weekly_work_hours": "Haftalık Çalışma Saati",
            "status": "Durum",
        }


class PurchaseCheckForm(forms.ModelForm):

    class Meta:
        model = PurchaseCheck

        fields = [
            "item_name",
            "price",
            "category",
            "is_need",
            "note",
        ]

        labels = {
            "item_name": "Ürün Adı",
            "price": "Fiyat",
            "category": "Kategori",
            "is_need": "Bu harcama gerekli mi?",
            "note": "Not",
        }

        widgets = {
    "is_need": forms.RadioSelect(
        choices=[
            (True, "Evet"),
            (False, "Hayır")
        ]
    ),

    "price": forms.NumberInput(attrs={
        "min": "0",
        "step": "0.01"
    }),
}
            
        
class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback

        fields = [
            "title",
            "message",
            "rating"
        ]

        labels = {
            "title": "Başlık",
            "message": "Yorum / Geri Bildirim",
            "rating": "Puan",
        }

        widgets = {
            "rating": forms.NumberInput(attrs={
                "min": 1,
                "max": 5
            })
        }      