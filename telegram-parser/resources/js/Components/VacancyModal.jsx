import React from 'react';

export default function VacancyModal({ vacancy, onClose, auth, isSaved, onSave, onUnsave }) {
    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg shadow-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto relative border border-gray-200">
                <button
                    onClick={() => isSaved ? onUnsave(vacancy.id) : onSave(vacancy.id)}
                    className="absolute top-4 right-4 p-2 text-gray-500 hover:text-blue-500 transition-colors rounded"
                >
                    <svg className={`w-6 h-6 ${isSaved ? 'fill-current text-blue-500' : ''}`} fill={isSaved ? 'currentColor' : 'none'} stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                    </svg>
                </button>
                <button
                    className="absolute top-4 left-4 p-2 text-gray-500 hover:text-gray-700 text-xl transition-colors rounded"
                    onClick={onClose}
                >
                    ✕
                </button>
                <div className="p-6 pt-16">  {/* Add pt-16 to account for absolute buttons */}
                    <h2 className="text-2xl font-bold text-gray-800 mb-6">{vacancy.title}</h2>
                    <div className="mb-4 flex items-center">
                        <img src={`/storage/source_logos/${vacancy.source}.png`} alt={vacancy.source} className="w-8 h-8 mr-3" />
                        <span className="font-semibold text-gray-700">{vacancy.source.toUpperCase()}</span>
                    </div>
                    <div className="mb-4 flex items-center">
                        {vacancy.logo && <img src={`/storage/${vacancy.logo}`} alt={vacancy.company} className="w-10 h-10 mr-3 rounded" />}
                        <span className="text-lg text-gray-700">{vacancy.company}</span>
                    </div>
                    <div className="mb-4">
                        <strong className="text-gray-800">Skills:</strong>
                        <div className="flex flex-wrap gap-2 mt-2">
                            {vacancy.skills.map((skill, index) => (
                                <span key={index} className="bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full">
                                    {skill}
                                </span>
                            ))}
                        </div>
                    </div>
                    <div className="mb-4">
                        <strong className="text-gray-800">Salary:</strong> <span className="text-gray-700">{vacancy.salary || 'N/A'}</span>
                    </div>
                    <div className="mb-4">
                        <strong className="text-gray-800">Country:</strong> <span className="text-gray-700">{vacancy.country}</span>
                    </div>
                    <div className="mb-4">
                        <strong className="text-gray-800">Posted:</strong> <span className="text-gray-700">{new Date(vacancy.posted_at).toLocaleDateString()}</span>
                    </div>
                    <div className="mb-6">
                        <a href={vacancy.url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:text-blue-700 underline transition-colors">
                            View on Website
                        </a>
                    </div>
                    <div className="border-t pt-4" dangerouslySetInnerHTML={{ __html: vacancy.description }} />
                </div>
            </div>
        </div>
    );
}