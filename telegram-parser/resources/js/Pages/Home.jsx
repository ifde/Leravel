import { useEffect, useState, useRef } from 'react';
import { usePage } from '@inertiajs/react';
import axios from 'axios';

// Configure Axios globally for credentials and CSRF
axios.defaults.withCredentials = true; // Sends cookies
axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
axios.defaults.headers.common['Accept'] = 'application/json';

// Function to get CSRF token from cookies
const getCsrfToken = () => {
    const name = 'XSRF-TOKEN';
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return decodeURIComponent(parts.pop().split(';').shift());
    return null;
};

// Add CSRF token to requests automatically
axios.interceptors.request.use((config) => {
    const token = getCsrfToken();
    if (token && ['post', 'put', 'delete', 'patch'].includes(config.method?.toLowerCase())) {
        config.headers['X-XSRF-TOKEN'] = token;
    }
    return config;
});

export default function TelegramMessages() {
    const { auth } = usePage().props;
    const [messages, setMessages] = useState([]);
    const [savedMessages, setSavedMessages] = useState([]);
    const [activeTab, setActiveTab] = useState('all');
    const [currentIndex, setCurrentIndex] = useState(0);
    const containerRef = useRef(null);

    // Fetch all messages
    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await axios.get('/api/get-telegram-messages');
                setMessages(response.data);
            } catch (error) {
                console.error('Failed to fetch messages:', error);
            }
        };
        fetchMessages();
    }, []);

    // Fetch saved messages
    useEffect(() => {
        if (auth?.user) {
            const fetchSavedMessages = async () => {
                try {
                    const response = await axios.get('/api/saved-messages');
                    setSavedMessages(response.data);
                } catch (error) {
                    console.error('Failed to fetch saved messages:', error);
                }
            };
            fetchSavedMessages();
        }
    }, [auth?.user]);

    // Echo listener
    useEffect(() => {
        window.Echo.channel('messages')
            .listen('.TelegramMessageReceived', (event) => {
                setMessages(prev => [event.message, ...prev]);
            });
        return () => window.Echo.leave('messages');
    }, []);

    // Keyboard navigation
    useEffect(() => {
        const handleKeyDown = (event) => {
            const currentMessages = activeTab === 'all' ? messages : savedMessages;
            if (event.key === 'ArrowDown' && currentIndex < currentMessages.length - 1) {
                setCurrentIndex(prev => prev + 1);
                scrollToMessage(currentIndex + 1);
            } else if (event.key === 'ArrowUp' && currentIndex > 0) {
                setCurrentIndex(prev => prev - 1);
                scrollToMessage(currentIndex - 1);
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [currentIndex, messages.length, savedMessages.length, activeTab]);

    const scrollToMessage = (index) => {
        if (containerRef.current) {
            const messageElement = containerRef.current.children[index];
            if (messageElement) {
                messageElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    };

    const handleSave = async (messageId) => {
        if (!auth?.user) return;
        console.log('Saving message:', messageId);
        try {
            const response = await axios.post(`/api/messages/${messageId}/save`);
            console.log('Save successful:', response.data);

            // Refresh saved messages
            const savedResponse = await axios.get('/api/saved-messages');
            setSavedMessages(savedResponse.data);
        } catch (error) {
            console.error('Failed to save message:', error.response?.data || error.message);
        }
    };

    const handleUnsave = async (messageId) => {
        if (!auth?.user) return;
        console.log('Unsaving message:', messageId);
        try {
            const response = await axios.delete(`/api/messages/${messageId}/save`);
            console.log('Unsave successful:', response.data);

            setSavedMessages(prev => prev.filter(msg => msg.id !== messageId));
        } catch (error) {
            console.error('Failed to unsave message:', error.response?.data || error.message);
        }
    };

    const currentMessages = activeTab === 'all' ? messages : savedMessages;
    const isSaved = (messageId) => savedMessages.some(msg => msg.id === messageId);

    return (
        <div className="relative h-screen overflow-hidden bg-gray-100 dark:bg-gray-900">
            {/* Tabs */}
            <div className="absolute top-4 left-4 z-10 flex space-x-2">
                <button
                    onClick={() => { setActiveTab('all'); setCurrentIndex(0); }}
                    className={`px-4 py-2 rounded-full ${activeTab === 'all' ? 'bg-blue-500 text-white' : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300'}`}
                >
                    All
                </button>
                {auth?.user && (
                    <button
                        onClick={() => { setActiveTab('saved'); setCurrentIndex(0); }}
                        className={`px-4 py-2 rounded-full ${activeTab === 'saved' ? 'bg-blue-500 text-white' : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300'}`}
                    >
                        Saved ({savedMessages.length})
                    </button>
                )}
            </div>

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
            {currentIndex < currentMessages.length - 1 && (
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
                {currentMessages.length === 0 ? (
                    <div className="flex items-center justify-center h-screen">
                        <p className="text-gray-500 dark:text-gray-400 text-lg">
                            {activeTab === 'saved' ? 'No saved messages yet' : 'No messages yet'}
                        </p>
                    </div>
                ) : (
                    currentMessages.map((msg, index) => (
                        <div
                            key={msg.id}
                            className="flex items-center justify-center h-screen snap-start px-4"
                        >
                            {/* Telegram-Style Message Box */}
                            <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-200 dark:border-gray-700 relative">
                                {auth?.user && (
                                    <button
                                        onClick={() => isSaved(msg.id) ? handleUnsave(msg.id) : handleSave(msg.id)}
                                        className="absolute top-4 right-4 text-gray-500 hover:text-blue-500"
                                    >
                                        <svg className={`w-6 h-6 ${isSaved(msg.id) ? 'fill-current' : ''}`} fill={isSaved(msg.id) ? 'currentColor' : 'none'} stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                                        </svg>
                                    </button>
                                )}
                                <div className="flex items-start space-x-3">
                                    {/* Avatar Placeholder */}
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