try {
    const searchButton = document.querySelector('.search-button');
    searchButton.disabled = true;

    const searchBox = document.querySelector('.search-box');
    searchBox.onkeyup = () => {
        if (searchBox.value.length > 0) {
            searchButton.disabled = false;
        } else {
            searchButton.disabled = true;
        }
    }
} catch (e) {
    console.log('Caught error:', e);
}