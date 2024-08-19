const register = document.querySelector('input[type="submit"]')
register.addEventListener('click', () => {
    var status
    const formData = new FormData(document.querySelector('form'));
    console.log(formData.get('pwd'));
    fetch('http://localhost:8080/Model.php', {
            'method': "POST",
            'body': formData,
        })
        .then(res => {
            status = res.status
            return res.text()
        })
        .then(data => {
            alert(data)
            if (status == 200)
                location.href = "/frontend/index.html"
        })
        .catch(err => { console.log(err) })
})