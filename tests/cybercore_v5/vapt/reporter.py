"""VAPT Reporter - Professional Security Reports"""
import json
from datetime import datetime
from typing import Dict, List

class VAPTReporter:
    """Generate professional VAPT reports"""
    
    def __init__(self, findings: List[Dict]):
        self.findings = findings
        self.report_date = datetime.now()
    
    def generate_executive_summary(self) -> str:
        """Generate executive summary"""
        total_findings = len(self.findings)
        critical = sum(1 for f in self.findings if f.get('severity') == 'CRITICAL')
        high = sum(1 for f in self.findings if f.get('severity') == 'HIGH')
        
        summary = f"""
EXECUTIVE SUMMARY
==================
Assessment Date: {self.report_date.strftime('%Y-%m-%d')}
Total Findings: {total_findings}
Critical: {critical}
High: {high}
        """
        return summary
    
    def generate_technical_report(self) -> str:
        """Generate technical report"""
        report = "TECHNICAL FINDINGS
" + "="*50 + "
"
        for idx, finding in enumerate(self.findings, 1):
            report += f"
{idx}. {finding.get('title', 'Finding')}
"
            report += f"   Severity: {finding.get('severity', 'N/A')}
"
            report += f"   Description: {finding.get('description', 'N/A')}
"
        return report
    
    def export_json(self, filename: str) -> None:
        """Export report as JSON"""
        report_data = {
            "report_date": self.report_date.isoformat(),
            "findings": self.findings
        }
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2)
