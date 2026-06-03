from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Profile, PurchaseCheck, Feedback
from .forms import ProfileForm, PurchaseCheckForm, FeedbackForm
from .services.analyzer import analyze_purchase
from .services.rag import search_knowledge_base
from .services.ai_client import generate_ai_comment, generate_fallback_comment, answer_purchase_question


@login_required
def dashboard_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if profile.monthly_income <= 0 or profile.weekly_work_hours <= 0:
        return redirect("profile")

    purchases = PurchaseCheck.objects.filter(user=request.user).order_by("-created_at")

    total_checks = purchases.count()
    high_risk_count = purchases.filter(risk_level="high").count()
    medium_risk_count = purchases.filter(risk_level="medium").count()
    low_risk_count = purchases.filter(risk_level="low").count()

    total_spending = sum(item.price for item in purchases)

    most_used_category = None
    if purchases.exists():
        most_used_category = (
            purchases
            .values("category__name")
            .annotate(count=Count("id"))
            .order_by("-count")
            .first()
        )

    high_risk_percentage = 0
    if total_checks > 0:
        high_risk_percentage = round((high_risk_count / total_checks) * 100, 1)

    financial_personality = "Dengeli Harcayıcı"
    if high_risk_percentage >= 60:
        financial_personality = "Dürtüsel Harcayıcı"
    elif high_risk_percentage >= 30:
        financial_personality = "Kontrollü Harcayıcı"

    most_common_risk = "Düşük"
    if high_risk_count >= medium_risk_count and high_risk_count >= low_risk_count and high_risk_count > 0:
        most_common_risk = "Yüksek"
    elif medium_risk_count >= high_risk_count and medium_risk_count >= low_risk_count and medium_risk_count > 0:
        most_common_risk = "Orta"

    category_dict = {}

    for purchase in purchases:
        category_name = purchase.category.name if purchase.category else "Kategorisiz"

        if category_name in category_dict:
            category_dict[category_name] += 1
        else:
            category_dict[category_name] = 1

    category_labels = list(category_dict.keys())
    category_data = list(category_dict.values())

    risk_labels = ["Düşük", "Orta", "Yüksek"]
    risk_data = [
        low_risk_count,
        medium_risk_count,
        high_risk_count,
    ]

    context = {
        "profile": profile,
        "purchases": purchases,
        "total_checks": total_checks,
        "high_risk_count": high_risk_count,
        "total_spending": total_spending,
        "most_used_category": most_used_category,
        "high_risk_percentage": high_risk_percentage,
        "category_labels": category_labels,
        "category_data": category_data,
        "risk_labels": risk_labels,
        "risk_data": risk_data,
        "financial_personality": financial_personality,
        "most_common_risk": most_common_risk,
    }

    return render(request, "finance/dashboard.html", context)


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "finance/profile.html", {"form": form})


@login_required
def purchase_add_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = PurchaseCheckForm(request.POST)

        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.save()

            analysis = analyze_purchase(purchase, profile)

            purchase.income_ratio = analysis["income_ratio"]
            purchase.work_hours_needed = analysis["work_hours_needed"]
            purchase.similar_category_count = analysis["similar_category_count"]
            purchase.risk_level = analysis["risk_level"]
            purchase.worthit_score = analysis["worthit_score"]

            keywords = [
                purchase.item_name,
                purchase.category.name if purchase.category else "",
                "ihtiyaç" if purchase.is_need else "istek",
                analysis["risk_level"],
                "yüksek tutar" if analysis["income_ratio"] >= 10 else "bütçe",
            ]

            rag_contexts = search_knowledge_base(keywords)

            try:
                ai_comment = generate_ai_comment(
                    purchase=purchase,
                    profile=profile,
                    analysis=analysis,
                    rag_contexts=rag_contexts,
                )
            except Exception:
                ai_comment = generate_fallback_comment(
                    purchase=purchase,
                    profile=profile,
                    analysis=analysis,
                )

            purchase.ai_comment = ai_comment
            purchase.save()

            return redirect("purchase_detail", pk=purchase.pk)
    else:
        form = PurchaseCheckForm()

    return render(request, "finance/purchase_form.html", {"form": form})


@login_required
def purchase_detail_view(request, pk):
    purchase = PurchaseCheck.objects.get(pk=pk, user=request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)

    answer = None
    question = ""

    if request.method == "POST":
        question = request.POST.get("question", "")

        if question:
            try:
                answer = answer_purchase_question(purchase, profile, question)
            except Exception:
                answer = "Şu anda AI yanıtı alınamadı. Harcamanın risk seviyesi ve gelire oranına göre tekrar değerlendirmeni öneririm."

    return render(
        request,
        "finance/purchase_detail.html",
        {
            "purchase": purchase,
            "answer": answer,
            "question": question,
        }
    )

@login_required
def purchase_update_view(request, pk):
    purchase = PurchaseCheck.objects.get(pk=pk, user=request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)

    if profile.monthly_income <= 0 or profile.weekly_work_hours <= 0:
        return redirect("profile")

    if request.method == "POST":
        form = PurchaseCheckForm(request.POST, instance=purchase)

        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.save()

            analysis = analyze_purchase(purchase, profile)

            purchase.income_ratio = analysis["income_ratio"]
            purchase.work_hours_needed = analysis["work_hours_needed"]
            purchase.similar_category_count = analysis["similar_category_count"]
            purchase.risk_level = analysis["risk_level"]
            purchase.worthit_score = analysis["worthit_score"]
            purchase.save()

            return redirect("purchase_detail", pk=purchase.pk)
    else:
        form = PurchaseCheckForm(instance=purchase)

    return render(request, "finance/purchase_form.html", {"form": form})


@login_required
def purchase_delete_view(request, pk):
    purchase = PurchaseCheck.objects.get(pk=pk, user=request.user)

    if request.method == "POST":
        purchase.delete()
        return redirect("dashboard")

    return render(request, "finance/purchase_confirm_delete.html", {"purchase": purchase})


@login_required
def feedback_list_view(request):
    feedbacks = Feedback.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "finance/feedback_list.html", {"feedbacks": feedbacks})


@login_required
def feedback_add_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)

        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect("feedback_list")
    else:
        form = FeedbackForm()

    return render(request, "finance/feedback_form.html", {"form": form})


@login_required
def feedback_update_view(request, pk):
    feedback = Feedback.objects.get(pk=pk, user=request.user)

    if request.method == "POST":
        form = FeedbackForm(request.POST, instance=feedback)

        if form.is_valid():
            form.save()
            return redirect("feedback_list")
    else:
        form = FeedbackForm(instance=feedback)

    return render(request, "finance/feedback_form.html", {"form": form})


@login_required
def feedback_delete_view(request, pk):
    feedback = Feedback.objects.get(pk=pk, user=request.user)

    if request.method == "POST":
        feedback.delete()
        return redirect("feedback_list")

    return render(request, "finance/feedback_confirm_delete.html", {"feedback": feedback})
@login_required
def purchase_list_view(request):
    purchases = PurchaseCheck.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "finance/purchase_list.html", {"purchases": purchases})