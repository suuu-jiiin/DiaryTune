from .utilsreal import analyze_emotion, recommend_music, recommend_reason
import pandas as pd

# 파일 경로
file_path = r"C:\Users\toozi\HCI\DiaryTune\new_song_info.csv"

# 'New Description' 열 읽어오기
df = pd.read_csv(file_path)
new_description_list = df['New Description'].dropna().tolist()  # 결측값 제거 후 리스트로 변환



def get_recommendation_counts(sentiment_labels, new_description_list):
    sentiment_counts = {}

    for sentiment_label in sentiment_labels:
        # 추천된 노래 리스트
        recommended_songs = recommend_music(sentiment_label, new_description_list)
        
        # 추천된 노래 개수 기록
        sentiment_counts[sentiment_label] = len(recommended_songs)
    
    return sentiment_counts

# 감정 키워드 사전
sentiment_keywords = {
    "sentiment_1": ["화난", "짜증", "적대적", "좌절", "냉담한"],
    "sentiment_2": ["걱정되는", "슬픈", "불안한", "피곤한", "상처받은", "우울한"],
    "sentiment_3": ["부끄러운", "외로운", "지루한", "무기력한"],
    "sentiment_4": ["행복한", "만족하는", "사랑스러운", "쾌활한", "편안한"],
    "sentiment_5": ["자신있는", "용감한", "열정적인", "활기찬", "신난"]
}

# 각 감정에 따른 추천 노래 개수 출력 함수
def print_recommendation_counts(sentiment_keywords, new_description_list):
    sentiment_counts = {}

    for sentiment_label, keywords in sentiment_keywords.items():
        # 추천된 노래 리스트
        recommended_songs = recommend_music(sentiment_label, new_description_list)
        
        # 추천된 노래 개수 기록
        sentiment_counts[sentiment_label] = len(recommended_songs)
        print(f"Sentiment '{sentiment_label}' has {len(recommended_songs)} recommended songs.")
    
    return sentiment_counts

# 실행
sentiment_counts = print_recommendation_counts(sentiment_keywords, new_description_list)
