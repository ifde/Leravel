import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import tailwindcss from '@tailwindcss/vite';

import react from '@vitejs/plugin-react'; // adding React

export default defineConfig({
    plugins: [
        // Vite says: "Okay, the main thing I am building is called 
        // resources/js/app.jsx. 
        // I will keep track of it using exactly that name and create a mapping"
        // See resources/app.blade.php
        laravel({
            input: ['resources/js/app.jsx'],
            refresh: true,
        }),
        react(),
        tailwindcss()
    ],
    server: {
        watch: {
            ignored: ['**/storage/framework/views/**'],
        },
    },
});
