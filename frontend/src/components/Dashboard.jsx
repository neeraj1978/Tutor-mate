import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    TrendingUp, CheckCircle, AlertCircle, MessageSquare, Send,
    BookOpen, Clock, Target, Image as ImageIcon, X
} from 'lucide-react';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell
} from 'recharts';
import axios from 'axios';
import Game from './Game';

const Dashboard = ({ user, onStartChat }) => {
    const [stats, setStats] = useState(null);
    const [recentSessions, setRecentSessions] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                // Ensure we have a valid ID
                const userId = user.id || user.user_id || user._id;
                if (!userId) {
                    console.warn("No user ID found in user object:", user);
                    setLoading(false);
                    return;
                }

                const response = await axios.get(`http://localhost:8000/dashboard/${userId}`);
                setStats(response.data.stats);
                setRecentSessions(response.data.recent_sessions);
            } catch (error) {
                console.error("Error fetching dashboard data:", error);
            } finally {
                setLoading(false);
            }
        };

        if (user) {
            fetchDashboardData();
        } else {
            setLoading(false);
        }
    }, [user]);


    if (loading) return (
        <div className="flex items-center justify-center h-96">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
    );

    // Prepare data for Bar Chart
    const chartData = stats?.subjects && stats.subjects.length > 0
        ? stats.subjects.map(sub => ({
            subject: sub.subject,
            score: sub.avg_score,
            fullMark: 100
        }))
        : [];

    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            return (
                <div className="bg-white p-4 rounded-xl shadow-lg border border-gray-100">
                    <p className="font-bold text-gray-800 mb-1">{label}</p>
                    <p className="text-primary font-medium">
                        Score: <span className="text-2xl font-bold">{payload[0].value}%</span>
                    </p>
                </div>
            );
        }
        return null;
    };

    return (
        <div className="space-y-6">
            <motion.header
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
                    Welcome back, {user?.name || 'Student'}! 👋
                </h1>
                <p className="text-gray-600 mt-2">Here's your learning progress at a glance</p>
            </motion.header>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.1 }}
                    className="card bg-white border-l-4 border-primary"
                >
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-gray-500 text-sm font-medium">Total Sessions</p>
                            <h3 className="text-3xl font-bold text-gray-900">{stats?.total_sessions || 0}</h3>
                        </div>
                        <div className="p-3 bg-indigo-50 rounded-full text-primary">
                            <Clock size={24} />
                        </div>
                    </div>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.2 }}
                    className="card bg-white border-l-4 border-secondary"
                >
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-gray-500 text-sm font-medium">Average Score</p>
                            <h3 className="text-3xl font-bold text-gray-900">{stats?.average_score || 0}%</h3>
                        </div>
                        <div className="p-3 bg-purple-50 rounded-full text-secondary">
                            <Target size={24} />
                        </div>
                    </div>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.3 }}
                    className="card bg-white border-l-4 border-green-500"
                >
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-gray-500 text-sm font-medium">Active Streak</p>
                            <h3 className="text-3xl font-bold text-gray-900">{stats?.streak || 0} {stats?.streak === 1 ? 'Day' : 'Days'}</h3>
                        </div>
                        <div className="p-3 bg-green-50 rounded-full text-green-500">
                            <TrendingUp size={24} />
                        </div>
                    </div>
                </motion.div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Skill Analysis Bar Chart */}
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 }}
                    className="card backdrop-blur-sm bg-white/80"
                >
                    <h2 className="text-lg font-semibold mb-6 flex items-center gap-2">
                        <div className="w-1 h-6 bg-gradient-to-b from-primary to-secondary rounded-full"></div>
                        Skill Analysis
                    </h2>
                    <div className="h-80 w-full">
                        {chartData.length > 0 ? (
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                                    <defs>
                                        <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="0%" stopColor="#4F46E5" stopOpacity={1} />
                                            <stop offset="100%" stopColor="#818cf8" stopOpacity={0.6} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                                    <XAxis
                                        dataKey="subject"
                                        axisLine={false}
                                        tickLine={false}
                                        tick={{ fill: '#6b7280', fontSize: 12, fontWeight: 500 }}
                                        dy={10}
                                    />
                                    <YAxis
                                        axisLine={false}
                                        tickLine={false}
                                        tick={{ fill: '#9ca3af', fontSize: 11 }}
                                        domain={[0, 100]}
                                    />
                                    <Tooltip content={<CustomTooltip />} cursor={{ fill: '#f9fafb' }} />
                                    <Bar
                                        dataKey="score"
                                        fill="url(#colorScore)"
                                        radius={[8, 8, 0, 0]}
                                        barSize={50}
                                        animationDuration={1500}
                                    >
                                        {chartData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill="url(#colorScore)" />
                                        ))}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        ) : (
                            <div className="flex items-center justify-center h-full text-gray-400">
                                <div className="text-center">
                                    <BookOpen size={48} className="mx-auto mb-3 opacity-50" />
                                    <p className="text-sm">Complete some learning sessions to see your skill analysis!</p>
                                </div>
                            </div>
                        )}
                    </div>
                </motion.div>

                {/* Daily Game Challenge */}
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 }}
                    className="card backdrop-blur-sm bg-white/80 flex flex-col h-[400px]"
                >
                    <Game user={user} />
                </motion.div>
            </div>
        </div>
    );
};

export default Dashboard;
