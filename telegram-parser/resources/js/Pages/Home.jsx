import { useEffect, useState } from 'react';

export default function TelegramMessages() {
    // saving a state for the messages array
    const [messages, setMessages] = useState([]);

    // useEffect(func, [])
    // 1. Creates a setup in the body
    // 2. Run only once at the load of the page 
    // (the dependency array [someVariable] is empty)
    // 3. stop listening when we leave the page (return)

    useEffect(() => {

        // Fetch existing messages on component load
        const fetchMessages = async () => {
            try {
                const response = await fetch('/api/get-telegram-messages');
                const data = await response.json();
                setMessages(data);
            } catch (error) {
                console.error('Failed to fetch messages:', error);
            }
        };

        fetchMessages();

        // Listen for real-time updates
        window.Echo.channel('messages')
            .listen('.TelegramMessageReceived', (event) => {
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