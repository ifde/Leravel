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

use App\Models\TelegramMessage;
use App\Models\User;
use App\Events\TelegramMessageReceived;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;


// Save a message (authenticated users only)
Route::middleware('auth')->post('/messages/{id}/save', function (Request $request, $id) {
    // it looks into config/auth.php to find a user
    $user = Auth::user();
    $message = TelegramMessage::findOrFail($id);

    if (!$user->savedMessages()->where('telegram_message_id', $id)->exists()) {
        $user->savedMessages()->attach($id);
        return response()->json(['status' => 'saved']);
    }

    return response()->json(['status' => 'already saved'], 200);
});

// Unsave a message
Route::middleware('auth')->delete('/messages/{id}/save', function (Request $request, $id) {
    $user = Auth::user();
    $user->savedMessages()->detach($id);
    return response()->json(['status' => 'unsaved']);
});

// Get saved messages for the user
Route::middleware('auth')->get('/saved-messages', function () {
    $user = Auth::user();
    return $user->savedMessages()->with('savedByUsers')->orderBy('posted_at', 'desc')->get();
});
