import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Command, 
  ArrowRight, 
  Sparkles, 
  Zap, 
  FileText, 
  Menu, 
  X, 
  CheckCircle, 
  Upload, 
  Wand2 
} from 'lucide-react';
import { useUser, useClerk } from '@clerk/clerk-react';

export default function LandingPage() {
  const navigate = useNavigate();
  const { isSignedIn, isLoaded } = useUser();
  const { openSignIn } = useClerk();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  // Redirect to dashboard if already signed in
  useEffect(() => {
    if (isLoaded && isSignedIn) {
      navigate('/dashboard');
    }
  }, [isLoaded, isSignedIn, navigate]);

  const handleGetStarted = () => {
    navigate('/dashboard');
  };

  const handleSignIn = () => {
    if (isSignedIn) {
      navigate('/dashboard');
    } else {
      openSignIn();
    }
  };

  // Prevent flash of content while checking auth status
  if (isSignedIn) return null; 

  return (
    <div className="min-h-screen bg-white font-sans text-slate-900 selection:bg-indigo-100 selection:text-indigo-900 overflow-x-hidden">
      
      {/* --- NAVIGATION --- */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-xl z-50 border-b border-slate-100/50">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3 cursor-pointer group" onClick={() => navigate('/')}>
            <div className="w-9 h-9 bg-slate-900 rounded-xl flex items-center justify-center text-white shadow-lg group-hover:scale-105 transition-transform duration-300">
              <Command size={18} />
            </div>
            <span className="font-bold text-xl tracking-tight text-slate-900">Merit</span>
          </div>

          <div className="hidden md:flex items-center gap-8">
            <button onClick={() => document.getElementById('how-it-works').scrollIntoView({behavior:'smooth'})} className="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">How it Works</button>
            <button onClick={() => document.getElementById('features').scrollIntoView({behavior:'smooth'})} className="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">Features</button>
            <div className="h-4 w-px bg-slate-200"></div>
            <button 
              onClick={handleSignIn} 
              className="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors"
            >
              Sign in
            </button>
            <button 
              onClick={handleGetStarted}
              className="px-5 py-2.5 bg-slate-900 hover:bg-black text-white text-sm font-medium rounded-xl transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5 active:translate-y-0"
            >
              Get Started
            </button>
          </div>

           <button className="md:hidden text-slate-600 p-2" onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
            {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

         {isMobileMenuOpen && (
          <div className="md:hidden absolute top-20 left-0 w-full bg-white border-b border-slate-100 p-6 flex flex-col gap-4 shadow-2xl animate-in slide-in-from-top-2 z-40">
            <button onClick={handleSignIn} className="text-left text-lg font-medium text-slate-600">
              Sign in
            </button>
            <button onClick={handleGetStarted} className="w-full py-3 bg-slate-900 text-white rounded-xl font-bold shadow-lg">Get Started</button>
          </div>
        )}
      </nav>

      <main>
        {/* --- HERO SECTION --- */}
        {/* Adjusted padding-top from pt-32/lg:pt-48 to pt-24/lg:pt-36 to reduce top margin */}
        <section className="relative pt-24 pb-20 lg:pt-36 lg:pb-32 overflow-hidden">
            {/* Background Gradients */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full z-0 pointer-events-none">
                <div className="absolute top-20 left-0 lg:left-1/4 w-[500px] h-[500px] bg-blue-100/40 rounded-full blur-[100px] animate-pulse-slow" />
                <div className="absolute top-40 right-0 lg:right-1/4 w-[400px] h-[400px] bg-indigo-100/40 rounded-full blur-[100px] animate-pulse-slow delay-1000" />
            </div>

            <div className="relative z-10 max-w-7xl mx-auto px-6 grid lg:grid-cols-2 gap-16 items-center">
                
                {/* Text Content */}
                <div className="text-center lg:text-left max-w-2xl mx-auto lg:mx-0">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-bold uppercase tracking-wide mb-8 shadow-sm animate-in fade-in slide-in-from-bottom-4 duration-700">
                        <span className="relative flex h-2 w-2">
                          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                          <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                        </span>
                        Launch Special: Free for first 100 users • No Credit Card Required
                    </div>

                    <h1 className="text-5xl lg:text-7xl font-bold tracking-tight text-slate-900 mb-6 leading-[1.1] animate-in fade-in slide-in-from-bottom-6 duration-700 delay-100">
                        Resume building, <br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600">reimagined by AI.</span>
                    </h1>

                    <p className="text-lg text-slate-600 mb-10 leading-relaxed animate-in fade-in slide-in-from-bottom-6 duration-700 delay-200">
                        Don't just format—<strong>upgrade</strong>. Upload your existing resume, and our AI will rewrite your bullets, optimize keywords for ATS, and format it perfectly in seconds.
                    </p>

                    <div className="flex flex-col sm:flex-row items-center gap-4 justify-center lg:justify-start animate-in fade-in slide-in-from-bottom-6 duration-700 delay-300">
                        <button 
                            onClick={handleGetStarted}
                            className="h-14 px-8 bg-slate-900 hover:bg-black text-white text-base font-bold rounded-2xl shadow-xl shadow-slate-900/20 transition-all hover:-translate-y-1 active:translate-y-0 flex items-center gap-2 w-full sm:w-auto justify-center"
                        >
                            Build My Resume <ArrowRight size={18} />
                        </button>
                    </div>
                </div>

                {/* Hero Visual: The Transformation */}
                <div className="relative h-[500px] lg:h-[600px] w-full flex items-center justify-center perspective-1000 animate-in fade-in zoom-in duration-1000 delay-300 hidden lg:flex">
                    
                    {/* Background Decorative Rings */}
                    <div className="absolute w-[500px] h-[500px] border border-slate-100 rounded-full animate-[spin_60s_linear_infinite]" />
                    <div className="absolute w-[350px] h-[350px] border border-slate-200/60 rounded-full animate-[spin_40s_linear_infinite_reverse]" />

                    {/* The "Old" Resume (Behind) */}
                    <div className="absolute w-80 h-[440px] bg-slate-50 rounded-xl border border-slate-200 rotate-[-6deg] translate-x-[-40px] translate-y-4 scale-95 opacity-60 z-0"></div>

                    {/* The "New" Resume (Front) */}
                    <div className="relative w-80 h-[440px] bg-white rounded-xl shadow-2xl border border-slate-100 rotate-[6deg] z-10 hover:rotate-0 transition-all duration-700 ease-out group cursor-default">
                         {/* Header */}
                         <div className="h-24 bg-slate-50 border-b border-slate-100 p-6 flex flex-col justify-center gap-2">
                            <div className="w-1/2 h-4 bg-slate-900 rounded-md"></div>
                            <div className="w-1/3 h-2 bg-slate-300 rounded-md"></div>
                         </div>
                         {/* Body */}
                         <div className="p-6 space-y-6">
                            <div className="space-y-2">
                                <div className="w-1/4 h-3 bg-blue-100 rounded-md"></div>
                                <div className="w-full h-2 bg-slate-100 rounded-md"></div>
                                <div className="w-5/6 h-2 bg-slate-100 rounded-md"></div>
                            </div>
                            <div className="space-y-2">
                                <div className="w-1/4 h-3 bg-blue-100 rounded-md"></div>
                                <div className="w-full h-2 bg-slate-100 rounded-md"></div>
                                <div className="w-11/12 h-2 bg-slate-100 rounded-md"></div>
                                <div className="w-4/5 h-2 bg-slate-100 rounded-md"></div>
                            </div>
                         </div>

                         {/* Floating Badges */}
                         <div className="absolute -right-12 top-20 bg-white p-3 rounded-xl shadow-xl border border-slate-100 flex items-center gap-3 animate-bounce-slow">
                            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center text-green-600">
                                <CheckCircle size={20} />
                            </div>
                            <div>
                                <div className="text-xs text-slate-500 font-medium">ATS Score</div>
                                <div className="text-sm font-bold text-slate-900">98/100</div>
                            </div>
                         </div>

                         <div className="absolute -left-12 bottom-32 bg-white p-3 rounded-xl shadow-xl border border-slate-100 flex items-center gap-3 animate-bounce-slow delay-700">
                            <div className="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center text-indigo-600">
                                <Sparkles size={20} />
                            </div>
                            <div>
                                <div className="text-xs text-slate-500 font-medium">AI Status</div>
                                <div className="text-sm font-bold text-slate-900">Optimized</div>
                            </div>
                         </div>
                    </div>
                </div>
            </div>
        </section>

        {/* --- HOW IT WORKS (Visual Steps) --- */}
        <section id="how-it-works" className="py-24 bg-slate-50/80 border-y border-slate-200">
            <div className="max-w-6xl mx-auto px-6">
                <div className="text-center max-w-2xl mx-auto mb-16">
                    <h2 className="text-3xl font-bold text-slate-900 mb-4 tracking-tight">From cluttered doc to hired.</h2>
                    <p className="text-lg text-slate-500">Stop wrestling with margins in Word. Our three-step intelligent process handles the heavy lifting for you.</p>
                </div>
                
                <div className="grid md:grid-cols-3 gap-8">
                     {/* Step 1 */}
                     <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 relative overflow-hidden group hover:shadow-xl hover:shadow-blue-900/5 transition-all duration-300">
                        <div className="absolute top-0 right-0 p-6 opacity-5 font-black text-8xl text-slate-900 select-none">-1-</div>
                        <div className="w-14 h-14 bg-blue-50 rounded-2xl flex items-center justify-center text-blue-600 mb-6 group-hover:scale-110 transition-transform duration-300">
                            <Upload size={28} />
                        </div>
                        <h3 className="text-xl font-bold text-slate-900 mb-3">Upload</h3>
                        <p className="text-slate-500 leading-relaxed">Drop your old PDF. We extract your history instantly so you don't have to retype a thing.</p>
                     </div>

                     {/* Step 2 */}
                     <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 relative overflow-hidden group hover:shadow-xl hover:shadow-indigo-900/5 transition-all duration-300">
                        <div className="absolute top-0 right-0 p-6 opacity-5 font-black text-8xl text-slate-900 select-none">-2-</div>
                        <div className="w-14 h-14 bg-indigo-50 rounded-2xl flex items-center justify-center text-indigo-600 mb-6 group-hover:scale-110 transition-transform duration-300">
                            <Wand2 size={28} />
                        </div>
                        <h3 className="text-xl font-bold text-slate-900 mb-3">Enhance</h3>
                        <p className="text-slate-500 leading-relaxed">Our AI chats with you to rewrite boring bullet points into powerful, results-driven achievements.</p>
                     </div>

                     {/* Step 3 */}
                     <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 relative overflow-hidden group hover:shadow-xl hover:shadow-emerald-900/5 transition-all duration-300">
                        <div className="absolute top-0 right-0 p-6 opacity-5 font-black text-8xl text-slate-900 select-none">-3-</div>
                        <div className="w-14 h-14 bg-emerald-50 rounded-2xl flex items-center justify-center text-emerald-600 mb-6 group-hover:scale-110 transition-transform duration-300">
                            <FileText size={28} />
                        </div>
                        <h3 className="text-xl font-bold text-slate-900 mb-3">Export</h3>
                        <p className="text-slate-500 leading-relaxed">Download a polished, ATS-optimized PDF that looks perfect on every device and passes every bot.</p>
                     </div>
                </div>
            </div>
        </section>

        {/* --- FEATURES GRID --- */}
        <section id="features" className="py-24 bg-white">
            <div className="max-w-6xl mx-auto px-6 grid md:grid-cols-2 gap-16 items-center">
                <div>
                    <h2 className="text-3xl font-bold text-slate-900 mb-6">Why top candidates switch to Merit</h2>
                    <div className="space-y-8">
                        <div className="flex gap-4">
                            <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center text-blue-600 shrink-0">
                                <Zap size={24} />
                            </div>
                            <div>
                                <h3 className="text-lg font-bold text-slate-900 mb-1">Beat the ATS</h3>
                                <p className="text-slate-500">75% of resumes are rejected by bots. Ours are designed to pass.</p>
                            </div>
                        </div>
                        <div className="flex gap-4">
                            <div className="w-12 h-12 bg-indigo-50 rounded-xl flex items-center justify-center text-indigo-600 shrink-0">
                                <Sparkles size={24} />
                            </div>
                            <div>
                                <h3 className="text-lg font-bold text-slate-900 mb-1">Live AI Assistant</h3>
                                <p className="text-slate-500">Like having a professional resume writer sitting next to you.</p>
                            </div>
                        </div>
                        <div className="flex gap-4">
                            <div className="w-12 h-12 bg-purple-50 rounded-xl flex items-center justify-center text-purple-600 shrink-0">
                                <Command size={24} />
                            </div>
                            <div>
                                <h3 className="text-lg font-bold text-slate-900 mb-1">Real-time Preview</h3>
                                <p className="text-slate-500">See your changes instantly. No more guessing how the PDF will look.</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="relative">
                    <div className="absolute inset-0 bg-gradient-to-tr from-blue-500/20 to-purple-500/20 rounded-3xl blur-2xl -z-10" />
                    <div className="bg-slate-900 rounded-3xl p-8 shadow-2xl text-white relative overflow-hidden">
                        <div className="absolute top-0 right-0 p-12 opacity-10">
                            <Command size={120} />
                        </div>
                        <div className="relative z-10">
                            <div className="text-sm font-medium text-blue-300 mb-2">PRO TIP</div>
                            <h3 className="text-2xl font-bold mb-4">"Quantify your impact."</h3>
                            <p className="text-slate-300 leading-relaxed mb-8">
                                Instead of "Managed a team", try "Led a team of 5 engineers to reduce deployment time by 40%."
                            </p>
                            <button onClick={handleGetStarted} className="w-full py-4 bg-white text-slate-900 rounded-xl font-bold hover:bg-blue-50 transition-colors">
                                Try it on your resume
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        {/* --- CALL TO ACTION --- */}
        <section className="py-24 bg-slate-50 border-t border-slate-200">
             <div className="max-w-4xl mx-auto px-6 text-center">
                <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-6 tracking-tight">Ready to stand out?</h2>
                <p className="text-xl text-slate-500 mb-10">Be one of the first 100 users to build your professional resume for free.</p>
                <button 
                  onClick={handleGetStarted}
                  className="px-10 py-5 bg-slate-900 hover:bg-black text-white text-lg font-bold rounded-2xl shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all active:scale-95"
                >
                  Build My Resume for Free
                </button>
             </div>
        </section>
      </main>

      {/* --- FOOTER --- */}
      <footer className="py-12 border-t border-slate-200 bg-white">
        <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-slate-900 rounded-lg flex items-center justify-center text-white">
                    <Command size={14} />
                </div>
                <span className="font-bold text-lg text-slate-900">Merit</span>
            </div>
            <div className="flex gap-8 text-sm text-slate-500">
                <a href="#" className="hover:text-slate-900 transition-colors">Privacy</a>
                <a href="#" className="hover:text-slate-900 transition-colors">Terms</a>
                <a href="#" className="hover:text-slate-900 transition-colors">Twitter</a>
            </div>
            <p className="text-slate-400 text-sm">© {new Date().getFullYear()} Merit AI.</p>
        </div>
      </footer>
    </div>
  );
}