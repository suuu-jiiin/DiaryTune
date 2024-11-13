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

  updateCalendar();
}
    
function updateCalendar() {
  // 월과 연도 업데이트
  document.getElementById("month-text").textContent = monthNames[currentMonth];
  document.getElementById("year-text").textContent = currentYear;
  
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
                // Django URL 패턴 사용
                const url = `/DiaryTune/diary/${year}/${month + 1}/${day}/${dayOfWeek}/`;
                window.location.href = url;
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

