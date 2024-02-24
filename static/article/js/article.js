const comment_input = document.getElementById('comment-input');
const comment_button = document.getElementById('comment-button');
const article_id = document.getElementById('content').title;
const csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

comment_button.onclick = function () {
    const url = `${window.location.origin}/comment/`;

    if (!comment_input.value) {
        return 1
    }

    $.ajax({
        url: url,
        method: "POST",
        data: {
            "comment": comment_input.value,
            "article_id": article_id,
            "csrfmiddlewaretoken": csrfmiddlewaretoken
        },
        success: function (data, status, xhr) {
        const comments = document.getElementById('comments');
        comments.innerHTML += `<div class="comment">
        <p><b><a class="text-black link-primary text-decoration-none" href="">${data.username}</a></b> - Just now</p>
        <p>${data.comment}</p>
      </div>
      <hr>`
        },
        error: function (jqXhr, textStatus, errorMessage) {
            alert(jqXhr.responseJSON.error)
            error.innerHTML = jqXhr.responseJSON.error
        }
    })
}
