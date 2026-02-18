<?php

use Inertia\Inertia;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});


use App\Events\TelegramMessageReceived;
use App\Models\TelegramMessage;
Route::get('/test-broadcast', function () {
    $message = TelegramMessage::first(); // Ensure a message exists
    broadcast(new TelegramMessageReceived($message));
    return 'Event fired!';
});

// applying middleware
// 1. Laravel sees Route::middleware([...])->group(...)
// 2. It creates a "route group" with the middleware applied
// 3. It calls the function () { ... } you provided.
// 4. We call Route::get(...) and Laravel registeres the routes
// PLUS adds the middleware
// It knows becase the group() function is the one executing these Route::get()
Route::middleware([\App\Http\Middleware\HandleInertiaRequests::class])->group(function () {
    Route::get('/react', function () {
        return Inertia::render('Home');
    });
});
