from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import Diary
from .models import csv_file
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .utils import analyze_emotion, recommend_music 
import json
import csv

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


def recommendation(request, year=None, month=None, day=None, dayofweek=None):
    # 해당 날짜에 작성된 일기를 조회
    try:
        diary = Diary.objects.get(year=year, month=month, day=day)
        diary_content = diary.diary_content
        activities = json.loads(diary.activities) if diary.activities else []
        weathers = json.loads(diary.weather) if diary.weather else []

        # 감정 분석 수행
        emotion_analysis = analyze_emotion(diary_content)
        selected_emotion = emotion_analysis.get('selected_sentiment')
        similar_words = emotion_analysis.get('similar_words')

        # 음악 추천 수행
        music_recommendation = recommend_music(diary_content, similar_words[0])

        diary.selected_sentiment = selected_emotion
        diary.similar_words = similar_words
        diary.song_title = music_recommendation.get('title')
        diary.song_artist = music_recommendation.get('artist')
        diary.song_description = music_recommendation.get('description')
        diary.reason = music_recommendation.get('reason')
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
            'music_recommendation': music_recommendation,
            'artist': music_recommendation.get('artist') if music_recommendation else None,  # 가수
            'title': music_recommendation.get('title') if music_recommendation else None   # 노래 제목
    }
    return render(request, 'DiaryTune/recommendation/music_recommendation.html', context)


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