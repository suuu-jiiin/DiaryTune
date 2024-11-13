//오늘의 활동 두 개만 선택
const checkboxes = document.querySelectorAll('input[type="checkbox"].activity');

checkboxes.forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
        const checkedCount = document.querySelectorAll('input[type="checkbox"].activity:checked').length;
        if (checkedCount > 2) {
            checkbox.checked = false; // Uncheck the current box if the limit is exceeded
            swal({
              icon: "error",
              content: {
                  element: "p",
                  attributes: {
                      innerHTML: "최대 두 개만 선택할 수 있어요",
                  }
              }
          });
        }
    });
});

//오늘의 날씨 두 개만 선택
const checkboxes_weather = document.querySelectorAll('input[type="checkbox"].weather');

checkboxes_weather.forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
        // Count how many checkboxes are currently checked
        const checkedCount_weather = document.querySelectorAll('input[type="checkbox"].weather:checked').length;
    
        // If more than 2 checkboxes are selected, uncheck the latest one and show an alert
        if (checkedCount_weather > 2) {
            checkbox.checked = false; // Uncheck the current checkbox
            swal({
              icon: "error",
              content: {
                  element: "p",
                  attributes: {
                      innerHTML: "최대 두 개만 선택할 수 있어요",
                  }
              }
          });
        }
    });
});

// 선택한 날짜 상단에 보여주기
document.addEventListener("DOMContentLoaded", () => {
    const view9Element = document.querySelector(".upper_icon .diary_date");

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
        console.error("diary_date element not found");
    }
});

// "back" 버튼 누르면 작성 취소되고 main화면으로 이동
function confirmExit() {
    const view9Element = document.querySelector(".upper_icon .back_img");
    const year = view9Element.getAttribute("data-year");
    const month = view9Element.getAttribute("data-month");
    const day = view9Element.getAttribute("data-day");

    swal({
        title: "편집한 내용이 저장되지 않았어요.",
        text: "정말 나가시는 거예요? 🥹",
        icon: "warning",
        buttons: {
            cancel: "취소",
            confirm: {
                text: "확인",
                value: true,
                visible: true,
                className: "btn-danger",
                closeModal: true
            }
        }
    }).then((isConfirm) => {
        if (isConfirm) {            
            // Django에서 URL을 동적으로 생성
            const url = document.querySelector('#exit-url').getAttribute('data-url');
            window.location.href = url;
        }
    });
}

//오늘의 일기 내용 작성(1)
function clearPlaceholder(element) {
    if (element.textContent === "내용을 입력해주세요") {
        element.textContent = ""; // placeholder 제거
    }
}

//오늘의 일기 내용 작성(2)
function restorePlaceholder(element) {
    if (element.textContent.trim() === "") {
        element.textContent = "내용을 입력해주세요"; // placeholder 복원
    }
}


// "완료" 버튼 누르면 작성된 내용들 저장 & main화면으로 이동
document.getElementById('saveButton').addEventListener('click', function() {
    // 선택된 "오늘의 활동"
    const selectedActivities = Array.from(document.querySelectorAll('input[type="checkbox"].activity:checked'))
      .map((checkbox) => checkbox.value);
    
    // 선택된 "오늘의 날씨"
    const selectedWeather = Array.from(document.querySelectorAll('input[type="checkbox"].weather:checked'))
      .map((checkbox) => checkbox.value);
  
    // 작성된 "오늘의 일기"
    const diaryContent = document.querySelector('.diary_text').textContent.trim();
  
    // Prepare data for Django
    const data = {
      activities: selectedActivities,
      weather: selectedWeather,
      diary: diaryContent,
    };
  
    // 보내는 URL (Django의 URL 패턴을 따라 설정)
    const url = window.location.pathname;  // 현재 URL로 POST 요청을 보냄
  
    // AJAX POST 요청 보내기
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),  // CSRF 토큰을 추가 (보안을 위해)
      },
      body: JSON.stringify(data),  // 데이터를 JSON 형식으로 전송
    })
    .then(response => response.json())  // 서버에서 JSON 응답을 받음
    .then(data => {
      if (data.success) {
        // 성공적으로 저장되었으면 main 화면으로 이동
        window.location.href = '/main/' + data.year + '/' + data.month + '/' + data.day + '/';
      } else {
        // 에러 처리 (예: 실패 메시지 출력)
        alert('저장에 실패했습니다. 다시 시도해주세요.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('저장 중 오류가 발생했습니다.');
    });
  });
  
// CSRF 토큰을 가져오는 함수 (Django에서 CSRF 보호를 위해 필요)
function getCsrfToken() {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  return csrfToken;
}
  
