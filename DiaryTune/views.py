from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import Diary
from .models import csv_file
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .utilsreal import analyze_emotion, recommend_reason, recommend_music, LLM 
# 아래는 내가 설정한 recommend_music 함수를 Django에서 호출
#from .utilsrecommendation import recommend_music
from sentence_transformers import SentenceTransformer
import json
import random

def main(request, year=None, month=None, day=None):
    context = {
        'year': year,
        'month': month,
        'day': day,
    } 
    return render(request, 'DiaryTune/main/main.html', context)

def diary(request, year=None, month=None, day=None, dayofweek=None):
    if request.method == 'POST':
        # POST 요청으로 데이터 저장 처리
        try:
            # POST 요청에서 JSON 데이터 받기
            data = json.loads(request.body)
            
            activities = data.get('activities', [])
            weather = data.get('weather', [])
            diary_content = data.get('diary', '')

            # 기존 다이어리가 있다면 업데이트, 없다면 새로 생성
            diary, created = Diary.objects.update_or_create(
                year=year,
                month=month,
                day=day,
                defaults={
                    'activities': json.dumps(activities),  # 리스트를 JSON으로 저장
                    'weather': json.dumps(weather),  # 리스트를 JSON으로 저장
                    'diary_content': diary_content,
                }
            )
            
            if created:
                message = "Diary created successfully!"
            else:
                message = "Diary updated successfully!"

            # 저장이 잘 되었는지 확인
            print(f"Diary saved successfully: {diary}")

            # 성공 메시지 리턴
            return JsonResponse({"message": message})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    else:
        # GET 요청으로 다이어리 페이지 보여주기
        try:
            # 해당 날짜의 다이어리 가져오기
            diary = Diary.objects.get(year=year, month=month, day=day)

            # Diary의 활동과 날씨를 리스트로 변환
            activities = json.loads(diary.activities) if diary.activities else []
            weather = json.loads(diary.weather) if diary.weather else []

            context = {
                'year': year,
                'month': month,
                'day': day,
                'dayofweek': dayofweek,
                'diary_content': diary.diary_content,
                'activities': activities,
                'weather': weather,
            }

        except Diary.DoesNotExist:
            # 만약 다이어리가 없으면 기본값을 전달
            context = {
                'year': year,
                'month': month,
                'day': day,
                'dayofweek': dayofweek,
                'diary_content': '',
                'activities': [],
                'weather': [],
            }

        return render(request, 'DiaryTune/diary/diary.html', context)


def delete_diary(request, year, month, day):
    # 해당 날짜의 일기를 가져옴
    diary = get_object_or_404(Diary, year=year, month=month, day=day)
    
    # 일기 삭제
    diary.delete()
    
    # 삭제 후 main 페이지로 리디렉션
    return redirect('main')  # 여기서 'main'은 main 화면을 표시하는 URL 이름입니다

# def recommendation(request, year=None, month=None, day=None, dayofweek=None):
#     # 해당 날짜에 작성된 일기를 조회
#     try:
#         diary = Diary.objects.get(year=year, month=month, day=day)
#         diary_content = diary.diary_content
#         activities = json.loads(diary.activities) if diary.activities else []
#         weathers = json.loads(diary.weather) if diary.weather else []

#         # LLM 모델 이용
#         llm_result = LLM(diary_content)
#         selected_sentiment = llm_result.get('sentiment')
#         keywords = llm_result.get('keywords')
#         song_data = llm_result.get('song', {})
#         song_title = song_data.get('title', "No Title")
#         song_artist = song_data.get('artist', "No Artist")
#         song_description = song_data.get('description', "No Description")
#         reason = llm_result.get('reason', "No Reason")
        
#         # Diary 객체 업데이트
#         diary.selected_sentiment = selected_sentiment
#         diary.similar_words = keywords
#         diary.song_title = song_title
#         diary.song_artist = song_artist
#         diary.song_description = song_description
#         diary.reason = reason
#         diary.save()

#     except Diary.DoesNotExist:
#         diary_content = None
#         selected_sentiment = None
#         activities = []
#         weathers = []
#         song_title = "No Title"
#         song_artist = "No Artist"
#         song_description = "No Description"
#         reason = "No Reason"

#     # 컨텍스트 구성
#     context = {
#         'year': year,
#         'month': month,
#         'day': day,
#         'dayofweek': dayofweek,
#         'diary_content': diary_content,
#         'selected_sentiment': selected_sentiment, 
#         'emotion_analysis': None,
#         'activities': activities,
#         'weather': weathers,
#         "music_recommendation": {
#             "description": song_description,
#             "reason": reason,
#             "title": song_title,
#             "artist": song_artist,
#         },
#     }
#     return render(request, 'DiaryTune/recommendation/music_recommendation.html', context)


