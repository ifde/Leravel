import '../css/app.css';
import './bootstrap';

import { createInertiaApp } from '@inertiajs/react';
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers';
import { createRoot } from 'react-dom/client';

const appName = import.meta.env.VITE_APP_NAME || 'Laravel';

createInertiaApp({
    title: (title) => `${title} - ${appName}`,
    resolve: (name) =>
        resolvePageComponent(
            `./Pages/${name}.jsx`,
            import.meta.glob('./Pages/**/*.jsx'),
        ),
    setup({ el, App, props }) {
        const root = createRoot(el);

        root.render(<App {...props} />);
    },
    progress: {
        color: '#4B5563',
    },
});

/*
The Chain of Command
Laravel sends an HTML page with <div id="app" 
data-page='{"component":"Home","props":{"user":"John"}}'></div>.

Inertia (JS) boots up and finds the element (el) and
 the data (props) from that attribute.

 App is just the Root React Component

Inertia (JS) uses your resolve function to
 find the actual React file for "Home".

The setup function is then called with all three pieces ready to go, 
allowing React to take over the page
*/
