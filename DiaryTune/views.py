from django.shortcuts import render

# Create your views here.
def main(request, year=None, month=None, day=None):
    context = {
        'year': year,
        'month': month,
        'day': day,
    }
    return render(request, 'DiaryTune/main/main.html', context)

def diary(request, year=None, month=None, day=None, dayofweek=None):
    context = {
        'year': year,
        'month': month,
        'day': day,
        'dayofweek': dayofweek,
    }
    return render(request, 'DiaryTune/diary/diary.html', context)

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