# Strava-Viewer
**...for viewing summaries of your activities using Dash framework.**

*You have to make some things before you can read your activities:*


Go to page: [towardsdatascience...](https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde)

Do as described there: (*You need to have Strava account and some activities on it*). Below is short summary of it.

1. You have to:

    - set up your API app in Strava
    - and then get access and refresh token to get data from Strava

2. Use browser and following links to get access and refresh token:

   Manually in browser:
   
   - https://www.strava.com/oauth/authorize?client_id=>>your_client_id<<&redirect_uri=http://localhost&response_type=code&scope=activity:read_all  
   This will open page:
   
   - http://localhost/?state=&code=>>somecode<<&scope=read,activity:read_all  
   Get **somecode** and put it in POST request:

   POST request:

    - https://www.strava.com/oauth/token?client_id=your_client_id&client_secret=your_client_secret&code=your_code_from_previous_step&grant_type=authorization_code

3. from *response* get: **refresh_token** and **access_token**

Put your **client_id**, **client_secret** and obtained in previous steps **access_token** and **refresh_token** in ***token.yaml*** file. It should look like this:

```{
client_id: 'xxxxx'
client_secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
refresh_token: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
access_token: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
grant_type: 'refresh_token'
f: 'json'}
```

Getting activities is based on code you can find here: [github...](https://github.com/franchyze923/Code_From_Tutorials/blob/master/Strava_Api/strava_api.py)

**access_token** could be used directly by it expires so **refresh_token** is used to get new access token.