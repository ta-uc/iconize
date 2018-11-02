"use strict";
let downKeyCode = null;
let getParam = (name, url) => {
    url = location.search;
    name = name.replace(/[\[\]]/g, "\\$&");
    let regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) {
        return '';
    }
    if (!results[2]) {
        return '';
    }
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}
let getId = iD => {
    if (iD) {
        return iD;
    } else {
        const rexp = "[a-zA-Z0-9]{32}";
        let path = location.pathname;
        return path.match(rexp);
    }
}
let createBlob = html => {
    let prpt = {
        type: "text/html",
    }
    let data = [html]
    let blob = new Blob(data, prpt);
    return blob;
}
let getData = () => {
    let author = $("#input_author").val();
    let title = $("#input_title").val();
    let s_title = $("#input_short_title").val()
    let code = createBlob($("#editcontent").summernote("code"));
    let color = $("#input_color").val();
    color = color.slice(1);
    let file = $('#input_file')[0].files[0];
    let del_icon = $('#del_icon');
    let date = $("#input_date").val();
    let data = new FormData();
    let token = getParam("token");
    data.append('author', author);
    data.append('title', title);
    data.append('s_title', s_title);
    data.append('code', code);
    data.append('color', color);
    data.append('date', date);
    data.append('token', token);
    data.append('iconfile', file);
    data.append('del', del_icon);
    return data;
}
let activateSummernote = html => {
    $("#editcontent,#content").append(html).summernote({
        height: 250,
        fontNames: ["YuGothic", "Yu Gothic", "Hiragino Kaku Gothic Pro", "Meiryo", "sans-serif", "Arial", "Arial Black", "Comic Sans MS", "Courier New", "Helvetica Neue", "Helvetica", "Impact", "Lucida Grande", "Tahoma", "Times New Roman", "Verdana"],
        fontSizes: ['8', '9', '10', '11', '12', '13', '14', '18', '24', '36'],
        toolbar: [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['paragraph']],
            ['table', ['table']],
            ['insert', ['picture', 'link']],
            ['view', ['fullscreen', 'codeview']],
            ['help', ['help']]
        ],
        maximumImageFileSize: 524288 * 2, //1MB
        placeholder: "Edit here",
    });
}
let xhrSetting = () => {
    let XHR = $.ajaxSettings.xhr();
    XHR.onprogress = e => {
        if (e.lengthComputable) {
            $("#progressGet").val(e.loaded / e.total);
        }
    };
    XHR.upload.onprogress = e => {
        $("#progress").val(e.loaded / e.total);
        if (e.lengthComputable) {}
    };
    return XHR;
}
let getContent = () => {
    let iD = getId();
    $("#progressGet").css("display", "inline");
    $.ajax({
        xhr: xhrSetting,
        url: "/posts/" + iD + "/content/",
        type: "GET",
        dataType: "html",
        contentType: "text/html"
    }).fail(() => {
        $("#editcontent,#content").html("<p class='alert alert-warning'>Failed to load the content.</p>");
    }).done(d => {
        let str = window.location.href;
        if (str.indexOf("edit") != -1) {
            activateSummernote(d);
        } else {
            $("#editcontent,#content").append(d);
        }
    }).always(()=>{
        $("#progressGet").css("display", "none");
    });
}
let post = () => {
    let d = getData();
    if (!validate(d)) return 1;
    $("#progress").css("visibility", "visible");
    $.ajax({
        xhr: xhrSetting,
        url: "/posts/create/",
        type: "POST",
        data: d,
        processData: false,
        contentType: false
    }).done(r => {
        if (r!=="error"){
            let iD = String(r[0]);
            let token = String(r[1]);
            $("#edit_link").click(() => {
                window.location.href = "/posts/" + iD + "/edit?token=" + token;
            });
            $("#jump_post").click(() => {
                jump_post(iD);
            });
            $("#token").val(token)
            $("#input_file,#post_button").css("visibility", "hidden");
            $("#msg").css("visibility", "visible");
            setTimeout(() => {
                window.scrollTo(0, document.body.scrollHeight);
            }, 10);
        }else{
            //server error
            $("#err").html("<p class='alert alert-warning'>Failed to upload. Try later.</p>")
        }
    }).fail(() => {
        //when connection failed.
        $("#err").html("<p class='alert alert-warning'>Failed to upload. Try later.</p>")
    }).always(()=>{
        $("#progress").css("visibility", "hidden");
    });
}
let update = () => {
    let d = getData();
    if (!validate(d)) return 1;
    $("#progress").css("visibility", "visible");
    $.ajax({
        xhr: xhrSetting,
        url: "./",
        type: "POST",
        data: d,
        processData: false,
        contentType: false
    }).done(r => {
        if(r !=="error"){
            alert(r);
            $("#progress").css("visibility", "hidden");
            $("#update_button").attr("disabled", true);
            setTimeout(() => {
                window.scrollTo(0, document.body.scrollHeight);
            }, 10);
            let iD = getId();
            window.location.href = "/posts/" + iD;
        }else{
            $("#err").html("<p class='alert alert-warning'>Failed to update. Try later.</p>")
        }
    }).fail(()=>{
        $("#err").html("<p class='alert alert-warning'>Failed to upload. Try later.</p>")
    }).always(()=>{
        $("#progress").css("visibility", "hidden");
    });
}
let deletePost = () => {
    let iD = getId();
    let token = getParam("token");
    let data = {
        "token": token
    };
    $.post("/posts/" + iD + "/delete/", data).done(r => {
            if(r !== "error"){
                alert(r);
            }else{
                $("#err").html("<p class='alert alert-warning'>Failed to delete. Try later.</p>")
                return 1;
            }
    });
    window.location.href = "/posts/";
    $("#delete_button").attr("disabled", true);
}
let sendToken = () => {
    let iD = getId();
    let token = $('#input_token').val();
    window.location.href = '/posts/' + iD + '/edit?token=' + token
}
let validate = data => {
    const cre = new RegExp("^([a-fA-F0-9]{6}$)|^([a-fA-F0-9]{8}$)|^([a-fA-F0-9]{3}$)");
    if (data.get("author") == '') {
        $("#input_author").css({
            border: "1px solid #FE2E2E"
        }).focus().tooltip("enable").tooltip("show");
        return false;
    }
    if (data.get("title") == '') {
        $("#input_title").css({
            border: "1px solid #FE2E2E"
        }).focus().tooltip("enable").tooltip("show");
        return false;
    }
    if (data.get("date") == '') {
        $("#input_date").css({
            border: "1px solid #FE2E2E"
        }).focus().tooltip("enable").tooltip("show");
        return false;
    }
    if ($("#editcontent").summernote("isEmpty")) {
        $("#wrap-editor").tooltip("enable").tooltip("show").focus();
        $("#editcontent").summernote({
            focus: true
        });
        return false;
    }
    if (!cre.test(data.get("color")) && data.get("color") !== "") {
        $("#input_color").css({
            border: "1px solid #FE2E2E"
        }).focus().tooltip("enable").tooltip("show");
        return false;
    }
    if (data.get("iconfile").size > 1024 * 512) {
        alert("File size over 512KB");
        return false;
    }
    return true;
}
let jump_post = iD => {
    let idstr = String(getId(iD))
    window.location.href = "/posts/" + idstr;
}
$(document).ready(() => {
    let str = window.location.href;
    if (str.indexOf("create") === -1) { // When the page is loaded as edit mode or view.
        getContent();                   // Fetch content and activate summernote.
    }else{                              // When the page is loaded as create mode.
        activateSummernote();
    };
    // When the page is loaded as view. Register the sw for each post.
    if ('serviceWorker' in navigator && (str.indexOf("create") === -1 &&
        str.indexOf("edit") === -1)) {
        const iD = getId();
        navigator.serviceWorker
            .register("/posts/"+iD+"/service-worker.js", {
                scope: "/posts/"+iD+"/"
            })
            .then(() => {
                console.log('Service Worker Registered');
            });
    }
    // When the page is loaded as create mode or edit mode.
    if (str.indexOf("create") !== -1 || str.indexOf("edit") !== -1){
        $("input:first").focus();
        let color = $("#input_color").val();
        $("#input_color").css("background-color", color);
        $('[data-toggle="tooltip"]').tooltip().tooltip("disable");
    }
    if (navigator.onLine){
        $("#badge").html('<span class="label label-success">online</span>');
    }else{
        $("#badge").html('<span class="label label-default">offline</span>');
    }
});
$("#post_button").click(post);
$("#update_button").click(update);
$("#delete_button").click(deletePost);
$("#token_button").click(sendToken);
$("input").on("keyup", function (e) {
    if ($(this).val().length >= $(this).attr("maxlength") ||
        e.which === downKeyCode && e.which === 13) {
        $(this).nextAll("input:first").focus();
    }
});
$("input").on("keydown", e => {
    downKeyCode = e.which;
})
$("#input_token").on("keyup", e => {
    if (e.which === 13) sendToken();
})
$("#input_date").change(() => {
    $("#editcontent").summernote({
        focus: true
    });
});
$("#input_color").click(function() {
    $(this).val("");
    $(this).css("background-color", "#FFF");
});
$("#input_color").change(function() {
    $(this).css("background-color", $(this).val());
});
$("#input_author,#input_title,#input_date,#input_color,#wrap-editor").on("keypress click", function() {
    $(this).css("border", "none").tooltip("hide").tooltip("disable");
});
$("#cpbtn").click(()=>{
    document.querySelector("#token").select();
    document.execCommand("copy");
})
window.addEventListener("online",() => {
    $("#badge").html('<span class="label label-success">online</span>');
});
window.addEventListener("offline",() => {
    $("#badge").html('<span class="label label-default">offline</span>');
});