from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .models import Diary
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

def main(request, year=None, month=None, day=None):
    context = {
        'year': year,
        'month': month,
        'day': day,
    }
    return render(request, 'DiaryTune/main/main.html', context)

def diary1(request, year=None, month=None, day=None, dayofweek=None):
    context = {
        'year': year,
        'month': month,
        'day': day,
        'dayofweek': dayofweek,
    }
    return render(request, 'DiaryTune/diary/diary.html', context)

def diary(request, year=None, month=None, day=None, dayofweek=None):
    if request.method == 'POST':
        # POST 요청으로 데이터 저장 처리
        try:
            data = json.loads(request.body)

            activities = data.get('activities', [])
            weather = data.get('weather', [])
            diary_content = data.get('diary', '')

            # Diary 객체를 업데이트 또는 생성
            diary = Diary.objects.create(
                year=year,
                month=month,
                day=day,
                activities=activities,
                weather=weather,
                diary_content=diary_content
            )
            
            # 저장이 잘 되었는지 확인
            print(f"Diary saved successfully: {diary}")

            # Diary 저장 후 main 페이지로 리디렉션
            return JsonResponse({"message": "Diary saved successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    else:
        # GET 요청으로 다이어리 페이지 보여주기
        context = {
            'year': year,
            'month': month,
            'day': day,
            'dayofweek': dayofweek,
        }
        return render(request, 'DiaryTune/diary/diary.html', context)

def save_diary(request, year=None, month=None, day=None, dayofweek=None, diary_id=None):
    if request.method == 'POST':
        # 요청 본문에서 데이터를 JSON으로 파싱
        data = json.loads(request.body)
        
        # 요청에서 받은 데이터 추출
        activities = data.get('activities', [])
        weather = data.get('weather', [])
        diary_content = data.get('diary', '')

        try:
            # Diary 객체 업데이트 또는 생성
            diary = Diary.objects.get(id=diary_id)  # diary_id를 기반으로 Diary 객체를 찾음
            diary.year = year
            diary.month = month
            diary.day = day
            diary.activities = activities
            diary.weather = weather
            diary.diary_content = diary_content
            diary.save()  # DB에 저장

            # 성공적으로 저장되었다는 메시지 반환
            return JsonResponse({"message": "Diary saved successfully!"})

        except Diary.DoesNotExist:
            # Diary 객체가 없으면 새로운 객체 생성
            diary = Diary.objects.create(
                year=year,
                month=month,
                day=day,
                activities=activities,
                weather=weather,
                diary_content=diary_content
            )
            return JsonResponse({"message": "Diary created successfully!"})
        
    return JsonResponse({"message": "Invalid request method"}, status=400)

def recommendation(request):
    return render(request, 'DiaryTune/recommendation/music_recommendation.html')

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