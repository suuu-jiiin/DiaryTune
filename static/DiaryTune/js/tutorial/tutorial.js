document.getElementById('play-btn').addEventListener('click', function() {
    window.location.href = 'https://www.youtube.com/watch?v=ekr2nIex040'; // 'intent://www.youtube.com/watch?v=VIDEO_ID#Intent;package=com.google.android.youtube;scheme=https;end;'
    }); 
    
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
