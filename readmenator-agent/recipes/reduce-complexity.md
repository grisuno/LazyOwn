# Recipe: Reduce File Complexity

Target hotspot: `static/js/html2pdf.bundle.min.js`
(complexity 1.0, centrality 1.0)

1. Read dependents: `grep -n 'static/js/html2pdf.bundle.min.js' readmenator-agent/ARCHITECTURE.md`
2. Extract functions/classes into new files in the same subsystem
3. Update imports
4. Regenerate: `readmenator .`
