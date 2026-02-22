import { useEffect, useState } from 'react';
import axios from 'axios';
// import Echo from '@/echo';
import { router } from '@inertiajs/react';
import HomeLayout from '@/Layouts/HomeLayout';
import VacancyModal from '@/Components/VacancyModal';

// Axios config (same as before)
axios.defaults.withCredentials = true;
axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
axios.defaults.headers.common['Accept'] = 'application/json';

const getCsrfToken = () => {
    const name = 'XSRF-TOKEN';
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return decodeURIComponent(parts.pop().split(';').shift());
    return null;
};

axios.interceptors.request.use((config) => {
    const token = getCsrfToken();
    if (token && ['post', 'put', 'delete', 'patch'].includes(config.method?.toLowerCase())) {
        config.headers['X-XSRF-TOKEN'] = token;
    }
    return config;
});

export default function Home({ auth }) {
    const [vacancies, setVacancies] = useState([]);
    const [selectedVacancy, setSelectedVacancy] = useState(null);
    const [savedVacancies, setSavedVacancies] = useState(new Set());
    const [filter, setFilter] = useState('all');

    useEffect(() => {
        axios.get('/api/vacancies')
            .then(response => setVacancies(response.data || []))
            .catch(error => console.error('Error fetching vacancies:', error));

        if (auth.user) {
            axios.get('/api/user/saved-vacancies')
                .then(response => setSavedVacancies(new Set((response.data || []).map(v => v.url))))
                .catch(() => { });
        }

        // Listen for the event
        window.Echo.channel('vacancies')
            .listen('.VacancyReceived', (e) => {
                console.log('Vacancy data:', e); // Is it nested?

                setVacancies(prev => {
                    const next = [e, ...prev].filter(Boolean);
                    return next.sort((a, b) => new Date(b?.posted_at || 0) - new Date(a?.posted_at || 0));
                });
                console.log("Event received");
            });

        return () => {
            window.Echo.leave('vacancies');  // Cleanup
        };
    }, [auth.user]);

    const formatDate = (dateString) => {
        if (!dateString) return '—';
        const date = new Date(dateString);
        if (isNaN(date)) return '—';
        return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    };

    const handleSave = async (url) => {
        if (!auth.user) {
            router.visit('/login');
            return;
        }
        try {
            await axios.post('/api/vacancies/save', { url });
            setSavedVacancies(prev => new Set([...prev, url]));
        } catch (error) {
            console.error('Save failed:', error);
        }
    };

    const handleUnsave = async (url) => {
        if (!auth.user) {
            router.visit('/login');
            return;
        }
        try {
            await axios.delete('/api/vacancies/unsave', { data: { url } });
            setSavedVacancies(prev => {
                const newSet = new Set(prev);
                newSet.delete(url);
                return newSet;
            });
        } catch (error) {
            console.error('Unsave failed:', error);
        }
    };

    const displayedVacancies = filter === 'saved'
        ? vacancies.filter(v => v && savedVacancies.has(v.url))
        : vacancies.filter(Boolean);

    return (
        <HomeLayout>
            <div className="container mx-auto p-4 pb-24 h-screen overflow-y-auto">
                <h1 className="text-2xl font-bold mb-4">Vacancies</h1>
                <div className="mb-4 flex space-x-4">
                    <div className="mb-4 flex space-x-4">
                        <button
                            onClick={() => setFilter('all')}
                            className={`px-4 py-2 rounded ${filter === 'all' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
                        >
                            All
                        </button>
                        <button
                            onClick={() => setFilter('saved')}
                            className={`px-4 py-2 rounded ${filter === 'saved' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
                        >
                            Saved ({savedVacancies.size})
                        </button>
                    </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {displayedVacancies.map(vacancy => {
                        const postedAt = vacancy?.posted_at ? new Date(vacancy.posted_at) : null;
                        const isNew = postedAt ? (Date.now() - postedAt.getTime()) < (24 * 60 * 60 * 1000) : false;
                        return (
                            <div
                                key={vacancy.url}  // Use url as key
                                className={`border rounded-lg p-4 shadow hover:shadow-lg cursor-pointer ${savedVacancies.has(vacancy.url) ? 'border-green-500' : ''}`}
                                onClick={() => setSelectedVacancy(vacancy)}
                            >
                                <div className="flex items-center mb-2">
                                    <img src={`/storage/source_logos/${vacancy.source.toLowerCase()}.png`} alt={vacancy.source} className="w-6 h-6 mr-2" />
                                    <span className="text-sm font-semibold">{vacancy.source.toUpperCase()}</span>
                                    {isNew && (
                                        <span className="ml-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full font-bold">
                                            NEW
                                        </span>
                                    )}
                                </div>
                                <h2 className="text-lg font-bold">{vacancy.title}</h2>
                                <div className="flex items-center mt-2">
                                    {vacancy.logo && <img src={`/storage/${vacancy.logo.toLowerCase()}`} alt={vacancy.company} className="w-8 h-8 mr-2" />}
                                    <p className="text-gray-600">{vacancy.company}</p>
                                </div>
                                <div className="flex flex-wrap gap-1 mt-2">
                                    {(vacancy.skills || []).map((skill, index) => (
                                        <span key={index} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                                            {skill}
                                        </span>
                                    ))}
                                </div>
                                <p className="text-sm text-gray-500 mt-2">{vacancy.country}</p>
                                <p className="text-sm text-gray-500">{formatDate(vacancy.posted_at)}</p>
                            </div>
                        );
                    })}
                </div>
                {selectedVacancy && (
                    <VacancyModal
                        vacancy={selectedVacancy}
                        onClose={() => setSelectedVacancy(null)}
                        auth={auth}
                        isSaved={savedVacancies.has(selectedVacancy.url)}
                        onSave={() => handleSave(selectedVacancy.url)}
                        onUnsave={() => handleUnsave(selectedVacancy.url)}
                    />
                )}
            </div>
        </HomeLayout>
    );
}