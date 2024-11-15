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


# class DiaryAdmin(admin.ModelAdmin):
#     # 표시할 필드 목록을 지정
#     list_display = ('year', 'month', 'day', 'diary_content', 'get_activities', 'get_weather', 'created_at', 'updated_at')
    
#     # 관리자 페이지에서 사용할 필드를 지정
#     fields = ('year', 'month', 'day', 'diary_content', 'activities', 'weather')
    
#     # 수정 페이지에서 각 필드를 나누어 표시할 수 있음
#     fieldsets = (
#         (None, {
#             'fields': ('year', 'month', 'day')
#         }),
#         ('Content', {
#             'fields': ('diary_content', 'activities', 'weather')
#         }),
#         ('Dates', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',),  # 이 필드는 접어서 보여줌
#         }),
#     )

#     # activities와 weather 필드를 문자열로 표시
#     def get_activities(self, obj):
#         return ', '.join(obj.get_activities())  # 리스트로 저장된 값들을 쉼표로 구분하여 출력

#     def get_weather(self, obj):
#         return ', '.join(obj.get_weather())  # 리스트로 저장된 값들을 쉼표로 구분하여 출력

# # 모델을 admin에 등록
# admin.site.register(Diary, DiaryAdmin)
