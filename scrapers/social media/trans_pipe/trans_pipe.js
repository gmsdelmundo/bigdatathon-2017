const translate = require('google-translate-api');
const files = require('fs');

let tweet = files.readFileSync("tweets_only.csv", "utf8")
let tweetsarr = tweet.split("\n")
let tweetsarrmod = [];
for(let i = 0; i < tweetsarr.length; i++){
	tmod = tweetsarr[i].split(/(,(?=\S))/).filter(function (s){
			return s!=",";		
		});
	tweetsarrmod.push(tmod)
}


translatedtweets = [];
for(let i = 0; i < tweetsarrmod.length; i++){
	translate(tweetsarrmod[i][2], {to: 'en'}).then(res => {
		    tweetsarrmod[i][2] = res.text;
		    console.log(tweetsarrmod[i].join(","));
		    
		    //=> I speak English 
		    //=> nl 
		}).catch(err => {
		    console.error(err);
		});
	
}
