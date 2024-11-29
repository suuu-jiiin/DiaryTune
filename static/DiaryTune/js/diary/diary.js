//오늘의 활동 두 개만 선택
const checkboxes = document.querySelectorAll('input[type="checkbox"].activity');

checkboxes.forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
        const checkedCount = document.querySelectorAll('input[type="checkbox"].activity:checked').length;
        if (checkedCount > 2) {
            checkbox.checked = false; // Uncheck the current box if the limit is exceeded
            swal({
                icon: "error",
                text: "최대 두 개만 선택할 수 있어요",
                button: "확인"
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
                text: "최대 두 개만 선택할 수 있어요",
                button: "확인"
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


// "완료" 버튼 클릭 이벤트
document.getElementById('saveButton').addEventListener('click', function() {
    // 선택된 "오늘의 활동"
    const selectedActivities = Array.from(document.querySelectorAll('input[type="checkbox"].activity:checked'))
        .map((checkbox) => checkbox.value);

    // 선택된 "오늘의 날씨"
    const selectedWeather = Array.from(document.querySelectorAll('input[type="checkbox"].weather:checked'))
        .map((checkbox) => checkbox.value);

    // 작성된 "오늘의 일기"
    const diaryContent = document.querySelector('.diary_text').textContent.trim();

    // CSRF 토큰 가져오기
    const csrfToken = getCsrfToken();

    // Prepare data for Django
    const data = {
        activities: selectedActivities,
        weather: selectedWeather,
        diary: diaryContent,
    };

    // URL에서 year, month, day, diary_id 값을 추출
    const urlParts = window.location.pathname.split('/'); // URL을 '/'로 분리
    const currentYear = urlParts[urlParts.length - 5];  // year
    const currentMonth = urlParts[urlParts.length - 4]; // month
    const currentDay = urlParts[urlParts.length - 3];   // day
    const dayofweek = urlParts[urlParts.length - 2];    // dayofweek
    
    fetch(window.location.pathname, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);  // 서버 응답 메시지 출력
        window.location.href = `/main/${currentYear}/${currentMonth}/${currentDay}/`; // main 페이지로 리디렉션
        //window.location.href = `/save_diary/${currentYear}/${currentMonth}/${currentDay}/`; // main 페이지로 리디렉션
    })
    .catch(error => {
        console.error('Error saving diary:', error);
    });

    
});


  
// CSRF 토큰을 가져오는 함수
function getCsrfToken() {
    const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
    if (!csrfTokenElement) {
        console.error('CSRF token element not found');
        return '';
    }
    return csrfTokenElement.getAttribute('content');
}
  
