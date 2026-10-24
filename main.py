import os
import sys


def show_menu():
    print("\n" + "=" * 50)
    print(" 🎓 CAMPUS PLACEMENT ANALYTICS HUB")
    print("=" * 50)
    print(" [1] Initialize Database & Generate Mock Records")
    print(" [2] Compute Analytics Pipelines & Launch Charts")
    print(" [3] Export Analytical Data Sheets to Excel (.xlsx)")
    print(" [4] Exit System Application")
    print("=" * 50)


def main():
    while True:
        show_menu()
        choice = input("👉 Select an operation handler (1-4): ").strip()

        if choice == '1':
            print("\n⚙️ Invoking data generation framework pipeline...")
            if os.path.exists('setup_data.py'):
                os.system(f'"{sys.executable}" setup_data.py')
            else:
                print("❌ Error: 'setup_data.py' module missing from folder workspace.")

        elif choice == '2':
            print("\n⚙️ Invoking statistical aggregation engines & plotting charts...")
            if os.path.exists('analyze_placements.py'):
                os.system(f'"{sys.executable}" analyze_placements.py')
            else:
                print("❌ Error: 'analyze_placements.py' module missing from folder workspace.")

        elif choice == '3':
            print("\n⚙️ Exporting cross-tabulated outputs to data sheets...")
            if os.path.exists('export_to_excel.py'):
                os.system(f'"{sys.executable}" export_to_excel.py')
            else:
                print("❌ Error: 'export_to_excel.py' module missing from folder workspace.")

        elif choice == '4':
            print("\n👋 System framework operations terminated safely. Goodbye!")
            break
        else:
            print("\n⚠️ Invalid selection option! Please provide an integer between 1 and 4.")


if __name__ == "__main__":
    main()
