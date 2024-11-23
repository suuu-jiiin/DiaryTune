from sentence_transformers import SentenceTransformer, util

# SBERT 모델 로드
model = SentenceTransformer('all-MiniLM-L6-v2')

# 감정 키워드 사전
sentiment_keywords = {
    "sentiment_1": ["화난", "짜증", "적대적", "좌절", "냉담"],
    "sentiment_2": ["걱정", "슬픔", "불안", "피곤", "상처", "우울"],
    "sentiment_3": ["부끄러운", "외로운", "지루한", "무기력"],
    "sentiment_4": ["행복", "만족", "사랑스러운", "쾌활", "편안"],
    "sentiment_5": ["자신", "용감", "열중", "활기찬", "신난"]
}

def recommend_music(sentiment_label, new_description_list):
    # 감정 키워드 매칭으로 1차 필터링
    filtered_descriptions = [
        desc for desc in new_description_list
        if any(keyword in desc for keyword in sentiment_keywords[sentiment_label])
    ]
    
    # 필터링된 결과가 없으면 모든 데이터를 대상으로 유사도 계산
    candidates = filtered_descriptions if filtered_descriptions else new_description_list
    
    # 감정 대표 텍스트 정의
    sentiment_texts = {
        "sentiment_1": "화난, 짜증, 적대적, 좌절, 냉담한 감정.",
        "sentiment_2": "걱정, 슬픔, 불안, 피곤, 상처, 우울한 감정.",
        "sentiment_3": "부끄러움, 외로움, 지루함, 무기력함과 같은 감정.",
        "sentiment_4": "행복, 만족, 사랑스러움, 쾌활, 편안한 감정.",
        "sentiment_5": "자신감, 용감함, 열정, 활기참, 신난 감정."
    }
    sentiment_text = sentiment_texts[sentiment_label]

    # 감정 대표 텍스트와 new_description 임베딩
    sentiment_embedding = model.encode(sentiment_text)
    descriptions_embeddings = model.encode(candidates)

    # 코사인 유사도 계산
    similarities = util.cos_sim(sentiment_embedding, descriptions_embeddings)

    # 유사도가 가장 높은 설명 선택
    recommended_idx = similarities.argmax()
    return candidates[recommended_idx]
