# checkers-bot

## Setup Instructions

1. Git Clone repo
2. Go to develop branch
3. `npm install -g firebase-tools`
4. `npm install`
5. run `firebase login` then login with your betterSG email
6. cd into functions
7. run `npm run build:watch`. This enables hot reload, if you are changing the functions live it will update the emulators
8. cd .. back into root
9. run `firebase emulators:start` on another shell
10. you should now be able to hit the functions urls at http://127.0.0.1:5001/checkmate-373101/asia-southeast1/xxxxx successfully
11. you should also be able to see the hosting site at http://127.0.0.1:5000/
12. Now can work on the functions or the website
13. Rmb to use https://ngrok.com/ (can install vs code extension) to expose localhost as an internet URL, in case you want to run locally but test with actual Telegram
14. I've set it up as a single page app. If you dont want a single page app, go to firebase.json and remove the rewrites section that is sending everything back to index.html.
