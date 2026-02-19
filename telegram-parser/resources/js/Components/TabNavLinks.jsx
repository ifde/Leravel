export default function TabNavLinks({ tabProps }) {
    const navLinkBaseClasses = 'inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium leading-5 transition duration-150 ease-in-out focus:outline-none border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 focus:border-gray-300 focus:text-gray-700';
    const navLinkActiveClasses = 'border-indigo-400 text-gray-900 focus:border-indigo-700';

    return (
        <div className="hidden space-x-8 sm:-my-px sm:ml-10 sm:flex">
            <button
                onClick={() => { tabProps.setActiveTab('all'); tabProps.setCurrentIndex(0); }}
                className={`${navLinkBaseClasses} ${tabProps.activeTab === 'all' ? navLinkActiveClasses : ''}`}
            >
                All
            </button>
            {tabProps.auth?.user && (
                <button
                    onClick={() => { tabProps.setActiveTab('saved'); tabProps.setCurrentIndex(0); }}
                    className={`${navLinkBaseClasses} ${tabProps.activeTab === 'saved' ? navLinkActiveClasses : ''}`}
                >
                    Saved ({tabProps.savedMessagesCount})
                </button>
            )}
        </div>
    );
}