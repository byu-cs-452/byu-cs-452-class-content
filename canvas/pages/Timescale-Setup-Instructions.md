### Setup your postgres in **Timescale**

#### Create an Account

First, create a free account with Timescale. [Click hereLinks to an external site.](https://console.cloud.timescale.com/signup) to sign up for a 30 day trial (no credit card required).

#### Create a Service

Create a database instance by clicking on "Create a Service"

![Screenshot 2024-08-14 at 2.56.07 PM.png](https://byu.instructure.com/courses/26600/files/9019830/preview)

#### Select the service type

Here we will choose "Time Series and Analytics"

![Screenshot 2024-08-14 at 2.56.59 PM.png](https://byu.instructure.com/courses/26600/files/9019831/preview)

#### Configure the service

You can leave the Region, Compute, Environment and Service Name settings at their default values. Then click "Create Service" at the bottom

![Screenshot 2024-08-14 at 2.57.59 PM.png](https://byu.instructure.com/courses/26600/files/9019833/preview)

This will deploy your postgres instance!

#### Copy the connection string

Finally, make sure to copy your connection string. You will either paste this into your code, or load it into your recommendation app with an environment variable. For example mine is:

```
postgres://tsdbadmin:ejdwe3un4v2l43wl@b44sdq0rd0.s2ajcw96u3.tsdb.cloud.timescale.com:33611/tsdb?sslmode=require
```

![Screenshot 2024-08-14 at 3.00.34 PM.png](https://byu.instructure.com/courses/26600/files/9019837/preview)