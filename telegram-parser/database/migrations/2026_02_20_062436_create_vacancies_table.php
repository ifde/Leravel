<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('vacancies', function (Blueprint $table) {
            $table->id();
            $table->string('title');
            $table->text('description')->nullable();
            $table->string('url')->unique();  // For checking duplicates
            $table->string('company')->nullable();
            $table->string('logo')->nullable();
            $table->string('grade')->nullable();  // Senior/Middle/Junior
            $table->json('skills')->nullable();  // Array of skills
            $table->string('experience')->nullable();
            $table->string('salary')->nullable();
            $table->string('source')->nullable();
            $table->string('country')->nullable();
            $table->timestamp('posted_at')->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('vacancies');
    }
};
