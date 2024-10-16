document.addEventListener("DOMContentLoaded", function () {
  var swiper = new Swiper(".main-swiper", {
    loop: true,
    autoplay: {
      delay: 3000, // Thời gian giữa các slide
      disableOnInteraction: false,
    },
    speed: 1000, // Tốc độ chuyển đổi (1000ms = 1 giây)
    effect: "slide", // Hiệu ứng slide nhẹ nhàng
    navigation: {
      nextEl: ".swiper-arrow-next",
      prevEl: ".swiper-arrow-prev",
    },
  });
});
