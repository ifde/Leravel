export default function NavigationArrows({ currentIndex, currentMessagesLength, setCurrentIndex, scrollToMessage }) {
    return (
        <>
            {currentIndex > 0 && (
                <button
                    onClick={() => {
                        setCurrentIndex(prev => prev - 1);
                        scrollToMessage(currentIndex - 1);
                    }}
                    className="absolute top-4 left-1/2 transform -translate-x-1/2 z-60 bg-white dark:bg-gray-800 rounded-full p-2 shadow-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition"
                >
                    <svg className="w-6 h-6 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                    </svg>
                </button>
            )}
            {currentIndex < currentMessagesLength - 1 && (
                <button
                    onClick={() => {
                        setCurrentIndex(prev => prev + 1);
                        scrollToMessage(currentIndex + 1);
                    }}
                    className="absolute bottom-4 left-1/2 transform -translate-x-1/2 z-60 bg-white dark:bg-gray-800 rounded-full p-2 shadow-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition"
                >
                    <svg className="w-6 h-6 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                </button>
            )}
        </>
    );
}