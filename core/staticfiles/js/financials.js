



// Get the modal
var modal = document.getElementById("filterModal");

// Get the button that opens the modal
var openModalBtn = document.getElementById("openModalBtn");

// Get the <span> element that closes the modal
var closeModalBtn = document.getElementById("closeModalBtn");

// When the user clicks the button, open the modal
openModalBtn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
closeModalBtn.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}



document.addEventListener('click', function(event) {
    if (!event.target.closest('.menu-container')) {
        const popups = document.querySelectorAll('.actions-popup');
        popups.forEach(popup => {
            popup.style.display = 'none';
            popup.classList.remove('top');
        });
    }
});

function toggleActions(bookingId) {
    event.stopPropagation();
    
    // Close all other popups
    const popups = document.querySelectorAll('.actions-popup');
    popups.forEach(popup => {
        if (popup.id !== `actions-popup-${bookingId}`) {
            popup.style.display = 'none';
            popup.classList.remove('top');
        }
    });
    
    const popup = document.getElementById(`actions-popup-${bookingId}`);
    const button = event.currentTarget;
    const buttonRect = button.getBoundingClientRect();
    const viewportHeight = window.innerHeight;
    
    // Clear any previous positioning
    popup.style.removeProperty('top');
    popup.style.removeProperty('bottom');
    
    // Calculate if there's more space above or below the button
    const spaceBelow = viewportHeight - buttonRect.bottom;
    const spaceAbove = buttonRect.top;
    
    // If there's not enough space below, show popup above
    if (spaceBelow < 150 && spaceAbove > spaceBelow) {
        popup.classList.add('top');
    } else {
        popup.classList.remove('top');
    }
    
    // Toggle display
    popup.style.display = popup.style.display === 'none' ? 'block' : 'none';
}


function openSearchModal() {
    document.getElementById('searchModal').style.display = 'block';
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

function closeSearchModal() {
    document.getElementById('searchModal').style.display = 'none';
    document.body.style.overflow = 'auto'; // Restore scrolling
}

function resetSearch() {
    document.getElementById('date').value = '';
    document.getElementById('reference').value = '';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('searchModal');
    if (event.target == modal) {
        closeSearchModal();
    }
}

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeSearchModal();
    }
});


