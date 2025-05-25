import { useState } from 'react';
import { Button } from './components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { CodeEditor } from '@/components/CodeEditor';
import { CodeShortcuts } from '@/components/CodeShortcuts';
import { AnalysisResults } from '@/components/AnalysisResults';
import { toast } from 'sonner';
import { Code, Play, Sparkles } from 'lucide-react';
import "./App.css"

interface AnalysisResult {
  lexicalAnalysis: string;
  syntaxAnalysis: string;
  semanticAnalysis: string;
  score: number;
}

function App() {
   const [code, setCode] = useState('# Enter your Python code here\nprint("Hello, CodeRate!")');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);

  const handleSubmitCode = async () => {
    if (!code.trim()) {
      toast.error('Please enter some code to analyze');
      return;
    }

    setIsAnalyzing(true);
    
    try {
      // This is where you'll make the API call to your backend
      // For now, I'll simulate the API call with mock data
      await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate API delay
      
      // Mock response - replace with actual API call
      const mockResult: AnalysisResult = {
        lexicalAnalysis: "Tokens identified: keywords (print, def), identifiers (hello_world), literals ('Hello, World!'), operators, delimiters. All tokens are valid Python lexemes.",
        syntaxAnalysis: "Code follows proper Python syntax. Indentation is correct. Function definition syntax is valid. Print statement structure is appropriate.",
        semanticAnalysis: "Function 'hello_world' is properly defined and called. No undefined variables or scope issues detected. Code logic is semantically correct.",
        score: Math.floor(Math.random() * 30) + 70 // Random score between 70-100
      };
      
      setAnalysisResult(mockResult);
      toast.success('Code analysis completed successfully!');
    } catch (error) {
      toast.error('Failed to analyze code. Please try again.');
      console.error('Analysis error:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleCodeInsert = (codeSnippet: string) => {
    setCode(prevCode => prevCode + '\n\n' + codeSnippet);
  };

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'bg-green-500';
    if (score >= 70) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="bg-black/20 backdrop-blur-md border-b border-white/10">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-r from-purple-400 to-pink-400 p-2 rounded-lg">
                <Code className="h-8 w-8 text-white" />
              </div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                CodeRate
              </h1>
            </div>
            <Badge variant="outline" className="text-purple-300 border-purple-400">
              <Sparkles className="h-4 w-4 mr-1" />
              AI-Powered Analysis
            </Badge>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Code Editor Section */}
          <div className="lg:col-span-2 space-y-6">
            <Card className="bg-black/40 backdrop-blur-md border-white/10">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Code className="h-5 w-5 mr-2 text-purple-400" />
                  Python Code Editor
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <CodeEditor value={code} onChange={setCode} />
                <div className="flex justify-between items-center">
                  <div className="text-sm text-gray-400">
                    Lines: {code.split('\n').length} | Characters: {code.length}
                  </div>
                  <Button 
                    onClick={handleSubmitCode}
                    disabled={isAnalyzing}
                    className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                  >
                    {isAnalyzing ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <Play className="h-4 w-4 mr-2" />
                        Analyze Code
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Analysis Results */}
            {analysisResult && (
              <AnalysisResults 
                result={analysisResult} 
                scoreColor={getScoreColor(analysisResult.score)} 
              />
            )}
          </div>

          {/* Code Shortcuts Section */}
          <div className="space-y-6">
            <CodeShortcuts onCodeInsert={handleCodeInsert} />
            
            {/* Tips Card */}
            <Card className="bg-black/40 backdrop-blur-md border-white/10">
              <CardHeader>
                <CardTitle className="text-white text-sm">💡 Tips</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="text-xs text-gray-300 space-y-1">
                  <p>• Use proper indentation (4 spaces)</p>
                  <p>• Add meaningful variable names</p>
                  <p>• Include comments for clarity</p>
                  <p>• Follow PEP 8 style guidelines</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App
