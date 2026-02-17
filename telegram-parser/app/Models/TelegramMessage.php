<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class TelegramMessage extends Model
{
    protected $fillable = ['channel', 'message', 'posted_at'];
}
