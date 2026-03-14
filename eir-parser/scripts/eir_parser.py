#!/usr/bin/env python3
"""
EIR File Parser & Interactive Viewer

Parse .eir healthcare files and display in interactive HTML format with AI integration.
"""

import os
import sys
import json
import yaml
import argparse
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import webbrowser
from pathlib import Path

class EIRParser:
    def __init__(self, eir_file):
        self.eir_file = eir_file
        self.data = self.load_eir_file()
    
    def load_eir_file(self):
        """Load and parse EIR file."""
        try:
            with open(self.eir_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading EIR file: {e}")
            sys.exit(1)
    
    def get_summary(self):
        """Get summary statistics."""
        entries = self.data.get('entries', [])
        
        categories = {}
        providers = {}
        date_range = {"earliest": None, "latest": None}
        
        for entry in entries:
            # Category counts
            category = entry.get('category', 'Unknown')
            categories[category] = categories.get(category, 0) + 1
            
            # Provider counts
            provider = entry.get('provider', {}).get('name', 'Unknown')
            providers[provider] = providers.get(provider, 0) + 1
            
            # Date range
            if entry.get('date'):
                date = entry['date']
                if not date_range["earliest"] or date < date_range["earliest"]:
                    date_range["earliest"] = date
                if not date_range["latest"] or date > date_range["latest"]:
                    date_range["latest"] = date
        
        return {
            "total_entries": len(entries),
            "categories": categories,
            "providers": providers,
            "date_range": date_range,
            "patient": self.data.get('patient', {}).get('name', 'Unknown')
        }
    
    def generate_html(self):
        """Generate interactive HTML view."""
        summary = self.get_summary()
        entries = self.data.get('entries', [])
        
        # Sort entries by date (newest first)
        def get_date_key(entry):
            date = entry.get('date', '1900-01-01')
            time = entry.get('time', '00')
            return f"{date}-{time.zfill(2)}"
        
        entries.sort(key=get_date_key, reverse=True)
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Journal - {summary['patient']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            color: #333;
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }}
        
        .summary-card {{
            background: rgba(255,255,255,0.2);
            padding: 1rem;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }}
        
        .summary-card h3 {{
            font-size: 0.9rem;
            opacity: 0.9;
            margin-bottom: 0.5rem;
        }}
        
        .summary-card .value {{
            font-size: 1.5rem;
            font-weight: bold;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .filters {{
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        
        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        
        .filter-group label {{
            font-weight: 600;
            font-size: 0.9rem;
            color: #666;
        }}
        
        .filter-group select, .filter-group input {{
            padding: 0.5rem;
            border: 2px solid #e9ecef;
            border-radius: 5px;
            font-size: 0.9rem;
        }}
        
        .entries {{
            display: grid;
            gap: 1rem;
        }}
        
        .entry {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .entry:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}
        
        .entry-header {{
            padding: 1rem;
            border-left: 4px solid #667eea;
        }}
        
        .entry-category {{
            font-size: 0.8rem;
            font-weight: bold;
            color: #667eea;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .entry-date {{
            font-size: 0.9rem;
            color: #666;
            float: right;
        }}
        
        .entry-title {{
            font-size: 1.2rem;
            font-weight: 600;
            margin: 0.5rem 0;
            color: #333;
        }}
        
        .entry-provider {{
            font-size: 0.9rem;
            color: #888;
        }}
        
        .entry-content {{
            padding: 0 1rem 1rem;
        }}
        
        .entry-details {{
            background: #f8f9fa;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
            font-size: 0.9rem;
        }}
        
        .entry-notes {{
            margin-top: 1rem;
        }}
        
        .entry-notes ul {{
            list-style: none;
            padding: 0;
        }}
        
        .entry-notes li {{
            background: #e3f2fd;
            padding: 0.5rem;
            margin: 0.25rem 0;
            border-radius: 3px;
            font-size: 0.9rem;
        }}
        
        .entry-tags {{
            display: flex;
            gap: 0.5rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }}
        
        .tag {{
            background: #667eea;
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 15px;
            font-size: 0.7rem;
            font-weight: 500;
        }}
        
        .ai-button {{
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: #4CAF50;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .ai-button:hover {{
            background: #45a049;
            transform: scale(1.05);
        }}
        
        .entry {{
            position: relative;
        }}
        
        .category-diagnoses {{ border-left-color: #e74c3c; }}
        .category-vaccinations {{ border-left-color: #2ecc71; }}
        .category-anteckningar {{ border-left-color: #3498db; }}
        .category-vårdkontakter {{ border-left-color: #f39c12; }}
        .category-remisser {{ border-left-color: #9b59b6; }}
        
        .hidden {{
            display: none !important;
        }}
        
        @media (max-width: 768px) {{
            .header {{ padding: 1rem; }}
            .header h1 {{ font-size: 2rem; }}
            .container {{ padding: 1rem; }}
            .filters {{ flex-direction: column; }}
            .summary {{ grid-template-columns: 1fr 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏥 Health Journal</h1>
        <p>Patient: {summary['patient']}</p>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Total Entries</h3>
                <div class="value">{summary['total_entries']}</div>
            </div>
            <div class="summary-card">
                <h3>Date Range</h3>
                <div class="value" style="font-size: 1rem;">
                    {summary['date_range'].get('earliest', 'N/A')} - {summary['date_range'].get('latest', 'N/A')}
                </div>
            </div>
            <div class="summary-card">
                <h3>Categories</h3>
                <div class="value">{len(summary['categories'])}</div>
            </div>
            <div class="summary-card">
                <h3>Providers</h3>
                <div class="value">{len(summary['providers'])}</div>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="filters">
            <div class="filter-group">
                <label>Category</label>
                <select id="categoryFilter">
                    <option value="">All Categories</option>
                    {self._generate_category_options(summary['categories'])}
                </select>
            </div>
            <div class="filter-group">
                <label>Provider</label>
                <select id="providerFilter">
                    <option value="">All Providers</option>
                    {self._generate_provider_options(summary['providers'])}
                </select>
            </div>
            <div class="filter-group">
                <label>Search</label>
                <input type="text" id="searchFilter" placeholder="Search entries...">
            </div>
        </div>
        
        <div class="entries" id="entries">
            {self._generate_entries_html(entries)}
        </div>
    </div>
    
    <script>
        // Filter functionality
        const categoryFilter = document.getElementById('categoryFilter');
        const providerFilter = document.getElementById('providerFilter');
        const searchFilter = document.getElementById('searchFilter');
        const entries = document.querySelectorAll('.entry');
        
        function filterEntries() {{
            const categoryValue = categoryFilter.value.toLowerCase();
            const providerValue = providerFilter.value.toLowerCase();
            const searchValue = searchFilter.value.toLowerCase();
            
            entries.forEach(entry => {{
                const category = entry.dataset.category?.toLowerCase() || '';
                const provider = entry.dataset.provider?.toLowerCase() || '';
                const text = entry.textContent.toLowerCase();
                
                const matchesCategory = !categoryValue || category.includes(categoryValue);
                const matchesProvider = !providerValue || provider.includes(providerValue);
                const matchesSearch = !searchValue || text.includes(searchValue);
                
                if (matchesCategory && matchesProvider && matchesSearch) {{
                    entry.classList.remove('hidden');
                }} else {{
                    entry.classList.add('hidden');
                }}
            }});
        }}
        
        categoryFilter.addEventListener('change', filterEntries);
        providerFilter.addEventListener('change', filterEntries);
        searchFilter.addEventListener('input', filterEntries);
        
        // AI Consultation functionality
        function askAI(entryId, entryData) {{
            const message = `I'd like to understand this health record entry:\\n\\nEntry ID: ${{entryId}}\\nDate: ${{entryData.date || 'Not specified'}}\\nCategory: ${{entryData.category}}\\nProvider: ${{entryData.provider?.name}}\\nSummary: ${{entryData.content?.summary}}\\nDetails: ${{entryData.content?.details}}\\n\\nCan you help me understand what this means?`;
            
            // Send to OpenClaw chat (this would be integrated with the actual API)
            console.log('AI Consultation Request:', message);
            alert('AI consultation request sent! Check the chat for response.');
            
            // In a real implementation, this would make an API call to OpenClaw
            // fetch('/api/openclaw/chat', {{
            //     method: 'POST',
            //     headers: {{'Content-Type': 'application/json'}},
            //     body: JSON.stringify({{message: message}})
            // }});
        }}
        
        // Add click handlers to entries
        entries.forEach((entry, index) => {{
            entry.addEventListener('click', (e) => {{
                if (e.target.classList.contains('ai-button')) {{
                    e.stopPropagation();
                    return;
                }}
                
                const entryData = JSON.parse(entry.dataset.entryData);
                askAI(entryData.id, entryData);
            }});
            
            const aiButton = entry.querySelector('.ai-button');
            if (aiButton) {{
                aiButton.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    const entryData = JSON.parse(entry.dataset.entryData);
                    askAI(entryData.id, entryData);
                }});
            }}
        }});
    </script>
</body>
</html>"""
        
        return html
    
    def _generate_category_options(self, categories):
        """Generate HTML options for category filter."""
        options = []
        for category, count in sorted(categories.items()):
            options.append(f'<option value="{category}">{category} ({count})</option>')
        return '\n'.join(options)
    
    def _generate_provider_options(self, providers):
        """Generate HTML options for provider filter."""
        options = []
        for provider, count in sorted(providers.items()):
            options.append(f'<option value="{provider}">{provider} ({count})</option>')
        return '\n'.join(options)
    
    def _generate_entries_html(self, entries):
        """Generate HTML for all entries."""
        html_entries = []
        
        for entry in entries:
            category = entry.get('category', 'unknown').lower()
            provider_name = entry.get('provider', {}).get('name', 'Unknown Provider')
            
            entry_html = f'''
            <div class="entry category-{category.replace(' ', '-').replace('ä', 'a').replace('ö', 'o').replace('å', 'a')}" 
                 data-category="{category}" 
                 data-provider="{provider_name}"
                 data-entry-data='{json.dumps(entry)}'>
                
                <button class="ai-button">🤖 Ask AI</button>
                
                <div class="entry-header">
                    <div class="entry-category">{entry.get('category', 'Unknown')}</div>
                    <div class="entry-date">{self._format_date(entry.get('date'), entry.get('time'))}</div>
                    <div class="entry-title">{entry.get('content', {}).get('summary', entry.get('type', 'No Title'))}</div>
                    <div class="entry-provider">📍 {provider_name}</div>
                </div>
                
                <div class="entry-content">
                    {self._generate_entry_content_html(entry)}
                </div>
            </div>'''
            
            html_entries.append(entry_html)
        
        return '\n'.join(html_entries)
    
    def _generate_entry_content_html(self, entry):
        """Generate HTML for entry content."""
        content = entry.get('content', {})
        html_parts = []
        
        # Details
        if content.get('details'):
            html_parts.append(f'<div class="entry-details">{content["details"]}</div>')
        
        # Notes
        notes = content.get('notes', [])
        if notes:
            html_parts.append('<div class="entry-notes"><strong>Notes:</strong><ul>')
            for note in notes:
                html_parts.append(f'<li>{note}</li>')
            html_parts.append('</ul></div>')
        
        # Responsible person
        responsible = entry.get('responsible_person', {})
        if responsible.get('name'):
            role = responsible.get('role', '')
            html_parts.append(f'<div><strong>Responsible:</strong> {responsible["name"]} {role}</div>')
        
        # Tags
        tags = entry.get('tags', [])
        if tags:
            html_parts.append('<div class="entry-tags">')
            for tag in tags:
                html_parts.append(f'<span class="tag">{tag}</span>')
            html_parts.append('</div>')
        
        return '\n'.join(html_parts)
    
    def _format_date(self, date, time=None):
        """Format date and time for display."""
        if not date:
            return 'No Date'
        
        try:
            if time:
                return f"{date} {time}:00"
            return date
        except:
            return str(date)

class EIRHTTPHandler(BaseHTTPRequestHandler):
    eir_parser = None
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html = self.eir_parser.generate_html()
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        return  # Suppress logging

def main():
    parser = argparse.ArgumentParser(description='EIR File Parser & Viewer')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # View command
    view_parser = subparsers.add_parser('view', help='Display EIR file summary')
    view_parser.add_argument('file', help='Path to .eir file')
    
    # Serve command
    serve_parser = subparsers.add_parser('serve', help='Serve interactive web view')
    serve_parser.add_argument('file', help='Path to .eir file')
    serve_parser.add_argument('--port', type=int, default=8080, help='Port to serve on')
    serve_parser.add_argument('--open', action='store_true', help='Open browser automatically')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if not os.path.exists(args.file):
        print(f"Error: File {args.file} not found")
        sys.exit(1)
    
    eir_parser = EIRParser(args.file)
    
    if args.command == 'view':
        summary = eir_parser.get_summary()
        print(f"\\n📋 Health Summary for {summary['patient']}")
        print(f"{'='*50}")
        print(f"Total Entries: {summary['total_entries']}")
        print(f"Date Range: {summary['date_range'].get('earliest', 'N/A')} - {summary['date_range'].get('latest', 'N/A')}")
        print(f"\\n📊 Categories:")
        for category, count in sorted(summary['categories'].items(), key=lambda x: x[1], reverse=True):
            print(f"  • {category}: {count}")
        
        print(f"\\n🏥 Healthcare Providers:")
        for provider, count in sorted(summary['providers'].items(), key=lambda x: x[1], reverse=True):
            print(f"  • {provider}: {count}")
    
    elif args.command == 'serve':
        EIRHTTPHandler.eir_parser = eir_parser
        
        httpd = HTTPServer(('localhost', args.port), EIRHTTPHandler)
        print(f"\\n🌐 EIR Viewer serving at http://localhost:{args.port}")
        print("Press Ctrl+C to stop the server")
        
        if args.open:
            webbrowser.open(f'http://localhost:{args.port}')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\n👋 Server stopped")
            httpd.server_close()

if __name__ == '__main__':
    main()