<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class TelegramMessage extends Model
{
    protected $fillable = ['channel', 'message', 'posted_at'];

    /**
     * Get all users that saved this message
     */
    public function savedByUsers()
    {
        return $this->belongsToMany(User::class, 'saved_messages');
    }
}
