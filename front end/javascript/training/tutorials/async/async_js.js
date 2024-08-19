const fs = require('fs');
const axios = require('axios');

const url = 'https://httpbin.org/post'
const data = {
    x: 1920,
    y: 1080,
};
const customHeaders = {
    "Content-Type": "application/json",
}

function getWithAxios(){
    axios.post(url, data, {
        headers: customHeaders,
    })
    .then(({ data }) => {
        console.log(data);
    })
    .catch((error) => {
        console.error(error);
    });
}


async function getuser(userId) {
    try {
      const response = await fetch(`https://api.com/api/user/${userId}`)
      const user = await response.json();
    } catch(err) {
      console.error(err);
    }
  }

async function getPosts() {
    return await fetch('https://jsonplaceholder.typicode.com/posts');
}

async function fetchPosts() {
    try {
        const response = await getPosts();
        return response.json();
    }
    catch (e) {
        console.log("Error found getting posts", e.message);
        throw e;
    }
}

async function fetchComments(comment_id) {
    try {
        const repo = await fetch(`https://jsonplaceholder.typicode.com/comments?postId=${comment_id}`);;
        return repo.json();
    }
    catch (e) {
        console.log("Error found", e.message);
        throw e;
    }
}

(async  function () {
    try {
        const allPosts = await fetchPosts();
        let data = [];
        for (element of allPosts) {
            let response = await fetchComments(element.id);
            data.push(response)
        }
        fs.writeFileSync('./reponse.json', JSON.stringify(data));
        console.log('Response saved to file')
    } catch (e) {
        console.log(e);
    }
})();