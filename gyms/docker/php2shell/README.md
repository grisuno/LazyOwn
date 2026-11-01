# php2shell lab

Docker labs for testing php2shell exploit.py (PHP 8.4.26 mod_php heap exploit).
Requires PHP 8.4.26 with mod_php, prefork, session.upload_progress enabled, display_errors=1.

## Testing with LazyOwn
From LazyOwn root:
```bash
docker run -d --name php2shell-target -p 8089:80 -v $(pwd)/gyms/docker/php2shell/www:/var/www/html php:8.4.26-apache
sleep 3
# use addon
php2shell url=http://127.0.0.1:8089/index.php cmd='id>/tmp/p1'
```
