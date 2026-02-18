import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import react from '@vitejs/plugin-react';

export default defineConfig({
    // Vite says: "Okay, the main thing I am building is called 
    // resources/js/app.jsx. 
    // I will keep track of it using exactly that name and create a mapping"
    // See resources/app.blade.php

    plugins: [
        laravel({
            input: 'resources/js/app.jsx',
            refresh: true,
        }),
        react(),
    ],
    server: {
        watch: {
            ignored: ['**/storage/framework/views/**'],
        },
    },
});
