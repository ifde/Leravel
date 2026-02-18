import { useEffect, useState } from 'react';
import Echo from 'laravel-echo';

export default function TelegramMessages() {
    const [messages, setMessages] = useState([]);

    useEffect(() => {

        // Listen for real-time updates
        window.Echo.channel('messages')
            .listen('.TelegramMessageReceived', (event) => {
                console.log("Event received!", event); // <-- Add this
                setMessages(prev => [event.message, ...prev]);
            });



        // Cleanup
        return () => {
            window.Echo.leave('messages');
        };
    }, []);

    return (
        <div>
            <h2>Telegram Messages</h2>
            <ul>
                {messages.map(msg => (
                    <li key={msg.id}>
                        <strong>{msg.channel}</strong>: {msg.message}
                        <em> ({msg.posted_at})</em>
                    </li>
                ))}
            </ul>
        </div>
    );
}