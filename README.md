# flask-basic-auth-nginx

Example of using Flask-BasicAuth and Nginx as a Reverse Proxy with the Authentication header in Nginx

## The Question

How do I reverse proxy to a backend that requires basic auth?

## Background

This example will show how to pass authorization headers via Nginx to a backend that requires authentication. We will have a flask application using the flask-basicauth package to protect a route with basic authentication as our backend. 

The front end reverse proxy which is using nginx, has its own set of credentials, we need to instruct nginx to pass the authentication to the backend, once the basic auth of nginx has succeeded.
