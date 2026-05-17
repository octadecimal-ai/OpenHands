#!/usr/bin/env python3
"""
T3.1: Test AppleScript bez TCC
Weryfikacja dostępu do macOS apps przed fazą TCC
"""
import subprocess
import json

def test_apple_script(app_name, script):
    """Wykonaj AppleScript i zwróć wynik"""
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "app": app_name,
            "success": result.returncode == 0,
            "output": result.stdout.strip()[:200] if result.stdout else None,
            "error": result.stderr.strip()[:200] if result.stderr else None
        }
    except Exception as e:
        return {"app": app_name, "success": False, "error": str(e)}

def main():
    print("=" * 60)
    print("T3.1: Test AppleScript - Dostęp do macOS Apps")
    print("=" * 60)
    
    tests = [
        ("Notes", '''tell application "Notes"
            set cnt to count of notes
            return "Notes count: " & cnt
        end tell'''),
        
        ("Reminders", '''tell application "Reminders"
            set lists to name of lists
            return "Lists: " & (item 1 of lists)
        end tell'''),
        
        ("Calendar", '''tell application "Calendar"
            set cnt to count of calendars
            return "Calendars count: " & cnt
        end tell'''),
    ]
    
    results = []
    for app, script in tests:
        print(f"\n🔍 Test: {app}")
        result = test_apple_script(app, script)
        results.append(result)
        
        if result["success"]:
            print(f"   ✅ {result['output']}")
        else:
            print(f"   ❌ {result['error']}")
    
    # Podsumowanie
    print("\n" + "=" * 60)
    print("PODSUMOWANIE")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r["success"])
    print(f"✅ Działające: {success_count}/{len(results)}")
    
    print("\n⚠️  UWAGA:")
    print("   AppleScript działa - oznacza to, że:")
    print("   1. TCC permissions są już nadane dla Terminal")
    print("   2. Lub aplikacje nie wymagają TCC dla tego use-case")
    print("   3. Sprawdź System Settings → Privacy & Security → Automation")
    print("   4. Potwierdź że Terminal ma dostęp do: Notes, Reminders")
    
    return 0 if success_count == len(results) else 1

if __name__ == "__main__":
    exit(main())