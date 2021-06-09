# flask-basic-auth-nginx

Example of using Flask-BasicAuth and Nginx as a Reverse Proxy with the Authentication header in Nginx

## The Question

How do I reverse proxy to a backend that requires basic auth?

## Background

This example will show how to pass authorization headers via Nginx to a backend that requires authentication. We will have a flask application using the flask-basicauth package to protect a route with basic authentication as our backend. 

The front end reverse proxy which is using nginx, has its own set of credentials, we need to instruct nginx to pass the authentication to the backend, once the basic auth of nginx has succeeded.

## Backend Authentication

The backend uses [Flask-BasicAuth](https://flask-basicauth.readthedocs.io/en/latest/) and is defined in line 6 and 7 of `flask-app/app.py`:

```
app.config['BASIC_AUTH_USERNAME'] = 'john'
app.config['BASIC_AUTH_PASSWORD'] = 'matrix'
```

And requires to authenticate before you can see the route:

```
@app.route('/secret')
@basic_auth.required
def secret_view():
    return 'authorized'
```

## Frontend Proxy

The frontend uses nginx and the `/` location block is protected with basic auth which was configured with `nginxuser` and password `password` with the following command:

```
htpasswd -c nginx/passwords nginxuser
```

For nginx in order to pass authentication to the backend, we need the username and password combination to be encoded with base64:

```
echo -n "john:matrix" | base64
am9objptYXRyaXg=
```

In our `nginx/nginx-flask.conf` configuration for nginx, we will pass it as a authentication header: `proxy_set_header Authorization "Basic am9objptYXRyaXg=";`, which will result in:

```
server {
    listen 80;
    server_name _;

    location / {
        auth_basic "Restricted access to this site";
        auth_basic_user_file /etc/nginx/passwords;
        proxy_pass http://flask-app:5000;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Authorization "Basic am9objptYXRyaXg=";
    }
}
```

## Usage

To boot the stack, get the source:

```
git clone https://github.com/ruanbekker/flask-basic-auth-nginx
cd flask-basic-auth-nginx
```

Then build and start the containers:

```
docker-compose up --build -d
```

Make a request with no authentication:

```
curl http://localhost:8080
<html>
<head><title>401 Authorization Required</title></head>
<body>
<center><h1>401 Authorization Required</h1></center>
<hr><center>nginx/1.19.10</center>
</body>
</html>
```

Make a request and pass the authentication (making sure nginx passes authentication and passes to the backend on a non protected route):

```
curl -u "nginxuser:password"  http://localhost:8080/welcome
welcome
```

Make a request and pass the authentication (making sure that the authorization header works to the protected route on the backend):

```
curl -u "nginxuser:password"  http://localhost:8080/secret
authorized
```
