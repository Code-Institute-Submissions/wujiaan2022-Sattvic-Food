// Grab all size buttons and the price display element
const sizeButtons = document.querySelectorAll('.size-button');
const productPriceDisplay = document.getElementById('product_price_display');
const selectedProductSizeInput = document.getElementById('selected_product_size');
const selectedProductPriceInput = document.getElementById('selected_product_price');

// Function to update the displayed price and selected size's ID/price
function selectSize(event) {
    // Deselect all buttons
    sizeButtons.forEach(button => button.classList.remove('selected'));

    // Select the clicked button
    const clickedButton = event.currentTarget;
    clickedButton.classList.add('selected');

    // Update the displayed price
    const selectedPrice = clickedButton.getAttribute('data-price');
    productPriceDisplay.textContent = '$' + selectedPrice;

    // Update hidden input fields with selected size's ID and price
    const selectedSizeId = clickedButton.getAttribute('data-size-id');
    selectedProductSizeInput.value = selectedSizeId;
    selectedProductPriceInput.value = selectedPrice;
}

// Add click event listeners to all size buttons
sizeButtons.forEach(button => button.addEventListener('click', selectSize));

// Select the first size by default (optional)
sizeButtons[0].click();