function like(postId){
    const likesCount = document.getElementById(`likes-count-${postId}`)
    const likeButton = document.getElementById(`like-button-${postId}`)

    fetch(`/like-post/${postId}`, {method: "POST"})
        .then(res => res.json())
        .then(data => {
            likesCount.innerHTML = data["likes"];
            if (data["liked"]){
                likeButton.className = "fas fa-thumbs-up";
            }
            else {
                likeButton.className = "far fa-thumbs-up";
            }
        })
        .catch((e) => alert("Could not like post"));
}