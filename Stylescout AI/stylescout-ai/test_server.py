"""
Test script to verify StyleScout AI MCP server is working correctly
"""
import sys
import subprocess
import json

def test_import():
    """Test if the module can be imported"""
    print("Test 1: Importing module...")
    try:
        import stylescout_ai.server
        print("✅ Module import successful")
        return True
    except ImportError as e:
        print(f"❌ Module import failed: {e}")
        return False

def test_dependencies():
    """Test if required dependencies are installed"""
    print("\nTest 2: Checking dependencies...")
    required = ['mcp', 'httpx']
    
    result = subprocess.run(
        ['pip', 'list', '--format=json'],
        capture_output=True,
        text=True
    )
    
    installed = json.loads(result.stdout)
    installed_names = {pkg['name'].lower() for pkg in installed}
    
    all_ok = True
    for dep in required:
        if dep in installed_names:
            version = next(pkg['version'] for pkg in installed if pkg['name'].lower() == dep)
            print(f"✅ {dep} {version} installed")
        else:
            print(f"❌ {dep} not installed")
            all_ok = False
    
    return all_ok

def test_entry_point():
    """Test if the entry point script exists"""
    print("\nTest 3: Checking entry point...")
    
    result = subprocess.run(
        ['where', 'stylescout-ai'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✅ Entry point found: {result.stdout.strip()}")
        return True
    else:
        print("❌ Entry point not found")
        return False

def test_server_structure():
    """Test if server has required components"""
    print("\nTest 4: Checking server structure...")
    
    try:
        from stylescout_ai import server
        
        # Check if main function exists
        if hasattr(server, 'main'):
            print("✅ main() function exists")
        else:
            print("❌ main() function not found")
            return False
        
        # Check if server object exists
        if hasattr(server, 'server'):
            print("✅ Server object exists")
        else:
            print("❌ Server object not found")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Structure check failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("StyleScout AI MCP Server - Verification Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Import Test", test_import()))
    results.append(("Dependencies Test", test_dependencies()))
    results.append(("Entry Point Test", test_entry_point()))
    results.append(("Server Structure Test", test_server_structure()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! The MCP server is ready to use.")
        print("\nNext steps:")
        print("1. Restart Claude Desktop completely")
        print("2. Look for the 🔌 tools icon")
        print("3. You should see 4 StyleScout tools")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nTo fix:")
        print("1. cd to project directory: cd 'D:\\Stylescout AI\\stylescout-ai'")
        print("2. Reinstall: pip install -e .")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
