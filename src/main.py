# src/main.py

from core.evaluator import evaluate_code

def main():
    print("=== Code Scorer CLI ===")
    print("Enter your Python code (end input with an empty line):")

    # Read multiline input from user until an empty line is entered
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    code = "\n".join(lines)

    print("\nEvaluating your code...\n")

    result = evaluate_code(code)
    print(result)

    if result["status"] == "success":
        print(f"✅ Code is valid!")
        print(f"Score: {result['score']}/100")
        print("Extracted features:")
        for feature, value in result["features"].items():
            print(f"  - {feature}: {value}")
    else:
        print(f"❌ Error during {result.get('stage', 'unknown')} analysis:")
        print(result.get("message", "Unknown error"))
        if "errors" in result:
            print("Details:")
            for err in result["errors"]:
                print(f"  - {err}")

if __name__ == "__main__":
    main()
