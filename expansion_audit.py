#!/usr/bin/env python3
"""
Expansion Services Audit Script
Run: python expansion_audit.py
"""

import os
import ast

services_dir = r'D:\Claude\expansion\services'
results = []

for filename in sorted(os.listdir(services_dir)):
    if filename.endswith('.py'):
        filepath = os.path.join(services_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
            
            # Check for main/run/start methods
            has_main = 'if __name__' in content
            has_start = 'def start' in content or 'def run' in content
            has_fastapi = 'FastAPI' in content or 'uvicorn' in content
            has_hardware = any(hw in content.lower() for hw in ['muse', 'eeg', 'hrv', 'bluetooth', 'usb', 'serial', 'stream', 'inlet'])
            
            # Check for TODO/NOT_IMPLEMENTED/placeholder
            is_scaffolding = any(marker in content.upper() for marker in ['TODO', 'NOT IMPLEMENTED', 'PLACEHOLDER'])
            
            lines = len(content.split('\n'))
            
            results.append({
                'file': filename,
                'lines': lines,
                'has_main': has_main,
                'has_start': has_start,
                'has_fastapi': has_fastapi,
                'has_hardware': has_hardware,
                'is_scaffolding': is_scaffolding,
                'runnable': has_main or has_start
            })
        except Exception as e:
            results.append({'file': filename, 'error': str(e)[:50]})

print('=' * 80)
print('EXPANSION SERVICES AUDIT - CODEX TRIAGE REPORT')
print('=' * 80)

working = [r for r in results if r.get('runnable') and not r.get('is_scaffolding')]
scaffold = [r for r in results if r.get('is_scaffolding')]
unknown = [r for r in results if not r.get('runnable') and not r.get('is_scaffolding') and not r.get('error')]
errors = [r for r in results if r.get('error')]

print(f'\n✅ LIKELY WORKING ({len(working)} services):')
for r in working:
    hw = '🧠' if r.get('has_hardware') else ''
    api = '🌐' if r.get('has_fastapi') else ''
    fname = r.get('file', '')
    lines = r.get('lines', 0)
    print(f'  {fname:50s} {lines:5d}L {hw} {api}')

print(f'\n⚠️  SCAFFOLDING ({len(scaffold)} services):')
for r in scaffold:
    fname = r.get('file', '')
    lines = r.get('lines', 0)
    print(f'  {fname:50s} {lines:5d}L (TODO/PLACEHOLDER found)')

print(f'\n❓ UNKNOWN/NO-ENTRY-POINT ({len(unknown)} services):')
for r in unknown:
    fname = r.get('file', '')
    lines = r.get('lines', 0)
    print(f'  {fname:50s} {lines:5d}L (no main/start)')

if errors:
    print(f'\n❌ PARSE ERRORS ({len(errors)}):')
    for r in errors:
        fname = r.get('file', '')
        err = r.get('error', '')
        print(f'  {fname:50s} {err}')

print('\n' + '=' * 80)
print('DETAILED ANALYSIS:')
print('=' * 80)
for r in sorted(results, key=lambda x: x['file']):
    status = 'OK' if r.get('runnable') else '??'
    if r.get('is_scaffolding'):
        status = 'WIP'
    fname = r.get('file', '')
    runnable = r.get('runnable')
    hw = r.get('has_hardware')
    api = r.get('has_fastapi')
    print(f'{status} {fname}: runnable={runnable} hw={hw} api={api}')
