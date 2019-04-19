# E-Patient

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

E-Patient is healthcare website, book appointments and view health records.

  - Type some Markdown on the left
  - See HTML in the right
  - Magic

# Features!

  - 2 factor authentication(email verification and phone number verificaiton)
  - Strong security


You can also:
  - Import and save files from GitHub, Dropbox, Google Drive and One Drive
  - Drag and drop markdown and HTML files into E-Patient
  - Export documents as Markdown, HTML and PDF

### User Levels

There are 3 user levels:

* [administrator] - manage all users, (add,delete)
* [doctor] - view Health records and acept appointments
* [patient] - Search doctors and book appointments.

### Installation

E-Patient requires [Python](https://www.python.org/downloads/) 3.0+ to run.

Install the dependencies and devDependencies and start the server.

```sh
$ pip3 install django
$ pip3 install twilio
$ node app
```

For production environments...

```sh
$ npm install --production
$ NODE_ENV=production node app
```

### Plugins

e-patient is currently extended with the following plugins. Instructions on how to use them in your own application are linked below.

| Plugin | README |
| ------ | ------ |
| Dropbox | [plugins/dropbox/README.md][PlDb] |
| Github | [plugins/github/README.md][PlGh] |
| Google Drive | [plugins/googledrive/README.md][PlGd] |


### Development

Want to contribute? Great!
Open your favorite Terminal and run these commands.

Run Server :
```sh
$ python3 manage.py runserver 0.0.0.0:80
```

Migrate:
```sh
$ python3 manage.py migrate
```

#### Building for source
For production release:

  -ALLOWED_HOSTS = ['*']


Edit settings.py to look for static files in a directory called static in our root directory:

  -STATIC_URL = '/python/static/'
  -STATIC_ROOT = '/usr/local/lsws/Example/demo/public/static'

Collect static files:
```sh
$ mkdir -p public/static
$ python3 manage.py collectstatic
```
Change owner::
```sh
$ chown -R nobody:nogroup /usr/local/lsws/Example/demo
```

Verify the deployment by navigating to your server address in your preferred browser.

```sh
127.0.0.1:8000
```

### Todos

 - Write MORE Tests
 - Add Night Mode

License
----

MIT

**Please visit live site**
https://e-patient.co/
