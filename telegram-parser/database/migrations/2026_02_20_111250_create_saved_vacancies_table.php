<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('saved_vacancies', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->string('url');  // Use url instead of vacancy_id
            $table->foreign('url')->references('url')->on('vacancies')->onDelete('cascade');  // Foreign key to vacancies.url
            $table->unique(['user_id', 'url']);  // Prevent duplicates
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('saved_vacancies');
    }
};