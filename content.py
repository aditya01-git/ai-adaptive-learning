LANGUAGES = ["Python", "Java", "JavaScript"]

TOPICS = [
    "Variables", "Data Types", "Conditions", "Loops",
    "Functions", "Arrays/Lists", "OOP", "DOM Basics"
]

TOPIC_META = {
    "Variables": {"icon": "📦", "level": "Beginner"},
    "Data Types": {"icon": "🧩", "level": "Beginner"},
    "Conditions": {"icon": "🔀", "level": "Beginner"},
    "Loops": {"icon": "🔁", "level": "Beginner"},
    "Functions": {"icon": "🧠", "level": "Beginner"},
    "Arrays/Lists": {"icon": "📚", "level": "Beginner"},
    "OOP": {"icon": "🏗️", "level": "Intermediate"},
    "DOM Basics": {"icon": "🌐", "level": "Intermediate"},
}

LANGUAGE_META = {
    "Python": {"icon": "🐍", "color": "#16A34A", "gradient": "linear-gradient(135deg,#15803D,#22C55E)"},
    "Java": {"icon": "☕", "color": "#EA580C", "gradient": "linear-gradient(135deg,#C2410C,#F97316)"},
    "JavaScript": {"icon": "⚡", "color": "#CA8A04", "gradient": "linear-gradient(135deg,#CA8A04,#FACC15)"},
}

