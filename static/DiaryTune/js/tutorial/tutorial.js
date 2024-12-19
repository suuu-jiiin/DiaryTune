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

const dislikeButton = document.getElementById('dislike');
if (dislikeButton) {
    dislikeButton.addEventListener('click', function() {
        const currentSrc = this.getAttribute('src');
        const dislikeOn = this.getAttribute('data-dislike-on');
        const dislikeOff = this.getAttribute('data-dislike-off');
        
        if (currentSrc === dislikeOff) {
            this.setAttribute('src', dislikeOn);
            // heart 버튼이 활성화되어 있다면 비활성화
            const heartButton = document.getElementById('heart');
            if (heartButton && heartButton.getAttribute('src') === heartButton.getAttribute('data-heart-on')) {
                heartButton.setAttribute('src', heartButton.getAttribute('data-heart-off'));
            }
        } else {
            this.setAttribute('src', dislikeOff);
        }
    });
}