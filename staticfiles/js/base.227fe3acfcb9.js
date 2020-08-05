try {
    let profileButton = document.getElementById('profileButton');

    profileButton.addEventListener('click', function () {
        alert('This feature is currently locked in Beta.');
    });
} catch (e) {
    console.log('Error:', e);
}