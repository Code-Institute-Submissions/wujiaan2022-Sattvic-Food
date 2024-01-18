$('.btt-link').click(function(e) {
    window.scrollTo(0,0)
})
	
    
    
$('#sort-selector').change(function() {
    var selector = $(this);
    var currentUrl = new URL(window.location);

    var selectedVal = selector.val();
    if(selectedVal != "reset"){
        var sort = selectedVal.split("_")[0];
        var direction = selectedVal.split("_")[1];

        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);

        window.location.replace(currentUrl);
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");

        window.location.replace(currentUrl);
    }
})

// $(document).ready(function(){
//     // Check if the button was previously clicked
//     if (localStorage.getItem('buttonClicked')) {
//         $('.add-to-bag-btn').addClass('clicked');
//     }

//     $('.add-to-bag-btn').click(function(e) {
//         // e.preventDefault(); // Prevents the default action of the anchor tag
//         $(this).addClass('clicked');
//         localStorage.setItem('buttonClicked', true); // Store the click state in local storage

//         // Redirect to the URL
//         window.location.href = $(this).attr('href');
//     });
// });



// $(document).ready(function(){
//     $('.add-to-bag-btn').click(function(e) {
//         // e.preventDefault(); // Prevents the default action of the anchor tag
//         $(this).addClass('clicked');
//         // Optional: Redirect to the URL after a delay if needed
//         // window.setTimeout(function(){
//         //     window.location.href = $(this).attr('href');
//         // }, 500);
//     });
// });

// $(document).ready(function(){
//     $('.add-to-bag-btn').click(function(e) {
//         // e.preventDefault(); // Prevents the default action of the anchor tag

//         var url = $(this).attr('href');
//         var button = $(this); // Reference to the button

//         $.ajax({
//             url: url,
//             type: 'GET', // or 'POST', depending on your server-side setup
//             success: function(response) {
//                 // Assuming your server returns a JSON response with a success status
//                 if (response.success) {
//                     button.addClass('clicked');
//                 } else {
//                     // Handle the case where adding to the cart failed
//                     alert('Failed to add to cart');
//                 }
//             },
//             error: function() {
//                 // Handle AJAX request error
//                 alert('Error adding to cart');
//             }
//         });
//     });
// });


