import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { CheckCircle, AlertCircle, Brain, Code, Target } from 'lucide-react';

interface AnalysisResult {
  lexicalAnalysis: string;
  syntaxAnalysis: string;
  semanticAnalysis: string;
  score: number;
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
        <Tabs defaultValue="lexical" className="w-full">
          <TabsList className="grid w-full grid-cols-3 bg-gray-800/50">
            <TabsTrigger 
              value="lexical" 
              className="data-[state=active]:bg-purple-600 data-[state=active]:text-white"
            >
              <Code className="h-4 w-4 mr-2" />
              Lexical
            </TabsTrigger>
            <TabsTrigger 
              value="syntax"
              className="data-[state=active]:bg-purple-600 data-[state=active]:text-white"
            >
              <CheckCircle className="h-4 w-4 mr-2" />
              Syntax
            </TabsTrigger>
            <TabsTrigger 
              value="semantic"
              className="data-[state=active]:bg-purple-600 data-[state=active]:text-white"
            >
              <Target className="h-4 w-4 mr-2" />
              Semantic
            </TabsTrigger>
          </TabsList>
          
          <TabsContent value="lexical" className="mt-4">
            <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700">
              <h4 className="text-purple-300 font-semibold mb-2 flex items-center">
                <Code className="h-4 w-4 mr-2" />
                Lexical Analysis
              </h4>
              <p className="text-gray-300 text-sm leading-relaxed">
                {result.lexicalAnalysis}
              </p>
            </div>
          </TabsContent>
          
          <TabsContent value="syntax" className="mt-4">
            <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700">
              <h4 className="text-green-300 font-semibold mb-2 flex items-center">
                <CheckCircle className="h-4 w-4 mr-2" />
                Syntax Analysis
              </h4>
              <p className="text-gray-300 text-sm leading-relaxed">
                {result.syntaxAnalysis}
              </p>
            </div>
          </TabsContent>
          
          <TabsContent value="semantic" className="mt-4">
            <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700">
              <h4 className="text-blue-300 font-semibold mb-2 flex items-center">
                <Target className="h-4 w-4 mr-2" />
                Semantic Analysis
              </h4>
              <p className="text-gray-300 text-sm leading-relaxed">
                {result.semanticAnalysis}
              </p>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
};
