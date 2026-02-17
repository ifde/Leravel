<?php

namespace App\Livewire;

use Livewire\Component;
use App\Models\TelegramMessage;

class TelegramMessages extends Component
{
    protected $listeners = [
            'echo:messages,TelegramMessageReceived' => '$refresh'
    ];

    public function render()
    {

        // Get all messages, newest first
        $messages = TelegramMessage::orderBy('posted_at', 'desc')->get();

        // view function helps to convert php to html 
        // it inserts the html into /resources/views/components/telegram-messages.blade.php
        return view('livewire.telegram-messages', [
            'messages' => $messages,
        ]);
    }
}
