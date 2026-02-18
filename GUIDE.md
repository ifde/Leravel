# How to start a project 

1. Start a Laravel app

`./vendor/bin/sail up -d`

2. Start a WebSocket

`./vendor/bin/sail artisan reverb:start`

You need the WebSocket because the Backend cannot "push" data to a browser over standard HTTP; it needs a middleman (Reverb) that keeps the connection alive

3. Open a new terminal and start Vite

`./vendor/bin/sail npm run dev --debug`

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

