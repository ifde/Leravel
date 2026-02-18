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
