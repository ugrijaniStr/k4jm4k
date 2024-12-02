statuses.forEach(status => {
    if(status.textContent.trim() === 'Online') {
        status.style.color = 'rgb(30, 255, 0)';
    } else if (status.textContent.trim() === 'Offline') {
        status.style.color = 'rgb(255, 0, 0)';
    }
});

infectedUsers = () => {
    let inputValue = document.getElementById('inputValue').value;
    const infectedUser = document.querySelectorAll('#address');

    if(inputValue == '!infected') {
        infectedUser.forEach(address => {
            document.getElementById('kajmak').innerText = '{{address}}';
        })
    }
}
