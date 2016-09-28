Quickstart:
-----------
```
git clone git://github.com/amesshaps/find-my-dress
cd find-my-dress
virtualenv env
source env/bin/activate
pip install -r requirements.txt
make serve
```

# Installing Open-CV
--------------------
... is a giant pain in the ass, apparently.  The hacks in [this article](http://www.mobileway.net/2015/02/14/install-opencv-for-python-on-mac-os-x/)
were helpful in getting set up, but they demonstrate a global installation.  If you want to install into a local
virtualenv, just symlink the `cv.py` and `cv2.so` files into the virtualenv instead:
```
cd /path/to/virtualenv
ln -s /usr/local/Cellar/opencv/<version>/lib/python/site-packages/cv.py lib/python/site-packages/cv.py
ln -s /usr/local/Cellar/opencv/<version>/lib/python/site-packages/cv2.so lib/python/site-packages/cv2.so
```

(Honestly, the global install may be a better option if you can live with it, as numpy is also required
and can be another pain to install.)
