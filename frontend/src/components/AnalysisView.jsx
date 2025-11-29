import React, { useState, useEffect } from 'react';
import { CheckCircle, XCircle, TrendingUp, BookOpen, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';
import axios from 'axios';

const AnalysisView = ({ onRestart, sessionData, user, onBackToDashboard }) => {
    const [analysis, setAnalysis] = useState(null);
    const [loading, setLoading] = useState(true);

    const analysisRequested = React.useRef(false);

    useEffect(() => {
        const generateAnalysis = async () => {
            if (analysisRequested.current) return;
            analysisRequested.current = true;

            setLoading(true);
            try {
                const userId = user?.id || user?.user_id || user?._id;
                const response = await axios.post('http://localhost:8000/chat/analyze', {
                    user_id: userId,
                    session_data: sessionData || {
                        subject: "General",
                        difficulty: "intermediate",
                        messages: []
                    }
                });

                setAnalysis(response.data);
            } catch (error) {
                console.error("Error generating analysis:", error);
                setAnalysis({
                    overall_score: 0,
                    strengths: ["Good conceptual understanding", "Clear explanations"],
                    weaknesses: ["Need more practice with advanced topics", "Could improve speed"],
                    recommendations: [
                        "Review fundamental concepts",
                        "Practice more complex problems",
                        "Focus on time management"
                    ]
                });
            } finally {
                setLoading(false);
            }
        };

        generateAnalysis();
    }, [sessionData, user?.id]);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-96">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary mx-auto mb-4"></div>
                    <p className="text-gray-600 font-medium">Analyzing your performance...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center"
            >
                <div className="inline-block p-4 bg-gradient-to-r from-primary to-secondary rounded-full mb-4">
                    <TrendingUp className="text-white" size={48} />
                </div>
                <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary mb-2">
                    Performance Analysis
                </h1>
                <p className="text-gray-600">Here's how you did!</p>
            </motion.div>

            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.1 }}
                className="card bg-gradient-to-br from-indigo-50 to-purple-50 border-indigo-100 text-center p-8"
            >
                <h2 className="text-lg font-semibold text-gray-700 mb-4">Overall Performance</h2>
                <div className="text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary mb-2">
                    {analysis?.overall_score ?? 0}%
                </div>
                <p className="text-gray-600">
                    {(analysis?.overall_score ?? 0) < 50
                        ? "Don't give up! Every expert was once a beginner."
                        : "Great job! Keep up the good work."}
                </p>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {(analysis?.overall_score ?? 0) >= 50 && (
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.2 }}
                        className="card"
                    >
                        <div className="flex items-center gap-2 mb-4">
                            <CheckCircle className="text-green-500" size={24} />
                            <h3 className="text-lg font-semibold">Strengths</h3>
                        </div>
                        <ul className="space-y-2">
                            {(analysis?.strengths || []).map((strength, idx) => (
                                <li key={idx} className="flex items-start gap-2">
                                    <ArrowRight className="text-green-500 shrink-0 mt-1" size={16} />
                                    <span className="text-gray-700">{strength}</span>
                                </li>
                            ))}
                        </ul>
                    </motion.div>
                )}

                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.2 }}
                    className="card"
                >
                    <div className="flex items-center gap-2 mb-4">
                        <XCircle className="text-orange-500" size={24} />
                        <h3 className="text-lg font-semibold">Areas to Improve</h3>
                    </div>
                    <ul className="space-y-2">
                        {(analysis?.weaknesses || []).map((weakness, idx) => (
                            <li key={idx} className="flex items-start gap-2">
                                <ArrowRight className="text-orange-500 shrink-0 mt-1" size={16} />
                                <span className="text-gray-700">{weakness}</span>
                            </li>
                        ))}
                    </ul>
                </motion.div>
            </div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="card bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-100"
            >
                <div className="flex items-center gap-2 mb-4">
                    <BookOpen className="text-primary" size={24} />
                    <h3 className="text-lg font-semibold">Recommended Video Lessons</h3>
                </div>
                <div className="space-y-3">
                    {(analysis?.recommendations || []).map((rec, idx) => (
                        <div key={idx} className="p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-all group cursor-pointer border border-transparent hover:border-primary/20">
                            <a
                                href={`https://www.youtube.com/results?search_query=${encodeURIComponent(rec.query || rec)}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex items-start gap-4"
                            >
                                <div className="w-12 h-12 rounded-lg bg-red-100 text-red-600 flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform">
                                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                                        <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z" />
                                    </svg>
                                </div>
                                <div>
                                    <h4 className="font-semibold text-gray-900 group-hover:text-primary transition-colors">
                                        {rec.title || rec}
                                    </h4>
                                    <p className="text-sm text-gray-500 flex items-center gap-1 mt-1">
                                        <span className="font-medium text-gray-700">{rec.channel || "YouTube"}</span>
                                        <span>•</span>
                                        <span className="text-red-500 text-xs font-semibold">Watch Now</span>
                                    </p>
                                </div>
                            </a>
                        </div>
                    ))}
                </div>
            </motion.div>

            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="flex gap-4 justify-center"
            >
                <button
                    onClick={onRestart}
                    className="px-6 py-3 bg-gradient-to-r from-primary to-secondary text-white rounded-lg font-semibold hover:shadow-lg transition-all"
                >
                    Start New Session
                </button>
                <button
                    onClick={onBackToDashboard || (() => window.location.href = '/')}
                    className="px-6 py-3 bg-white border-2 border-primary text-primary rounded-lg font-semibold hover:bg-gray-50 transition-all"
                >
                    Back to Dashboard
                </button>
            </motion.div>
        </div>
    );
};

export default AnalysisView;
