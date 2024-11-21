// '좋아요' 기능 구현
document.getElementById('heart').addEventListener('click', function() {
    const heartImage = this;
    const heartOn = heartImage.getAttribute('data-heart-on'); // heart-2 이미지 경로
    const heartOff = heartImage.getAttribute('data-heart-off'); // heart-1 이미지 경로

    // 현재 이미지를 heart-1에서 heart-2로 변경하고 다시 heart-1로 되돌리기
    if (heartImage.src.includes(heartOff)) {
        heartImage.src = heartOn;
    } else {
        heartImage.src = heartOff;
    }
});

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