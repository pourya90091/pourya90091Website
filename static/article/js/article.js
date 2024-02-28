const commentInput = document.getElementById('comment-input');
const commentButton = document.getElementById('comment-button');
const articleId = document.getElementById('content').title;
const csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

commentButton.onclick = function () {
    const url = `${window.location.origin}/comment/`;

    if (!commentInput.value) {
        return 1;
    }

    $.ajax({
        url: url,
        method: 'POST',
        data: {
            'comment': commentInput.value,
            'articleId': articleId,
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        },
        success: function (data, status, xhr) {
        commentInput.value = '';

        const comments = document.getElementById('comments');
        comments.innerHTML += `<div class="comment" title="${data.comment_id}">
        <p><b><a class="text-black link-primary text-decoration-none" href="">${data.username}</a></b> - Just now</p>
        <p>
            ${data.comment}
            <a class="text-black link-secondary text-decoration-none" style="cursor: pointer;" onclick="replyBox(this.parentNode.parentNode)">reply</a>
            <a class="text-black link-secondary text-decoration-none" style="cursor: pointer;" onclick="deleteComment(this.parentNode.parentNode)">delete</a>
        </p>
      </div>
      <hr>`;
        },
        error: function (jqXhr, textStatus, errorMessage) {
            alert(jqXhr.responseJSON.error);
        }
    })
}

function replyBox(commentElement) {
    if (commentElement.getElementsByClassName('reply-box').length == 1) {
        commentElement.getElementsByClassName('reply-box')[0].remove();
    } else {
        newReplyBox = document.createElement('div');
        newReplyBox.className = 'reply-box';
        newReplyBox.innerHTML = `
        <textarea autofocus class="form-control" name="reply-input" id="reply-input" rows="10" placeholder="Reply..."></textarea>
        <button id="reply-button" class="btn btn-dark mt-3 mb-3" onclick="saveReply(this.parentNode.parentNode)">Reply</button>`;
    
        commentElement.appendChild(newReplyBox);
    }
}

function saveReply(commentElement) {
    const url = `${window.location.origin}/reply/`;

    let replyInput = commentElement.querySelector('textarea#reply-input');
    if (!replyInput.value) {
        return 1;
    }

    $.ajax({
        url: url,
        method: 'POST',
        data: {
            'reply': replyInput.value,
            'comment_id': commentElement.title,
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        },
        success: function (data, status, xhr) {
            commentElement.getElementsByClassName('reply-box')[0].remove();
            commentElement.innerHTML += `<hr>
            <div class="reply" title="${data.reply_id}" style="margin-left: 10%;">
                <p><b><a class="text-black link-primary text-decoration-none" href="">${data.username}</a></b> - Just now</p>
                <p>
                    ${data.reply}
                    <a class="text-black link-secondary text-decoration-none" style="cursor: pointer;" onclick="deleteReply(this.parentNode.parentNode)">delete</a>
                </p>
            </div>`;
        },
        error: function (jqXhr, textStatus, errorMessage) {
            alert(jqXhr.responseJSON.error);
        }
    })
}

function deleteReply(replyElement) {
    const url = `${window.location.origin}/delete-reply/`;

    $.ajax({
        url: url,
        method: 'POST',
        data: {
            'reply_id': replyElement.title,
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        },
        success: function (data, status, xhr) {
            replyElement.remove();
        },
        error: function (jqXhr, textStatus, errorMessage) {
            alert(jqXhr.responseJSON.error);
        }
    })
}

function deleteComment(commentElement) {
    const url = `${window.location.origin}/delete-comment/`;

    $.ajax({
        url: url,
        method: 'POST',
        data: {
            'comment_id': commentElement.title,
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        },
        success: function (data, status, xhr) {
            commentElement.remove();
        },
        error: function (jqXhr, textStatus, errorMessage) {
            alert(jqXhr.responseJSON.error);
        }
    })
}
