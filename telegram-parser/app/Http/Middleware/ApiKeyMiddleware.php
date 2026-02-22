<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;
use Illuminate\Support\Facades\Log;

class ApiKeyMiddleware
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $apiKey = $request->header('X-API-Key');

        $expectedKey = config('services.telegram_parser.api_key');

        // This will show up in storage/logs/laravel.log
        Log::info('API Auth Check', [
            'incoming_header' => $apiKey,
            'expected_from_env' => $expectedKey,
            'match' => ($apiKey === $expectedKey)
        ]);

        if ($apiKey !== $expectedKey) {
            return response()->json(['error' => 'Unauthorized'], 401);
        }

        return $next($request);
    }
}
