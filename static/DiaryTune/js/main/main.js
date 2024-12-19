const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"];

function getParams() {
var url = window.location.pathname.split('/');
var params = {};

// URL에서 연도, 월, 일을 추출 
if (url.length >= 5) {  
params['year'] = url[2];   // 연도
params['month'] = url[3];  // 월
params['day'] = url[4];    // 일
}

return params;
}


let params = getParams();

let currentMonth = new Date().getMonth();  // 현재 월로 초기화 (0-11)
let currentYear = new Date().getFullYear();

if(params['year'] !== undefined && params['month'] !== undefined && params['day'] !== undefined) {
let date = new Date(`${params['year']}-${params['month']}-${params['day']}`);
currentYear = date.getFullYear();
currentMonth = date.getMonth();
}

document.addEventListener("DOMContentLoaded", () => {
// 이전/다음 버튼에 대한 이벤트 리스너 설정
document.getElementById("prev").addEventListener("click", () => changeMonth(-1));
document.getElementById("next").addEventListener("click", () => changeMonth(1));

// 초기 달력 설정
updateCalendar();
});

function changeMonth(direction) {
    currentMonth += direction;

    // 월 단위가 넘어가는 경우 연도 변경
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    } else if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }

    // 달력 업데이트
    updateCalendar();

    // 감정 카운트 업데이트
    fetch(`/DiaryTune/get_monthly_sentiments/${currentYear}/${currentMonth + 1}/`)
        .then(response => response.json())
        .then(data => {
            // 각 감정 카운트 업데이트
            for (let i = 1; i <= 5; i++) {
                const countElement = document.querySelector(`.count_text_${i}`);
                if (countElement) {
                    countElement.textContent = data[`sentiment_${i}`] || 0;
                }
            }
        })
        .catch(error => console.error('Error updating sentiment counts:', error));
}

function updateCalendar() {
// 월과 연도 업데이트
document.getElementById("month-text").textContent = monthNames[currentMonth];
document.getElementById("year-text").textContent = currentYear;

// 감정 카운트 업데이트를 위한 AJAX 요청 추가
fetch(`/DiaryTune/get_monthly_sentiments/${currentYear}/${currentMonth + 1}/`)
    .then(response => response.json())
    .then(data => {
        // 각 감정 카운트 업데이트
        for (let i = 1; i <= 5; i++) {
            const countElement = document.querySelector(`.count_text_${i}`);
            if (countElement) {
                countElement.textContent = data[`sentiment_${i}`] || 0;
            }
        }
    })
    .catch(error => console.error('Error updating sentiment counts:', error));

// 날짜 업데이트
generateDates(currentYear, currentMonth);
}

