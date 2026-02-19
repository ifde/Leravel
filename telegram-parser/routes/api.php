<?php

use App\Models\TelegramMessage;
use App\Events\TelegramMessageReceived;
use Illuminate\Http\Request;

// GET all messages
Route::get('/get-telegram-messages', function () {
    return TelegramMessage::orderBy('posted_at', 'desc')->get();
});

Route::middleware(\App\Http\Middleware\ApiKeyMiddleware::class)->post('/post-telegram-message', function (Request $request) {
    // \Log is a global facade 
    // It provides a static interface for the real Log object
    \Log::info('Incoming message:', $request->all());

    // Validate the request
    $validated = $request->validate([
        'channel' => 'required|string|max:255',
        'message' => 'required|string',
        'posted_at' => 'required|date',
        'profile_pic_path' => 'nullable|string',
    ]);

    try {
        // Create the message in the database
        $telegramMessage = TelegramMessage::create([
            'channel' => $validated['channel'],
            'message' => $validated['message'],
            'posted_at' => $validated['posted_at'],
            'profile_pic_path' => $validated['profile_pic_path'],
        ]);

        // Broadcast the event to WebSocket listeners
        TelegramMessageReceived::dispatch($telegramMessage);

        return response()->json([
            'id' => $telegramMessage->id,
            'status' => 'success',
            'message' => 'Message saved and broadcasted'
        ], 201);
    } catch (\Exception $e) {
        \Log::error('Failed to save message:', ['error' => $e->getMessage()]);
        return response()->json([
            'status' => 'error',
            'message' => $e->getMessage()
        ], 400);
    }
});

// POST a new message (from Python script)
Route::post('/telegram-messages', function (Request $request) {
    // \Log is a global facade 
    // It provides a static interface for the real Log object
    \Log::info('Incoming message:', $request->all());

    // Validate the request
    $validated = $request->validate([
        'channel' => 'required|string|max:255',
        'message' => 'required|string',
        'posted_at' => 'required|date',
    ]);

    try {
        // Create the message in the database
        $telegramMessage = TelegramMessage::create([
            'channel' => $validated['channel'],
            'message' => $validated['message'],
            'posted_at' => $validated['posted_at'],
        ]);

        // Broadcast the event to WebSocket listeners
        TelegramMessageReceived::dispatch($telegramMessage);

        return response()->json([
            'id' => $telegramMessage->id,
            'status' => 'success',
            'message' => 'Message saved and broadcasted'
        ], 201);
    } catch (\Exception $e) {
        \Log::error('Failed to save message:', ['error' => $e->getMessage()]);
        return response()->json([
            'status' => 'error',
            'message' => $e->getMessage()
        ], 400);
    }
});

use App\Models\User;
use Illuminate\Support\Facades\Auth;


// Save a message (authenticated users only)
// Make sure to add ['auth', 'web'] because we want api routes to share
// the same session context as 'web'
Route::middleware(['auth', 'web'])->post('/messages/{id}/save', function (Request $request, $id) {
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
Route::middleware(['auth', 'web'])->delete('/messages/{id}/save', function (Request $request, $id) {
    $user = Auth::user();
    $user->savedMessages()->detach($id);
    return response()->json(['status' => 'unsaved']);
});

// Get saved messages for the user
Route::middleware(['auth', 'web'])->get('/saved-messages', function () {
    $user = Auth::user();
    return $user->savedMessages()->with('savedByUsers')->orderBy('posted_at', 'desc')->get();
});
