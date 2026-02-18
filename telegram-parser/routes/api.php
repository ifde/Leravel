<?php

use App\Models\TelegramMessage;
use App\Events\TelegramMessageReceived;
use Illuminate\Http\Request;

Route::post('/broadcast-telegram-message', function (Request $request) {
    // 1. Find the message Python just inserted
    $message = TelegramMessage::findOrFail($request->message_id);

    // 2. Dispatch the event (this triggers the WebSocket broadcast)
    TelegramMessageReceived::dispatch($message);

    // event(new TelegramMessageReceived($message));

    return response()->json(['status' => 'success']);
})->withoutMiddleware(\App\Http\Middleware\VerifyCsrfToken::class);