function generateDates(year, month) {
const datesContainer = document.getElementById("dates");
datesContainer.innerHTML = "";  // 기존 날짜 지우기

// calendar-date 클래스를 가진 div 생성
const calendarDateContainer = document.createElement("div");
calendarDateContainer.classList.add("calendar-date");

// 해당 월의 첫 번째 날과 마지막 날 구하기
const firstDay = new Date(year, month, 1);
const lastDay = new Date(year, month + 1, 0);
const daysInMonth = lastDay.getDate();
const startDay = firstDay.getDay();
const totalDays = daysInMonth + startDay;

// 주 단위로 나누어 날짜를 출력
for (let week = 0; week < Math.ceil(totalDays / 7); week++) {
const weekContainer = document.createElement("div");

// week 값에 따라 클래스 이름을 설정
switch (week) {
case 0:
weekContainer.classList.add("first");
break;
case 1:
weekContainer.classList.add("second");
break;
case 2:
weekContainer.classList.add("third");
break;
case 3:
weekContainer.classList.add("fourth");
break;
case 4:
weekContainer.classList.add("fifth");
break;
default:
break;
}

// 각 주의 날짜 추가
for (let dayIndex = 0; dayIndex < 7; dayIndex++) {
const day = week * 7 + dayIndex - startDay + 1;
const dateCell = document.createElement("div");

// 요일에 맞는 클래스 설정
let dayClass;
const dayOfWeek = new Date(year, month, day).getDay();

switch (dayOfWeek) {
case 0: dayClass = "sun"; break;
case 1: dayClass = "mon"; break;
case 2: dayClass = "tue"; break;
case 3: dayClass = "wed"; break;
case 4: dayClass = "thu"; break;
case 5: dayClass = "fri"; break;
case 6: dayClass = "sat"; break;
}

// 요일 클래스를 div에 추가
dateCell.classList.add(dayClass);

// overlap-group-3 및 rectangle 구조 생성
const overlapGroup = document.createElement("div");
overlapGroup.classList.add("overlap-group-3");

const rectangle = document.createElement("div");
rectangle.classList.add("rectangle");   

// 날짜를 표시할 텍스트 요소 추가
const textWrapper = document.createElement("div");
textWrapper.classList.add("text-wrapper-9");
textWrapper.textContent = day >= 1 && day <= daysInMonth ? day : ""; // 유효한 날짜만 표시

if (day >= 1 && day <= daysInMonth) {
    
    fetch(`/DiaryTune/check_diary/${year}/${month + 1}/${day}/`)
        .then(response => {
            return response.json();
        })
        .then(data => {
            if (data.exists) {
                // 감정에 따른 배경색 설정
                const sentimentColors = {
                    'sentiment_1': '#FFD4D4', // 빨간색 계열 - 화남/슬픔
                    'sentiment_2': '#E8F1FF', // 파란색 계열 - 약간 부정
                    'sentiment_3': '#E6FFE6', // 초록색 계열 - 중립
                    'sentiment_4': '#FFF0F6', // 핑크색 계열 - 약간 긍정
                    'sentiment_5': '#FFF2CC'  // 노랑색 계열 - 매우 긍정
                };
                
                rectangle.style.backgroundColor = sentimentColors[data.sentiment] || '#E8F1FF';

                const sentimentImg = document.createElement("img");
                sentimentImg.classList.add("sentiment-icon");
                sentimentImg.src = `/static/DiaryTune/images/${data.sentiment}.png`;
                sentimentImg.alt = data.sentiment;
                sentimentImg.style.width = "33px";
                sentimentImg.style.height = "33px";
                sentimentImg.style.marginTop = "22px";
                sentimentImg.style.marginLeft = "8px";
                rectangle.appendChild(sentimentImg);
            }
        })
        .catch(error => {
            console.error('Error checking diary:', error);
        });

    dateCell.addEventListener("click", () => {
        const currenDate = new Date();
        const selectedDate = new Date(year, month, day);

        // 미래 날짜 클릭 시 알림
        if (selectedDate > currenDate) {
            swal({
                icon: "error",
                content: {
                    element: "p",
                    attributes: {
                        innerHTML: "미래의 하루는 기록할 수 없어요! 🥹",
                    }
                }
            });
        } else {
            // 선택된 날짜에 해당하는 일기 존재 여부 확인
            fetch(`/DiaryTune/check_diary/${year}/${month + 1}/${day}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.exists) {
                        // 일기가 있으면 recommendation 페이지로 이동
                        const recommend_url = `/DiaryTune/recommendation/${year}/${month + 1}/${day}/${dayOfWeek}/`;
                        window.location.href = recommend_url;
                    } else {
                        // 일기가 없으면 diary 페이지로 이동
                        const diary_url = `/DiaryTune/diary/${year}/${month + 1}/${day}/${dayOfWeek}/`;
                        window.location.href = diary_url;
                    }
                })
                .catch(error => {
                    console.error('Error checking diary:', error);
                    swal("오류", "일기 확인 중 문제가 발생했습니다.", "error");
                });
        }
    });
}

// 구조에 추가
rectangle.appendChild(textWrapper);
overlapGroup.appendChild(rectangle);
dateCell.appendChild(overlapGroup);
weekContainer.appendChild(dateCell);
}
// 주를 calendar-date div에 추가
calendarDateContainer.appendChild(weekContainer);
}    
// 모든 주를 담은 calendar-date div를 전체 날짜 컨테이너에 추가
datesContainer.appendChild(calendarDateContainer);
}

function loadDiaryData(year, month) {
fetch(`/DiaryTune/get_monthly_diary_data/${year}/${month}/`)
.then(response => response.json())
.then(data => {
const sentimentImages = JSON.parse(document.getElementById("sentiment-images").textContent);
data.diary_data.forEach(diary => {
const dayElement = document.getElementById(`day-${diary.day}`);
if (dayElement) {
    if (!dayElement.querySelector(".sentiment-icon")) { // 중복 방지
        const img = document.createElement("img");
        img.classList.add("sentiment-icon");
        img.src = sentimentImages[diary.sentiment] || sentimentImages["default"];
        img.alt = diary.sentiment;
        dayElement.appendChild(img);
    }
}
});
})
.catch(error => console.error("Failed to load diary data:", error));
}

