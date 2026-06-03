from pathlib import Path
from django.conf import settings


def search_knowledge_base(keywords):

    base_path = settings.BASE_DIR / "knowledge_base"

    results = []

    for file_path in base_path.glob("*.txt"):

        content = file_path.read_text(encoding="utf-8")

        score = 0

        for keyword in keywords:
            if keyword.lower() in content.lower():
                score += 1

        if score > 0:
            results.append({
                "score": score,
                "content": content
            })

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return [item["content"] for item in results[:3]]