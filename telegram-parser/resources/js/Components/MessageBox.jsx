export default function MessageBox({ msg, auth, isSaved, onSave, onUnsave }) {
    return (
        <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-200 dark:border-gray-700 relative">
            {auth?.user && (
                <button
                    onClick={() => isSaved(msg.id) ? onUnsave(msg.id) : onSave(msg.id)}
                    className="absolute top-4 right-4 text-gray-500 hover:text-blue-500"
                >
                    <svg className={`w-6 h-6 ${isSaved(msg.id) ? 'fill-current' : ''}`} fill={isSaved(msg.id) ? 'currentColor' : 'none'} stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                    </svg>
                </button>
            )}
            <div className="flex items-start space-x-3">
                {/* Profile Picture or Avatar Placeholder */}
                {msg.profile_pic_path ? (
                    <img
                        src={`/storage/${msg.profile_pic_path}`}
                        alt={`${msg.channel} profile`}
                        className="w-10 h-10 rounded-full object-cover"
                        onError={(e) => {
                            e.target.style.display = 'none';
                            const placeholder = e.target.nextSibling;
                            if (placeholder) placeholder.style.display = 'flex';
                        }}
                    />
                ) : null}
                <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm ${msg.profile_pic_path ? 'hidden' : 'bg-blue-500'}`}
                >
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
    );
}