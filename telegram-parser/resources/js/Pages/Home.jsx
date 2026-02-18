import { useEffect, useState, useRef } from 'react';

export default function TelegramMessages() {
    const [messages, setMessages] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const containerRef = useRef(null);

    // Fetch existing messages on component load (runs once)
    useEffect(() => {
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
    }, []);

    // Listen for real-time updates (runs once)
    useEffect(() => {
        window.Echo.channel('messages')
            .listen('.TelegramMessageReceived', (event) => {
                setMessages(prev => [event.message, ...prev]);
            });

        return () => {
            window.Echo.leave('messages');
        };
    }, []);

    // Keyboard navigation (runs once)
    useEffect(() => {
        const handleKeyDown = (event) => {
            if (event.key === 'ArrowDown' && currentIndex < messages.length - 1) {
                setCurrentIndex(prev => prev + 1);
                scrollToMessage(currentIndex + 1);
            } else if (event.key === 'ArrowUp' && currentIndex > 0) {
                setCurrentIndex(prev => prev - 1);
                scrollToMessage(currentIndex - 1);
            }
        };

        window.addEventListener('keydown', handleKeyDown);

        return () => {
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, [currentIndex, messages.length]);

    const scrollToMessage = (index) => {
        if (containerRef.current) {
            const messageElement = containerRef.current.children[index];
            if (messageElement) {
                messageElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    };

    return (
        <div className="relative h-screen overflow-hidden bg-gray-100 dark:bg-gray-900">
            {/* Navigation Arrows */}
            {currentIndex > 0 && (
                <button
                    onClick={() => {
                        setCurrentIndex(prev => prev - 1);
                        scrollToMessage(currentIndex - 1);
                    }}
                    className="absolute top-4 left-1/2 transform -translate-x-1/2 z-10 bg-white dark:bg-gray-800 rounded-full p-2 shadow-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition"
                >
                    <svg className="w-6 h-6 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                    </svg>
                </button>
            )}
            {currentIndex < messages.length - 1 && (
                <button
                    onClick={() => {
                        setCurrentIndex(prev => prev + 1);
                        scrollToMessage(currentIndex + 1);
                    }}
                    className="absolute bottom-4 left-1/2 transform -translate-x-1/2 z-10 bg-white dark:bg-gray-800 rounded-full p-2 shadow-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition"
                >
                    <svg className="w-6 h-6 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                </button>
            )}

            {/* Scrollable Messages Container */}
            <div
                ref={containerRef}
                className="h-full overflow-y-auto snap-y snap-mandatory"
                style={{ scrollBehavior: 'smooth' }}
            >
                {messages.length === 0 ? (
                    <div className="flex items-center justify-center h-screen">
                        <p className="text-gray-500 dark:text-gray-400 text-lg">No messages yet</p>
                    </div>
                ) : (
                    messages.map((msg, index) => (
                        <div
                            key={msg.id}
                            className="flex items-center justify-center h-screen snap-start px-4"
                        >
                            {/* Telegram-Style Message Box */}
                            <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-200 dark:border-gray-700">
                                <div className="flex items-start space-x-3">
                                    {/* Avatar Placeholder (Telegram-style) */}
                                    <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold text-sm">
                                        {msg.channel.charAt(0).toUpperCase()}
                                    </div>
                                    {/* Message Content */}
                                    <div className="flex-1">
                                        <div className="flex items-center space-x-2 mb-2">
                                            <span className="font-semibold text-gray-900 dark:text-white">{msg.channel}</span>
                                            <span className="text-xs text-gray-500 dark:text-gray-400">
                                                {new Date(msg.posted_at).toLocaleString()}
                                            </span>
                                        </div>
                                        <p className="text-gray-800 dark:text-gray-200 leading-relaxed">{msg.message}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}