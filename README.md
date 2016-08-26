# Parkleitsystem API Kleve

Experimental Flask app that scrapes data from the Cleves park guidance system and RESTfully exposes them.

Unfortunately, the source website uses server side caching, so recurrent use wil feed the API  with stale data. A more robust back end solution is required to make it truly useful (maybe at some point in the future).

Demo:

[parkleitsystem.nitri.de/api/parkleitsystem](http://parkleitsystem.nitri.de/api/parkleitsystem)

![](pls.png?raw=true)
