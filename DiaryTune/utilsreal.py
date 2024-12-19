import openai
import os
from sentence_transformers import SentenceTransformer, util
import json
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# 감정 키워드 사전
sentiment_keywords = {
    "sentiment_1": ["화난", "짜증", "적대적", "좌절", "냉담한"],
    "sentiment_2": ["걱정되는", "슬픈", "불안한", "피곤한", "상처받은", "우울한"],
    "sentiment_3": ["부끄러운", "외로운", "지루한", "무기력한"],
    "sentiment_4": ["행복한", "만족하는", "사랑스러운", "쾌활한", "편안한"],
    "sentiment_5": ["자신있는", "용감한", "열정적인", "활기찬", "신난"]
}

# 감정 분석 함수
def analyze_emotion(diary_content):
    sentiment = ""
    similar_words = []
    try:

        prompt = f"""
        아래의 일기 내용을 읽고 감정을 분석한 후, JSON 형식으로 결과를 반환하세요.
        1. 입력된 일기 내용에서 감정을 분석하여 주어진 sentiment_keywords 중에서 가장 연관이 있는 'sentiment_1' ~ 'sentiment_5' 중 하나를 선택하고 선택된 것을 "선택된 감정"으로 정의합니다.
        2. 선택된 감정과 유사한 3개의 형용사 키워드를 한국어로 반환하여 ["키워드1", "키워드2", "키워드3"]으로 정의합니다.
        
        출력 형식 (JSON):
        {{
            "sentiment": "선택된 감정",
            "similar_words": ["키워드1", "키워드2", "키워드3"]
        }}
        
        입력된 일기: "{diary_content}"
        sentiment_keywords: {sentiment_keywords}
        """

        
        # OpenAI API 호출
        response = openai.ChatCompletion.create(
             model="gpt-3.5-turbo",
            #prompt=prompt,
            messages=[
                {"role": "system", "content": "You are an assistant that analyzes diary entries."},
                {"role": "user", "content": prompt}
                ],
            max_tokens=1000,
            #stop=None,
            temperature=0.7
        )
        
        response_text = response['choices'][0]['message']['content'].strip()
        data = json.loads(response_text)
        
        # sentiment_data = response.choices[0].text.strip().split("\n")
        logging.debug("Response text: %s", response['choices'][0]['message']['content'].strip())
        
        
        # 결과 반환
        sentiment_value = data.get("sentiment")
        similar_words = data.get("similar_words")

        if sentiment_value and similar_words:
            return {"sentiment": sentiment_value, "keywords": similar_words}
        else:
            raise ValueError("Invalid sentiment or keywords")

    except json.JSONDecodeError as json_error:
        return {"error": "JSON 파싱 실패", "details": str(json_error)}
    except KeyError as key_error:
        return {"error": "응답에 필요한 키가 누락되었습니다", "details": str(key_error)}
    except Exception as e:
        return {"error": "예기치 못한 오류 발생", "details": str(e)}
    

'''
노래추천 with BERT
'''
# SBERT 모델 로드
model = SentenceTransformer('all-MiniLM-L6-v2')

def recommend_music(sentiment_label, new_description_list):
    if sentiment_label == 'sentiment_1':
        sentiment_label = 'sentiment_2'
        
    # 감정 키워드 매칭으로 1차 필터링
    filtered_descriptions = [
        desc for desc in new_description_list
        if any(keyword in desc for keyword in sentiment_keywords[sentiment_label])
    ]
    
    # 필터링된 결과가 없으면 모든 데이터를 대상으로 유사도 계산
    candidates = filtered_descriptions if filtered_descriptions else new_description_list
    
    sentiment_text = sentiment_keywords[sentiment_label]

    # 감정 대표 텍스트와 new_description 임베딩
    sentiment_embedding = model.encode(sentiment_text)
    descriptions_embeddings = model.encode(candidates)

    # 코사인 유사도 계산
    similarities = util.cos_sim(sentiment_embedding, descriptions_embeddings)
    
    top_k = 7  # 가져올 상위 개수
    
    # 랜덤성 추가: 상위 20개 중에서 7개 랜덤 선택
    top_n = min(20, len(candidates))  # 전체 후보가 20개보다 적을 경우 처리
    top_indices = similarities.argsort(descending=True)[:top_n]
    
    # 랜덤하게 7개 선택 (중복 제거)
    import random
    selected_indices = random.sample(top_indices.flatten().tolist(), min(top_k, top_n))
    
    # Extract descriptions using the indices
    top_descriptions = [candidates[idx] for idx in selected_indices]

    return top_descriptions

