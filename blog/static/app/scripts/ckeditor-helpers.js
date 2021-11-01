function runCallbackOnCkeditorChanges(editor, cb) {
    element = editor.element;
    editor.on('change', function() {
        cb();
    });
}

function addInsertImageButtonToCkeditor(editor) {
    editor.addCommand("insertImgCmd", {
        exec: function(editor) {
            editor.insertHtml(`
            <div class="img_holder">
                <div class="img_caption">This is your image caption. You can delete it if desired.</div>
                <img class="w-full" src="https://i.imgur.com/FNgayBK.png"/>
            </div>`);
        }
    });
    editor.ui.addButton('InsertCustomImage', {
        label: "Insert Image",
        command: 'insertImgCmd',
        icon: `/static/app/images/picture-icon.svg`
    });
}

function addInsertVideoButtonToCkeditor(editor) {
    editor.addCommand("insertYouTubeVideo", {
        exec: function(editor) {
            editor.insertHtml(`
            <iframe 
                width="100%" 
                height="400"
                src="https://www.youtube.com/embed/9c_uKTU3VxI?rel=0"
                frameborder="0"
                allow="autoplay;
                encrypted-media"
                allowfullscreen="">
            </iframe>`);
        }
    });
    editor.ui.addButton('InsertYouTubeVideo', {
        label: "Embed YouTube Video",
        command: 'insertYouTubeVideo',
        icon: `/static/app/images/youtube.svg`
    });
}