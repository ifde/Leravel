<?php

namespace App\Http\Controllers;

use App\Models\Vacancy;
use Illuminate\Http\Request;
use App\Events\VacancyReceived;

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

        // Default posted_at to Jan 1, 1970 if NULL
        $validated['posted_at'] = $validated['posted_at'] ?? '1970-01-01 00:00:00';

        $vacancy = Vacancy::create($validated);

        VacancyReceived::dispatch($vacancy);

        return response()->json($vacancy, 201);
    }

    public function index() 
    {
        $vacancies = Vacancy::orderBy('posted_at', 'desc')->get();
        return response()->json($vacancies);
    }

    
    public function save(Request $request)
    {
        $user = auth()->user();
        if (!$user) return response()->json(['error' => 'Unauthorized'], 401);

        $url = $request->input('url');
        $vacancy = Vacancy::where('url', $url)->first();
        if (!$vacancy) return response()->json(['error' => 'Vacancy not found'], 404);

        try {
            $user->savedVacancies()->attach($vacancy->url);
            return response()->json(['message' => 'Saved']);
        } catch (\Exception $e) {
            return response()->json(['error' => 'Failed to save'], 500);
        }
    }

    public function unsave(Request $request)
    {
        $user = auth()->user();
        if (!$user) return response()->json(['error' => 'Unauthorized'], 401);

        $url = $request->input('url');
        $vacancy = Vacancy::where('url', $url)->first();
        if (!$vacancy) return response()->json(['error' => 'Vacancy not found'], 404);

        try {
            $user->savedVacancies()->detach($vacancy->url);
            return response()->json(['message' => 'Unsaved']);
        } catch (\Exception $e) {
            return response()->json(['error' => 'Failed to unsave'], 500);
        }
    }

    public function isSaved(Request $request)
    {
        $user = auth()->user();
        if (!$user) return response()->json(false);

        $url = $request->query('url');
        return response()->json($user->savedVacancies()->where('url', $url)->exists());
    }



    public function getSaved()
    {
        return response()->json(auth()->user()->savedVacancies);
    }
}