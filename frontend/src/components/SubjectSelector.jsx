import React, { useState } from 'react';
import { Calculator, Book, Globe, Microscope, ArrowRight, Plus } from 'lucide-react';
import { motion } from 'framer-motion';

const subjects = [
    { id: 'Mathematics', name: 'Mathematics', icon: Calculator, color: 'bg-blue-100 text-blue-600' },
    { id: 'Computer Science', name: 'Computer Science', icon: Microscope, color: 'bg-green-100 text-green-600' },
    { id: 'History', name: 'History', icon: Book, color: 'bg-amber-100 text-amber-600' },
    { id: 'Literature', name: 'Literature', icon: Globe, color: 'bg-purple-100 text-purple-600' },
];

const SubjectSelector = ({ onSelect }) => {
    const [customSubject, setCustomSubject] = useState("");

    const handleCustomSubmit = (e) => {
        e.preventDefault();
        if (customSubject.trim()) {
            onSelect(customSubject.trim());
        }
    };

    return (
        <div className="max-w-4xl mx-auto mt-12">
            <div className="text-center mb-12">
                <h1 className="text-4xl font-bold mb-4">What do you want to master today?</h1>
                <p className="text-xl text-gray-600">Pick a subject or enter your own topic.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                {subjects.map((subject, index) => (
                    <motion.button
                        key={subject.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        onClick={() => onSelect(subject.id)}
                        className="card hover:shadow-lg transition-all text-left group"
                    >
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-4">
                                <div className={`p-4 rounded-xl ${subject.color}`}>
                                    <subject.icon size={32} />
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold">{subject.name}</h3>
                                    <p className="text-gray-500">College Level</p>
                                </div>
                            </div>
                            <div className="opacity-0 group-hover:opacity-100 transition-opacity text-primary">
                                <ArrowRight size={24} />
                            </div>
                        </div>
                    </motion.button>
                ))}
            </div>

            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="card bg-gray-50 border-dashed border-2 border-gray-300"
            >
                <form onSubmit={handleCustomSubmit} className="flex flex-col md:flex-row items-center gap-4">
                    <div className="p-3 bg-white rounded-full text-gray-400 shadow-sm">
                        <Plus size={24} />
                    </div>
                    <div className="flex-1 w-full">
                        <label htmlFor="custom" className="sr-only">Custom Subject</label>
                        <input
                            id="custom"
                            type="text"
                            placeholder="Enter any subject (e.g. Quantum Physics, Macroeconomics)..."
                            className="w-full bg-white border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-primary focus:border-transparent outline-none text-lg placeholder-gray-500 shadow-sm transition-all"
                            value={customSubject}
                            onChange={(e) => setCustomSubject(e.target.value)}
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={!customSubject.trim()}
                        className="btn-primary whitespace-nowrap disabled:opacity-50 disabled:cursor-not-allowed w-full md:w-auto"
                    >
                        Start Learning
                    </button>
                </form>
            </motion.div>
        </div>
    );
};

export default SubjectSelector;
