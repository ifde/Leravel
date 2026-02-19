import { useEffect, useState, useRef } from 'react';
import { usePage } from '@inertiajs/react';
import axios from 'axios';
import HomeLayout from '@/Layouts/HomeLayout';
import NavigationArrows from '@/Components/NavigationArrows';
import MessageBox from '@/Components/MessageBox';

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
        <HomeLayout tabProps={{ activeTab, setActiveTab, setCurrentIndex, savedMessagesCount: savedMessages.length, auth }}>
            <div className="relative h-full overflow-hidden bg-gray-100 dark:bg-gray-900">
                <NavigationArrows
                    currentIndex={currentIndex}
                    currentMessagesLength={currentMessages.length}
                    setCurrentIndex={setCurrentIndex}
                    scrollToMessage={scrollToMessage}
                />
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
                                <MessageBox
                                    msg={msg}
                                    auth={auth}
                                    isSaved={isSaved}
                                    onSave={handleSave}
                                    onUnsave={handleUnsave}
                                />
                            </div>
                        ))
                    )}
                </div>
            </div>
        </HomeLayout>
    );
}