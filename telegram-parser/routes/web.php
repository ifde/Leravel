<?php

use App\Http\Controllers\ProfileController;
use Illuminate\Foundation\Application;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;

Route::get('/', function () {
    return Inertia::render('Welcome', [
        'canLogin' => Route::has('login'),
        'canRegister' => Route::has('register'),
        'laravelVersion' => Application::VERSION,
        'phpVersion' => PHP_VERSION,
    ]);
});

Route::get('/dashboard', function () {
    return Inertia::render('Dashboard');
})->middleware(['auth', 'verified'])->name('dashboard');

Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
});

require __DIR__.'/auth.php';

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
