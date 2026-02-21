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



1. Create a VPS 

Or download the private-public key pair from Yandex and unzip it into a special folder:   
`unzip /Users/admin/Downloads/ssh-key-1771671861436.zip -d /Users/admin/.ssh/`

Set the private key to be able to read only by you:     
`chmod 600 /Users/admin/.ssh/ssh-key-1771671861436`

Connect using   
`ssh -i ~/.ssh/ssh-key-1771671861436 laravel@158.160.0.235`






