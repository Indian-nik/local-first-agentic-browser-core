#!/usr/bin/env python3
"""Example STQA Usage - Software Testing and Quality Assurance"""

from cybercore_v5.stqa import (
    SoftwareTester,
    TestAutomation,
    QualityAnalyzer
)

def main():
    print("=" * 60)
    print("CyberCore v5.0 - STQA Example")
    print("=" * 60)
    
    # Example 1: Software Testing
    print("\n[1] Software Testing")
    print("-" * 60)
    
    tester = SoftwareTester(application="MyApp v1.0")
    
    # Functional testing
    print("\nRunning functional tests...")
    test_cases = [
        {"name": "User Login", "type": "functional"},
        {"name": "Data Validation", "type": "functional"},
        {"name": "Error Handling", "type": "functional"}
    ]
    
    functional_results = tester.functional_testing(test_cases)
    print(f"  Total tests: {functional_results['total_tests']}")
    print(f"  Passed: {functional_results['passed']}")
    print(f"  Failed: {functional_results['failed']}")
    
    # Integration testing
    print("\nRunning integration tests...")
    components = ["Database", "API", "Frontend", "Cache"]
    integration_results = tester.integration_testing(components)
    print(f"  Integration tests: {len(integration_results['integration_tests'])}")
    
    # Performance testing
    print("\nRunning performance tests...")
    load_config = {"users": 1000, "duration": 300}
    perf_results = tester.performance_testing(load_config)
    metrics = perf_results['metrics']
    print(f"  Response time: {metrics['response_time_ms']}ms")
    print(f"  Throughput: {metrics['throughput_rps']} req/s")
    print(f"  Error rate: {metrics['error_rate'] * 100}%")
    
    # Security testing
    print("\nRunning security tests...")
    security_results = tester.security_testing()
    print(f"  Security tests: {len(security_results['tests'])}")
    
    # Example 2: Test Automation
    print("\n[2] Test Automation")
    print("-" * 60)
    
    automation = TestAutomation(project_name="MyProject")
    
    # Define test functions
    def test_authentication():
        assert True  # Your test logic here
    
    def test_data_processing():
        assert True  # Your test logic here
    
    def test_api_endpoints():
        assert True  # Your test logic here
    
    # Add tests to automation suite
    automation.add_test("Authentication", test_authentication)
    automation.add_test("Data Processing", test_data_processing)
    automation.add_test("API Endpoints", test_api_endpoints)
    
    # Run all automated tests
    print("\nRunning automated test suite...")
    auto_results = automation.run_all_tests()
    print(f"  Total tests: {auto_results['total_tests']}")
    print(f"  Passed: {auto_results['passed']}")
    print(f"  Duration: {auto_results['duration_seconds']:.2f}s")
    
    # CI/CD integration
    print("\nSimulating CI/CD pipeline...")
    ci_config = {"pipeline": "github-actions", "build": 42}
    ci_results = automation.continuous_integration(ci_config)
    print(f"  CI Status: {ci_results['ci_status']}")
    print(f"  Build: #{ci_results['build_number']}")
    
    # Example 3: Quality Analysis
    print("\n[3] Code Quality Analysis")
    print("-" * 60)
    
    analyzer = QualityAnalyzer(project_path="/path/to/project")
    
    print("\nAnalyzing code quality...")
    metrics = analyzer.analyze_code_quality()
    
    # Display metrics
    print(f"\nMaintainability:")
    print(f"  Index: {metrics['maintainability']['maintainability_index']}")
    print(f"  Rating: {metrics['maintainability']['rating']}")
    
    print(f"\nComplexity:")
    print(f"  Average: {metrics['complexity']['average_complexity']}")
    print(f"  Maximum: {metrics['complexity']['max_complexity']}")
    
    print(f"\nTest Coverage:")
    print(f"  Line Coverage: {metrics['test_coverage']['line_coverage']}%")
    print(f"  Branch Coverage: {metrics['test_coverage']['branch_coverage']}%")
    print(f"  Function Coverage: {metrics['test_coverage']['function_coverage']}%")
    
    print(f"\nTechnical Debt:")
    print(f"  Debt Hours: {metrics['technical_debt']['debt_hours']}")
    print(f"  SQALE Rating: {metrics['technical_debt']['sqale_rating']}")
    
    # Generate quality report
    print("\nGenerating quality report...")
    quality_report = analyzer.generate_quality_report()
    print(quality_report)
    
    print("\n" + "=" * 60)
    print("STQA Assessment Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
