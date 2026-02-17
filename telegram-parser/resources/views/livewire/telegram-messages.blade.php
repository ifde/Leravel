<div wire:poll.1s>
    <h2>Telegram Messages</h2>
    <ul>
        @foreach($messages as $msg)
            <li>
                <strong>{{ $msg->channel }}</strong>:
                {{ $msg->message }}
                <em>({{ $msg->posted_at }})</em>
            </li>
        @endforeach
    </ul>
</div>