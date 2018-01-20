cp -R ./* /data/tigereye/
cd /data/tigereye
mkdir logs
ps ax |grep gunicorn|grep -v grep|cut -d ' ' -f1|xargs kill
gunicorn -w2 -D -b 0.0.0.0:5000 wsgi:application
