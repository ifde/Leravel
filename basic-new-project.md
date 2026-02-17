
## Pre

`alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'`

## Create new Project

`curl -s "https://laravel.build/name?with=pgsql,redis&devcontainer" | bash`

## Set up your project

`cd name && sail up -d`

`sail art migrate`

## Test

http://localhost/


`printf '{\n  "preset": "laravel",\n  "rules": {\n    "binary_operator_spaces": false,\n    "single_line_empty_body": false,\n    "not_operator_with_successor_space": false\n  }\n}\n' > pint.json`

## Add Laravel Nova

`sail composer config repositories.nova '{"type": "composer", "url": "https://laravelsatis.com"}' --file composer.json`

`sail composer require laravel/nova`

`sail art nova:install`

`sail art migrate`

`sail art nova:user`

`echo "/public/vendor" >> .gitignore`

### Add `ValidateNovaLicenseCommand`

`sail art make:command ValidateNovaLicenseCommand`

```
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Cache;

class ValidateNovaLicenseCommand extends Command
{
    protected $signature = 'app:validate-nova';

    protected $description = 'Validate Nova License online without registration';

    public function handle(): void
    {
        Cache::forget('nova_valid_license_key');
        Cache::rememberForever('nova_valid_license_key', fn () => true);
    }
}

```

`sail art app:validate-nova`

### Branding

Settings file `config/nova.php`:

```
    'brand' => [
        'logo' => resource_path('/img/logo.svg'),

        'colors' => [
            '400' => '24, 182, 155, 0.5',
            '500' => '24, 182, 155',
            '600' => '24, 182, 155, 0.75',
        ],
    ],
```

Logo file: `resources/img/logo.svg`

### Nova Service Provider

Provider file: `app/Providers/NovaServiceProvider.php`

```
public function boot(): void
{
    parent::boot();

    Nova::footer(fn () => '');
}

// ...

protected function gate(): void
{
    Gate::define('viewNova', function (User $user) {
        return true;
    });
}
```


## Laravel Lang

`sail composer require laravel-lang/common`

`sail php artisan lang:add ru en`

## Laravel Telescope

> Именно `install`, да

```
sail composer require laravel/telescope
sail php artisan telescope:install
sail php artisan migrate
```

`TelescopeServiceProvider.php` -> `Telescope::night();`


## Laravel Horizon

```
sail composer require laravel/horizon
sail php artisan horizon:install
```

`HorizonServiceProvider.php`:
```

```


## Laravel Pulse

```
sail composer require laravel/pulse
sail php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
sail php artisan migrate
```

Чтобы добавить авторизацию при переходе в пульс, необходимо в `app/Providers/AppServiceProvider.php` Добавить проверку на пользователя:

```
public function boot(): void
{
    Gate::define('viewPulse', function (User $user) {
        return $user->isAdmin();
    });
 
    // ...
}
```

## Nutgram

```

sail composer require nutgram/laravel

sail php artisan vendor:publish --provider="Nutgram\Laravel\NutgramServiceProvider" --tag="nutgram"

sail art nutgram:run

```

Добавить в `api.php`:
```
<?php

/** @var SergiX44\Nutgram\Nutgram $bot */

use Illuminate\Support\Facades\Route;
use SergiX44\Nutgram\Nutgram;

Route::post('/tg/webhook', fn (Nutgram $bot) => $bot->run());

```
+ Если проект новый, не забыть зарегистрировать в `bootstrap/app.php`:

`api: __DIR__.'/../routes/api.php',`


## Boost

```
sail composer require laravel/boost --dev
sail php artisan boost:install
```

Настройка для Sail в `.cursor/mcp.json`:
```
{
    "mcpServers": {
        "laravel-boost": {
            "command": "vendor/bin/sail",
            "args": [
                "php",
                "artisan",
                "boost:mcp"
            ]
        }
    }
}
```
