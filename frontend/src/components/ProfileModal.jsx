import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, User, Mail, GraduationCap, Calendar } from 'lucide-react';

const ProfileModal = ({ user, onClose }) => {
    if (!user) return null;

    return (
        <AnimatePresence>
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm" onClick={onClose}>
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden"
                    onClick={(e) => e.stopPropagation()}
                >
                    {/* Header */}
                    <div className="bg-gradient-to-r from-primary to-secondary p-6 text-white relative">
                        <button
                            onClick={onClose}
                            className="absolute top-4 right-4 text-white/80 hover:text-white hover:bg-white/20 rounded-full p-1 transition-colors"
                        >
                            <X size={20} />
                        </button>

                        <div className="flex flex-col items-center mt-4">
                            <div className="w-24 h-24 rounded-full bg-white text-primary flex items-center justify-center text-4xl font-bold shadow-lg mb-4">
                                {user.name ? user.name[0].toUpperCase() : 'U'}
                            </div>
                            <h2 className="text-2xl font-bold">{user.name}</h2>
                            <p className="text-white/80">{user.grade_level || "Student"}</p>
                        </div>
                    </div>

                    {/* Body */}
                    <div className="p-6 space-y-6">
                        <div className="space-y-4">
                            <div className="flex items-center gap-4 p-3 bg-gray-50 rounded-xl">
                                <div className="p-2 bg-blue-100 text-blue-600 rounded-lg">
                                    <Mail size={20} />
                                </div>
                                <div>
                                    <p className="text-xs text-gray-500 font-medium">Email Address</p>
                                    <p className="text-gray-900 font-medium">{user.email}</p>
                                </div>
                            </div>

                            <div className="flex items-center gap-4 p-3 bg-gray-50 rounded-xl">
                                <div className="p-2 bg-purple-100 text-purple-600 rounded-lg">
                                    <GraduationCap size={20} />
                                </div>
                                <div>
                                    <p className="text-xs text-gray-500 font-medium">Grade / Year</p>
                                    <p className="text-gray-900 font-medium">{user.grade_level || "Not specified"}</p>
                                </div>
                            </div>

                            <div className="flex items-center gap-4 p-3 bg-gray-50 rounded-xl">
                                <div className="p-2 bg-green-100 text-green-600 rounded-lg">
                                    <Calendar size={20} />
                                </div>
                                <div>
                                    <p className="text-xs text-gray-500 font-medium">Member Since</p>
                                    <p className="text-gray-900 font-medium">November 2025</p>
                                </div>
                            </div>
                        </div>

                        <button
                            onClick={onClose}
                            className="w-full py-3 bg-gray-100 text-gray-700 font-semibold rounded-xl hover:bg-gray-200 transition-colors"
                        >
                            Close Profile
                        </button>
                    </div>
                </motion.div>
            </div>
        </AnimatePresence>
    );
};

export default ProfileModal;
