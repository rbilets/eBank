const name = document.querySelector('#name');
const funds = document.querySelector('#funds');
const ownerId = document.querySelector('#owner_id');

function validate() {
    let status = true;
    if (name.value === '') {
        name.placeholder = 'Write name';
        name.classList.add('red');
        status = false;
    } else {
        name.classList.remove('red');
    }

    if (funds.value === '' || Number.isNaN(funds.value)) {
        funds.placeholder = 'It should be a number and not null';
        funds.classList.add('red');
        status = false;
    } else {
        funds.classList.remove('red');
    }

    return status;
}

document.querySelector('.btn').onclick = function (event) {
    event.preventDefault();

    if (!validate()) {
        return;
    }

    const data = {
        name: name.value,
        funds: funds.value,
        owner_id: ownerId.value,
    };

    fetch('http://127.0.0.1:5000/walletCreate', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
        },
        body: JSON.stringify(data),
    }).then((response) => {
        if (response.status === 200) {
            window.location.replace('/wallets');
            return response.json();
        }
        throw response.status;
    }).catch((error) => {
        if (error === 409 || error === 400) {
            document.getElementById('result').innerText = 'Wrong owner id';
        }
    });
};
