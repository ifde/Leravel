<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class TelegramMessage extends Model
{
    /**
     * Allows TelegramMessage::factory()->create() for testing/seeding.
     * It creates fake data for convenience
     */
    use HasFactory;

    protected $fillable = ['channel', 'message', 'posted_at', 'profile_pic_path'];

    /**
     * Get all users that saved this message
     */
    public function savedByUsers()
    {
        return $this->belongsToMany(User::class, 'saved_messages');
    }
}