def recommendation(request, year=None, month=None, day=None, dayofweek=None):
    # 해당 날짜에 작성된 일기를 조회
    try:
        diary = Diary.objects.get(year=year, month=month, day=day)
        diary_content = diary.diary_content
        activities = json.loads(diary.activities) if diary.activities else []
        weathers = json.loads(diary.weather) if diary.weather else []

        # 음악 추천 수행
        # CSV 파일에서 데이터 읽기
        description_list = get_new_descriptions()
        
        # 감정 분석 실행 with LLM
        emotion_analysis = analyze_emotion(diary_content)
        sentiment = emotion_analysis.get('sentiment')
        keywords = emotion_analysis.get('keywords')
        
        # 음악 추천 with BERT
        music_recommendation = recommend_music(sentiment, description_list)
        
        # 추천 결과 관련 데이터 가져오기
        #song_data = csv_file.objects.filter(description=music_recommendation).first()
        random_description = random.choice(music_recommendation)
        
        # 랜덤으로 선택한 설명으로 song_data 조회
        song_data = csv_file.objects.filter(description=random_description).first()
        song_title = song_data.title if song_data else "추천 결과 없음"
        song_artist = song_data.artist if song_data else "추천 결과 없음"
        song_description = random_description
        
        # 음악 추천 이유 with LLM
        recommendation_reason = recommend_reason(diary_content, keywords[0], song_data)
        
        diary.selected_sentiment = sentiment
        diary.similar_words = keywords
        diary.song_title = song_title
        diary.song_artist = song_artist
        diary.song_description = song_description
        diary.reason = recommendation_reason.get('reason')
        diary.save()

    except Diary.DoesNotExist:
        diary_content = None
        emotion_analysis = None
        activities = []
        weathers = []    
        music_recommendation = None

    context = {
            'year': year,
            'month': month,
            'day': day,
            'dayofweek': dayofweek,
            'diary_content': diary_content,
            'emotion_analysis': emotion_analysis,
            'activities': activities,
            'weather': weathers,
            "music_recommendation": {
                "description": song_description,
                "reason": recommendation_reason.get('reason'),
                "title": song_title,
                "artist": song_artist,
            },
    }
    return render(request, 'DiaryTune/recommendation/music_recommendation.html', context)

# DB에 있는 CSV 파일에서 new_description 데이터를 읽어오기
def get_new_descriptions():
    
    # ORM을 사용하여 모든 description 필드 데이터 가져오기
    descriptions = list(csv_file.objects.values_list('description', flat=True))
    return descriptions

def tutorial(request):
    return render(request, 'DiaryTune/tutorial/tutorial_1.html')

def tutorial_2(request):
    return render(request, 'DiaryTune/tutorial/tutorial_2.html')

def tutorial_3(request):
    return render(request, 'DiaryTune/tutorial/tutorial_3.html')

def tutorial_4(request):
    return render(request, 'DiaryTune/tutorial/tutorial_4.html')

def tutorial_5(request):
    return render(request, 'DiaryTune/tutorial/tutorial_5.html')

def tutorial_6(request):
    return render(request, 'DiaryTune/tutorial/tutorial_6.html')

def tutorial_7(request):
    return render(request, 'DiaryTune/tutorial/tutorial_7.html')

def check_diary(request, year, month, day):
    try:
        # 해당 날짜의 Diary가 있는지 확인
        diary_exists = Diary.objects.filter(year=year, month=month, day=day).exists()
        return JsonResponse({"exists": diary_exists})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    
# 음악 추천 제대로 되는지 확인
def test_recommendation(request):
    # DB에서 모든 곡의 title, artist, description 가져오기
    songs = csv_file.objects.all().values('title', 'artist', 'description')

    # 곡 설명 리스트와 매핑 정보 준비
    description_list = [song['description'] for song in songs]
    song_mapping = {song['description']: (song['title'], song['artist']) for song in songs}

    # 테스트할 감정 라벨
    sentiment_label = "sentiment_1"  # 예: 부끄러움, 외로움, 지루함, 무기력함과 같은 감정

    # 추천 실행
    recommended_description = recommend_music(sentiment_label, description_list)

    # 추천된 곡의 title, artist 조회
    song_title, song_artist = song_mapping.get(recommended_description, ("알 수 없음", "알 수 없음"))

    # 결과 반환
    return JsonResponse({
        "추천된 곡 설명": recommended_description,
        "추천된 곡 제목": song_title,
        "추천된 곡 아티스트": song_artist,
    })
    
def toggle_like(request, diary_id):
    if request.method == 'POST':
        try:
            diary = Diary.objects.get(id=diary_id)
            diary.like = not diary.like  # 현재 상태 반전
            diary.save()  # 변경 사항 저장
            return JsonResponse({'success': True, 'like': diary.like})  # 변경된 상태 반환
        except Diary.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Diary not found'})  # Diary가 없을 때
    return JsonResponse({'success': False, 'error': 'Invalid request method'})  # POST가 아닐 때


def save_diary(request, year, month, day):
    # POST 요청일 때만 처리하도록 조건 추가
    if request.method == 'POST':
        try:
            # 클라이언트에서 보낸 데이터 받기
            data = json.loads(request.body)

            # 활동, 날씨, 일기 내용
            activities = data.get('activities', [])
            weather = data.get('weather', [])
            diary_content = data.get('diary', '')

            # Diary 모델에 일기 내용 저장
            diary = Diary.objects.create(
                year=year,
                month=month,
                day=day,
                diary_content=diary_content,
                activities=json.dumps(activities),
                weather=json.dumps(weather)
            )
            
            # 감정 분석 실행
            emotion_analysis = analyze_emotion(diary_content)
            sentiment = emotion_analysis.get('sentiment')
            keywords = emotion_analysis.get('keywords')

            # 감정 분석 결과를 일기에 저장
            diary.selected_sentiment = sentiment
            diary.similar_words = keywords
            diary.save()

            # 성공적으로 처리했을 경우 응답 반환
            return JsonResponse({'message': 'Diary saved successfully!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        # GET 요청은 처리하지 않음
        return JsonResponse({'error': 'Invalid request method'}, status=405)