function runCallbackOnCkeditorChanges(editor, cb) {
    element = editor.element;
    editor.on('change', function() {
        cb();
    });
}

function configurePostEditor(editor) {
    editor.config.contentsCss = [ '/static/app/css/tailwind-output.css' ];
    editor.config.extraAllowedContent = 'div(img_holder,img_caption,img){*}; iframe(img)[*]{*};';
    editor.config.extraPlugins = 'autogrow';
    editor.config.autoGrow_minHeight = 300;
    editor.config.autoGrow_maxHeight = 500;
    editor.config.autoGrow_onStartup = true;
    editor.config.bodyClass = 'post-content';
}

function addInsertImageButtonToCkeditor(editor) {
    editor.addCommand("insertImgCmd", {
        exec: function(editor) {
            editor.insertHtml(`
                <div class="img_holder">
                    <div class="img_caption">This is your image caption. You can edit or delete it if desired.</div>
                    <div class="img" style="background-image: url('https://i.imgur.com/FNgayBK.png')"></div>
                </div>
                <p></p>`
            );
        }
    });
    editor.ui.addButton('InsertCustomImage', {
        label: "Insert Image",
        command: 'insertImgCmd',
        icon: `{% static 'app/images/picture-icon.svg' %}`
    });
}

function addInsertVideoButtonToCkeditor(editor) {
    editor.addCommand("insertYouTubeVideo", {
        exec: function(editor) {
            editor.insertHtml(`
                <div class="img_holder">
                    <div class="img_caption">This is your video caption. You can edit or delete it if desired.</div>
                    <iframe 
                        class='img'
                        width="100%" 
                        src="https://www.youtube.com/embed/jmMpw6fDaXg"
                        frameborder="0"
                        allow="autoplay;
                        encrypted-media"
                        allowfullscreen="">
                    </iframe>
                </div>
                <p></p>`
            );
        }
    });
    editor.ui.addButton('InsertYouTubeVideo', {
        label: "Embed YouTube Video",
        command: 'insertYouTubeVideo',
        icon: `{%static'app/images/youtube.svg'%}`
    });
}