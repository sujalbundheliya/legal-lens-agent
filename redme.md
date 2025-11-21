Legal Lens Agent — README
=========================

**Project:** Legal Lens Agent**Purpose:** Extract, summarise and evaluate legislative documents (PDF → text → structured sections → rule checks).

Table of contents
-----------------

1.  Project layout
    
2.  Requirements & installation
    
3.  Environment variables (.env)
    
4.  Step-by-step run instructions (exact commands)
    
5.  What each script does (inputs, outputs)
    
6.  Expected outputs / file locations
    
7.  Troubleshooting & tips
    
8.  Next steps & optional enhancements
    

1 — Project layout
------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   legal-lens-agent/  ├─ src/  │  ├─ extract_text.py       # Task 1: PDF -> cleaned text  │  ├─ summarise.py          # Task 2: cleaned text -> 7-bullet summary  │  ├─ extract_sections.py   # Task 3: cleaned text -> sections.json  │  └─ rule_checker.py       # Task 4: sections.json -> rules_output.json  ├─ outputs/  │  ├─ full_text.txt  │  ├─ summary.txt  │  ├─ sections.json  │  └─ rules_output.json  ├─ requirements.txt  └─ README.md   `

2 — Requirements & installation
-------------------------------

1.  Create and activate a virtual environment:
    

**Linux / macOS**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python -m venv venv  source venv/bin/activate   `

**Windows (PowerShell)**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python -m venv venv  venv\Scripts\Activate.ps1   `

1.  Install Python packages:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install -r requirements.txt   `

requirements.txt (provided) includes:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pypdf>=3.10.0  pdfplumber>=0.9.0  python-dotenv>=1.0.0  requests>=2.28.0   `

3 — Environment variables (.env)
--------------------------------

Create a .env file in the repo root. Minimum:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   PERPLEXITY_API_KEY=your_perplexity_api_key_here   `

Optional (if you choose to use OpenAI for summarization later):

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   OPENAI_API_KEY=your_openai_api_key_here   `

**Important:** Do **NOT** commit .env to GitHub. Add it to .gitignore.

4 — Step-by-step run instructions
---------------------------------

Run each task in order. Inputs and outputs are consistent across steps.

**1) Extract text from PDF (Task 1)**Default demo PDF (uploaded) used if you do not pass --pdf. Replace path with your PDF if needed.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python src/extract_text.py   `

If you omit --pdf it uses the built-in demo path. Output: outputs/full\_text.txt.

**2) Generate 7-bullet summary (Task 2)**(Uses Perplexity sonar by default; ensure PERPLEXITY\_API\_KEY is set.)

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python src/summarise.py   `

Output: outputs/summary.txt

**3) Extract structured sections (Task 3)**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python src/extract_sections.py   `

Output: outputs/sections.json

**4) Run rule checks (Task 4)**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python src/rule_checker.py   `

Output: outputs/rules\_output.json

5 — What each script does (quick)
---------------------------------

*   **src/extract\_text.py**Reads a PDF, extracts text (pypdf or pdfplumber), cleans line-breaks/hyphenation/headings, writes outputs/full\_text.txt.
    
*   **src/summarise.py**Reads outputs/full\_text.txt, calls Perplexity sonar to produce a 7-bullet summary, writes outputs/summary.txt. Truncates very large documents to avoid token limits.
    
*   **src/extract\_sections.py**Reads outputs/full\_text.txt, prompts Perplexity sonar to extract seven fields into strict JSON with text + evidence keys for each field. Writes outputs/sections.json.
    
*   **src/rule\_checker.py**Reads outputs/sections.json and outputs/full\_text.txt. Runs six rule checks, using section text, evidence or keyword fallbacks. Writes outputs/rules\_output.json.
    

6 — Expected outputs (examples)
-------------------------------

*   outputs/full\_text.txt — cleaned, readable plain text of the PDF.
    
*   outputs/summary.txt — 7 bullet point summary (plain text).
    
*   outputs/sections.json — JSON object with keys: definitions, obligations, responsibilities, eligibility, payments, penalties, record\_keeping. Each key maps to {"text": "...", "evidence": "..."}.
    
*   outputs/rules\_output.json — array of 6 objects:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   [    {"rule": "Act must define key terms", "status": "pass", "evidence": "...", "confidence": 92},    ...  ]   `

7 — Troubleshooting & tips
--------------------------

### Common issues

*   **Missing PERPLEXITY\_API\_KEY** → script raises RuntimeError. Add the key to .env.
    
*   **400 Bad Request from Perplexity** → model name or payload wrong. This project uses model name "sonar" (the one permitted on the tested key). If your account allows other model names, you may change model in the payload.
    
*   **Large documents truncated** → summariser and extractor implement a safe character cap. For full coverage, implement chunking by splitting the text by headings and calling the model per chunk, then merge results.
    
*   **PDF extraction yields garbled text** → try --prefer pdfplumber or --prefer pypdf depending on your PDF:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python src/extract_text.py --pdf path/to/doc.pdf --prefer pdfplumber   `

### Debugging tips

*   Inspect outputs/full\_text.txt if sections extraction looks wrong.
    
*   If sections.json evidence keys are empty, re-run src/extract\_sections.py and check printed raw response (scripts print raw Perplexity errors).
    
*   If rules\_output.json returns unexpected fails, open outputs/sections.json to confirm presence of text or evidence.
    

8 — Next steps & optional enhancements
--------------------------------------

*   **Add chunking**: split full\_text.txt at headings and call models per chunk (recommended for very long Acts).
    
*   **Switch summariser to OpenAI**: for higher quality summarisation, replace summarise.py call to use openai (requires OPENAI\_API\_KEY).
    
*   **Add unit tests**: tests/test\_rule\_checker.py to assert expected pass/fail on sample sections.json.
    
*   **Create pipeline.py**: convenience script to run all steps in order (python pipeline.py). Keep the modular scripts for submission.
    
*   **Create a short demo video**: 2-minute recording showing the pipeline (run commands + outputs open in editor).
    

Assignment reference
--------------------

The assignment brief you provided is at:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   /data/data.pdf   `

(Use this path if you want to include the PDF in your repo or refer to it in your submission.)

### Contact / Notes

If you want, I can:

*   Produce a polished README.md variant for GitHub (with badges and usage examples).
    
*   Generate a pipeline.py.
    
*   Create a 2-minute video script and storyboard.
    

Tell me which of these to produce next.