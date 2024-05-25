const showusersbtn = document.querySelector('#getbtn');
showusersbtn.addEventListener('click', getUsers);

function getUsers() {
    resetDOM();
    axios.get('https://jsonplaceholder.typicode.com/users')
        .then(response => {
            (response.data).forEach(datum => {
                const userdiv = addDiv();
                userdiv.setAttribute('id', `div-${datum.id}`);
                document.querySelector('body').appendChild(userdiv);
                const ul = document.createElement('ul');
                ul.style.listStyle = "none";
                const name = document.createElement('li');
                name.innerHTML = `<strong>Name: </strong> ${datum.name}`;
                ul.appendChild(name);

                const id = document.createElement('li');
                id.innerHTML = `<strong>ID: </strong> ${datum.id}`;
                ul.appendChild(id);

                const username = document.createElement('li');
                username.innerHTML = `<strong>UserName: </strong> ${datum.username}`;
                ul.appendChild(username);

                const email = document.createElement('li');
                email.innerHTML = `<strong>Email: </strong> ${datum.email}`;
                ul.appendChild(email);

                const address = document.createElement('li');
                address.innerHTML = `<strong>Address: </strong> ${datum.address.suite} ${datum.address.street} ${datum.address.city}  ${datum.address.zipcode}`;
                ul.appendChild(address);

                const website = document.createElement('li');
                website.innerHTML = `<strong>Website: </strong> ${datum.website}`;
                ul.appendChild(website);

                userdiv.appendChild(ul);

                const btn = document.createElement('button');
                btn.setAttribute('id', datum.id);
                btn.addEventListener('click', function() { getPosts(datum.id); });
                btn.textContent = "show posts";
                btn.style.color = "#1E4747";
                userdiv.appendChild(btn);
                btn.setAttribute('hidepost', true);
                btn.setAttribute('id', `userpost-${datum.id}`);
            })
        })
        .catch(err => console.log(err));
}

function getPosts(id) {
    const btn = document.querySelector(`#userpost-${id}`);
    const userdiv = document.querySelector(`#div-${id}`);

    if (btn.getAttribute('hidepost') == "true") {

        const postsdiv = userdiv.appendChild(document.createElement('div'));
        postsdiv.style.marginLeft = "40px";

        postsdiv.setAttribute('id', 'postsdiv');
        axios.get(
                "https://jsonplaceholder.typicode.com/posts/", {
                    params: {
                        ID: id,
                        _limit: 10
                    }
                }
            )
            .then(res => {
                (res.data).forEach(datum => {

                    const postdiv = document.createElement('div');
                    postsdiv.appendChild(postdiv);
                    postdiv.style.paddingLeft = "0px";
                    postdiv.style.borderLeft = "solid 4px #497979";
                    postdiv.setAttribute('id', `post-${datum.id}`);
                    postdiv.style.backgroundColor = '#02A1A1';
                    postdiv.marginBottom = "5px";
                    postdiv.padding = '4px';
                    const ul = postdiv.appendChild(document.createElement('ul'));
                    ul.style.listStyle = "none";
                    const idli = document.createElement('li');
                    idli.innerHTML = `<strong>ID:</strong> ${datum.id}`;
                    ul.appendChild(idli);

                    const titleli = document.createElement('li');
                    titleli.innerHTML = `<strong>Title:</strong> ${datum.title}`;
                    ul.appendChild(titleli);

                    const bodyli = document.createElement('li');
                    bodyli.innerHTML = `<strong>Body:</strong> ${datum.body}`;
                    ul.appendChild(bodyli);
                });
            })
            .catch(err => console.log(err));
        btn.setAttribute('hidepost', false);
        btn.textContent = "hide posts";
        return;
    } else {
        userdiv.removeChild(document.querySelector("#postsdiv"));
        btn.setAttribute('hidepost', true);
        btn.textContent = "show posts";
    }
}

