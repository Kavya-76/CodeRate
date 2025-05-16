from src.model import CodeScoringModel

def main():
    scorer = CodeScoringModel()
    scorer.train_from_csv("data/code_samples.csv")

    while True:
        print("\nPaste your Python code (type 'exit' to quit):")
        code_lines = []
        while True:
            line = input()
            if line.lower() == 'exit':
                return
            if line == '':
                break
            code_lines.append(line)

        code_input = "\n".join(code_lines)
        score = scorer.predict_score(code_input)
        print(f"\nPredicted Score: {score}/100")

if __name__ == '__main__':
    main()