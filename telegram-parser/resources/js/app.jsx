import './bootstrap';
import { createInertiaApp } from '@inertiajs/react';
import { createRoot } from 'react-dom/client';

createInertiaApp({
    resolve: name => {
        const pages = import.meta.glob('./Pages/**/*.jsx', { eager: true }); //
        return pages[`./Pages/${name}.jsx`];
    },
    setup({ el, App, props }) {
        createRoot(el).render(<App {...props} />); //
    },
});


/*
The Chain of Command
Laravel sends an HTML page with <div id="app" 
data-page='{"component":"Home","props":{"user":"John"}}'></div>.

Inertia (JS) boots up and finds the element (el) and
 the data (props) from that attribute.

Inertia (JS) uses your resolve function to
 find the actual React file for "Home".

The setup function is then called with all three pieces ready to go, 
allowing React to take over the page
*/
