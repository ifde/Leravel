<?php

namespace App\Events;

use App\Models\Vacancy;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

// make sure to use BroadcastNow
class VacancyReceived implements ShouldBroadcastNow
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public $vacancy;

    public function __construct(Vacancy $vacancy)
    {
        $this->vacancy = $vacancy;
    }

    public function broadcastOn() : array
    {
        return [
            new Channel('vacancies'), // Public channel for vacancies
        ];  
    }

    public function broadcastAs() : string
    {
        return 'VacancyReceived';  // Event name
    }

    // Fixing Payload Too Large
    public function broadcastWith()
    {
        // Return only essential fields to keep payload small
        return [
            'id' => $this->vacancy->id,
            'title' => $this->vacancy->title,
            'company' => $this->vacancy->company,
            'url' => $this->vacancy->url,
            'source' => $this->vacancy->source,
            'posted_at' => $this->vacancy->posted_at,
            'description' => substr($this->vacancy->description, 0, 500),  // Truncate to 500 chars
        ];
    }
}