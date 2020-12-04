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