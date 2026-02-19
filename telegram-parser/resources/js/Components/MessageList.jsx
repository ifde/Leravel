import MessageBox from './MessageBox';

export default function MessageList({ messages, auth, savedMessages, handleSave, handleUnsave }) {
    const isSaved = (messageId) => savedMessages.some(msg => msg.id === messageId);

    return (
        <div className="h-full overflow-y-auto snap-y snap-mandatory" style={{ scrollBehavior: 'smooth' }}>
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
    );
}