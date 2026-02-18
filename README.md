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

3. Installing Livewire/livewaire (the UI) **NOT USED ANYMORE - SWITCHED TO REACT**

`./vendor/bin/sail composer require livewire/livewire`

`./vendor/bin/sail artisan livewire:publish`    
used to copy Livewire's internal files into your own project's directories so you can customize them

4. Create a model and a Migration for Telegram Messages

`./vendor/bin/sail artisan make:model TelegramMessage -m`

Running the migration       

`./vendor/bin/sail artisan migrate`

5. Create the Livewire UI **NOT USED ANYMORE - SWITCHED TO REACT**

`./vendor/bin/sail artisan make:livewire TelegramMessages --class`

6. Run the script that gets messages from Telegram 

`uv run python main.py`     
Note: might need a bot API key

It uses `routes/api.php` where a post method is defined 
`Route::post('/broadcast-telegram-message'`

**Make sure to add**    
`api: __DIR__.'/../routes/api.php'` in `bootstrap/app.php`      
I spent so much time fixing it

7. Now let's install the websocket so that when the script pushes messages to the database the webpage is updated 

`./vendor/bin/sail artisan install:broadcasting`

Start a WebSocket in the new terminal:      
`./vendor/bin/sail artisan reverb:start -- debug`

**Add the port to the docker compose!** 
`- '${REVERB_PORT:-8080}:8080' # <--- Add this line`

Create an event     
`./vendor/bin/sail artisan make:event TelegramMessageReceived`

How it works:

- We have a class `class TelegramMessageReceived implements ShouldBroadcast`

It acts as event

We trigger the event in our PHP code 
`TelegramMessageReceived::dispatch($message);`

It is broadcasted on this channel: 

`Channel('messages')`

It sends data to a Reverb WebSocket

- Then on the frontend we use it 

```jsx
// Listen for real-time updates
        window.Echo.channel('messages')
            .listen('.TelegramMessageReceived', (event) => {
                console.log("Event received!", event); // <-- Add this
                setMessages(prev => [event.message, ...prev]);
            });
```

8. Then run `./vendor/bin/sail npm run dev`

It starts Vite, which is a factory for frontend assets

9. Installing Inertia

`./vendor/bin/sail composer require inertiajs/inertia-laravel`

`./vendor/bin/sail artisan inertia:middleware`

Then we register the middleware in `bootstrap/app.php`

Then install React `./vendor/bin/sail npm install @inertiajs/react react react-dom @vitejs/plugin-react`

**Laravel**     
When you visit a page, Laravel's Inertia::render('Dashboard') sends a JSON response to the browser that says: "The user needs the 'Dashboard' component"         


**Inertia**
Inertia handles this 'Dashboard' by fetching a React Component from Vite     

**Vite**    
When you run `./vendor/bin/sail npm run dev`, Vite is working in the background.    
It takes your .jsx files and turns them into a single, optimized .js file.      
The "Finished Chairs" (JavaScript) are now sitting on a shelf in the Vite server, ready to be picked up.


### How Vite + Inertia + React work together

1. When you visit http://localhost  
The Route: Your browser sends a request to Laravel.     
The Controller: A controller method runs and returns Inertia::render('Home', ['data' => $val]). 
The Middleware: The HandleInertiaRequests middleware runs. 
It looks at the $rootView property to find your app.blade.php file

2. Laravel renders app.blade.php into standard HTML to send back to your browser    
@inertia: This renders a `<div id="app" data-page="...">`. All the data from your controller and middleware is converted into a JSON string and placed inside that data-page attribute.
@vite: This renders a <script> tag pointing to your resources/js/app.jsx

3. Your browser receives the HTML and sees the <script> tag for app.jsx:
The Fetch: The browser requests app.jsx. Since you are in development (npm run dev), the Vite server provides this file.
The Execution: The browser runs the code in app.jsx immediately.


### Sail tinker 

Use it to run PHP code in an interactive shell 

`./vendor/bin/sail tinker`

```php
<?php
>>> $response = Http::post('http://laravel/api/telegram-messages', ['channel' => 'test', 'message' => 'test', 'posted_at' => now()]);
>>> $response->status();
```

### Sail shell

`sail shell`

### See the logs

`tail -f storage/logs/laravel.log`












