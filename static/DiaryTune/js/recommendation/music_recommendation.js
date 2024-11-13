document.getElementById('heart').addEventListener('click', function() {
    const heartImage = this;
    if (heartImage.src.includes('heart-1.png')) {
      heartImage.src = 'img/heart-2.png'; // heart-2 이미지로 변경
    } else {
      heartImage.src = 'img/heart-1.png'; // heart-1 이미지로 되돌리기
    }
  });

  document.getElementById('play-btn').addEventListener('click', function() {
  window.location.href = 'https://www.youtube.com/'; // 'intent://www.youtube.com/watch?v=VIDEO_ID#Intent;package=com.google.android.youtube;scheme=https;end;'
  });      
  
  // 페이지 이동 기능 추가
  document.querySelector('.modify').addEventListener('click', () => {
      window.location.href = '../diary/diary.html'; // modify가 이동할 URL
  });

  document.querySelector('.back').addEventListener('click', () => {
      window.location.href = '../main/main.html'; // back이 이동할 URL
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
      // 삭제 로직 실행
          window.location.href = '../main/main.html'
          } 
      });
  });