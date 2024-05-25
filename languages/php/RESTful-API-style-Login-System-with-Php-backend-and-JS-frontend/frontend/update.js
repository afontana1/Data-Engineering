const update = document.querySelector('input[type="submit"]')
update.addEventListener('click', () => {
    const data = new URLSearchParams(new FormData(document.querySelector('form')))
    console.log(document.cookie)
    var status
    fetch("http://localhost:8080/Model.php", {
            method: "PUT",
            credentials: 'include',
            mode: 'cors',
            body: data
        })
        .then(res => {
            status = res.status
            return res.text()
        })
        .then(data => {
            alert(data)
            if (status == 200)
                location.href = "./index.html"
        })

})