pyuic5 design.ui -o design.py

QT_DEBUG_PLUGINS=1 python app.py
ln -s /usr/lib/x86_64-linux-gnu/libxcb-util.so.0 /usr/lib/x86_64-linux-gnu/libxcb-util.so.1
