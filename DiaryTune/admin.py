from .models import Diary, csv_file
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render
import csv

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

# csv_file 모델을 위한 Admin 설정
class csv_fileAdmin(admin.ModelAdmin):
     # 목록에 표시할 필드
    list_display = ('title', 'artist', 'album', 'lyrics', 'original_description', 'new_description')
    
    # 검색 필드 설정
    search_fields = ('title', 'artist', 'new_description')
    
    # 필터 추가
    list_filter = ('artist', 'album')
    
    change_list_template = 'admin/upload_csv.html'  # 커스텀 업로드 CSV 페이지
    list_per_page = 20  # 한 페이지에 20개 항목 표시
    
    
    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path('upload-csv/', self.upload_csv)  # 업로드 페이지 URL 추가
    #     ]
    #     return custom_urls + urls

    # def upload_csv(self, request):
    #     if request.method == 'POST' and request.FILES['csv_file']:
    #         csv_file = request.FILES['csv_file']
    #         decoded_file = csv_file.read().decode('utf-8').splitlines()
    #         reader = csv.reader(decoded_file)

    #         next(reader)  # CSV 헤더 건너뛰기

    #         for row in reader:
    #             csv_file.objects.create(
    #                 title=row[0],
    #                 artist=row[1],
    #                 mood=row[2],
    #                 description=row[3]
    #             )
    #         self.message_user(request, "CSV 파일이 성공적으로 업로드되었습니다.")
    #         return HttpResponse(status=200)
        
    #     self.message_user(request, "CSV 파일 업로드 실패! 다시 시도해 주세요.", level='error')
    #     return render(request, 'admin/upload_csv.html')

admin.site.register(csv_file, csv_fileAdmin)