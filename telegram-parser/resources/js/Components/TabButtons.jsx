export default function TabButtons({ className, activeTab, setActiveTab, setCurrentIndex, savedMessagesCount, auth }) {
    const baseClasses = "px-4 py-2 rounded-full";
    const activeClasses = "bg-blue-500 text-white";
    const inactiveClasses = "bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300";

    return (
        <div className={className}>
            <button
                onClick={() => { setActiveTab('all'); setCurrentIndex(0); }}
                className={`${baseClasses} ${activeTab === 'all' ? activeClasses : inactiveClasses}`}
            >
                All
            </button>
            {auth?.user && (
                <button
                    onClick={() => { setActiveTab('saved'); setCurrentIndex(0); }}
                    className={`${baseClasses} ${activeTab === 'saved' ? activeClasses : inactiveClasses}`}
                >
                    Saved ({savedMessagesCount})
                </button>
            )}
        </div>
    );
}