const comment_input = document.getElementById('comment-input');
const comment_button = document.getElementById('comment-button');
const article_id = document.getElementById('content').title;
const csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

comment_button.onclick = function () {
    const url = `${window.location.origin}/comment/`;

    if (!comment_input.value) {
        return 1;
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
        comments.innerHTML += `<div class="comment" title="${data.comment_id}">
        <p><b><a class="text-black link-primary text-decoration-none" href="">${data.username}</a></b> - Just now</p>
        <p>
            ${data.comment}
            <a class="text-black link-secondary text-decoration-none" style="cursor: pointer;" onclick="reply_box(this.parentNode.parentNode)">reply</a>
            <a class="text-black link-secondary text-decoration-none" style="cursor: pointer;" onclick="delete_comment(this.parentNode.parentNode)">delete</a>
        </p>
      </div>
      <hr>`
        },
        error: function (jqXhr, textStatus, errorMessage) {
            alert(jqXhr.responseJSON.error);
        }
    })
}

function reply_box(comment_element) {
    if (comment_element.getElementsByClassName('reply-box').length == 1) {
        comment_element.getElementsByClassName('reply-box')[0].remove();
    }
    else {
        reply_box = document.createElement('div');
        reply_box.className = 'reply-box';
        reply_box.innerHTML = `
        <textarea class="form-control" name="reply-input" id="reply-input" rows="10" placeholder="Reply..."></textarea>
        <button id="reply-button" class="btn btn-dark mt-3 mb-3" onclick="save_reply(this.parentNode.parentNode)">Reply</button>`;
    
        comment_element.appendChild(reply_box);
    }
}

function save_reply(comment_element) {
    const url = `${window.location.origin}/reply/`;

    let reply_input = comment_element.querySelector('textarea#reply-input');
    if (!reply_input.value) {
        return 1;
    }

    $.ajax({
        url: url,
        method: "POST",
        data: {
            "reply": reply_input.value,
            "comment_id": comment_element.title,
            "csrfmiddlewaretoken": csrfmiddlewaretoken
        },
        success: function (data, status, xhr) {
            comment_element.getElementsByClassName('reply-box')[0].remove();
            comment_element.innerHTML += `<hr>
            <div class="reply" title="${data.reply_id}" style="margin-left: 10%;">
                <p><b><a class="text-black link-primary text-decoration-none" href="">${data.username}</a></b> - Just now</p>
                <p>
                    ${data.reply}
                    <a class="text-black link-secondary text-decoration-none" style="cursor: pointer;" onclick="delete_reply(this.parentNode.parentNode)">delete</a>
                </p>
            </div>`
        },
        error: function (jqXhr, textStatus, errorMessage) {
            alert(jqXhr.responseJSON.error);
        }
    })
}

function delete_reply(reply_element) {
    const url = `${window.location.origin}/delete-reply/`;

    $.ajax({
        url: url,
        method: "POST",
        data: {
            "reply_id": reply_element.title,
            "csrfmiddlewaretoken": csrfmiddlewaretoken
        },
        success: function (data, status, xhr) {
            reply_element.remove()
        },
        error: function (jqXhr, textStatus, errorMessage) {
            alert(jqXhr.responseJSON.error);
        }
    })
}

function delete_comment(comment_element) {
    const url = `${window.location.origin}/delete-comment/`;

    $.ajax({
        url: url,
        method: "POST",
        data: {
            "comment_id": comment_element.title,
            "csrfmiddlewaretoken": csrfmiddlewaretoken
        },
        success: function (data, status, xhr) {
            comment_element.remove()
        },
        error: function (jqXhr, textStatus, errorMessage) {
            alert(jqXhr.responseJSON.error);
        }
    })
}
