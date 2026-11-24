// 모바일(1190px 이하) 햄버거 메뉴 토글
// 기존 버전은 존재하지 않는 header.html/footer.html 을 불러오고,
// 창 크기가 바뀔 때마다 클릭 이벤트를 중복으로 붙여 메뉴가 안 열리는 문제가 있었음.
$(function () {
  $('.nav_btn').on('click', function () {
    $('.nav_area').toggleClass('active');
  });
  $(window).on('resize', function () {
    if ($(window).width() > 1190) $('.nav_area').removeClass('active');
  });
});
