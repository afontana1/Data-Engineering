const btn = document.querySelector('button')
const reply = document.querySelector('.reply')

btn.addEventListener('click', ()=>{
    fetch('http://localhost:8080/backend/server.php')
    .then(res=>res.json())
    .then(data =>{
        // console.log(data)
        if(data.status){
          reply.innerHTML = data.status  
        }
        else{
            reply.replaceChildren('')
            data.forEach(row=>{
                const pElm = document.createElement('p')
                pElm.innerHTML = `
                ${row.actor_id} &emsp; &emsp; ${row.first_name} &emsp; &emsp;${row.last_name}
                `
                reply.appendChild(pElm)
            })
        }
    })
})