function getPostandcomments() {
    resetDOM();
    const maindiv = document.createElement('div');
    maindiv.style.textAlign = "center"
    document.querySelector('body').appendChild(maindiv);
    axios.all([getallPosts(), getComments()])
        .then(axios.spread(function(posts, comments) {

            const h1 = document.createElement('h1');
            h1.textContent = "Top 10 Posts";
            maindiv.appendChild(h1);

            posts = posts.data;
            posts.forEach(post => {
                const div = addDiv();
                div.style.textAlign = "left";
                maindiv.appendChild(div);
                const ul = document.createElement('ul');
                div.appendChild(ul);
                ul.style.listStyle = "none";
                const idli = document.createElement('li');
                idli.innerHTML = `<strong>ID: </strong> ${post.id}`;
                ul.appendChild(idli);

                const useridli = document.createElement('li');
                useridli.innerHTML = `<strong>UserID: </strong> ${post.userId}`;
                ul.appendChild(useridli);

                const titleli = document.createElement('li');
                titleli.innerHTML = `<strong>Title: </strong> ${post.title}`;
                ul.appendChild(titleli);

                const bodyli = document.createElement('li');
                bodyli.innerHTML = `<strong>Body: </strong> ${post.body}`;
                ul.appendChild(bodyli);

            });

            const h2 = document.createElement('h1');
            h2.textContent = "Top 8 Coments";
            maindiv.appendChild(h2);

            comments = comments.data;
            comments.forEach(comment => {
                const div = addDiv();
                div.style.textAlign = "left";
                maindiv.appendChild(div);
                const ul2 = document.createElement('ul');
                div.appendChild(ul2);
                ul2.style.listStyle = "none";
                const idli = document.createElement('li');
                idli.innerHTML = `<strong>ID: </strong> ${comment.id}`;
                ul2.appendChild(idli);

                const postidli = document.createElement('li');
                postidli.innerHTML = `<strong>PostID: </strong> ${comment.postId}`;
                ul2.appendChild(postidli);

                const nameli = document.createElement('li');
                nameli.innerHTML = `<strong>Name: </strong> ${comment.name}`;
                ul2.appendChild(nameli);

                const emailli = document.createElement('li');
                emailli.innerHTML = `<strong>Email: </strong> ${comment.email}`;
                ul2.appendChild(emailli);

                const bodyli = document.createElement('li');
                bodyli.innerHTML = `<strong>Body: </strong> ${comment.body}`;
                ul2.appendChild(bodyli);
            });
        }));

}

function getallPosts() {
    return axios({
        method: 'get',
        url: 'https://jsonplaceholder.typicode.com/posts',
        params: {
            _limit: 10
        }
    });

}

function getComments() {
    return axios({
        method: 'get',
        url: 'https://jsonplaceholder.typicode.com/comments',
        params: {
            _limit: 8
        }
    });

}

function resetDOM() {
    const body = document.querySelector('body');
    const children = [...(body.children)];
    children.forEach(child => { if (child instanceof HTMLDivElement) { body.removeChild(child) } });
}

function addDiv() {
    const div = document.createElement('div');

    div.style.width = "80%";
    div.style.marginLeft = "auto";
    div.style.marginRight = "auto";
    div.style.marginBottom = "8px";
    div.style.padding = "5px";

    div.style.borderTop = "solid 4px #045959";
    div.style.borderBottom = "solid 4px #045959";

    div.style.backgroundColor = "#CEF0F0"

    return div;

}

function displayForm() {
    resetDOM();
    const div = addDiv();
    document.querySelector('body').appendChild(div);
    div.innerHTML = `
    <label for="uid">UserId</label>
    <br>
    <input type="text" name="userid" value="" id="uid"/>
    <br>
    <label for="title">Title</label>
    <br>
    <input type="text" name="posttitle" id="title" value=""/>
    <br>
    <label for="body">Body</label>
    <br>
    <textarea row="5" col="10" name="body" id="body" style="width:400px;height:200px;overflow:scroll; box-sizing:border-box;"></textarea>
    <br>
    <button type="submit" onclick="submitPost(this.parentElement)">post</button>

    `;

}

function submitPost(div) {
    const children = div.querySelectorAll("Input[type=text]");

    const id = children.item(0).value;
    const title = children.item(1).value;
    const body = div.querySelector("textarea").value;
    resetDOM();

    axios.post("https://jsonplaceholder.typicode.com/posts", {
            data: {
                userId: id,
                title: title,
                body: body
            }
        })
        .then(res => {
            const resdiv = addDiv();
            const data = res.data;

            resdiv.innerHTML = `
            <ul>
                <li><strong>User Id: </strong>${data.data.userId}</li>
                <li><strong>Post Id</strong>${data.id}</li>
                <li><strong>Post Title: </strong>${data.data.title}</li>
                <li><strong>Post Body: </strong>${data.data.body}</li>
            </ul>
            `;
            document.querySelector('body').appendChild(resdiv);

        })
        .catch(err => console.log(err));

}