function updateItemTotal(row) {
    const price = parseFloat(row.querySelector('.price').textContent.replace('$', ''));
    const quantity = parseInt(row.querySelector('.quantity').textContent);
    const itemTotal = price * quantity;

    // Cập nhật tổng giá cho từng mặt hàng
    row.querySelector('.item-total').textContent = `$${itemTotal.toFixed(2)}`;
}

function updateTotals() {
    const rows = document.querySelectorAll('tbody tr');
    let totalItems = 0;
    let totalPrice = 0;

    rows.forEach(row => {
        const quantityValue = parseInt(row.querySelector('.quantity').textContent);
        totalItems += quantityValue;

        // Cập nhật tổng cho từng mặt hàng
        updateItemTotal(row); // Gọi hàm này để cập nhật tổng giá cho từng mặt hàng
        const itemTotal = parseFloat(row.querySelector('.item-total').textContent.replace('$', ''));
        totalPrice += itemTotal;
    });

    // Cập nhật tổng số mặt hàng và tổng giá
    document.getElementById('total-items').textContent = totalItems;
    document.getElementById('total-price').textContent = `$${totalPrice.toFixed(2)}`;
}

function incrementQuantity(button) {
    const quantitySpan = button.previousElementSibling;
    const quantityValue = parseInt(quantitySpan.textContent) + 1;
    quantitySpan.textContent = quantityValue;

    // Cập nhật tổng cho từng mặt hàng và tổng giỏ hàng
    updateItemTotal(button.closest('tr'));
    updateTotals();
}

function decrementQuantity(button) {
    const quantitySpan = button.nextElementSibling;
    let quantityValue = parseInt(quantitySpan.textContent);

    if (quantityValue > 1) {
        quantityValue -= 1;
        quantitySpan.textContent = quantityValue;

        // Cập nhật tổng cho từng mặt hàng và tổng giỏ hàng
        updateItemTotal(button.closest('tr'));
    }

    updateTotals();
}

// Khởi tạo tổng ngay khi trang được tải
document.addEventListener('DOMContentLoaded', updateTotals);