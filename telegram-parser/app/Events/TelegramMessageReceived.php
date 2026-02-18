<?php

namespace App\Events;

use App\Models\TelegramMessage;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

// 'implements' is for interfaces
// ShouldBroadcastNow hands the event to the driver (Reverb)
class TelegramMessageReceived implements ShouldBroadcastNow
{
    // telling PHP to take all the functions defined in those three files 
    // and virtually paste them directly into your our class
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public $message;

    /**
     * Create a new event instance.
     */
    public function __construct(TelegramMessage $message)
    {
        $this->message = $message;
    }

    /**
     * Get the channels the event should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel>
     */
    public function broadcastOn(): array
    {
        return [
            new Channel('messages'),
        ];
    }

    public function broadcastAs(): string
    {
        return 'TelegramMessageReceived';
    }
}
