document.body.onload = function(){
      $("#sign-up-section").hide();
}

const switchWindows = function(target){

      $("#sign-in-section").hide();
      $("#sign-up-section").hide();
      $("#spinner").show();
      setTimeout(function(){ 
            $("#spinner").hide();
            switch(target){
                  case "sign-in-section" : $("#sign-in-section").show();break;
                  case "sign-up-section" : $("#sign-up-section").show();break;
                  default : $("#sign-in-section").show();break;
            }
      }, 200);
};

const postPreview = {
      preview: function(){
            $("#previewPostTitle").text($("#postTitle").val());
            $("#previewPostCategory").text($("#postCategory").val());
            $("#previewPostDate").text($("#postDate").val());
            $("#previewPostAuthor").text($("#postAuthor").val());
            $("#previewPost").html($("#editor").html());
            $('#preview-modal').modal('toggle');
            readTime.reflect("previewPost","previewPostTimer");
      },

}

const readTime = {
      avgWordsPerMin: 200,
      post: null,
      postTimer: null,
      getReadTime: function(){
            let count = this.getWordCount(this.post);
            let time = Math.ceil(count / this.avgWordsPerMin);           
            document.getElementById(this.postTimer).innerHTML = time  + " minute read";
      },
      getTimeDetails: function(){
            let count = this.getWordCount(this.post);
            document.getElementById(this.postTimer).title = count + " words read at " + this.avgWordsPerMin + " words per minute.";
      },
      getWordCount: function(){
            return this.post.innerText.match(/\w+/g).length;
      },
      reflect: function(post,postTimer){
            this.post = document.getElementById(post);
            this.postTimer = postTimer;
            this.getReadTime();
            this.getTimeDetails();
      }
}

$(function () {
      $('[data-toggle="tooltip"]').tooltip()
})
