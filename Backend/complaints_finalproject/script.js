function showNextSection() {
    document.querySelector('.section').style.display = 'none';
    document.getElementById('purchase-details-section').style.display = 'block';
}

function showPreviousSection() {
    document.getElementById('purchase-details-section').style.display = 'none';
    document.querySelector('.section').style.display = 'block';
}

document.getElementById('complaint-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    var formData = new FormData(this);
    //let formData = new FormData(this);
    fetch('http://127.0.0.1:8006/submit_complaint', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(error => { throw new Error(error.detail); });
           // throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.message === "Complaint registered successfully!") {
            document.getElementById('complaint-form').style.display = 'none';
        document.getElementById('success-section').style.display = 'block';
        //document.getElementById('success-message').textContent = `Your complaint has been registered successfully! Your token number is: ${complaintId}`;
        this.reset();
        showPreviousSection();
        } else {
            alert('Failed to register complaint.');;
        }
    })
    .catch(error => {
        alert('Failed to register complaint.34');
    });

   
//     const response = await fetch('http://127.0.0.1:8000/submit_complaint', {
//         method: 'POST',
   
//             body: formData
//         });
       
   
    
//     if (response.ok) {
//        // const complaintId = result.id;
//         document.getElementById('complaint-form').style.display = 'none';
//         document.getElementById('success-section').style.display = 'block';
//         //document.getElementById('success-message').textContent = `Your complaint has been registered successfully! Your token number is: ${complaintId}`;
//         this.reset();
//         showPreviousSection();
//     } else {
//         alert('Failed to register complaint.');
       
//     }
});