CONTENT = {
"Python": {
"Variables": {
"explain": "A variable is a named box that stores a value. Python creates the variable when you assign something to a name, so you do not write a type before it.",
"example": 'name = "Aditya"\\nage = 19\\nprint(name, age)',
"challenge": "Create a variable called name and a variable called age, then print both.",
"keywords": ["print", "=", "name", "age"],
"quiz": [
("Which line creates an integer variable?", ["x = 5", "int x = 5", "integer x = 5", "var x = 5"], 0),
("Which is a valid Python variable name?", ["2name", "my-name", "my_name", "class"], 2),
("What does assignment use?", ["=", "==", "=>", ":="], 0)]},
"Data Types": {
"explain": "Python has built-in types such as int, float, str, bool, list and dict. The type tells Python what kind of value it is working with.",
"example": 'age = 19\\nprice = 9.5\\nname = "Ada"\\nactive = True\\nprint(type(age), type(name))',
"challenge": "Create an integer, a float, a string and a boolean, then print their types.",
"keywords": ["int", "float", "str", "bool", "type"],
"quiz": [
("What type is 10?", ["str", "int", "float", "bool"], 1),
("What type is 3.14?", ["int", "float", "str", "list"], 1),
("Which function checks a value's type?", ["typeof()", "type()", "checktype()", "datatype()"], 1)]},
"Conditions": {
"explain": "Conditions let a program choose between paths. Python uses if, elif and else, with indentation defining each block.",
"example": 'marks = 72\\nif marks >= 40:\\n    print("Pass")\\nelse:\\n    print("Fail")',
"challenge": "Write an if/else that prints Pass when marks are at least 40, otherwise Fail.",
"keywords": ["if", "else", "print"],
"quiz": [
("Which keyword means another condition?", ["elseif", "elif", "else if", "when"], 1),
("Which operator checks equality?", ["=", "==", "===", "=>"], 1),
("What happens when an if condition is false and else exists?", ["The else block runs", "The program stops", "The if block runs", "Nothing always happens"], 0)]},
"Loops": {
"explain": "Loops repeat code. A for loop commonly walks through a sequence or range, while a while loop continues while its condition is true.",
"example": 'for i in range(1, 4):\\n    print(i)\\n\\nn = 3\\nwhile n > 0:\\n    n -= 1',
"challenge": "Use a loop to print the numbers 1 through 5.",
"keywords": ["for", "range", "print"],
"quiz": [
("What does range(3) produce?", ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "3 only"], 1),
("Which loop is based on a condition?", ["while", "switch", "repeat", "foreach"], 0),
("What does break do?", ["Skips one iteration", "Exits the loop", "Restarts the loop", "Pauses forever"], 1)]},
"Functions": {
"explain": "A function is reusable code. In Python, def defines a function and return sends a result back to the caller.",
"example": 'def add(a, b):\\n    return a + b\\n\\nresult = add(2, 3)\\nprint(result)',
"challenge": "Create a function that accepts two numbers and returns their sum.",
"keywords": ["def", "return"],
"quiz": [
("Which keyword defines a Python function?", ["func", "def", "function", "method"], 1),
("Which keyword sends a result back?", ["give", "return", "output", "yield only"], 1),
("How do you call add?", ["call add", "add()", "run add", "function.add()"], 1)]},
"Arrays/Lists": {
"explain": "Python lists store multiple ordered values. Indexing starts at zero, and lists can grow or shrink.",
"example": 'fruits = ["apple", "banana", "mango"]\\nfruits.append("orange")\\nprint(fruits[0])\\nprint(len(fruits))',
"challenge": "Create a list of three fruits, add one more fruit, and print the first item.",
"keywords": ["[", "]", "append", "print"],
"quiz": [
("What is the first list index?", ["0", "1", "-1", "first"], 0),
("Which method adds to the end?", ["push()", "append()", "add()", "put()"], 1),
("What does len([1,2,3]) return?", ["2", "3", "4", "1"], 1)]},
"OOP": {
"explain": "Object-oriented programming groups data and behavior into classes. Objects are instances of those classes.",
"example": 'class Dog:\\n    def __init__(self, name):\\n        self.name = name\\n\\n    def bark(self):\\n        print(self.name, "says woof")\\n\\nDog("Rex").bark()',
"challenge": "Create a Student class with a name attribute and a method that prints the name.",
"keywords": ["class", "def", "self"],
"quiz": [
("Which keyword creates a class?", ["object", "class", "struct", "new"], 1),
("What is __init__ commonly used for?", ["Looping", "Construction/initialization", "Printing", "Inheritance only"], 1),
("What does self represent?", ["Current object", "Parent class", "Global variable", "Module"], 0)]},
"DOM Basics": {
"explain": "The DOM is the browser's object representation of an HTML page. JavaScript can select elements, change their text, and respond to events.",
"example": 'button = document.getElementById("btn")\\nbutton.addEventListener("click", function():\\n    print("clicked"))',
"challenge": "For Python, describe the DOM in a comment or write pseudocode showing how a button click would be handled.",
"keywords": ["document", "element", "event"],
"quiz": [
("What does DOM stand for?", ["Data Object Model", "Document Object Model", "Document Output Method", "Digital Object Map"], 1),
("Which language normally manipulates the browser DOM?", ["Python", "Java", "JavaScript", "SQL"], 2),
("What is an event?", ["A user/browser action", "A variable type", "A database", "A loop"], 0)]},
},
"Java": {
"Variables": {
"explain": "Java is statically typed, so a variable declaration normally includes its data type. The type tells the compiler what values are allowed.",
"example": 'int age = 19;\\nString name = "Aditya";\\nfinal double PI = 3.14;\\nSystem.out.println(name);',
"challenge": "Declare an int age, a String name and print both.",
"keywords": ["int", "String", "System.out"],
"quiz": [
("Which correctly declares an integer?", ["int x = 5;", "integer x = 5;", "x := 5;", "var x = 5"], 0),
("Which type stores text?", ["String", "string", "Text", "char only"], 0),
("Which keyword makes a variable constant?", ["const", "final", "fixed", "static"], 1)]},
"Data Types": {
"explain": "Java has primitive types such as int, double, char and boolean, plus reference types such as String and arrays.",
"example": """int count = 10;\ndouble price = 4.5;\nchar grade = 'A';\nboolean active = true;""",
"challenge": "Create variables using int, double, char and boolean.",
"keywords": ["int", "double", "char", "boolean"],
"quiz": [
("Which type stores true or false?", ["boolean", "bool", "bit", "logical"], 0),
("Which type stores decimal numbers such as 3.5?", ["int", "double", "char", "boolean"], 1),
("A single character can use:", ["char", "String only", "text", "character"], 0)]},
"Conditions": {
"explain": "Java uses if, else if and else. Conditions evaluate to boolean values. For String content, use equals() rather than ==.",
"example": 'int marks = 72;\\nif (marks >= 40) {\\n    System.out.println("Pass");\\n} else {\\n    System.out.println("Fail");\\n}',
"challenge": "Write an if/else that prints Pass when marks are at least 40.",
"keywords": ["if", "else", "System.out"],
"quiz": [
("Which syntax is correct?", ["else if", "elif", "elseif", "else-if"], 0),
("An if condition must be:", ["boolean", "int", "String", "double"], 0),
("How should String contents normally be compared?", ["equals()", "==", "=", "compare"], 0)]},
"Loops": {
"explain": "Java provides for, while and do-while loops. A do-while executes its body at least once before checking the condition.",
"example": 'for (int i = 1; i <= 5; i++) {\\n    System.out.println(i);\\n}',
"challenge": "Use a for loop to print numbers 1 through 5.",
"keywords": ["for", "System.out"],
"quiz": [
("How many times does i=0; i<3; i++ run?", ["2", "3", "4", "Infinite"], 1),
("Which loop runs at least once?", ["while", "do-while", "for", "foreach"], 1),
("What does break do?", ["Exits the loop", "Skips current iteration", "Restarts", "Prints"], 0)]},
"Functions": {
"explain": "Java functions are called methods and live inside classes. A method declares a return type, name and parameters.",
"example": 'static int add(int a, int b) {\\n    return a + b;\\n}\\n\\npublic static void main(String[] args) {\\n    System.out.println(add(2, 3));\\n}',
"challenge": "Write a method that accepts two ints and returns their sum.",
"keywords": ["static", "return", "int"],
"quiz": [
("A method returning nothing uses:", ["void", "null", "none", "empty"], 0),
("Which keyword sends a value back?", ["send", "return", "output", "back"], 1),
("What is method overloading?", ["Same name, different parameter lists", "Same name only", "Different classes only", "Recursion"], 0)]},
"Arrays/Lists": {
"explain": "Java arrays have fixed size and use zero-based indexes. ArrayList provides a resizable collection.",
"example": 'int[] nums = {10, 20, 30};\\nSystem.out.println(nums[0]);\\nSystem.out.println(nums.length);',
"challenge": "Create an int array with three values and print the first value.",
"keywords": ["int[]", "[", "]", "System.out"],
"quiz": [
("What is the first array index?", ["0", "1", "-1", "first"], 0),
("How do you get an array length?", ["length", "length()", "size()", "len()"], 0),
("An array of size 5 has last index:", ["4", "5", "6", "1"], 0)]},
"OOP": {
"explain": "Java is object-oriented. Classes define objects, constructors initialize them, and inheritance uses extends.",
"example": 'class Student {\\n    String name;\\n    Student(String name) { this.name = name; }\\n}\\nStudent s = new Student("Ada");',
"challenge": "Create a Student class with a name field and a constructor.",
"keywords": ["class", "new", "this"],
"quiz": [
("Which keyword creates an object?", ["new", "make", "object", "create"], 0),
("Which keyword means inheritance from a class?", ["extends", "inherits", "parent", "super"], 0),
("Which keyword refers to the current object?", ["this", "self", "current", "me"], 0)]},
"DOM Basics": {
"explain": "Java does not normally control a browser DOM directly. In web applications, Java may provide backend services while JavaScript handles DOM interaction.",
"example": '/* Java backend idea */\\nclass PageService {\\n    String getMessage() { return "Hello"; }\\n}',
"challenge": "Explain in a comment how Java and JavaScript can work together in a web application.",
"keywords": ["JavaScript", "backend", "web"],
"quiz": [
("Which language directly manipulates the browser DOM?", ["Java", "JavaScript", "SQL", "C"], 1),
("Java is commonly used on the web for:", ["Backend/server logic", "DOM syntax", "CSS styling", "HTML tags"], 0),
("DOM stands for:", ["Document Object Model", "Data Object Machine", "Digital Output Method", "Document Order Map"], 0)]},
},
"JavaScript": {
"Variables": {
"explain": "Use let for values that can be reassigned and const for bindings you do not reassign. Both are block scoped.",
"example": 'let score = 10;\\nscore = 20;\\nconst name = "Aditya";\\nconsole.log(name, score);',
"challenge": "Create a const name and a let score, then print them.",
"keywords": ["let", "const", "console.log"],
"quiz": [
("Which is reassignable?", ["let", "const", "both never", "class"], 0),
("Which should be used for a binding you will not reassign?", ["const", "let", "fixed", "final"], 0),
("Which function prints to the console?", ["print()", "console.log()", "echo()", "write()"], 1)]},
"Data Types": {
"explain": "JavaScript values include string, number, boolean, undefined, null, object and more. JavaScript uses dynamic typing.",
"example": 'const name = "Ada";\\nconst age = 19;\\nconst active = true;\\nconsole.log(typeof age);',
"challenge": "Create a string, number and boolean, then use typeof on each.",
"keywords": ["const", "typeof"],
"quiz": [
("What is typeof 10?", ["number", "int", "float", "numeric"], 0),
("Which represents true/false?", ["boolean", "bool", "logical", "bit"], 0),
("Which operator checks type?", ["typeof", "type()", "getType()", "datatype"], 0)]},
"Conditions": {
"explain": "JavaScript uses if, else if and else. Prefer strict equality === because it avoids unwanted type conversion.",
"example": 'const marks = 72;\\nif (marks >= 40) {\\n  console.log("Pass");\\n} else {\\n  console.log("Fail");\\n}',
"challenge": "Write an if/else that prints Pass when marks are at least 40.",
"keywords": ["if", "else", "console.log"],
"quiz": [
("Which is strict equality?", ["==", "=", "===", "!="], 2),
("Which value is falsy?", ["0", "'0'", "[]", "{}"], 0),
("What does else do?", ["Runs when previous conditions are false", "Always runs", "Repeats", "Defines a variable"], 0)]},
"Loops": {
"explain": "JavaScript supports for, while, do-while and for...of. Loops repeat work until a condition or collection is exhausted.",
"example": 'for (let i = 1; i <= 5; i++) {\\n  console.log(i);\\n}',
"challenge": "Use a loop to print the numbers 1 through 5.",
"keywords": ["for", "console.log"],
"quiz": [
("Which loop is good for array values?", ["for...of", "for...in only", "repeat", "each"], 0),
("What does break do?", ["Exits the loop", "Skips one iteration", "Restarts", "Declares a variable"], 0),
("Which loop checks condition before each normal iteration?", ["while", "class", "switch", "map"], 0)]},
"Functions": {
"explain": "Functions package reusable logic. JavaScript supports declarations, function expressions and arrow functions.",
"example": 'function add(a, b) { return a + b; }\\nconst multiply = (a, b) => a * b;\\nconsole.log(add(2, 3));',
"challenge": "Write a function that accepts two numbers and returns their sum.",
"keywords": ["function", "return"],
"quiz": [
("Which is an arrow function?", ["(a,b) => a+b", "def add(a,b)", "function ->", "a,b ->"], 0),
("What does return do?", ["Sends a value back", "Prints automatically", "Loops", "Stops the browser"], 0),
("A function declaration is generally:", ["Hoisted", "Never callable", "A class", "A variable only"], 0)]},
"Arrays/Lists": {
"explain": "JavaScript arrays are ordered collections. Useful methods include push, pop, map, filter and forEach.",
"example": 'const nums = [1, 2, 3];\\nnums.push(4);\\nconst doubled = nums.map(n => n * 2);\\nconsole.log(doubled);',
"challenge": "Create an array of three fruits, push a fourth fruit, and print the first item.",
"keywords": ["[", "]", "push", "console.log"],
"quiz": [
("Which adds an item to the end?", ["push()", "append()", "add()", "insert()"], 0),
("Which creates a new transformed array?", ["map()", "forEach()", "push()", "pop()"], 0),
("What is the first index?", ["0", "1", "-1", "first"], 0)]},
"OOP": {
"explain": "JavaScript supports classes built on prototypes. A constructor initializes an object, this refers to the current instance, and extends supports inheritance.",
"example": 'class Student {\\n  constructor(name) { this.name = name; }\\n  greet() { console.log(this.name); }\\n}\\nnew Student("Ada").greet();',
"challenge": "Create a Student class with a name and a greet method.",
"keywords": ["class", "constructor", "this"],
"quiz": [
("Which method initializes a class instance?", ["constructor", "init", "new", "setup"], 0),
("What does this usually refer to in a method?", ["Current object", "Parent class", "Global always", "Module"], 0),
("Which keyword supports class inheritance?", ["extends", "inherits", "parent", "super only"], 0)]},
"DOM Basics": {
"explain": "The DOM represents the HTML document as objects. JavaScript can select elements, change content, styles and listen for events.",
"example": 'const button = document.getElementById("btn");\\nbutton.addEventListener("click", () => {\\n  document.getElementById("msg").textContent = "Clicked!";\\n});',
"challenge": "Select a button by id and add a click event that changes a message.",
"keywords": ["document", "getElementById", "addEventListener"],
"quiz": [
("Which selects an element by id?", ["document.getElementById()", "document.select()", "getId()", "queryId()"], 0),
("Which method attaches an event handler?", ["addEventListener()", "addEvent()", "listen()", "onClick()"], 0),
("Which object represents the page?", ["document", "window.document only", "page", "htmlObject"], 0)]},
}
}

def get_topic(language, topic):
    return CONTENT[language][topic]
