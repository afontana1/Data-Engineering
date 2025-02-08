const signup = document.querySelector('.signup')
const login = document.querySelector('.login')
const update = document.querySelector('.update')

signup.addEventListener('click', () => location.href = "/frontend/register.html")
login.addEventListener('click', () => location.href = "/frontend/login.html")
update.addEventListener('click', () => location.href = "/frontend/update.html")

const logout = document.querySelector(".logout")
const dlt = document.querySelector(".unsubscribe")

logout.addEventListener('click', () => {

    fetch("http://localhost:8080/Model.php", {

            credentials: 'include',
            mode: 'cors'
        })
        .then(res => res.text())
        .then(data => {
            alert(data)
            location.href = 'index.html'
        })
})

dlt.addEventListener('click', () => {
    fetch('http://localhost:8080/Model.php', {
            method: 'DELETE',
            credentials: 'include',
            mode: 'cors'
        })
        .then(res => res.text())
        .then(data => {
            alert(data)
        })
})