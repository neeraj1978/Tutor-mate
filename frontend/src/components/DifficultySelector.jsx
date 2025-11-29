import React from 'react';
import { Zap, TrendingUp, Award } from 'lucide-react';
import { motion } from 'framer-motion';

const difficulties = [
    {
        id: 'beginner',
        name: 'Beginner',
        icon: Zap,
        color: 'bg-green-100 text-green-600 border-green-300',
        gradient: 'from-green-400 to-emerald-500',
        description: 'Perfect for school students and beginners'
    },
    {
        id: 'intermediate',
        name: 'Intermediate',
        icon: TrendingUp,
        color: 'bg-yellow-100 text-yellow-600 border-yellow-300',
        gradient: 'from-yellow-400 to-orange-500',
        description: 'Ideal for college students and learners'
    },
    {
        id: 'advanced',
        name: 'Advanced',
        icon: Award,
        color: 'bg-red-100 text-red-600 border-red-300',
        gradient: 'from-red-400 to-pink-500',
        description: 'For professionals and experts'
    },
];

const DifficultySelector = ({ subject, onSelect, onBack }) => {
    return (
        <div className="max-w-3xl mx-auto mt-12">
            <div className="text-center mb-12">
                <button
                    onClick={onBack}
                    className="text-gray-500 hover:text-gray-700 mb-4 inline-flex items-center gap-2"
                >
                    ← Back to Subjects
                </button>
                <h1 className="text-4xl font-bold mb-4">Choose Your Level</h1>
                <p className="text-xl text-gray-600">
                    Subject: <span className="font-semibold text-primary">{subject}</span>
                </p>
                <p className="text-gray-500 mt-2">Select the difficulty that matches your current knowledge</p>
            </div>

            <div className="space-y-4">
                {difficulties.map((difficulty, index) => (
                    <motion.button
                        key={difficulty.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        onClick={() => onSelect(difficulty.id)}
                        className={`w-full card hover:shadow-xl transition-all text-left group border-2 ${difficulty.color} relative overflow-hidden`}
                    >
                        <div className={`absolute inset-0 bg-gradient-to-r ${difficulty.gradient} opacity-0 group-hover:opacity-10 transition-opacity`}></div>
                        <div className="flex items-center justify-between relative z-10">
                            <div className="flex items-center gap-4">
                                <div className={`p-4 rounded-xl ${difficulty.color}`}>
                                    <difficulty.icon size={32} />
                                </div>
                                <div>
                                    <h3 className="text-2xl font-bold">{difficulty.name}</h3>
                                    <p className="text-gray-600 text-sm">{difficulty.description}</p>
                                </div>
                            </div>
                            <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                                <div className={`px-4 py-2 rounded-lg bg-gradient-to-r ${difficulty.gradient} text-white font-medium`}>
                                    Start →
                                </div>
                            </div>
                        </div>
                    </motion.button>
                ))}
            </div>
        </div>
    );
};

export default DifficultySelector;
