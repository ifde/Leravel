<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Vacancy extends Model
{
    use HasFactory;

    protected $fillable = [
        'title',
        'description',
        'url',
        'company',
        'logo',
        'grade',
        'skills',
        'experience',
        'salary',
        'source',
        'country',
        'posted_at',
    ];

    protected $casts = [
        'skills' => 'array',  // Cast to array
    ];
}