def recommend_reason(diary_content: str, emotion: str, song_data: dict) -> dict:
    """
    일기 내용과 감정을 기반으로 OpenAI를 사용하여 감정에 맞는 음악을 추천하는 이유를 생성하는 함수입니다.
    :param diary_content: 사용자가 작성한 일기 내용
    :param emotion: 감정 상태 (예: 슬픔, 우울 등)
    :param song_data: 추천된 노래 정보 (title, artist, description 포함)
    :return: 추천 이유를 포함한 딕셔너리
    """
    try:
        song_title = getattr(song_data, 'title', "추천 결과 없음")
        song_artist = getattr(song_data, 'artist', "추천 결과 없음")
        song_description = getattr(song_data, 'description', "추천 결과 없음")

        
        prompt = f"""
        예시)
        '일기 내용' : 오늘은 아침부터 비가 왔다. 그래서 엄마한테 학교로 데려달라고 했는데 거절당했다. 
                     우울한 기분에 깜빡하고 숙제를 챙기지 않았다. 근데 선생님한테 숙제를 안 해왔다고 혼났다.
                     기분전환하러 엄마랑 쇼핑하러 갔다. 근데 내가 원하는 옷들이 없어서 너무 너무 슬펐다. 
                     오늘은 되는 게 하나도 없는 날인가보다ㅠㅠ
        '감정' : 슬픈, 우울한, 스트레스
        '노래' : Day6 - Happy
        '노래 설명' : 점점 커지는 벽에 부딪히며 애달픈 마음을 솔직하게 털어놓는 곡. 슬프지만 특별한 공감을 전해준다
        '추천 이유' : 슬픈 감정을 위로해주고 힘든 순간을 극복하는 데 큰 도움이 될 거예요.

        {diary_content}의 감정은 {emotion}인데, 추천 노래는 {song_artist}의 {song_title}이고 추천 노래의 설명은 {song_description}이야. 
        예시를 참고하여, '추천 이유'를 "감정 효과 + 도움 내용"의 구조로 한 줄로 존댓말로 적어줘.
        출력 형식(JSON):
        {{
            "reason": "추천 이유"
        }}
        """

        # OpenAI ChatCompletion 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that generates reasons for music recommendations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        # 응답 파싱
        response_text = response['choices'][0]['message']['content'].strip()
        result = json.loads(response_text)  # JSON 형식으로 파싱

        # 추천 이유 추출
        reason = result.get("reason", "추천 이유 생성 실패")

        return {"reason": reason}

    except json.JSONDecodeError as json_error:
        return {"error": "JSON 파싱 실패", "details": str(json_error)}
    except Exception as e:
        raise Exception(f"Error recommending music: {str(e)}")
   
    
    
# LLM 다 합침 (감정 분석, 음악 추천, 음악 추천 이유)
# 3. 감정 분석 결과를 기반으로, 아래 노래 데이터 중 가장 적합한 노래를 선택합니다. 노래의 데이터의 "description"을 참고하여 감정과 가장 유사한 노래를 고르세요
def LLM(diary_content):
    try:

        prompt = f"""
        아래의 일기 내용을 기반으로 감정을 분석하고, 추천 노래 및 이유를 작성하세요.
        1. 입력된 일기 내용에서 감정을 분석하여 주어진 sentiment_keywords 중에서 가장 연관이 있는 'sentiment_1' ~ 'sentiment_5' 중 하나를 선택합니다.
        2. 선택된 감정에 적합한 감정 키워드 3개를 한국어로 반환합니다.
        3. 감정 분석 결과를 기반으로, 감정과 가장 유사한 노래를 고르세요.        
        4. 추천된 노래에 대해 "감정 효과 + 도움 내용"의 구조로 존댓말로 작성된 추천 이유를 반환합니다.
        
        출력 형식 (JSON):
        {{
            "sentiment": "선택된 감정",
            "similar_words": ["키워드1", "키워드2", "키워드3"],
            "recommended_song": {{
                "title": "추천된 노래 제목",
                "artist": "추천된 노래 아티스트",
                "description": "노래 설명"
            }},
            "reason": "추천 이유"
        }}
        
        입력된 일기 내용: "{diary_content}"
        sentiment_keywords: {sentiment_keywords}
        """

        # OpenAI API 호출 
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that analyzes diary entries and recommends music."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        # 결과 파싱
        response_text = response['choices'][0]['message']['content'].strip()
        result = json.loads(response_text)

        # 결과에서 필요한 정보 추출
        sentiment = result.get("sentiment")
        similar_words = result.get("similar_words")
        recommended_song = result.get("recommended_song")
        reason = result.get("reason")

        if not all([sentiment, similar_words, recommended_song, reason]):
            raise ValueError("Some required fields are missing in the response.")

        # 최종 결과 반환
        return {
            "sentiment": sentiment,
            "keywords": similar_words,
            "song": recommended_song,
            "reason": reason
        }

    except json.JSONDecodeError as json_error:
        return {"error": "JSON parsing failed", "details": str(json_error)}
    except KeyError as key_error:
        return {"error": "Missing required key in response", "details": str(key_error)}
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}
 