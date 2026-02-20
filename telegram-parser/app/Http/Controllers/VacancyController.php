<?php

namespace App\Http\Controllers;

use App\Models\Vacancy;
use Illuminate\Http\Request;

class VacancyController extends Controller
{
    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|string',
            'description' => 'nullable|string',
            'url' => 'required|string',
            'company' => 'nullable|string',
            'logo' => 'nullable|string',
            'grade' => 'nullable|string',
            'skills' => 'nullable|array',
            'experience' => 'nullable|string',
            'salary' => 'nullable|string',
            'source' => 'nullable|string',
            'country' => 'nullable|string',
            'posted_at' => 'nullable|date',
        ]);

        // Check if vacancy already exists
        $exists = Vacancy::where('url', $validated['url'])->exists();
        if ($exists) {
            return response()->json(['message' => 'Vacancy already exists'], 409);
        }

        $vacancy = Vacancy::create($validated);

        return response()->json($vacancy, 201);
    }
}