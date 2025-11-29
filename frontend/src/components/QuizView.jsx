import React, { useState } from 'react';
import axios from 'axios';
import { Check, X, ArrowRight, Lightbulb } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const QuizView = () => {
    const [step, setStep] = useState('upload'); // upload, diagnosis, practice, results
    const [file, setFile] = useState(null);
    const [diagnosis, setDiagnosis] = useState(null);
    const [practiceSet, setPracticeSet] = useState(null);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [answers, setAnswers] = useState({});
    const [showExplanation, setShowExplanation] = useState(false);
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileUpload = async (e) => {
        const uploadedFile = e.target.files[0];
        setFile(uploadedFile);

        // Simulate upload for demo (in real app, use FormData)
        // For this demo, we'll trigger the diagnosis directly assuming data is already on server
        // or we just call the diagnose endpoint if we had the file content.

        // To make this work with the python backend demo flow, let's just trigger diagnosis
        setLoading(true);
        try {
            // In a real scenario, we'd POST the file here.
            // For the demo, we assume the backend has loaded the sample data via run_demo.py logic or similar.
            // But wait, the API expects file upload. Let's implement a simple file upload.

            const formData = new FormData();
            formData.append('file', uploadedFile);

            // We need to upload quiz and responses. For simplicity in this UI demo, 
            // we'll assume the user is uploading the "responses.json" and the quiz is already there.
            await axios.post('http://localhost:8000/ingest/responses', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            const diagResponse = await axios.post('http://localhost:8000/diagnose');
            setDiagnosis(diagResponse.data);
            setStep('diagnosis');
        } catch (error) {
            console.error("Error uploading:", error);
            alert("Error uploading file. Make sure backend is running and quiz is ingested.");
        } finally {
            setLoading(false);
        }
    };

    const startPractice = async () => {
        setLoading(true);
        try {
            const response = await axios.get('http://localhost:8000/practice');
            setPracticeSet(response.data);
            setStep('practice');
        } catch (error) {
            console.error("Error starting practice:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleAnswerSubmit = () => {
        if (currentQuestionIndex < totalQuestions - 1) {
            setCurrentQuestionIndex(curr => curr + 1);
            setShowExplanation(false);
        } else {
            submitQuiz();
        }
    };

    const submitQuiz = async () => {
        setLoading(true);
        try {
            const response = await axios.post('http://localhost:8000/submit_practice', answers);
            setResults(response.data);
            setStep('results');
        } catch (error) {
            console.error("Error submitting quiz:", error);
        } finally {
            setLoading(false);
        }
    };

    if (step === 'upload') {
        return (
            <div className="max-w-xl mx-auto mt-12 text-center">
                <div className="card border-dashed border-2 border-gray-300 p-12 flex flex-col items-center justify-center hover:border-primary transition-colors cursor-pointer relative">
                    <input
                        type="file"
                        onChange={handleFileUpload}
                        className="absolute inset-0 opacity-0 cursor-pointer"
                        accept=".json"
                    />
                    <div className="bg-indigo-50 p-4 rounded-full text-primary mb-4">
                        <ArrowRight size={32} />
                    </div>
                    <h3 className="text-xl font-semibold mb-2">Upload your Quiz Results</h3>
                    <p className="text-gray-500">Upload your JSON response file to get a personalized diagnosis.</p>
                    {loading && <p className="mt-4 text-primary font-medium">Analyzing...</p>}
                </div>
            </div>
        );
    }

    if (step === 'diagnosis') {
        return (
            <div className="space-y-6">
                <header className="text-center mb-8">
                    <h2 className="text-2xl font-bold">Diagnosis Complete</h2>
                    <p className="text-gray-600">We found a few areas where you can improve.</p>
                </header>

                <div className="grid gap-4">
                    {diagnosis?.weak_concepts?.map((c, i) => (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.1 }}
                            key={i}
                            className="card border-l-4 border-l-accent"
                        >
                            <h3 className="font-bold text-lg">{c.concept}</h3>
                            <p className="text-gray-600 mt-1">{c.reason}</p>
                        </motion.div>
                    ))}
                </div>

                <div className="flex justify-center mt-8">
                    <button onClick={startPractice} className="btn-primary flex items-center gap-2 text-lg px-8 py-3">
                        Start Personalized Practice <ArrowRight size={20} />
                    </button>
                </div>
            </div>
        );
    }

    if (step === 'practice' && practiceSet) {
        // Flatten questions for easier navigation
        const allQuestions = practiceSet.practice_set.flatMap(group =>
            group.questions.map(q => ({ ...q, concept: group.concept }))
        );
        const question = allQuestions[currentQuestionIndex];
        const totalQuestions = allQuestions.length;

        return (
            <div className="max-w-2xl mx-auto">
                <div className="mb-6 flex justify-between items-center">
                    <span className="text-sm font-medium text-gray-500">Question {currentQuestionIndex + 1} of {totalQuestions}</span>
                    <span className="bg-indigo-100 text-primary px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide">
                        {question.concept}
                    </span>
                </div>

                <div className="card min-h-[300px] flex flex-col justify-between">
                    <div>
                        <h3 className="text-xl font-medium leading-relaxed mb-6">{question.question}</h3>

                        <input
                            type="text"
                            placeholder="Type your answer..."
                            className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none text-lg"
                            value={answers[question.question] || ''}
                            onChange={(e) => setAnswers({ ...answers, [question.question]: e.target.value })}
                        />
                    </div>

                    <div className="mt-8 flex justify-between items-center">
                        <button
                            onClick={() => setShowExplanation(!showExplanation)}
                            className="text-gray-500 hover:text-primary flex items-center gap-2 text-sm font-medium"
                        >
                            <Lightbulb size={16} />
                            {showExplanation ? 'Hide Hint' : 'Show Hint'}
                        </button>

                        <button onClick={handleAnswerSubmit} className="btn-primary">
                            {currentQuestionIndex === totalQuestions - 1 ? 'Finish' : 'Next Question'}
                        </button>
                    </div>
                </div>

                <AnimatePresence>
                    {showExplanation && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="mt-4 bg-yellow-50 border border-yellow-200 p-4 rounded-lg text-yellow-800 text-sm"
                        >
                            <strong>Hint:</strong> Try to break down the problem step by step. (Real hint would come from Explanation Agent)
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        );
    }

    if (step === 'results') {
        return (
            <div className="text-center max-w-xl mx-auto mt-12">
                <div className="mb-6 inline-flex p-4 bg-green-100 text-green-600 rounded-full">
                    <Check size={48} />
                </div>
                <h2 className="text-3xl font-bold mb-2">Great Job!</h2>
                <p className="text-gray-600 mb-8">You've completed your practice session.</p>

                <div className="card mb-8">
                    <div className="grid grid-cols-2 gap-4 text-center">
                        <div>
                            <p className="text-gray-500 text-sm">Score</p>
                            <p className="text-3xl font-bold text-primary">{results.score} / {results.total}</p>
                        </div>
                        <div>
                            <p className="text-gray-500 text-sm">Accuracy</p>
                            <p className="text-3xl font-bold text-secondary">{Math.round((results.score / results.total) * 100)}%</p>
                        </div>
                    </div>
                </div>

                <button onClick={() => window.location.reload()} className="btn-secondary">
                    Back to Dashboard
                </button>
            </div>
        );
    }

    return <div>Loading...</div>;
};

export default QuizView;
