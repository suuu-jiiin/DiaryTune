from django.db.models import Count

def monthly_report(request, year, month):
    # ... existing code ...
    
    # 활동 랭킹 계산
    activity_ranking = DiaryEntry.objects.filter(
        created_at__year=year,
        created_at__month=month
    ).values('activities').annotate(
        count=Count('activities')
    ).order_by('-count')[:3]

    # 날씨 랭킹 계산
    weather_ranking = DiaryEntry.objects.filter(
        created_at__year=year,
        created_at__month=month
    ).values('weather').annotate(
        count=Count('weather')
    ).order_by('-count')[:3]

    context = {
        'month': month,
        'date_labels': date_labels,
        'sentiment_scores': sentiment_scores,
        'activity_ranking': activity_ranking,
        'weather_ranking': weather_ranking,
    }
    
    return render(request, 'DiaryTune/reports/monthly_report.html', context) 