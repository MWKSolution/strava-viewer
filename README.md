# Strava-Viewer  
**...for viewing simple summaries of your Strava activities using  [Dash](https://dash.plotly.com) framework and [Strava API](https://developers.strava.com)**  
*Working example could be seen at* **[Heroku](https://strava-viewer-mwk.herokuapp.com/)**

---

Before you start your application...  
1. You have to:
    - have Strava account and some activities on it
    - set up your API app in [Strava](https://developers.strava.com/docs/getting-started/#account)
    - and then get **client_id** and **client_secret**
2. Then use browser and following links to get **access** and **refresh** tokens:  
   Manually in browser *(put appropriate data when in CAPITALS)*:
   - https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost&response_type=code&scope=activity:read_all  
   This will open Strava authorization page. Click authorize. This will in turn open page:
   - http://localhost/?state=&code=SOMECODE&scope=read,activity:read_all  
   Get **somecode** and put it in POST request:
   POST request:
   - https://www.strava.com/oauth/token?client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&code=SOMECODE_FROM_PREVIOUS_STEP&grant_type=authorization_code
4. from *response* get: **refresh_token** and **access_token**

Put your **client_id**, **client_secret** and obtained in previous steps **access_token** and **refresh_token** in ***token.yaml*** file. It should look like this:
```{
client_id: 'xxxxx'
client_secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
refresh_token: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
access_token: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
grant_type: 'refresh_token'
f: 'json'
```
Now you can get your activities from Strava.  
[getLoggedInAthleteActivities](https://developers.strava.com/docs/reference/#api-Activities-getLoggedInAthleteActivities)

**access_token** could be used directly by it expires so **refresh_token** is used to get new access token.  
[Refreshing Expired Access Tokens](https://developers.strava.com/docs/authentication/#refreshingexpiredaccesstokens)

---

### Strava-Viewer app

Some simple summaries of activities data are presented using  **[Dash](https://dash.plotly.com)** framework.  
When first used, app has empty dashboard. Click **Refresh data** or **Reload all data**, this will create **activities.json** file or will connect to redis database.  
You should have ***redis.yaml*** file with valid data to connect to redis database:   
```
host: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
port: xxxxx
username: 'xxxxxxxx'
password: 'xxxxxxxx'
```
After adding new activities to Strava clicking **Refresh data**, this will update **activities.json** file or redis database and than barchart.

---

### Heroku deployment  
!!! All necessary files for Heroku deployment are included but don't forget to remove ***token.yaml*** and ***redis.yaml*** from ***.gitignore***!!!
