<?php

namespace App\Models;

// use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    /** @use HasFactory<\Database\Factories\UserFactory> */
    use HasFactory, Notifiable;

    /**
     * The attributes that are mass assignable.
     *
     * @var list<string>
     */
    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    /**
     * The attributes that should be hidden for serialization.
     *
     * @var list<string>
     */
    protected $hidden = [
        'password',
        'remember_token',
    ];

    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'email_verified_at' => 'datetime',
            'password' => 'hashed',
        ];
    }

    /**
     * Get all saved messages of a user
     */
    public function savedMessages()
    {
        return $this->belongsToMany(TelegramMessage::class, 'saved_messages');
    }

    /**
     * Get all saved vacancies of a user
     */
    public function savedVacancies()
    {
        return $this->belongsToMany(
            Vacancy::class,           // 1. Related model class
            'saved_vacancies',             // 2. Pivot table name
            'user_id',        // 3. Foreign key on pivot for THIS model
            'url',        // 4. Foreign key on pivot for RELATED model
            'id',   // 5. Local key on THIS model (optional, defaults to 'id')
            'url'  // 6. Related key on RELATED model (optional, defaults to 'id')
        );
    }
}
