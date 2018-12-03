// reference
// https://qiita.com/Mono/items/54c362034fef14ddad02

function summernoteOnImageUpload(files) {
    $.each(files, function(idx, file) {
        var max_width = 1000;
        var max_height = 1000;

        var reader = new FileReader();

        reader.onload = function() {
            var tmpImg = new Image();
            tmpImg.src = reader.result;

            tmpImg.onload = function() {
                var tmpW = tmpImg.width;
                var tmpH = tmpImg.height;

                if (tmpW > tmpH) {
                    if (tmpW > max_width) {
                       tmpH *= max_width / tmpW;
                       tmpW = max_width;
                    }
                } else {
                    if (tmpH > max_height) {
                       tmpW *= max_height / tmpH;
                       tmpH = max_height;
                    }
                }
                var canvas = document.createElement('canvas');
                canvas.width = tmpW;
                canvas.height = tmpH;
                var ctx = canvas.getContext('2d');
                ctx.drawImage(this, 0, 0, tmpW, tmpH);
                sURL = canvas.toDataURL("image/jpeg");
                var imgNode = document.createElement('img');
                imgNode.src=sURL;

                $('#editcontent,#content').summernote('insertNode', imgNode);
            }
        }
        reader.readAsDataURL(file);
    });
}