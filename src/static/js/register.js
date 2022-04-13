const username = document.querySelector('#username');
const firstName = document.querySelector('#firstName');
const lastName = document.querySelector('#lastName');
const email = document.querySelector('#email');
const password = document.querySelector('#password');

function validate() {
    const validateEmail = (email) => String(email)
        .toLowerCase()
        .match(
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
        );
    let status = true;

    if (!validateEmail(email.value)) {
        email.value = '';
        email.placeholder = 'Email is incorrect';
        email.classList.add('red');
        status = false;
    } else {
        email.classList.remove('red');
    }

    if ((password.value).length < 8) {
        password.value = '';
        password.placeholder = 'Must contain at least 8';
        password.classList.add('red');
        status = false;
    } else {
        password.classList.remove('red');
    }

    if (firstName.value === '') {
        firstName.placeholder = 'Write your name';
        firstName.classList.add('red');
        status = false;
    } else {
        firstName.classList.remove('red');
    }

    if (lastName.value === '') {
        lastName.placeholder = 'Write your surname';
        lastName.classList.add('red');
        status = false;
    } else {
        lastName.classList.remove('red');
    }

    return status;
}

document.querySelector('.btn').onclick = function (event) {
    event.preventDefault();

    if (!validate()) {
        return;
    }

    const data = {
        username: username.value,
        first_name: firstName.value,
        last_name: lastName.value,
        email: email.value,
        password: password.value,
    };

    fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
        },
        body: JSON.stringify(data),
    }).then((response) => {
        if (response.status === 200) {
            window.location.replace('/');
            return response.json();
        }
        throw response.status;
    }).catch((error) => {
        if (error === 409) {
            username.placeholder = 'Nickname is already used or empty';
            username.classList.add('red');
        }
    });
};
