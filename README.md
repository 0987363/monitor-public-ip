- Monitor public ip and send modified to TG.
- Manual example:
```
python3 main.py --name "RouterOS" --cache ./public_ip_cache.txt --token "xxx" --chat "yyy
```

- Auto example:
```
echo '0 * * * * python3 main.py --name "RouterOS" --cache ./public_ip_cache.txt --token "xxx" --chat "yyy' >> /etc/crontab
```
