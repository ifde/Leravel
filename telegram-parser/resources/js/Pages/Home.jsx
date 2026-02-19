import { useEffect, useState } from 'react';
import axios from 'axios';
import HomeLayout from '@/Layouts/HomeLayout';
import MessageBox from '@/Components/MessageBox';

// Configure Axios globally for credentials and CSRF
axios.defaults.withCredentials = true;
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
    const [messages, setMessages] = useState([]);

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

    // Echo listener
    useEffect(() => {
        window.Echo.channel('messages')
            .listen('.TelegramMessageReceived', (event) => {
                setMessages(prev => [event.message, ...prev]);
            });
        return () => window.Echo.leave('messages');
    }, []);

    return (
        <HomeLayout>
            <div className="h-full overflow-y-auto bg-gray-100 dark:bg-gray-900 py-8 space-y-8"> {/* Add space-y-8 for spacing */}
                {messages.length === 0 ? (
                    <div className="flex items-center justify-center h-full">
                        <p className="text-gray-500 dark:text-gray-400 text-lg">No messages yet</p>
                    </div>
                ) : (
                    messages.map((msg) => (
                        <div key={msg.id} className="flex justify-center px-4"> {/* Center each message */}
                            <MessageBox
                                msg={msg}
                                auth={null}
                                isSaved={() => false}
                                onSave={() => { }}
                                onUnsave={() => { }}
                            />
                        </div>
                    ))
                )}
            </div>
        </HomeLayout>
    );
}