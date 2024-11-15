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

  document.getElementById('play-btn').addEventListener('click', function() {
  window.location.href = 'https://www.youtube.com/'; // 'intent://www.youtube.com/watch?v=VIDEO_ID#Intent;package=com.google.android.youtube;scheme=https;end;'
  });      
  
  // 페이지 이동 기능 추가
  document.querySelector('.modify').addEventListener('click', () => {
    // DiaryTune 경로 이후의 값을 가져옵니다.
    const urlParts = window.location.pathname.split('/').filter(part => part); // 빈 문자열 요소 제거
    const baseIndex = urlParts.indexOf('recommendation');
    const currentYear = urlParts[baseIndex + 1];  
    const currentMonth = urlParts[baseIndex + 2]; 
    const currentDay = urlParts[baseIndex + 3];  
    const dayofweek = urlParts[baseIndex + 4]; 
    window.location.href = `http://127.0.0.1:8000/DiaryTune/diary/${currentYear}/${currentMonth}/${currentDay}/${dayofweek}`; // modify가 이동할 URL
  });

  document.querySelector('.back').addEventListener('click', () => {
    // DiaryTune 경로 이후의 값을 가져옵니다.
    const urlParts = window.location.pathname.split('/').filter(part => part); // 빈 문자열 요소 제거
    const baseIndex = urlParts.indexOf('recommendation');
    const currentYear = urlParts[baseIndex + 1];  
    const currentMonth = urlParts[baseIndex + 2]; 
    const currentDay = urlParts[baseIndex + 3];  
    const dayofweek = urlParts[baseIndex + 4]; 
    window.location.href = `http://127.0.0.1:8000/DiaryTune/main/${currentYear}/${currentMonth}/${currentDay}/`; // back이 이동할 URL
  });

  document.querySelector('.trash').addEventListener('click', () => {
      swal({
          title: "이 작업은 되돌릴 수 없어요.",
          text: "정말 삭제하시겠어요? 🥹 ",
          icon: "warning",
          buttons: ["취소", "삭제"],
          dangerMode: true,
      }).then((willDelete) => {
          if (willDelete) {
            // 삭제 요청 URL
            // DiaryTune 경로 이후의 값을 가져옵니다.
            const urlParts = window.location.pathname.split('/').filter(part => part); // 빈 문자열 요소 제거
            const baseIndex = urlParts.indexOf('recommendation');
            const currentYear = urlParts[baseIndex + 1];  
            const currentMonth = urlParts[baseIndex + 2]; 
            const currentDay = urlParts[baseIndex + 3];  
            const dayofweek = urlParts[baseIndex + 4]; 
            
            const deleteUrl = `/DiaryTune/diary/delete/${currentYear}/${currentMonth}/${currentDay}/`;
            
            // 삭제 요청을 보내기
            window.location.href = deleteUrl;
            // 삭제 로직 실행
            // window.location.href = `http://127.0.0.1:8000/DiaryTune/main/`
          } 
      });
  });

  // 선택한 날짜 상단에 보여주기
document.addEventListener("DOMContentLoaded", () => {
    const view9Element = document.querySelector(".bar .date");

    if (view9Element) {
        // 'data-' 속성에서 Django 템플릿 변수 가져오기
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