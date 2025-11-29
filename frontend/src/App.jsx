import React, { useState, useEffect } from 'react';
import { BookOpen, LayoutDashboard, LogOut, GraduationCap, MessageSquare, Menu, X } from 'lucide-react';
import Dashboard from './components/Dashboard';
import SubjectSelector from './components/SubjectSelector';
import ChatInterface from './components/ChatInterface';
import AnalysisView from './components/AnalysisView';
import Login from './components/Login';
import Register from './components/Register';
import ProfileModal from './components/ProfileModal';

const App = () => {
  const [user, setUser] = useState(null);
  const [view, setView] = useState('login'); // login, register, dashboard, select-subject, select-difficulty, chat, analysis
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [selectedDifficulty, setSelectedDifficulty] = useState(null);
  const [sessionData, setSessionData] = useState(null);
  const [showProfile, setShowProfile] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Check for stored user on load
  useEffect(() => {
    const storedUser = localStorage.getItem('tutorMateUser');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
      setView('dashboard');
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('tutorMateUser', JSON.stringify(userData));
    setView('dashboard');
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('tutorMateUser');
    setView('login');
    setSelectedSubject(null);
    setSelectedDifficulty(null);
    setSessionData(null);
    setSidebarOpen(false);
  };

  const handleSubjectSelect = (subject) => {
    setSelectedSubject(subject);
    setView('select-difficulty');
    setSidebarOpen(false);
  };

  const handleDifficultySelect = (difficulty) => {
    setSelectedDifficulty(difficulty);
    setView('chat');
    setSidebarOpen(false);
  };

  const handleChatComplete = (data) => {
    setSessionData(data);
    setView('analysis');
  };

  const handleViewChange = (newView) => {
    setView(newView);
    setSidebarOpen(false);
  };

  // Auth Views
  if (!user) {
    if (view === 'register') {
      return <Register onRegister={handleLogin} onSwitchToLogin={() => setView('login')} />;
    }
    return <Login onLogin={handleLogin} onSwitchToRegister={() => setView('register')} />;
  }

  // Main App Layout
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col md:flex-row">
      {/* Mobile Header */}
      <div className="md:hidden bg-white border-b border-gray-200 p-4 flex items-center justify-between sticky top-0 z-30">
        <div className="flex items-center gap-2 text-primary font-bold text-xl">
          <GraduationCap size={24} />
          <span>TutorMate</span>
        </div>
        <button
          onClick={() => setSidebarOpen(true)}
          className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg"
        >
          <Menu size={24} />
        </button>
      </div>

      {/* Mobile Overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 flex flex-col
        transform transition-transform duration-300 ease-in-out
        md:relative md:translate-x-0
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="p-6 border-b border-gray-100 flex items-center justify-between">
          <div className="flex items-center gap-2 text-primary font-bold text-xl">
            <GraduationCap size={28} />
            <span>TutorMate</span>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="md:hidden p-1 text-gray-400 hover:text-gray-600"
          >
            <X size={24} />
          </button>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          <button
            onClick={() => handleViewChange('dashboard')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${view === 'dashboard' ? 'bg-primary text-white shadow-lg shadow-primary/30' : 'text-gray-600 hover:bg-gray-50'}`}
          >
            <LayoutDashboard size={20} />
            <span className="font-medium">Dashboard</span>
          </button>

          <button
            onClick={() => handleViewChange('select-subject')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${['select-subject', 'select-difficulty', 'chat', 'analysis'].includes(view) ? 'bg-primary text-white shadow-lg shadow-primary/30' : 'text-gray-600 hover:bg-gray-50'}`}
          >
            <MessageSquare size={20} />
            <span className="font-medium">Tutor Chat</span>
          </button>
        </nav>

        <div className="p-4 border-t border-gray-100">
          <button
            onClick={() => setShowProfile(true)}
            className="w-full flex items-center gap-3 px-4 py-3 mb-2 hover:bg-gray-50 rounded-xl transition-colors text-left"
          >
            <div className="w-10 h-10 rounded-full bg-gradient-to-r from-primary to-secondary flex items-center justify-center text-white font-bold shrink-0">
              {user.name[0].toUpperCase()}
            </div>
            <div className="overflow-hidden">
              <p className="font-medium text-gray-900 truncate">{user.name}</p>
              <p className="text-xs text-gray-500 truncate">{user.email}</p>
            </div>
          </button>
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-2 px-4 py-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors text-sm font-medium"
          >
            <LogOut size={18} />
            <span>Sign Out</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-4 md:p-8 overflow-y-auto h-[calc(100vh-64px)] md:h-screen relative">
        {view === 'dashboard' && <Dashboard user={user} onStartChat={() => handleViewChange('select-subject')} />}
        {view === 'select-subject' && <SubjectSelector onSelect={handleSubjectSelect} />}
        {view === 'select-difficulty' && (
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Select Difficulty Level</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {['Beginner', 'Intermediate', 'Advanced'].map((level) => (
                <button
                  key={level}
                  onClick={() => handleDifficultySelect(level.toLowerCase())}
                  className="p-8 rounded-2xl bg-white border-2 border-transparent hover:border-primary shadow-lg hover:shadow-xl transition-all group text-center"
                >
                  <div className={`w-16 h-16 mx-auto rounded-full flex items-center justify-center mb-4 ${level === 'Beginner' ? 'bg-green-100 text-green-600' :
                    level === 'Intermediate' ? 'bg-blue-100 text-blue-600' :
                      'bg-purple-100 text-purple-600'
                    }`}>
                    <span className="text-2xl font-bold">{level[0]}</span>
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">{level}</h3>
                  <p className="text-gray-500 text-sm">
                    {level === 'Beginner' ? 'Start with the basics' :
                      level === 'Intermediate' ? 'Challenge your understanding' :
                        'Master complex concepts'}
                  </p>
                </button>
              ))}
            </div>
            <button onClick={() => handleViewChange('select-subject')} className="mt-8 text-gray-500 hover:text-gray-900 flex items-center justify-center gap-2 mx-auto">
              ← Back to Subjects
            </button>
          </div>
        )}
        {view === 'chat' && (
          <ChatInterface
            subject={selectedSubject}
            difficulty={selectedDifficulty}
            gradeLevel={user.grade_level || "College Year 1"}
            onComplete={handleChatComplete}
          />
        )}
        {view === 'analysis' && <AnalysisView sessionData={sessionData} user={user} onRestart={() => handleViewChange('select-subject')} onBackToDashboard={() => handleViewChange('dashboard')} />}

        {/* Profile Modal */}
        {showProfile && <ProfileModal user={user} onClose={() => setShowProfile(false)} />}
      </main>
    </div>
  );
};

export default App;
