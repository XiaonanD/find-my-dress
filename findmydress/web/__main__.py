#! /usr/bin/env python
from findmydress.web.app import app
from findmydress.web import views


if __name__ == '__main__':
    app.run(debug=True)
