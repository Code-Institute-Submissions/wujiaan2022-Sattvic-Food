$(document).ready(function() {
    $('.size-button').click(function() {
        var price = $(this).data('price');
        $('#price-display').text(' $' + price);
    });
});


$(document).ready(function() {
    $('.size-button').on('click', function() {
        $('.size-button').removeClass('active');
        $(this).addClass('active');
        // Additional functionality goes here
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const sizeButtons = document.querySelectorAll('.size-button');
    const productSizeInput = document.getElementById('product_size_id');

    sizeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const productSizeId = this.getAttribute('data-size-id');
            productSizeInput.value = productSizeId;
        });
    });
});

// document.querySelectorAll('.size-button').forEach(button => {
//     button.addEventListener('click', function() {
//         document.querySelectorAll('.size-button').forEach(btn => btn.classList.remove('active'));
//         this.classList.add('active');
//         // Existing functionality for price update
//     });
// });
 

