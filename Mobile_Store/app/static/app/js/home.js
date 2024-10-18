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
document.querySelectorAll('.add-btn').forEach(function(button) {
  button.addEventListener('click', function() {
      var productId = this.getAttribute('data-product');

      // Ghi thông báo vào local storage
      localStorage.setItem('cartNotification', '1 product added successfully!');

      // Chuyển hướng đến một URL khác hoặc reload trang
      // Để reload trang, chỉ cần gọi:
      window.location.reload();
  });
});

// Khi trang được tải lại, kiểm tra và hiển thị thông báo
window.addEventListener('load', function() {
  var notification = localStorage.getItem('cartNotification');
  if (notification) {
      var notificationDiv = document.getElementById('notification');
      notificationDiv.textContent = notification; // Cập nhật nội dung thông báo
      notificationDiv.style.display = 'block'; // Hiện thông báo

      // Xóa thông báo khỏi local storage sau khi hiển thị
      localStorage.removeItem('cartNotification');

      // Ẩn thông báo sau 3 giây
      setTimeout(function() {
          notificationDiv.style.display = 'none';
      }, 1000); // 2000ms = 3 giây
  }
});