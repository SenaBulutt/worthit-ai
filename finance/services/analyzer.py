from datetime import timedelta
from django.utils import timezone


def analyze_purchase(purchase, profile):
    price = float(purchase.price)
    income = float(profile.monthly_income)

    income_ratio = 0
    work_hours_needed = 0

    if income > 0:
        income_ratio = round((price / income) * 100, 2)

    if profile.weekly_work_hours > 0 and income > 0:
        monthly_hours = profile.weekly_work_hours * 4
        hourly_income = income / monthly_hours
        work_hours_needed = round(price / hourly_income, 2)

    three_months_ago = timezone.now() - timedelta(days=90)

    similar_count = PurchaseCheckSafeCount(
        purchase=purchase,
        three_months_ago=three_months_ago
    )

    risk = "low"

    if income_ratio >= 20 or (not purchase.is_need and income_ratio >= 15):
        risk = "high"
    elif income_ratio >= 10 or similar_count >= 3:
        risk = "medium"

    worthit_score = 100

    if income_ratio >= 50:
        worthit_score -= 50
    elif income_ratio >= 30:
        worthit_score -= 35
    elif income_ratio >= 15:
        worthit_score -= 20

    if not purchase.is_need:
        worthit_score -= 15

    if similar_count >= 5:
        worthit_score -= 15
    elif similar_count >= 3:
        worthit_score -= 10

    if worthit_score < 0:
        worthit_score = 0

    return {
        "income_ratio": income_ratio,
        "work_hours_needed": work_hours_needed,
        "similar_category_count": similar_count,
        "risk_level": risk,
        "worthit_score": worthit_score,
    }


def PurchaseCheckSafeCount(purchase, three_months_ago):
    return purchase.user.purchasecheck_set.filter(
        category=purchase.category,
        created_at__gte=three_months_ago
    ).exclude(id=purchase.id).count()