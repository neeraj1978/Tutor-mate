import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Clock, Trophy, Award, AlertCircle, CheckCircle, XCircle, Brain, Puzzle, Type, Image as ImageIcon } from 'lucide-react';
import axios from 'axios';

const Game = ({ user }) => {
    const [gameData, setGameData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [timeLeft, setTimeLeft] = useState(0);
    const [result, setResult] = useState(null);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState(null);
    const [gameStarted, setGameStarted] = useState(false);

    // State for different game types
    const [mcqAnswers, setMcqAnswers] = useState({}); // { 0: "Option A", 1: "Option B" }
    const [textInput, setTextInput] = useState("");
    const [sentenceWords, setSentenceWords] = useState([]); // For Sentence Builder

    const fetchGame = async () => {
        try {
            setLoading(true);
            const userId = user.id || user.user_id || user._id;
            const response = await axios.get(`http://localhost:8000/game/current?user_id=${userId}`);
            setGameData(response.data);
            setTimeLeft(response.data.time_remaining);

            // If played, show the last result if available
            if (response.data.played && response.data.last_result) {
                setResult(response.data.last_result);
            } else {
                setResult(null);
            }

            // Reset local state
            setMcqAnswers({});
            setTextInput("");
            setSentenceWords([]);
        } catch (err) {
            console.error("Error fetching game:", err);
            setError("Failed to load the challenge.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchGame();
    }, [user]);

    useEffect(() => {
        if (timeLeft <= 0) {
            if (gameData && !loading) {
                const timer = setTimeout(() => fetchGame(), 2000);
                return () => clearTimeout(timer);
            }
            return;
        }
        const timer = setInterval(() => {
            setTimeLeft((prev) => {
                if (prev <= 1) {
                    fetchGame();
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);
        return () => clearInterval(timer);
    }, [timeLeft, gameData, loading]);

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    const handleSubmit = async () => {
        setSubmitting(true);
        let answerPayload = null;

        const { game } = gameData;

        if (game.type === "MCQ_SET") {
            answerPayload = mcqAnswers;
        } else if (game.type === "SENTENCE_BUILDER") {
            answerPayload = sentenceWords.join(" ");
        } else {
            answerPayload = textInput; // Logic, Shape, Word Scramble
        }

        try {
            const userId = user.id || user.user_id || user._id;
            const response = await axios.post('http://localhost:8000/game/submit', {
                user_id: userId,
                window_id: gameData.window_id,
                answer: answerPayload
            });

            setResult(response.data);
            setGameData(prev => ({ ...prev, played: true }));
            setTimeLeft(3600); // Immediate 1-hour cooldown
        } catch (err) {
            console.error("Error submitting game:", err);
            setError("Failed to submit answer.");
        } finally {
            setSubmitting(false);
        }
    };

    // Render Helpers
    const renderGameContent = () => {
        if (!gameData || !gameData.game) return null;
        const { game } = gameData;

        switch (game.type) {
            case "MCQ_SET":
                return (
                    <div className="space-y-6">
                        {game.questions.map((q, idx) => (
                            <div key={idx} className="p-4 bg-white rounded-xl border border-gray-100 shadow-sm">
                                <p className="font-medium text-gray-800 mb-3">{idx + 1}. {q.q}</p>
                                <div className="grid grid-cols-1 gap-2">
                                    {q.options.map((opt, optIdx) => (
                                        <button
                                            key={optIdx}
                                            onClick={() => setMcqAnswers(prev => ({ ...prev, [idx]: opt }))}
                                            className={`p-2 rounded-lg text-left text-sm transition-all border ${mcqAnswers[idx] === opt
                                                ? 'bg-primary/10 border-primary text-primary font-medium'
                                                : 'bg-gray-50 border-transparent hover:bg-gray-100'
                                                }`}
                                        >
                                            {opt}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                );

            case "LOGIC_PUZZLE":
                return (
                    <div className="space-y-4">
                        <div className="p-4 bg-purple-50 rounded-xl border border-purple-100 text-purple-900">
                            <Brain className="mb-2 text-purple-500" size={24} />
                            <p className="font-medium text-lg">{game.question}</p>
                        </div>
                        <div className="space-y-2">
                            {game.options.map((opt, idx) => (
                                <button
                                    key={idx}
                                    onClick={() => setTextInput(opt)}
                                    className={`w-full p-3 rounded-xl border-2 text-left transition-all ${textInput === opt
                                        ? 'border-purple-500 bg-purple-50 text-purple-700'
                                        : 'border-gray-100 hover:border-purple-200 hover:bg-gray-50'
                                        }`}
                                >
                                    {opt}
                                </button>
                            ))}
                        </div>
                    </div>
                );

            case "SHAPE_COUNT":
                return (
                    <div className="space-y-4 text-center">
                        <p className="font-medium text-lg text-gray-800">{game.question}</p>
                        <div className="flex justify-center">
                            {/* Use placeholder if image path starts with / but not found, or use generated asset */}
                            <img src={game.image || "/shapes_triangle_1.png"} alt="Shape Puzzle" className="rounded-xl border-2 border-gray-100 max-h-60 object-contain" />
                        </div>
                        <input
                            type="number"
                            value={textInput}
                            onChange={(e) => setTextInput(e.target.value)}
                            placeholder="Enter number..."
                            className="w-full p-3 text-center text-xl font-bold border-2 border-gray-200 rounded-xl focus:border-primary focus:ring-0 outline-none"
                        />
                    </div>
                );

            case "WORD_SCRAMBLE":
                return (
                    <div className="space-y-6 text-center">
                        <p className="text-gray-600">Unscramble the letters to find the word:</p>
                        <div className="p-6 bg-gray-800 rounded-xl text-white font-mono text-3xl tracking-widest shadow-inner">
                            {game.scrambled}
                        </div>
                        <input
                            type="text"
                            value={textInput}
                            onChange={(e) => setTextInput(e.target.value)}
                            placeholder="Type the word..."
                            className="w-full p-3 text-center text-xl font-bold border-2 border-gray-200 rounded-xl focus:border-primary focus:ring-0 outline-none uppercase"
                        />
                    </div>
                );

            case "SENTENCE_BUILDER":
                return (
                    <div className="space-y-6">
                        <p className="font-medium text-gray-800">{game.question}</p>

                        {/* Built Sentence Area */}
                        <div className="min-h-[60px] p-4 bg-gray-50 rounded-xl border-2 border-dashed border-gray-300 flex flex-wrap gap-2 items-center">
                            {sentenceWords.length === 0 && <span className="text-gray-400 italic">Click words below to build sentence...</span>}
                            {sentenceWords.map((word, idx) => (
                                <button
                                    key={idx}
                                    onClick={() => setSentenceWords(prev => prev.filter((_, i) => i !== idx))}
                                    className="px-3 py-1 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-red-50 hover:border-red-200 hover:text-red-500 transition-colors"
                                >
                                    {word}
                                </button>
                            ))}
                        </div>

                        {/* Available Words */}
                        <div className="flex flex-wrap gap-2">
                            {game.words.map((word, idx) => (
                                <button
                                    key={idx}
                                    onClick={() => setSentenceWords(prev => [...prev, word])}
                                    className="px-3 py-2 bg-blue-50 text-blue-700 rounded-lg font-medium hover:bg-blue-100 transition-colors"
                                >
                                    {word}
                                </button>
                            ))}
                        </div>
                    </div>
                );

            default:
                return <div>Unknown Game Type</div>;
        }
    };

    if (loading) return (
        <div className="h-full flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
    );

    if (error) return (
        <div className="h-full flex flex-col items-center justify-center text-red-500 p-4 text-center">
            <AlertCircle size={32} className="mb-2" />
            <p>{error}</p>
            <button onClick={fetchGame} className="mt-4 text-sm text-primary hover:underline">Try Again</button>
        </div>
    );

    // Manual Start Screen
    if (!gameStarted && !gameData?.played) {
        return (
            <div className="h-full flex flex-col items-center justify-center p-6 text-center space-y-6">
                <div className="relative">
                    <div className="absolute inset-0 bg-primary/20 rounded-full blur-xl animate-pulse"></div>
                    <Trophy size={80} className="text-primary relative z-10" />
                </div>

                <div className="space-y-2">
                    <h3 className="text-2xl font-bold text-gray-900">Ready for a Challenge?</h3>
                    <p className="text-gray-500 max-w-xs mx-auto">
                        Test your knowledge and earn badges! You have 2 minutes to solve the puzzle.
                    </p>
                </div>

                <button
                    onClick={() => setGameStarted(true)}
                    className="px-8 py-3 bg-gradient-to-r from-primary to-secondary text-white rounded-xl font-bold text-lg shadow-lg shadow-primary/30 hover:shadow-xl hover:scale-105 transition-all flex items-center gap-2"
                >
                    <Puzzle size={20} />
                    Let's Play
                </button>
            </div>
        );
    }

    if (gameData?.played) {
        return (
            <div className="h-full flex flex-col items-center justify-center p-6 text-center">
                <div className="mb-6 relative">
                    <div className="absolute inset-0 bg-primary/20 rounded-full blur-xl animate-pulse"></div>
                    <Clock size={64} className="text-primary relative z-10" />
                </div>
                <h3 className="text-2xl font-bold text-gray-800 mb-2">Next Challenge In</h3>
                <div className="text-4xl font-mono font-bold text-primary mb-6">
                    {formatTime(timeLeft)}
                </div>
                <p className="text-gray-500 max-w-xs mb-4">
                    You've completed this window's challenge.
                </p>
                {result && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className={`p-4 rounded-xl border flex items-center gap-4 ${result.correct ? 'bg-yellow-50 border-yellow-200' : 'bg-blue-50 border-blue-200'}`}
                    >
                        {result.correct ? (
                            <img
                                src={result.reward === "Gold" ? "/gold_star_badge_1764317379368.png" :
                                    result.reward === "Silver" ? "/silver_star_badge_1764317396021.png" :
                                        "/bronze_star_badge_1764317418251.png"}
                                alt="Badge"
                                className="w-16 h-16 object-contain drop-shadow-md"
                            />
                        ) : (
                            <div className="text-4xl">🙂</div>
                        )}
                        <div className="text-left">
                            <p className="font-bold text-gray-800 text-lg">{result.correct ? "Awesome!" : "Keep Going!"}</p>
                            <p className="text-sm text-gray-600">
                                {result.correct
                                    ? `You earned a ${result.reward} TutorMate Graduate Badge!`
                                    : `Don't worry! Correct answer: ${result.correct_answer}`}
                            </p>
                        </div>
                    </motion.div>
                )}
            </div>
        );
    }

    const { game } = gameData;

    return (
        <div className="h-full flex flex-col">
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                    <div className="p-2 bg-yellow-100 rounded-lg text-yellow-600">
                        <Trophy size={20} />
                    </div>
                    <div>
                        <h3 className="font-bold text-gray-900">Daily Challenge</h3>
                        <p className="text-xs text-gray-500">{game.type.replace('_', ' ')}</p>
                    </div>
                </div>
                <div className="flex items-center gap-2 bg-gray-100 px-3 py-1 rounded-full">
                    <Clock size={14} className="text-gray-500" />
                    <span className={`font-mono font-bold ${timeLeft < 10 ? 'text-red-500' : 'text-gray-700'}`}>
                        {formatTime(timeLeft)}
                    </span>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto pr-2">
                {renderGameContent()}
            </div>

            <div className="mt-4 pt-4 border-t border-gray-100">
                <button
                    onClick={handleSubmit}
                    disabled={submitting}
                    className="w-full py-3 bg-gradient-to-r from-primary to-secondary text-white rounded-xl font-bold shadow-lg shadow-primary/30 hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                    {submitting ? (
                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    ) : (
                        <>
                            <span>Submit Answer</span>
                            <Award size={18} />
                        </>
                    )}
                </button>
            </div>
        </div>
    );
};

export default Game;
