from django.shortcuts import render
from django.http import HttpResponse
from .utils import crawl_data  # 크롤링을 위한 유틸리티 함수 임포트

def index(request):
    if request.method == 'POST':
        # POST 요청일 때, 사용자가 제출한 데이터 가져오기
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # 크롤링 코드 실행
        # result = crawl_data(date)
        crawl_data(start_date, end_date)

        # # 결과를 파일로 저장
        # with open('result.txt', 'w') as f:
        #     f.write(result)

        # 다운로드 링크 생성
        download_link = '/download/'

        # 결과 페이지 렌더링
        return render(request, 'templates/runpage/result.html', {'download_link': download_link})
    else:
        # GET 요청일 때, 입력 폼 렌더링
        return render(request, 'templates/runpage/index.html')
