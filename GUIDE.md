# How to start a project 

1. Start a Laravel app

`./vendor/bin/sail up -d`

2. Start a WebSocket

`./vendor/bin/sail artisan reverb:start`

You need the WebSocket because the Backend cannot "push" data to a browser over standard HTTP; it needs a middleman (Reverb) that keeps the connection alive

3. Open a new terminal and start Vite

`./vendor/bin/sail npm run dev --debug`

Vite renders `jsx` to a normal `Java Script` that browser understands

4. Open a new terminal and start a Telegram parser 

```bash
cd ..
uv run python main.py
```

5. *Optional* Clear cache

`./vendor/bin/sail artisan config:clear`
`./vendor/bin/sail artisan cache:clear `

6. Output the logs

`tail -f storage/logs/laravel.log`

# How to deploy a Laravel project 

0. Load on GitHub

```
git add .
git commmit -m "Init"
git remote add origin https://github.com/ifde/Leravel.git
git push -u origin main
```

1. Create a VPS 

Or download the private-public key pair from Yandex and unzip it into a special folder:   
`unzip /Users/admin/Downloads/ssh-key-1771671861436.zip -d /Users/admin/.ssh/`

Set the private key to be able to read only by you:     
`chmod 600 /Users/admin/.ssh/ssh-key-1771671861436`

Connect using   
`ssh -i ~/.ssh/ssh-key-1771671861436 laravel@158.160.0.235`


2. Inside a VPS

Clone a repository  
```
git clone https://github.com/ifde/Leravel.git
cd Leravel
```

Copy your .env  to the VPS (run in the local)
`scp -i ~/.ssh/ssh-key-1771671861436 telegram-parser/.env.production laravel@158.160.0.235:~/Leravel/telegram-parser/.env`

Install composer on a VPS (it is a PHP utilite that will create a /vendor folder)   
```
sudo apt update
sudo apt install php-cli unzip curl
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
composer --version
```

Donwload PHP 8.4    
```
sudo add-apt-repository ppa:ondrej/php -y
sudo apt install php8.4-cli php8.4-curl php8.4-dom php8.4-xml php8.4-mbstring php8.4-bcmath php8.4-zip -y
sudo update-alternatives --set php /usr/bin/php8.4
php -v
sudo apt install php8.4-curl php8.4-xml php8.4-mysql php8.4-sqlite3 -y
```

Run the composer    
`composer install --optimize-autoloader --no-dev`

3. Frontend     
```
sudo apt install nodejs npm
npm install
npm run build
```

4. Install postgres     
```
sudo apt update
sudo apt install postgresql postgresql-contrib php8.4-pgsql -y
sudo -u postgres psql
CREATE USER sail WITH ENCRYPTED PASSWORD 'get it from .env.production';
GRANT ALL PRIVILEGES ON DATABASE laravel TO sail;
ALTER DATABASE laravel OWNER TO sail;
```

Run the migrations      
```
php artisan config:clear
```

5. Configure Nginx

Production (The VPS): On a real server, Laravel is just a folder of PHP files. It needs a "bodyguard" (Nginx or Apache) to:         
- Listen for traffic on port 80/443.
- Handle SSL (HTTPS).
- Pass PHP requests to the PHP-FPM processor.

Since you have Nginx and Postgres installed, the final step is to connect them. Nginx doesn't speak "PHP" directly; it uses a middleman called PHP-FPM.

```
sudo apt install nginx -y
sudo apt -o Acquire::ForceIPv4=true install php8.4-fpm -y
```

Insert this   
```
server {
    listen 80;
    server_name 158.160.0.235; # Your IP or Domain
    root /home/laravel/Leravel/telegram-parser/public; # MUST point to /public

    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.4-fpm.sock; # The middleman
    }
}
```

Link the file to the enabled Nginx folder, remove default Nginx welcome page (it conflicts), test and restart
```
sudo ln -s /etc/nginx/sites-available/telegram-parser /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
```

Nginx runs as a www-data user and wants permissions to read file from your project  
```
sudo chown -R www-data:www-data /home/laravel/Leravel/telegram-parser/storage /home/laravel/Leravel/telegram-parser/bootstrap/cache
sudo chmod -R 775 /home/laravel/Leravel/telegram-parser/storage /home/laravel/Leravel/telegram-parser/bootstrap/cache
sudo chown -R www-data:www-data storage bootstrap/cache
sudo chmod -R 775 storage bootstrap/cache
sudo usermod -a -G www-data laravel
```

```
sudo chown -R laravel:www-data storage bootstrap/cache
sudo chmod -R 775 storage bootstrap/cache
sudo find storage -type d -exec chmod 775 {} +
sudo find storage -type f -exec chmod 664 {} +
```

```
sudo chmod 755 /home/laravel
sudo chmod 755 /home/laravel/Leravel
sudo chmod 755 /home/laravel/Leravel/telegram-parser
sudo chmod 755 /home/laravel/Leravel/telegram-parser/public
```

6. Make it production ready

```
php artisan config:cache
php artisan route:cache
php artisan view:cache
```






