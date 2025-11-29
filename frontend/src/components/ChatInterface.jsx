import React, { useState, useEffect, useRef } from 'react';
import { Send, User, Bot, Loader2 } from 'lucide-react';
import axios from 'axios';
import { motion } from 'framer-motion';

const ChatInterface = ({ subject, difficulty, gradeLevel, onComplete }) => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [questionCount, setQuestionCount] = useState(0);
    const [sessionData, setSessionData] = useState({ subject, difficulty, messages: [] });
    const [isComplete, setIsComplete] = useState(false);
    const MAX_QUESTIONS = 5;
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        const startSession = async () => {
            setLoading(true);
            try {
                const response = await axios.post('http://localhost:8000/chat/start', {
                    subject,
                    difficulty,
                    grade_level: gradeLevel
                });
                setMessages([{ role: 'ai', content: response.data.message + " " + (response.data.question || "") }]);
                setQuestionCount(1);
            } catch (error) {
                console.error("Error starting chat:", error);
                setMessages([{ role: 'ai', content: "Failed to start session. Please try again." }]);
            } finally {
                setLoading(false);
            }
        };
        startSession();
    }, [subject, difficulty, gradeLevel]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = input;
        setInput("");
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setLoading(true);

        try {
            const history = messages.map(m => ({ role: m.role, content: m.content }));

            const response = await axios.post('http://localhost:8000/chat/message', {
                session_id: "demo_session",
                message: userMessage,
                history: history,
                difficulty: difficulty,
                grade_level: gradeLevel
            });

            const aiResponse = response.data;

            // Increment count AFTER the user answers the current question
            // If questionCount is 1, user just answered Q1.
            const questionsAnswered = questionCount;

            if (questionsAnswered >= MAX_QUESTIONS) {
                // User just answered the 5th question
                const finalMessage = `${aiResponse.feedback}\n\n🎉 You've completed all ${MAX_QUESTIONS} questions! Click 'View Results' to see your analysis.`;

                const finalMessages = [
                    ...messages,
                    { role: 'user', content: userMessage },
                    { role: 'ai', content: finalMessage, is_correct: aiResponse.is_correct }
                ];
                setMessages(prev => [...prev, { role: 'ai', content: finalMessage, is_correct: aiResponse.is_correct }]);
                setSessionData({ subject, difficulty, messages: finalMessages });
                setIsComplete(true);
                setLoading(false);
                return;
            }

            const newQuestionCount = questionCount + 1;
            setQuestionCount(newQuestionCount);

            const updatedMessages = [
                ...messages,
                { role: 'user', content: userMessage },
                {
                    role: 'ai',
                    content: `${aiResponse.feedback}\n\n${aiResponse.next_question}`,
                    is_correct: aiResponse.is_correct
                }
            ];
            setSessionData({ subject, difficulty, messages: updatedMessages });

            const aiText = `${aiResponse.feedback}\n\n${aiResponse.next_question}`;
            setMessages(prev => [...prev, { role: 'ai', content: aiText, is_correct: aiResponse.is_correct }]);
        } catch (error) {
            console.error("Error sending message:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto h-[600px] flex flex-col card p-0 overflow-hidden shadow-xl">
            <div className="bg-gradient-to-r from-primary to-secondary p-4 flex justify-between items-center text-white">
                <div>
                    <h2 className="font-bold text-lg">{subject}</h2>
                    <div className="flex items-center gap-2 mt-1">
                        <span className="text-xs bg-white/20 px-2 py-1 rounded-full capitalize">{difficulty}</span>
                        <span className="text-xs">Question {questionCount} of {MAX_QUESTIONS}</span>
                    </div>
                </div>
                <button onClick={() => onComplete({ session_data: sessionData })} className="text-sm hover:bg-white/20 px-3 py-1 rounded-lg transition-colors">
                    End Session →
                </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-gray-50 to-white">
                {messages.map((msg, idx) => (
                    <motion.div
                        key={idx}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                    >
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-gradient-to-r from-primary to-secondary text-white' : 'bg-gradient-to-r from-green-400 to-emerald-500 text-white'}`}>
                            {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                        </div>
                        <div className={`max-w-[80%] p-3 rounded-2xl ${msg.role === 'user' ? 'bg-gradient-to-r from-primary to-secondary text-white rounded-tr-none shadow-md' : 'bg-white border border-gray-200 rounded-tl-none shadow-sm'}`}>
                            <p className="whitespace-pre-wrap">{msg.content}</p>
                        </div>
                    </motion.div>
                ))}
                {loading && (
                    <div className="flex gap-3">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-green-400 to-emerald-500 text-white flex items-center justify-center shrink-0">
                            <Bot size={16} />
                        </div>
                        <div className="bg-white border border-gray-200 p-3 rounded-2xl rounded-tl-none shadow-sm">
                            <Loader2 className="animate-spin text-gray-400" size={20} />
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="p-4 bg-white border-t">
                {isComplete ? (
                    <motion.button
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        onClick={() => onComplete({
                            subject,
                            difficulty,
                            grade_level: gradeLevel,
                            messages: messages,
                            session_data: { messages: messages, subject, difficulty, grade_level: gradeLevel }
                        })}
                        className="w-full bg-gradient-to-r from-green-500 to-emerald-600 text-white p-3 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2"
                    >
                        View Results <Send size={20} />
                    </motion.button>
                ) : (
                    <div className="flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Type your answer..."
                            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-primary focus:border-transparent outline-none"
                            disabled={loading}
                        />
                        <button
                            onClick={handleSend}
                            disabled={loading || !input.trim()}
                            className="bg-gradient-to-r from-primary to-secondary text-white p-2 rounded-lg hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                        >
                            <Send size={20} />
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ChatInterface;
