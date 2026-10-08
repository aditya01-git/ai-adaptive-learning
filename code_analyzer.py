"""Safe static code analysis. User code is NEVER executed."""
import ast, re

def _balance(code):
    pairs={")":"(","]":"[","}":"{"}; stack=[]; issues=[]; quote=None
    for line_no,line in enumerate(code.splitlines(),1):
        escaped=False
        for ch in line:
            if quote:
                if ch==quote and not escaped: quote=None
                escaped=(ch=="\\" and not escaped); continue
            if ch in "'\"": quote=ch
            elif ch in "([{": stack.append((ch,line_no))
            elif ch in pairs:
                if not stack or stack[-1][0]!=pairs[ch]:
                    issues.append(f"Line {line_no}: unexpected '{ch}'."); return issues
                stack.pop()
    for ch,n in stack: issues.append(f"Line {n}: '{ch}' is not closed.")
    return issues

def check_python(code):
    try: tree=ast.parse(code)
    except SyntaxError as e: return [f"Syntax error on line {e.lineno}: {e.msg}"]
    issues=[]
    for n in ast.walk(tree):
        if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load): pass
        if isinstance(n,ast.Compare) and any(isinstance(op,ast.Is) for op in n.ops):
            issues.append(f"Line {n.lineno}: use == for value comparison instead of 'is'.")
        if isinstance(n,ast.FunctionDef):
            if any(isinstance(d,(ast.List,ast.Dict,ast.Set)) for d in n.args.defaults):
                issues.append(f"Line {n.lineno}: avoid mutable default arguments in '{n.name}'.")
    return issues

def check_java(code):
    issues=_balance(code)
    if "class " not in code: issues.append("Java code should contain a class.")
    if "main(" not in code and "static void main" not in code:
        issues.append("Tip: executable Java examples usually include a main method.")
    if re.search(r'\\bString\\s*\\w+\\s*==\\s*',code):
        issues.append("Use .equals() to compare String contents.")
    for n,line in enumerate(code.splitlines(),1):
        s=line.strip()
        if s and re.match(r"(int|double|float|boolean|String|char|return|System\\.)",s) and not s.endswith((";","{","}")):
            issues.append(f"Line {n}: this statement may need a semicolon.")
    return list(dict.fromkeys(issues))

def check_javascript(code):
    issues=_balance(code)
    for n,line in enumerate(code.splitlines(),1):
        if re.search(r'\\bvar\\s+',line): issues.append(f"Line {n}: prefer let or const instead of var.")
        if re.search(r'(?<![=!])==(?!=)',line): issues.append(f"Line {n}: prefer === for strict equality.")
        if re.search(r'\\bif\\s*\\([^)]*[^=!<>]=[^=][^)]*\\)',line):
            issues.append(f"Line {n}: check whether '=' should be '===' inside the condition.")
    return list(dict.fromkeys(issues))

def check_code(language, code):
    if not code.strip(): return ["Write some code first."]
    return {"Python":check_python,"Java":check_java,"JavaScript":check_javascript}[language](code)

def evaluate_challenge(language, code, keywords):
    text=code.lower()
    if not code.strip(): return False, 0.0, "No code was submitted."
    hits=sum(1 for k in keywords if k.lower() in text)
    ratio=hits/max(1,len(keywords))
    issues=check_code(language,code)
    if any(x.lower().startswith(("syntax error","line")) and "tip:" not in x.lower() for x in issues):
        ratio*=0.7
    passed=ratio>=0.65 and not any("syntax error" in x.lower() for x in issues)
    score=round(min(100,ratio*100),1)
    msg="Challenge looks on track. Great job!" if passed else "You have the right idea, but some required pieces are missing. Use the hints and try again."
    return passed,score,msg
