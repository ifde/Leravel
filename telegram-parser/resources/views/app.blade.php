<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0" />
        
        <!-- This is needed for React Fast Refresh during development -->
        @viteReactRefresh 
        
        <!-- This loads your main React entry point 
         Laravel sees this and asks the system: 
         "Hey, do we have anything in our 'Map' that is
          labeled exactly resources/js/app.jsx?"-->
        @vite('resources/js/app.jsx')
        
        <!-- This allows Inertia to inject head tags from React -->
        @inertiaHead
    </head>
    <body>
        <!-- This is the mounting point for your React app, 
         it creates the div element with id="app"  -->
        @inertia
    </body>
</html>
