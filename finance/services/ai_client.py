import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

MODEL_NAME = "llama-3.3-70b-versatile"


def generate_ai_comment(purchase, profile, analysis, rag_contexts):
    context_text = "\n\n".join(rag_contexts)

    prompt = f"""
Sen finansal farkındalık odaklı bir harcama karar asistanısın.

Kullanıcı bilgileri:
- Aylık gelir: {profile.monthly_income} TL
- Haftalık çalışma saati: {profile.weekly_work_hours}

Harcama:
- Ürün: {purchase.item_name}
- Fiyat: {purchase.price} TL
- Kategori: {purchase.category}
- İhtiyaç mı?: {"Evet" if purchase.is_need else "Hayır"}

Analiz:
- Gelire oranı: %{analysis["income_ratio"]}
- Çalışma karşılığı: {analysis["work_hours_needed"]} saat
- Benzer kategori sorgusu: {analysis["similar_category_count"]}
- Risk seviyesi: {analysis["risk_level"]}

Bilgi tabanı:
{context_text}

Kullanıcıya:
1. Kısa analiz
2. Neden riskli/risksiz olduğu
3. 3 maddelik öneri
4. Son karar: AL / ERTELE / ALTERNATİF ARA

formatında kısa ve anlaşılır cevap ver.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
    )

    return response.choices[0].message.content


def answer_purchase_question(purchase, profile, question):
    prompt = f"""
Sen finansal karar destek asistanısın.

Kullanıcı bilgileri:
- Aylık gelir: {profile.monthly_income} TL
- Haftalık çalışma saati: {profile.weekly_work_hours}

Harcama bilgileri:
- Ürün: {purchase.item_name}
- Fiyat: {purchase.price} TL
- Kategori: {purchase.category}
- İhtiyaç mı?: {"Evet" if purchase.is_need else "Hayır"}
- Gelire oranı: %{purchase.income_ratio}
- Çalışma karşılığı: {purchase.work_hours_needed} saat
- Risk seviyesi: {purchase.get_risk_level_display()}
- WorthIt skoru: {purchase.worthit_score}/100

Kullanıcının sorusu:
{question}

Kısa, net ve finansal farkındalık odaklı cevap ver.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
    )

    return response.choices[0].message.content


def generate_fallback_comment(purchase, profile, analysis):
    risk_map = {
        "low": "Düşük",
        "medium": "Orta",
        "high": "Yüksek",
    }

    risk_text = risk_map.get(analysis["risk_level"], analysis["risk_level"])

    if analysis["risk_level"] == "high":
        decision = "ERTELE"
    elif analysis["risk_level"] == "medium":
        decision = "ALTERNATİF ARA"
    else:
        decision = "AL"

    need_text = "ihtiyaç" if purchase.is_need else "istek"

    return f"""
Kısa analiz:
Bu harcama aylık gelirinin %{analysis["income_ratio"]} kadarına denk geliyor. Bu harcama {need_text} olarak değerlendirildi.

Neden böyle değerlendirildi?
Bu ürün için yaklaşık {analysis["work_hours_needed"]} saat çalışman gerekiyor. Son 3 ayda aynı kategoride {analysis["similar_category_count"]} benzer sorgu bulunuyor. Risk seviyesi: {risk_text}.

Öneriler:
1. Satın almadan önce bütçende bu harcamaya gerçekten yer olup olmadığını kontrol et.
2. Daha uygun fiyatlı alternatifleri araştır.
3. İhtiyaç değilse 24 saat bekleme kuralını uygula.

Son karar: {decision}
"""