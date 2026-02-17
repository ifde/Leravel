# Telegram Parser PHP project

### Guide

1. `curl -s "https://laravel.build/name?with=pgsql,redis&devcontainer" | bash`

This executes a script to create a basis PHP laravel project 
It is all in a docker container so no PHP exists on the host

You can run `alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'` to create a shell alias for sail      
Note: `sail` is a utility that helps you run the PHP executabes inside docker automatically     

2. `./vendor/bin/sail up -d`

This starts the docker containers

Then run `sail art migrate` to apply databse migrations         
`art` is a shorthand for `artisan`      
it is a utility within laravel that dose lots of things

App is available at `https://localhost`

3. Installing Livewire/livewaire (the UI)

`./vendor/bin/sail composer require livewire/livewire`

`./vendor/bin/sail artisan livewire:publish`    
used to copy Livewire's internal files into your own project's directories so you can customize them

4. Create a model and a Migration for Telegram Messages

`./vendor/bin/sail artisan make:model TelegramMessage -m`

Running the migration       

`./vendor/bin/sail artisan migrate`

5. Create the UI 

`./vendor/bin/sail artisan make:livewire TelegramMessages --class`

6. Run the script that gets messages from Telegram 

`uv run python main.py`     
Note: might need a bot API key

7. Now let's install the websocket so that when the script pushes messages to the database the webpage is updated 

`./vendor/bin/sail artisan install:broadcasting`

Start a WebSocket in the new terminal:      
`./vendor/bin/sail artisan reverb:start`

Create an event     
`./vendor/bin/sail artisan make:event TelegramMessageReceived`

How it works:

- We have a class `class TelegramMessageReceived implements ShouldBroadcast`

It acts as event

We trigger the event in our PHP code 
`TelegramMessageReceived::dispatch($message);`

It is broadcasted on this channel: 

`PrivateChannel('messages')`

It sends data to a Reverb WebSocket

- Then on the frontend

```javascript
Echo.private('message') // Laravel adds 'private-' prefix automatically
    .listen('TelegramMessageReceived', (e) => {
        console.log('New message arrived!', e.message);
        // Here is where you append the message to your HTML list
    });
```

`Echo` is the library by Laravel     
`Echo.private('message')` return a class that throws the events     
We get them with `.listen`     

8. Then run `./vendor/bin/sail npm run dev`

It starts Vite, which is a factory for frontend assets

9. Installing Inertia

`./vendor/bin/sail composer require inertiajs/inertia-laravel`

`./vendor/bin/sail artisan inertia:middleware`

Then we register the middleware in `bootstarp/app.php`

Then install React `./vendor/bin/sail npm install @inertiajs/react react react-dom @vitejs/plugin-react`

Vite: The factory that turns raw wood (JSX/CSS) into a finished chair (JavaScript) that the browser can actually understand.

Inertia: The delivery truck that carries that chair from the Laravel warehouse to your house without you having to reload the page.








