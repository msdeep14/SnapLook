# SnapLook

application developed in django(python) which extracts images of specific hashtag from twitter and also analyze the images for their facial expression(anger, contempt, disgust, fear, happiness, neutral, sadness and surprise) using MICROSOFT emotion API.

## Installation

  1. install TwitterAPI `pip install TwitterAPI`
  2. app is developed in virtual env (name = vsnap), `python3 -m venv vsnap`
  3. get consumer_key, consumer_secret, access_token, access_token_key from https://dev.twitter.com/
  4. get your microsoft subscription key from azure.microsoft.com
  5. host is set to `127.0.0.1:8000`, you can change according to your setup
  
## Execution

After completing the setup, enter a string for example `#hashtag` to get the images, initial hashtag is set to `#katrinakaif`

You can get all the images you searched by using hashtag keyword as `#msdeep14`

### initial code references : 

[Photo Gallery Web Application](https://github.com/amangoeliitb/Photo-Gallery-Web-Application)
