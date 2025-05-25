import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { CheckCircle, AlertCircle, Brain, Code, Target, TreePine, BarChart3 } from 'lucide-react';

interface AnalysisResult {
  status: string;
  tokens: string[];
  ast_tree: string;
  features: {
    function_count: number;
    variable_count: number;
    binop_count: number;
    avg_param_count: number;
    function_call_count: number;
  };
  score: number;
  debug_info?: string | null;
}

interface AnalysisResultsProps {
  result: AnalysisResult;
  scoreColor: string;
}

export const AnalysisResults: React.FC<AnalysisResultsProps> = ({ result, scoreColor }) => {
  const getScoreLabel = (score: number) => {
    if (score >= 90) return { label: 'Excellent', icon: CheckCircle, color: 'text-green-400' };
    if (score >= 70) return { label: 'Good', icon: CheckCircle, color: 'text-yellow-400' };
    return { label: 'Needs Improvement', icon: AlertCircle, color: 'text-red-400' };
  };

  const scoreInfo = getScoreLabel(result.score);
  const ScoreIcon = scoreInfo.icon;

  return (
    <Card className="bg-black/40 backdrop-blur-md border-white/10">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-white flex items-center">
            <Brain className="h-5 w-5 mr-2 text-purple-400" />
            Analysis Results
          </CardTitle>
          <div className="flex items-center space-x-3">
            <Badge variant="outline" className={`${scoreInfo.color} border-current`}>
              <ScoreIcon className="h-4 w-4 mr-1" />
              {scoreInfo.label}
            </Badge>
            <div className="text-right">
              <div className="text-2xl font-bold text-white">{result.score}/100</div>
              <Progress value={result.score} className="w-20 h-2" />
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="tokens" className="w-full">
          <TabsList className="grid w-full grid-cols-4 bg-gray-800/50">
            <TabsTrigger 
              value="tokens" 
              className="data-[state=active]:bg-purple-600 data-[state=active]:text-white"
            >
              <Code className="h-4 w-4 mr-2" />
              Tokens
            </TabsTrigger>
            <TabsTrigger 
              value="ast"
              className="data-[state=active]:bg-purple-600 data-[state=active]:text-white"
            >
              <TreePine className="h-4 w-4 mr-2" />
              AST
            </TabsTrigger>
            <TabsTrigger 
              value="features"
              className="data-[state=active]:bg-purple-600 data-[state=active]:text-white"
            >
              <BarChart3 className="h-4 w-4 mr-2" />
              Features
            </TabsTrigger>
            <TabsTrigger 
              value="summary"
              className="data-[state=active]:bg-purple-600 data-[state=active]:text-white"
            >
              <Target className="h-4 w-4 mr-2" />
              Summary
            </TabsTrigger>
          </TabsList>
          
          <TabsContent value="tokens" className="mt-4">
            <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700">
              <h4 className="text-purple-300 font-semibold mb-3 flex items-center">
                <Code className="h-4 w-4 mr-2" />
                Lexical Tokens ({result.tokens.length})
              </h4>
              <div className="space-y-2">
                {result.tokens.map((token, index) => (
                  <div key={index} className="bg-gray-800/50 rounded px-3 py-2 border border-gray-600">
                    <code className="text-green-300 text-sm font-mono">{token}</code>
                  </div>
                ))}
              </div>
            </div>
          </TabsContent>
          
          <TabsContent value="ast" className="mt-4">
            <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700">
              <h4 className="text-green-300 font-semibold mb-3 flex items-center">
                <TreePine className="h-4 w-4 mr-2" />
                Abstract Syntax Tree
              </h4>
              <pre className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap font-mono bg-gray-800/50 p-3 rounded border border-gray-600 overflow-x-auto">
                {result.ast_tree}
              </pre>
            </div>
          </TabsContent>
          
          <TabsContent value="features" className="mt-4">
            <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700">
              <h4 className="text-blue-300 font-semibold mb-3 flex items-center">
                <BarChart3 className="h-4 w-4 mr-2" />
                Code Features Analysis
              </h4>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-800/50 rounded p-3 border border-gray-600">
                  <div className="text-gray-400 text-xs uppercase tracking-wide mb-1">Functions</div>
                  <div className="text-white text-lg font-semibold">{result.features.function_count}</div>
                </div>
                <div className="bg-gray-800/50 rounded p-3 border border-gray-600">
                  <div className="text-gray-400 text-xs uppercase tracking-wide mb-1">Variables</div>
                  <div className="text-white text-lg font-semibold">{result.features.variable_count}</div>
                </div>
                <div className="bg-gray-800/50 rounded p-3 border border-gray-600">
                  <div className="text-gray-400 text-xs uppercase tracking-wide mb-1">Binary Operations</div>
                  <div className="text-white text-lg font-semibold">{result.features.binop_count}</div>
                </div>
                <div className="bg-gray-800/50 rounded p-3 border border-gray-600">
                  <div className="text-gray-400 text-xs uppercase tracking-wide mb-1">Function Calls</div>
                  <div className="text-white text-lg font-semibold">{result.features.function_call_count}</div>
                </div>
                <div className="bg-gray-800/50 rounded p-3 border border-gray-600 col-span-2">
                  <div className="text-gray-400 text-xs uppercase tracking-wide mb-1">Avg Parameters</div>
                  <div className="text-white text-lg font-semibold">{result.features.avg_param_count.toFixed(1)}</div>
                </div>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="summary" className="mt-4">
            <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700">
              <h4 className="text-orange-300 font-semibold mb-3 flex items-center">
                <Target className="h-4 w-4 mr-2" />
                Analysis Summary
              </h4>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Status:</span>
                  <Badge variant={result.status === 'success' ? 'default' : 'destructive'}>
                    {result.status}
                  </Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Overall Score:</span>
                  <span className="text-white font-semibold">{result.score}/100</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Total Tokens:</span>
                  <span className="text-white font-semibold">{result.tokens.length}</span>
                </div>
                {result.debug_info && (
                  <div className="mt-3 p-3 bg-gray-800/50 rounded border border-gray-600">
                    <div className="text-gray-400 text-xs uppercase tracking-wide mb-1">Debug Info</div>
                    <div className="text-gray-300 text-sm">{result.debug_info}</div>
                  </div>
                )}
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
};
