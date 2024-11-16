from django.contrib import admin
from .models import Diary

class DiaryAdmin(admin.ModelAdmin):
    # 관리 페이지에서 보여줄 필드들 지정
    list_display = ('year', 'month', 'day', 'diary_content', 'get_activities', 'get_weather', 'created_at', 'updated_at')  # 필요한 필드들
    search_fields = ('diary_content',)  # 일기 내용으로 검색할 수 있도록 설정
    fields = ('year', 'month', 'day', 'diary_content')  # 필드 순서 지정
    list_filter = ('year', 'month')  # 연도와 월로 필터링 추가
    
    # 사용자가 작성한 일기만 보이도록 필터링
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # 관리자 권한을 가진 사용자는 모든 일기를 볼 수 있음
        return queryset.filter(user=request.user)  # 일반 사용자는 본인 작성 일기만 볼 수 있음
    
admin.site.register(Diary, DiaryAdmin)


