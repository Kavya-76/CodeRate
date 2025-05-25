import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Code } from 'lucide-react';

interface CodeShortcutsProps {
  onCodeInsert: (code: string) => void;
}

export const CodeShortcuts: React.FC<CodeShortcutsProps> = ({ onCodeInsert }) => {
  const shortcuts = [
    {
      category: "Control Flow",
      items: [
        {
          name: "If-Else",
          code: `if condition:
    # code block
    pass
else:
    # else block
    pass`
        },
        {
          name: "For Loop",
          code: `for i in range(10):
    print(i)`
        },
        {
          name: "While Loop",
          code: `while condition:
    # code block
    break`
        }
      ]
    },
    {
      category: "Functions",
      items: [
        {
          name: "Function",
          code: `def function_name(parameter):
    """Function description"""
    return result`
        },
        {
          name: "Class",
          code: `class MyClass:
    def __init__(self, value):
        self.value = value
    
    def method(self):
        return self.value`
        }
      ]
    },
    {
      category: "Data Structures",
      items: [
        {
          name: "List",
          code: `my_list = [1, 2, 3, 4, 5]
for item in my_list:
    print(item)`
        },
        {
          name: "Dictionary",
          code: `my_dict = {
    "key1": "value1",
    "key2": "value2"
}
for key, value in my_dict.items():
    print(f"{key}: {value}")`
        }
      ]
    },
    {
      category: "Common Patterns",
      items: [
        {
          name: "Try-Except",
          code: `try:
    # risky code
    result = risky_operation()
except Exception as e:
    print(f"Error: {e}")
finally:
    # cleanup code
    pass`
        },
        {
          name: "List Comprehension",
          code: `# List comprehension
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers if x % 2 == 0]
print(squares)`
        }
      ]
    }
  ];

  return (
    <Card className="bg-black/40 backdrop-blur-md border-white/10">
      <CardHeader>
        <CardTitle className="text-white flex items-center">
          <Code className="h-5 w-5 mr-2 text-purple-400" />
          Code Shortcuts
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {shortcuts.map((category, categoryIndex) => (
          <div key={categoryIndex}>
            <h4 className="text-sm font-semibold text-purple-300 mb-2">
              {category.category}
            </h4>
            <div className="space-y-2">
              {category.items.map((item, itemIndex) => (
                <Button
                  key={itemIndex}
                  variant="outline"
                  size="sm"
                  onClick={() => onCodeInsert(item.code)}
                  className="w-full justify-start text-left h-auto py-2 bg-gray-800/50 border-gray-600 text-gray-300 hover:bg-gray-700/50 hover:text-white hover:border-purple-400"
                >
                  <div className="text-xs">
                    {item.name}
                  </div>
                </Button>
              ))}
            </div>
            {categoryIndex < shortcuts.length - 1 && (
              <Separator className="mt-4 bg-gray-700" />
            )}
          </div>
        ))}
      </CardContent>
    </Card>
  );
};