//'좋아요' / '싫어요' 기능 구현
const likeBtn = document.getElementById('like-btn');
const dislikeBtn = document.getElementById('dislike-btn');

likeBtn.addEventListener('click', function() {
    const likeEmpty = '/static/DiaryTune/images/heart-1.png';
    const likeFill = '/static/DiaryTune/images/heart-2.png';
    
    // URL에서 현재 날짜 정보 가져오기
    const urlParts = window.location.pathname.split('/').filter(part => part);
    const baseIndex = urlParts.indexOf('recommendation');
    const currentYear = urlParts[baseIndex + 1];
    const currentMonth = urlParts[baseIndex + 2];
    const currentDay = urlParts[baseIndex + 3];
    
    if (this.src.includes('heart-1')) {
        this.src = likeFill;
        dislikeBtn.src = '/static/DiaryTune/images/dislike_empty.png';
        
        // 좋아요 상태를 서버에 저장
        fetch(`/DiaryTune/like/${currentYear}/${currentMonth}/${currentDay}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                liked: true
            })
        });
    } else {
        this.src = likeEmpty;
        
        // 좋아요 취소 상태를 서버에 저장
        fetch(`/DiaryTune/like/${currentYear}/${currentMonth}/${currentDay}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                liked: false
            })
        });
    }
});

// 페이지 로드 시 좋아요 상태 확인
document.addEventListener('DOMContentLoaded', function() {
    const urlParts = window.location.pathname.split('/').filter(part => part);
    const baseIndex = urlParts.indexOf('recommendation');
    const currentYear = urlParts[baseIndex + 1];
    const currentMonth = urlParts[baseIndex + 2];
    const currentDay = urlParts[baseIndex + 3];
    
    // 서버에서 좋아요 상태 가져오기
    fetch(`/DiaryTune/like/${currentYear}/${currentMonth}/${currentDay}/`)
        .then(response => response.json())
        .then(data => {
            if (data.liked) {
                likeBtn.src = '/static/DiaryTune/images/heart-2.png';
            } else {
                likeBtn.src = '/static/DiaryTune/images/heart-1.png';
            }
        });
});

dislikeBtn.addEventListener('click', function() {
    const dislikeEmpty = this.getAttribute('data-dislike-empty');
    const dislikeFill = this.getAttribute('data-dislike-fill');
    
    if (this.src.includes('empty')) {
        this.src = dislikeFill;
        likeBtn.src = likeBtn.getAttribute('data-like-empty');
        
        // URL에서 현재 날짜 정보 가져오기
        const urlParts = window.location.pathname.split('/').filter(part => part);
        const baseIndex = urlParts.indexOf('recommendation');
        const currentYear = urlParts[baseIndex + 1];
        const currentMonth = urlParts[baseIndex + 2];
        const currentDay = urlParts[baseIndex + 3];
        const currentDayOfWeek = urlParts[baseIndex + 4];
        
        const recommend_url = `/DiaryTune/recommendation/${currentYear}/${currentMonth}/${currentDay}/${currentDayOfWeek}/`;
        window.location.href = recommend_url;
    } else {
        this.src = dislikeEmpty;
    }
});

// CSRF 토큰 가져오기
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 'Play' 버튼 누르면 유튜브 연결
document.getElementById('play-btn').addEventListener('click', function() {
    // 가수와 노래 제목 가져오기
    const musicBox = document.querySelector('.musicbox');

    const title = musicBox.getAttribute('data-title');
    const artist = musicBox.getAttribute('data-artist');

    // YouTube 검색 URL 생성
    const query = encodeURIComponent(`${artist} ${title}`);
    const youtubeUrl = `https://www.youtube.com/results?search_query=${query}`;

    // YouTube 검색 페이지로 이동
    window.location.href = youtubeUrl;
});
  
// '수정' 아이콘 누르면 해당 날짜에 맞는 'diary.html' 연결
document.querySelector('.modify').addEventListener('click', () => {
  // user가 선택한 날짜(년도, 월, 일, 요일(index)) 받기
  const urlParts = window.location.pathname.split('/').filter(part => part); // 빈 문자열 요소 제거
  const baseIndex = urlParts.indexOf('recommendation');
  const currentYear = urlParts[baseIndex + 1];  
  const currentMonth = urlParts[baseIndex + 2]; 
  const currentDay = urlParts[baseIndex + 3];  
  const dayofweek = urlParts[baseIndex + 4]; 

  window.location.href = `/DiaryTune/diary/${currentYear}/${currentMonth}/${currentDay}/${dayofweek}`; // 이동할 URL
});

