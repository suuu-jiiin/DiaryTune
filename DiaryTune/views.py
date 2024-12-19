from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.templatetags.static import static
from .models import Diary
from .models import csv_file
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .utilsreal import analyze_emotion, recommend_music, recommend_reason
from django.db.models import Count
from sentence_transformers import SentenceTransformer
import json
import random
from datetime import datetime, date, timedelta
from django.views.decorators.http import require_http_methods
from django.utils import timezone

def main(request, year=None, month=None, day=None):

    # 해당 월의 감정 카운트만 계산
    sentiment_totals = Diary.objects.filter(
        year=year,
        month=month
    ).values('selected_sentiment').annotate(
        count=Count('selected_sentiment')
    ).order_by('selected_sentiment')

    # 감정별 카운트를 딕셔너리로 변환
    sentiment_counts = {
        'sentiment_1': 0,
        'sentiment_2': 0,
        'sentiment_3': 0,
        'sentiment_4': 0,
        'sentiment_5': 0
    }
    
    for item in sentiment_totals:
        if item['selected_sentiment']:  # None 체크
            sentiment_counts[item['selected_sentiment']] = item['count']

    # 모든 날짜의 일기 데이터 가져오기 (예시)
    diary_data = Diary.objects.filter(year=year, month=month)

    # 날짜별 데이터 구성
    diary_data_list = []
    for diary in diary_data:
        diary_data_list.append({
            'day': diary.day,
            'sentiment': diary.selected_sentiment,
            'sentiment_image': f'images/sentiments/{diary.selected_sentiment}.png' if diary.selected_sentiment else None
        })

    context = {
        'year': year,
        'month': month,
        'sentiment_totals': sentiment_counts,
        'diary_data': diary_data_list,  # 템플릿에서 사용할 diary_data 추가
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
            
            # 감정 분석 실행 with LLM
            emotion_analysis = analyze_emotion(diary_content)
            sentiment = emotion_analysis.get('sentiment')
            keywords = emotion_analysis.get('keywords')


            # 기존 다이어리가 있다면 업데이트, 없다면 새로 생성
            diary, created = Diary.objects.update_or_create(
                year=year,
                month=month,
                day=day,
                defaults={
                    'activities': json.dumps(activities),  # 리스트를 JSON으로 저장
                    'weather': json.dumps(weather),  # 리스트를 JSON으로 저장
                    'diary_content': diary_content,
                    'selected_sentiment': sentiment,  # 감정 결과 저장
                    'similar_words': keywords,  # 키워드를 JSON으로 저장
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
            sentiment = diary.selected_sentiment

            context = {
                'year': year,
                'month': month,
                'day': day,
                'dayofweek': dayofweek,
                'diary_content': diary.diary_content,
                'activities': activities,
                'weather': weather,
                'sentiment': sentiment,
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
                'sentiment': None,
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
    try:
        diary = Diary.objects.get(year=year, month=month, day=day)
        diary_content = diary.diary_content
        activities = json.loads(diary.activities) if diary.activities else []
        weathers = json.loads(diary.weather) if diary.weather else []
        sentiment = diary.selected_sentiment
        keywords = diary.similar_words

        # 좋아요가 눌려있지 않은 경우 새로운 추천 실행
        if not diary.like:
            # 음악 추천 with BERT
            description_list = get_new_descriptions()
            music_recommendation = recommend_music(sentiment, description_list)
            random_description = random.choice(music_recommendation)
            
            # 랜덤으로 선택한 설명으로 song_data 조회
            song_data = csv_file.objects.filter(description=random_description).first()
            
            # 추천된 음악 정보 저장
            diary.song_title = song_data.title if song_data else "추천 결과 없음"
            diary.song_artist = song_data.artist if song_data else "추천 결과 없음"
            diary.song_description = random_description
            
            # 음악 추천 이유 with LLM
            recommendation_reason = recommend_reason(diary_content, keywords[0], song_data)
            diary.reason = recommendation_reason.get('reason')
            diary.save()
        
        context = {
            'year': year,
            'month': month,
            'day': day,
            'dayofweek': dayofweek,
            'diary_content': diary_content,
            'emotion_analysis': {
                "sentiment": sentiment,
                "keywords": keywords,
            },
            'activities': activities,
            'weather': weathers,
            "music_recommendation": {
                "description": diary.song_description,
                "reason": diary.reason,
                "title": diary.song_title,
                "artist": diary.song_artist,
            },
        }

    except Diary.DoesNotExist:
        context = {
            'year': year,
            'month': month,
            'day': day,
            'dayofweek': dayofweek,
            'diary_content': None,
            'emotion_analysis': None,
            'activities': [],
            'weathers': [],
            'music_recommendation': None,
        }

    return render(request, 'DiaryTune/recommendation/music_recommendation.html', context)

# DB에 있는 CSV 파일에서 new_description 데이터를 읽어오기
def get_new_descriptions():
    
    # ORM을 사용하여 모든 description 필드 데이터 가져오기
    descriptions = list(csv_file.objects.values_list('description', flat=True))
    return descriptions

# 이달의 음표 Count
def sentiment_count_view():
    # 감정별 개수 집계
    sentiment_counts = Diary.objects.values('selected_sentiment').annotate(count=Count('selected_sentiment'))

    # 모든 감정을 포함하여 count 초기화
    sentiment_totals = {
        'sentiment_1': 0,
        'sentiment_2': 0,
        'sentiment_3': 0,
        'sentiment_4': 0,
        'sentiment_5': 0,
    }

    # 집계 결과 영
    for sentiment in sentiment_counts:
        sentiment_totals[sentiment['selected_sentiment']] = sentiment['count']

    return sentiment_totals

def get_sentiment(request, year, month):
    diary_entries = Diary.objects.filter(date__year=year, date__month=month)
    
    diary_data = []
    sentiment_images = {
        "sentiment_1": "static/DiaryTune/images/sentiment_1.png",
        "sentiment_2": "static/DiaryTune/images/sentiment_2.png",
        "sentiment_3": "static/DiaryTune/images/sentiment_3.png",
        "sentiment_4": "static/DiaryTune/images/sentiment_4.png",
        "sentiment_5": "static/DiaryTune/images/sentiment_5.png",
    }

    for entry in diary_entries:
        diary_data.append({
            "day": entry.date.day,
            "sentiment": entry.sentiment,
            "sentiment_image": sentiment_images.get(entry.sentiment, "DiaryTune/images/default.jpg"),
        })
    
    return render(request, "main.html", {"diary_data": diary_data})

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
        # 해당 날짜의 Diary 객체 가져오기
        diary = Diary.objects.filter(year=year, month=month, day=day).first()
        
        if diary:
            return JsonResponse({
                "exists": True,
                "sentiment": diary.selected_sentiment  # selected_sentiment 값도 함께 반환
            })
        else:
            return JsonResponse({
                "exists": False,
                "sentiment": None
            })
            
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
        
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
            return JsonResponse({
                'message': 'Diary saved successfully!',
                'sentiment': sentiment,  # 분석된 감정 값을 여기 포함
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        # GET 요청은 처리하지 않음
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

def monthly_report(request):
    # URL 파라미터에서 year와 month를 가져옴
    year = int(request.GET.get('year', date.today().year))
    month = int(request.GET.get('month', date.today().month))
    
    # 해당 월의 마지막 날짜 계산
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    last_day = (next_month - timedelta(days=1)).day
    
    diary_entries = Diary.objects.filter(
        year=year,
        month=month,
        day__lte=last_day
    ).order_by('year', 'month', 'day')
    
    date_labels = []
    sentiment_scores = []
    
    sentiment_mapping = {
        'sentiment_1': 1,
        'sentiment_2': 2,
        'sentiment_3': 3,
        'sentiment_4': 4,
        'sentiment_5': 5
    }
    
    for entry in diary_entries:
        date_str = f"{entry.month}/{entry.day}"
        date_labels.append(date_str)
        sentiment_scores.append(sentiment_mapping.get(entry.selected_sentiment, 0))

    # 활동 랭킹 계산 수정
    activity_ranking = []
    weather_ranking = []
    
    for entry in diary_entries:
        # JSON 문자열을 파이썬 리스트로 변환
        activities = json.loads(entry.activities) if entry.activities else []
        weather = json.loads(entry.weather) if entry.weather else []
        
        # 각 활동과 날씨를 개별적으로 카운트
        for activity in activities:
            activity_ranking.append(activity)
        for w in weather:
            weather_ranking.append(w)
    
    # 활동 빈도수 계산
    activity_counts = {}
    for activity in activity_ranking:
        activity_counts[activity] = activity_counts.get(activity, 0) + 1
    
    # 날씨 빈도수 계산
    weather_counts = {}
    for w in weather_ranking:
        weather_counts[w] = weather_counts.get(w, 0) + 1
    
    # 상위 3개 추출
    top_activities = sorted(activity_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    top_weather = sorted(weather_counts.items(), key=lambda x: x[1], reverse=True)[:3]

    context = {
        'month': month,
        'date_labels': date_labels,
        'sentiment_scores': sentiment_scores,
        'activity_ranking': [{'activity': act[0], 'count': act[1]} for act in top_activities],
        'weather_ranking': [{'weather': w[0], 'count': w[1]} for w in top_weather],
    }
    return render(request, 'DiaryTune/reports/monthly_report.html', context)

@require_http_methods(["GET", "POST"])
def like_diary(request, year, month, day):
    try:
        # 해당 날짜의 일기 찾기 (year, month, day 개별 필드 사용)
        diary = Diary.objects.get(
            year=year,
            month=month,
            day=day
        )
        
        if request.method == "POST":
            # POST 요청일 경우 좋아요 상태 업데이트
            data = json.loads(request.body)
            diary.like = data.get('liked', False)  
            diary.save()
            
        # GET 요청이거나 POST 처리 후 현재 상태 반환
        return JsonResponse({'liked': diary.like})  
        
    except Diary.DoesNotExist:
        return JsonResponse({'error': 'Diary not found'}, status=404)

def get_monthly_sentiments(request, year, month):
    sentiment_totals = Diary.objects.filter(
        year=year,
        month=month
    ).values('selected_sentiment').annotate(
        count=Count('selected_sentiment')
    )

    sentiment_counts = {
        'sentiment_1': 0,
        'sentiment_2': 0,
        'sentiment_3': 0,
        'sentiment_4': 0,
        'sentiment_5': 0
    }
    
    for item in sentiment_totals:
        if item['selected_sentiment']:  # None 체크
            sentiment_counts[item['selected_sentiment']] = item['count']

    return JsonResponse(sentiment_counts)