$(document).ready(function() {
    $('.size-button').on('click', function() {
        $('.size-button').removeClass('active');
        $(this).addClass('active');
        // Additional functionality goes here
    });
});



// document.querySelectorAll('.size-button').forEach(button => {
//     button.addEventListener('click', function() {
//         document.querySelectorAll('.size-button').forEach(btn => btn.classList.remove('active'));
//         this.classList.add('active');
//         // Existing functionality for price update
//     });
// });
 