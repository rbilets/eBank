document.querySelector('.btn').onclick = function (event) {
    event.preventDefault();

    const user = {
        username: document.querySelector('#username').value,
        password: document.querySelector('#password').value,
    };
    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
        },
        body: JSON.stringify(user),
    }).then((response) => {
        if (response.status === 200) {
            window.location.replace('/profile');
            return response.json();
        }
        throw response.status;
    }).catch((error) => {
        if (error === 401) {
            document.getElementById('result').innerText = 'Wrong username or password';
        }
    });
};
