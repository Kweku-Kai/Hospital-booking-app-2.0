document.addEventListener('DOMContentLoaded', function () {
    const registerPatientForm = document.getElementById('registerPatientForm');
    const bookPatientForm = document.getElementById('bookPatientForm');
    const registerSection = document.getElementById('registerSection');
    const bookingsList = document.getElementById('bookingsList');

    // Fetch today's bookings on page load
    fetch('/bookings')
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                data.forEach(booking => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <div>${booking.patientId}</div>
                        <div>${booking.caseType}</div>
                        <div>${booking.purpose}</div>
                        <div>${booking.bookingTime}</div>
                    `;
                    bookingsList.appendChild(li);
                });
            }
        });

    registerPatientForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(registerPatientForm);
        fetch('/register', {
            method: 'POST',
            body: formData
        }).then(response => response.json()).then(data => {
            if (data.success) {
                alert('Patient registered successfully!');
                registerPatientForm.reset();
                registerSection.style.display = 'none';
            } else {
                alert('Error: ' + data.error);
            }
        });
    });

    bookPatientForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(bookPatientForm);
        fetch('/book', {
            method: 'POST',
            body: formData
        }).then(response => response.json()).then(data => {
            if (data.success) {
                alert('Booking successful!');
                bookPatientForm.reset();
                location.reload(); // Refresh the page to show the new booking
            } else {
                alert('Error: ' + data.error);
            }
        });
    });

    window.showRegisterForm = function () {
        registerSection.style.display = 'block';
    };

    window.printBookings = function () {
        // Implement print functionality
        window.print();
    };
});
