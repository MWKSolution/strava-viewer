# Strava-Viewer

**...for viewing simple summaries of your Strava activities using  [Dash](https://dash.plotly.com) framework and [Strava API](https://developers.strava.com)**  
*Working example could be seen at* [Heroku](https://strava-viewer.herokuapp.com/)
---

*You have to do some things before you can read your activities:*


Go to this page: [towardsdatascience.com...](https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde)  
Do as described there: (*You need to have Strava account and some activities on it*). Below is short summary of it.
1. You have to:  
    - set up your API app in Strava
    - and then get **client_id** and **client_secret**
2. Then use browser and following links to get **access** and **refresh** tokens:  
   Manually in browser:
   - https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost&response_type=code&scope=activity:read_all  
   This will open Strava authorization page. Click authorize. This will in turn open page:
   - http://localhost/?state=&code=SOMECODE&scope=read,activity:read_all  
   Get **somecode** and put it in POST request:
   POST request:
    - https://www.strava.com/oauth/token?client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&code=SOMECODE_FROM_PREVIOUS_STEP&grant_type=authorization_code
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
Now you can get your activities from Strava.  
Getting activities is based on code you can find here: [github.com...](https://github.com/franchyze923/Code_From_Tutorials/blob/master/Strava_Api/strava_api.py)  
**access_token** could be used directly by it expires so **refresh_token** is used to get new access token.

---

### Strava-Viewer app

Some simple summaries of activities data are presented using  [Dash](https://dash.plotly.com) framework.  
When first used, app has empty dashboard. Click **Load or refresh data**, this will crate **activities.json** file.  
After adding new activities to Strava clicking **Load or refresh data**, this will update **activities.json** file and barchart.

---

### Heroku deployment  
!!! All necessary files for Heroku deployment are included but don't forget to remove ***token.yaml*** from ***.gitignore***!!!  
You can also remove ***activities.json*** from ***.gitignore*** which will prevent see empty barchart at first start or after Heroku dyno restart.