// '<(뒤로 가기)' 아이콘 누르면 해당 날짜에 맞는 'main.html'로 이동
document.querySelector('.back').addEventListener('click', () => {
  // 이동할 URL
  const url = document.querySelector('#exit-url').getAttribute('data-url');
  window.location.href = url;
});

// '삭제' 아이콘 누르면 해당 날짜의 일기 삭제되고 해당 날짜에 맞는 'main.html'로 이동
document.querySelector('.trash').addEventListener('click', () => {
    swal({
        title: "이 작업은 되돌릴 수 없어요.",
        text: "정말 삭제하시겠어요? 🥹 ",
        icon: "warning",
        buttons: ["취소", "삭제"],
        dangerMode: true,
    }).then((willDelete) => {
        if (willDelete) {
          // user가 선택한 날짜(년도, 월, 일, 요일(index)) 받기
          const urlParts = window.location.pathname.split('/').filter(part => part); // 빈 문자열 요소 제거
          const baseIndex = urlParts.indexOf('recommendation');
          const currentYear = urlParts[baseIndex + 1];  
          const currentMonth = urlParts[baseIndex + 2]; 
          const currentDay = urlParts[baseIndex + 3];  
          
          // 삭제 요청 URL
          const deleteUrl = `/DiaryTune/diary/delete/${currentYear}/${currentMonth}/${currentDay}/`;
          
          // 삭제 요청을 보내기
          window.location.href = deleteUrl;

        } 
    });
});

// user가 선택한 날짜 상단에 보여주기
document.addEventListener("DOMContentLoaded", () => {
    const view9Element = document.querySelector(".bar .date");

    if (view9Element) {
        // user가 선택한 날짜(월, 일, 요일(index)) 받기  
        const month = view9Element.getAttribute("data-month");
        const day = view9Element.getAttribute("data-day");
        const dayofweek = view9Element.getAttribute("data-dayofweek");

        const dayNames = ["일", "월", "화", "수", "목", "금", "토"];
        const dayOfWeekName = dayNames[parseInt(dayofweek)];

        if (month && day && dayOfWeekName) {
            // 한글 요일로 텍스트 업데이트
            const dateText = `${month}월 ${day}일 (${dayOfWeekName})`;
            view9Element.textContent = dateText;
        } else {
            console.error("Date parameters are missing");
        }
    } else {
        console.error("date element not found");
    }
});

// DB에 저장된 오늘의 활동, 날씨 UI에 제공
document.addEventListener('DOMContentLoaded', () => {
    // 날씨 이미지 설정
    const weather1 = document.querySelector('.weather1');
    const weather2 = document.querySelector('.weather2');
    if (weather1) {
        const weather1Img = weather1.getAttribute('data-weather-img');
        if (weather1Img) {
            weather1.style.backgroundImage = `url(${weather1Img})`;
        }
    }
    if (weather2) {
        const weather2Img = weather2.getAttribute('data-weather-img');
        if (weather2Img) {
            weather2.style.backgroundImage = `url(${weather2Img})`;
        }
    }

    // 활동 이미지 설정
    const activity1 = document.querySelector('.activity1');
    const activity2 = document.querySelector('.activity2');
    if (activity1) {
        const activity1Img = activity1.getAttribute('data-activity-img');
        if (activity1Img) {
            activity1.style.backgroundImage = `url(${activity1Img})`;
        }
    }
    if (activity2) {
        const activity2Img = activity2.getAttribute('data-activity-img');
        if (activity2Img) {
            activity2.style.backgroundImage = `url(${activity2Img})`;
        }
    }
});

document.querySelectorAll('.musics').forEach(element => {
    const text = element.textContent.replace(/[#\s-]/g, ''); // #, 공백, - 기호 제거
    const length = text.length;
    
    if (length <= 15) { // 실제 텍스트가 10자 이하일 경우
        element.style.fontSize = '10px';
    } else {
        element.style.fontSize = '8px';
    }
});

// 음악 제목 폰트 크기 조절
document.querySelectorAll('.music_title').forEach(element => {
    // 모바일 체크 (화면 너비가 750px 이하인 경우 모바일로 간주)
    if (window.innerWidth > 750) {
        const text = element.textContent.replace(/[#\s-]/g, ''); // #, 공백, - 기호 제거
        const length = text.length;
        
        if (length <= 20) { // 실제 텍스트가 20자 이하일 경우
            element.style.fontSize = '16px';
        } else {
            element.style.fontSize = '13px';
        }
    }
    // 모바일의 경우 CSS의 설정을 따름
});