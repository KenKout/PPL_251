from utils import Parser


def test_0001():
    """Test basic class with main method"""
    source = """class Program { static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_0002():
    """Test method with parameters"""
    source = """class Math { int add(int a; int b) { return a + b; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_0003():
    """Test class with attribute declaration"""
    source = """class Test { int x; static void main() { x := 42; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_0004():
    """Test class with string attribute"""
    source = """class Test { string name; static void main() { name := "Alice"; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_0005():
    """Test final attribute declaration"""
    source = """class Constants { final float PI := 3.14159; static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_0006():
    """Test if-else statement"""
    source = """class Test { 
        static void main() { 
            if (x > 0) then { 
                io.writeStrLn("positive"); 
            } else { 
                io.writeStrLn("negative"); 
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_0007():
    """Test for loop with to keyword"""
    source = """class Test { 
        static void main() { 
            int i;
            for i := 1 to 10 do { 
                i := i + 1; 
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_0008():
    """Test for loop with downto keyword"""
    source = """class Test { 
        static void main() { 
            int i;
            for i := 10 downto 1 do { 
                io.writeInt(i); 
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_0009():
    """Test array declaration and access"""
    source = """class Test { 
        static void main() { 
            int[3] arr := {1, 2, 3};
            int first;
            first := arr[0];
            arr[1] := 42;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_0010():
    """Test string concatenation and object creation"""
    source = """class Test { 
        static void main() { 
            string result;
            Test obj;
            result := "Hello" ^ " " ^ "World";
            obj := new Test();
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_0011():
    """Test parser error: missing closing brace in class declaration"""
    # Line 35: Each class declaration starts with the keyword `class` and then an identifier, which is the class name, and ends with a nullable list of members enclosed by a pair of curly braces `{}`.
    source = """class Test { int x := 1; """  # Thiếu dấu }
    expected = "Error on line 1 col 25: <EOF>"
    assert Parser(source).parse() == expected

def test_001():
    # Missing class name (Program Structure §Class Declaration)
    # Line 35: Each class declaration starts with the keyword `class` and then an identifier, which is the class name, and ends with a nullable list of members enclosed by a pair of curly braces `{}`.
    source = """class { }"""
    expected = "Error on line 1 col 6: {"
    assert Parser(source).parse() == expected

def test_002():
    # Missing class body (expects '{') (Program Structure)
    # Line 35: Each class declaration starts with the keyword `class` and then an identifier, which is the class name, and ends with a nullable list of members enclosed by a pair of curly braces `{}`.
    source = """class A"""
    expected = "Error on line 1 col 7: <EOF>"
    assert Parser(source).parse() == expected

def test_003():
    # 'extends' must be followed by superclass name (Program Structure)
    # Line 37: Between the class name and the list of members, there may be an optional keyword `extends` followed by an identifier, which is the superclass name.
    source = """class A extends {"""
    expected = "Error on line 1 col 16: {"
    assert Parser(source).parse() == expected

def test_004():
    # 'extends' missing superclass name (Program Structure)
    # Line 37: Between the class name and the list of members, there may be an optional keyword `extends` followed by an identifier, which is the superclass name.
    source = """class A extends"""
    expected = "Error on line 1 col 15: <EOF>"
    assert Parser(source).parse() == expected

def test_005():
    # Extra token after superclass (Program Structure)
    # Line 37: Between the class name and the list of members, there may be an optional keyword `extends` followed by an identifier, which is the superclass name.
    source = """class A extends B C {}"""
    expected = "Error on line 1 col 18: C"
    assert Parser(source).parse() == expected

def test_006():
    # Duplicate 'extends' (Program Structure)
    # Line 37: Between the class name and the list of members, there may be an optional keyword `extends` followed by an identifier, which is the superclass name.
    source = """class A extends extends B {}"""
    expected = "Error on line 1 col 16: extends"
    assert Parser(source).parse() == expected

def test_007():
    # Keyword used as class name (Identifier/Keyword)
    # Line 191: The following character sequences are reserved as keywords and cannot be used as identifiers:
    source = """class static {}"""
    expected = "Error on line 1 col 6: static"
    assert Parser(source).parse() == expected

def test_008():
    # Destructor token at top level (Program Structure)
    # Line 29: As its simplicity, an OPLang compiler does not support compiling many files, so an OPLang program is written just in one file only. An OPLang program consists of many class declarations.
    source = """~A(){}"""
    expected = "Error on line 1 col 0: ~"
    assert Parser(source).parse() == expected

def test_009():
    # Second class missing name (Program Structure)
    # Line 35: Each class declaration starts with the keyword `class` and then an identifier, which is the class name, and ends with a nullable list of members enclosed by a pair of curly braces `{}`.
    source = """class A {} class {}"""
    expected = "Error on line 1 col 17: {"
    assert Parser(source).parse() == expected

def test_010():
    # Unexpected token after class (Program Structure)
    # Line 29: An OPLang program consists of many class declarations.
    source = """class A {} extends B"""
    expected = "Error on line 1 col 11: extends"
    assert Parser(source).parse() == expected

def test_011():
    # Parentheses instead of '{' after class name (Separators)
    # Line 35: ... and ends with a nullable list of members enclosed by a pair of curly braces `{}`.
    source = """class A ()"""
    expected = "Error on line 1 col 8: ("
    assert Parser(source).parse() == expected

def test_012():
    # Top-level 'new' expression (Program Structure)
    # Line 29: An OPLang program consists of many class declarations.
    source = """new A();"""
    expected = "Error on line 1 col 0: new"
    assert Parser(source).parse() == expected

def test_013():
    # Top-level attribute (Program Structure)
    # Line 29: An OPLang program consists of many class declarations.
    source = """static int x;"""
    expected = "Error on line 1 col 0: static"
    assert Parser(source).parse() == expected

def test_014():
    # Top-level attribute (Program Structure)
    # Line 29: An OPLang program consists of many class declarations.
    source = """final int x := 0;"""
    expected = "Error on line 1 col 0: final"
    assert Parser(source).parse() == expected

def test_015():
    # Top-level method (Program Structure)
    # Line 29: An OPLang program consists of many class declarations.
    source = """void main() {}"""
    expected = "Error on line 1 col 0: void"
    assert Parser(source).parse() == expected

def test_016():
    # Top-level declaration (Program Structure)
    # Line 29: An OPLang program consists of many class declarations.
    source = """int a;"""
    expected = "Error on line 1 col 0: int"
    assert Parser(source).parse() == expected

def test_017():
    # Missing class name, immediate '{' (Program Structure)
    # Line 35: Each class declaration starts with the keyword `class` and then an identifier, which is the class name...
    source = """class  {}"""
    expected = "Error on line 1 col 7: {"
    assert Parser(source).parse() == expected

def test_018():
    # Unclosed class body (Separators)
    # Line 35: ... and ends with a nullable list of members enclosed by a pair of curly braces `{}`.
    source = """class A {"""
    expected = "Error on line 1 col 9: <EOF>"
    assert Parser(source).parse() == expected

def test_019():
    # 'class' without name/body (Program Structure)
    # Line 35: Each class declaration starts with the keyword `class` and then an identifier, which is the class name...
    source = """class"""
    expected = "Error on line 1 col 5: <EOF>"
    assert Parser(source).parse() == expected

def test_020():
    # Unexpected token at top-level (Program Structure)
    # Line 29: An OPLang program consists of many class declarations.
    source = """extends"""
    expected = "Error on line 1 col 0: extends"
    assert Parser(source).parse() == expected

def test_021():
    # Attribute: missing identifier after type (Attributes)
    # Line 62: After keywords `static` and `final` if any, an attribute declaration starts with a type, followed by a non-nullable comma-separated list of attribute names and ended with a semicolon.
    source = """class A {int:=5;}"""
    expected = "Error on line 1 col 12: :="
    assert Parser(source).parse() == expected

def test_022():
    # Attribute: trailing comma (Attributes)
    # Line 62: ... followed by a non-nullable comma-separated list of attribute names...
    source = """class A {int a,;}"""
    expected = "Error on line 1 col 15: ;"
    assert Parser(source).parse() == expected

def test_023():
    # Attribute: wrong ':' instead of ':=' (Attributes)
    # Line 62: An attribute name in the list is an identifier optionally followed by an equal and an expression.
    source = """class A {int x: 5;}"""
    expected = "Error on line 1 col 14: :"
    assert Parser(source).parse() == expected

def test_024():
    # Attribute: comma before first identifier (Attributes)
    # Line 62: ... an attribute declaration starts with a type, followed by a non-nullable comma-separated list of attribute names...
    source = """class A {int,x;}"""
    expected = "Error on line 1 col 12: ,"
    assert Parser(source).parse() == expected

def test_025():
    # Attribute: missing comma between identifiers (Attributes)
    # Line 62: ... followed by a non-nullable comma-separated list of attribute names...
    source = """class A {int x y;}"""
    expected = "Error on line 1 col 15: y"
    assert Parser(source).parse() == expected

def test_026():
    # Array declaration: missing size (Array Type)
    # Line 324: In an array declaration, it is required that there must be an integer literal between the two square bracket.
    source = """class A {int[] a;}"""
    expected = "Error on line 1 col 13: ]"
    assert Parser(source).parse() == expected

def test_027():
    # Array declaration: non-integer literal size (Array Type)
    # Line 324: In an array declaration, it is required that there must be an integer literal between the two square bracket.
    source = """class A {int[a] x;}"""
    expected = "Error on line 1 col 13: a"
    assert Parser(source).parse() == expected

def test_028():
    # Array declaration: second dimension not supported (Array Type)
    # Line 315: For simplicity reason, OPLang supports only one-dimensional arrays.
    source = """class A {int[5][5] a;}"""
    expected = "Error on line 1 col 15: ["
    assert Parser(source).parse() == expected

def test_029():
    # Array: '(' instead of '[' (Separators / Array Type)
    # Line 318: <element type>[<size>]
    source = """class A {int(5) a;}"""
    expected = "Error on line 1 col 12: ("
    assert Parser(source).parse() == expected

def test_030():
    # Attribute: modifiers but no identifier (Attributes)
    # Line 62: ... an attribute declaration starts with a type, followed by a non-nullable comma-separated list of attribute names...
    source = """class A {final static int := 0;}"""
    expected = "Error on line 1 col 26: :="
    assert Parser(source).parse() == expected

def test_031():
    # Attribute: missing semicolon (Attributes)
    # Line 62: ... and ended with a semicolon.
    source = """class A {int x}"""
    expected = "Error on line 1 col 14: }"
    assert Parser(source).parse() == expected

def test_032():
    # Array literal: empty (Array Literals require non-null list)
    # Line 277: An **array literal** is non-nullable comma-separated list of literals enclosed by a pair of curly parentheses.
    source = """class A {int[3] a := {};}"""
    expected = "Error on line 1 col 22: }"
    assert Parser(source).parse() == expected

def test_033():
    # Attribute init: missing expression (Attributes)
    # Line 62: An attribute name in the list is an identifier optionally followed by an equal and an expression.
    source = """class A {int x := ;}"""
    expected = "Error on line 1 col 18: ;"
    assert Parser(source).parse() == expected

def test_034():
    # Attribute: leading comma (Attributes)
    # Line 39: A `<member>` may be static, preceded by the keyword `static`, or instance. A member of a class can be either an attribute or a method.
    source = """class A {,int x;}"""
    expected = "Error on line 1 col 9: ,"
    assert Parser(source).parse() == expected

def test_035():
    # Attribute: trailing comma before ';' (Attributes)
    # Line 62: ... followed by a non-nullable comma-separated list of attribute names...
    source = """class A {int x, y,;}"""
    expected = "Error on line 1 col 18: ;"
    assert Parser(source).parse() == expected

def test_036():
    # Attribute: missing identifier after type name (Attributes)
    # Line 62: ... an attribute declaration starts with a type, followed by a non-nullable comma-separated list of attribute names...
    source = """class A {boolean:=true;}"""
    expected = "Error on line 1 col 16: :="
    assert Parser(source).parse() == expected

def test_037():
    # Attribute: modifier without type (Attributes)
    # Line 62: After keywords `static` and `final` if any, an attribute declaration starts with a type...
    source = """class A {final := 0;}"""
    expected = "Error on line 1 col 15: :="
    assert Parser(source).parse() == expected

def test_038():
    # Attribute: modifier without type (Attributes)
    # Line 62: After keywords `static` and `final` if any, an attribute declaration starts with a type...
    source = """class A {static := 0;}"""
    expected = "Error on line 1 col 16: :="
    assert Parser(source).parse() == expected

def test_039():
    # Array declaration: missing closing ']' (Array Type)
    # Line 318: <element type>[<size>]
    source = """class A {int[5a;}"""
    expected = "Error on line 1 col 14: a"
    assert Parser(source).parse() == expected

def test_040():
    # Attribute: missing comma between y and z (Attributes)
    # Line 62: ... followed by a non-nullable comma-separated list of attribute names...
    source = """class A {int x, y z;}"""
    expected = "Error on line 1 col 18: z"
    assert Parser(source).parse() == expected

def test_041():
    # Method: missing '(' (Method declaration)
    # Line 75: <return type> <identifier>(<list of parameters>) <block statement>
    source = """class A {int foo) {}}"""
    expected = "Error on line 1 col 16: )"
    assert Parser(source).parse() == expected

def test_042():
    # Method: missing ')' (Method declaration)
    # Line 75: <return type> <identifier>(<list of parameters>) <block statement>
    source = """class A {int foo( {} }"""
    expected = "Error on line 1 col 18: {"
    assert Parser(source).parse() == expected

def test_043():
    # Method: missing block (Method declaration)
    # Line 75: <return type> <identifier>(<list of parameters>) <block statement>
    source = """class A {int foo();}"""
    expected = "Error on line 1 col 18: ;"
    assert Parser(source).parse() == expected

def test_044():
    # Params: repeated type after comma (semicolon-separated declarations) (Method)
    # Line 84: The `<list of parameters>` is a nullable semicolon-separated list of parameter declaration.
    source = """class A {int foo(int a, int b) {}}"""
    expected = "Error on line 1 col 24: int"
    assert Parser(source).parse() == expected

def test_045():
    # Mixed separators: comma inside a declaration followed by a new type (Method)
    # Line 84: The `<list of parameters>` is a nullable semicolon-separated list of parameter declaration.
    source = """class A {int foo(int a; int b, int c) {}}"""
    expected = "Error on line 1 col 31: int"
    assert Parser(source).parse() == expected

def test_046():
    # Wrong param syntax 'a:int' (Method params are '<type> <id-list>') (Method)
    # Line 87: <type> <identifier-list>
    source = """class A {int foo(a:int) {}}"""
    expected = "Error on line 1 col 18: :"
    assert Parser(source).parse() == expected

def test_047():
    # '&' cannot precede type in params (Method)
    # Line 93: <type> & <identifier-list>
    source = """class A {int foo(& int a) {}}"""
    expected = "Error on line 1 col 17: &"
    assert Parser(source).parse() == expected

def test_048():
    # '&' repeated before second name in a reference param declaration (Method)
    # Line 93: <type> & <identifier-list>
    source = """class A {int foo(int & a, & b) {}}"""
    expected = "Error on line 1 col 26: &"
    assert Parser(source).parse() == expected

def test_049():
    # Trailing semicolon in param list (Method)
    # Line 84: The `<list of parameters>` is a nullable semicolon-separated list of parameter declaration.
    source = """class A {int foo(int a;) {}}"""
    expected = "Error on line 1 col 23: )"
    assert Parser(source).parse() == expected

def test_050():
    # Param list starting with a semicolon (Method)
    # Line 84: The `<list of parameters>` is a nullable semicolon-separated list of parameter declaration.
    source = """class A {int foo(;) {}}"""
    expected = "Error on line 1 col 17: ;"
    assert Parser(source).parse() == expected

def test_051():
    # Double semicolon in param list (Method)
    # Line 84: The `<list of parameters>` is a nullable semicolon-separated list of parameter declaration.
    source = """class A {int foo(int a;; int b) {}}"""
    expected = "Error on line 1 col 23: ;"
    assert Parser(source).parse() == expected

def test_052():
    # Missing identifier list after type (Method params)
    # Line 87: <type> <identifier-list>
    source = """class A {int foo(int) {}}"""
    expected = "Error on line 1 col 20: )"
    assert Parser(source).parse() == expected

def test_053():
    # Missing comma between parameter identifiers (Method params)
    # Line 96: where `<identifier-list>` is a comma-separated list of identifiers of the same type.
    source = """class A {int foo(int a b) {}}"""
    expected = "Error on line 1 col 23: b"
    assert Parser(source).parse() == expected

def test_054():
    # Double '&' in reference return type (Method)
    # Line 81: <type> & <identifier>(<list of parameters>) <block statement>
    source = """class A {int && foo() {}}"""
    expected = "Error on line 1 col 13: &&"
    assert Parser(source).parse() == expected

def test_055():
    # Misplaced '&' after method name (Method)
    # Line 81: <type> & <identifier>(<list of parameters>) <block statement>
    source = """class A {int foo&() {}}"""
    expected = "Error on line 1 col 16: &"
    assert Parser(source).parse() == expected

# def test_056():
#     # Missing return type ('foo' not constructor) (Method)
#     # Line 75: <return type> <identifier>(<list of parameters>) <block statement>
#     source = """class A {foo() {}}"""
#     expected = "Error on line 1 col 9: foo"
#     assert Parser(source).parse() == expected

def test_057():
    # 'static' must be before return type (Method)
    # Line 72: After keyword `static` if any, each method declaration has the form:
    source = """class A {int static foo() {}}"""
    expected = "Error on line 1 col 13: static"
    assert Parser(source).parse() == expected

def test_058():
    # Misordered reference return type tokens (Method)
    # Line 72: After keyword `static` if any, each method declaration has the form:
    source = """class A {static & int foo() {}}"""
    expected = "Error on line 1 col 16: &"
    assert Parser(source).parse() == expected

def test_059():
    # '[' instead of '(' for params (Method)
    # Line 75: <return type> <identifier>(<list of parameters>) <block statement>
    source = """class A {int foo[int a] {}}"""
    expected = "Error on line 1 col 16: ["
    assert Parser(source).parse() == expected

def test_060():
    # Default argument not supported (Method params)
    # Line 87: <type> <identifier-list>
    source = """class A {int foo(int a=3) {}}"""
    expected = "Error Token ="
    assert Parser(source).parse() == expected

def test_061():
    # Unsized array type in params (Array Type)
    # Line 324: In an array declaration, it is required that there must be an integer literal between the two square bracket.
    source = """class A {int foo(int[] a) {}}"""
    expected = "Error on line 1 col 21: ]"
    assert Parser(source).parse() == expected

def test_062():
    # 'final' not allowed in param declaration (Method params)
    # Line 87: <type> <identifier-list>
    source = """class A {int foo(final int a) {}}"""
    expected = "Error on line 1 col 17: final"
    assert Parser(source).parse() == expected

def test_063():
    # Missing identifier after reference '&' (Method params)
    # Line 93: <type> & <identifier-list>
    source = """class A {int foo(string & ) {}}"""
    expected = "Error on line 1 col 26: )"
    assert Parser(source).parse() == expected

def test_064():
    # Trailing comma at end of param declaration (Method params)
    # Line 96: where `<identifier-list>` is a comma-separated list of identifiers of the same type.
    source = """class A {int foo(int a,) {}}"""
    expected = "Error on line 1 col 23: )"
    assert Parser(source).parse() == expected

def test_065():
    # Missing identifier list before ';' (Method params)
    # Line 87: <type> <identifier-list>
    source = """class A {int foo(int; a) {}}"""
    expected = "Error on line 1 col 20: ;"
    assert Parser(source).parse() == expected

def test_066():
    # Double ';' between parameter declarations (Method params)
    # Line 84: The `<list of parameters>` is a nullable semicolon-separated list of parameter declaration.
    source = """class A {int foo(int a; ; int b) {}}"""
    expected = "Error on line 1 col 24: ;"
    assert Parser(source).parse() == expected

def test_067():
    # Missing identifier after '&' (Method params)
    # Line 93: <type> & <identifier-list>
    source = """class A {int foo(int & ) {}}"""
    expected = "Error on line 1 col 23: )"
    assert Parser(source).parse() == expected

def test_068():
    # 'class' keyword used as method name without return type (Method)
    # Line 191: The following character sequences are reserved as keywords and cannot be used as identifiers:
    source = """class A {class() {}}"""
    expected = "Error on line 1 col 9: class"
    assert Parser(source).parse() == expected

def test_069():
    # '~' cannot start method name (Destructor syntax is separate) (Method)
    # Line 146: Has no return type
    source = """class A {int ~A() {}}"""
    expected = "Error on line 1 col 13: ~"
    assert Parser(source).parse() == expected

def test_070():
    # Double '&' in static reference return type (Method)
    # Line 81: <type> & <identifier>(<list of parameters>) <block statement>
    source = """class A {static int && foo() {}}"""
    expected = "Error on line 1 col 20: &&"
    assert Parser(source).parse() == expected

# def test_071():
#     # Constructor name must match class (Constructor)
#     # Line 130: - Have the same name as the class
#     source = """class A {B() {}}"""
#     expected = "Error on line 1 col 9: B"
#     assert Parser(source).parse() == expected

def test_072():
    # Constructor missing '(' (Constructor)
    # Line 112: <identifier>() <block statement>
    source = """class A {A{}}"""
    expected = "Error on line 1 col 10: {"
    assert Parser(source).parse() == expected

def test_073():
    # Constructor missing block (Constructor)
    # Line 112: <identifier>() <block statement>
    source = """class A {A() ;}"""
    expected = "Error on line 1 col 13: ;"
    assert Parser(source).parse() == expected

def test_074():
    # 'static' constructor not allowed (Constructor)
    # Line 112: <identifier>() <block statement>
    source = """class A {static A() {}}"""
    expected = "Error on line 1 col 17: ("
    assert Parser(source).parse() == expected

def test_075():
    # Wrong param syntax 'x:int' (Constructor params)
    # Line 87: <type> <identifier-list>
    source = """class A {A(x:int) {}}"""
    expected = "Error on line 1 col 12: :"
    assert Parser(source).parse() == expected

def test_076():
    # Repeated type after comma in single declaration (Constructor params)
    # Line 84: The `<list of parameters>` is a nullable semicolon-separated list of parameter declaration.
    source = """class A {A(int x, int y) {}}"""
    expected = "Error on line 1 col 18: int"
    assert Parser(source).parse() == expected

def test_077():
    # Param list with just ';' (Constructor)
    # Line 84: The `<list of parameters>` is a nullable semicolon-separated list of parameter declaration.
    source = """class A {A(;) {}}"""
    expected = "Error on line 1 col 11: ;"
    assert Parser(source).parse() == expected

def test_078():
    # Missing identifier before ';' (Constructor params)
    # Line 87: <type> <identifier-list>
    source = """class A {A(int; float y) {}}"""
    expected = "Error on line 1 col 14: ;"
    assert Parser(source).parse() == expected

def test_079():
    # Double ';' between parameter declarations (Constructor params)
    # Line 84: The `<list of parameters>` is a nullable semicolon-separated list of parameter declaration.
    source = """class A {A(int x;; int y) {}}"""
    expected = "Error on line 1 col 17: ;"
    assert Parser(source).parse() == expected

def test_080():
    # Missing identifier after '&' (Constructor params)
    # Line 93: <type> & <identifier-list>
    source = """class A {A(int & ) {}}"""
    expected = "Error on line 1 col 17: )"
    assert Parser(source).parse() == expected

def test_081():
    # '[' instead of '(' (Constructor)
    # Line 112: <identifier>() <block statement>
    source = """class A {A[int x] {}}"""
    expected = "Error on line 1 col 11: int"
    assert Parser(source).parse() == expected

def test_082():
    # Missing type after semicolon in params (Constructor)
    # Line 84: The `<list of parameters>` is a nullable semicolon-separated list of parameter declaration.
    source = """class A {A( int length; width ) {}}"""
    expected = "Error on line 1 col 30: )"
    assert Parser(source).parse() == expected

def test_083():
    # ')' instead of '(' (Constructor)
    # Line 112: <identifier>() <block statement>
    source = """class A {A) {}}"""
    expected = "Error on line 1 col 10: )"
    assert Parser(source).parse() == expected

def test_084():
    # '{' inside parameter list (Constructor)
    # Line 126: <identifier>(<list of parameters>) <block statement>
    source = """class A {A( {} }"""
    expected = "Error on line 1 col 12: {"
    assert Parser(source).parse() == expected

def test_085():
    # Trailing comma in param declaration (Constructor)
    # Line 96: where `<identifier-list>` is a comma-separated list of identifiers of the same type.
    source = """class A {A(int a,) {}}"""
    expected = "Error on line 1 col 17: )"
    assert Parser(source).parse() == expected

def test_086():
    # Double ',' in param declaration (Constructor)
    # Line 96: where `<identifier-list>` is a comma-separated list of identifiers of the same type.
    source = """class A {A(int a,, int b) {}}"""
    expected = "Error on line 1 col 17: ,"
    assert Parser(source).parse() == expected

def test_087():
    # Unsized array in params (Array Type)
    # Line 324: In an array declaration, it is required that there must be an integer literal between the two square bracket.
    source = """class A {A(int[] a) {}}"""
    expected = "Error on line 1 col 15: ]"
    assert Parser(source).parse() == expected

def test_088():
    # Leading '&' in params (Constructor)
    # Line 93: <type> & <identifier-list>
    source = """class A {A(& int a){}}"""
    expected = "Error on line 1 col 11: &"
    assert Parser(source).parse() == expected

def test_089():
    # Extra semicolons in params (Constructor)
    # Line 84: The `<list of parameters>` is a nullable semicolon-separated list of parameter declaration.
    source = """class A {A(float length, width; ; ) {}}"""
    expected = "Error on line 1 col 32: ;"
    assert Parser(source).parse() == expected

def test_090():
    # 'new' expression where type is expected (Constructor params)
    # Line 87: <type> <identifier-list>
    source = """class A {A(new B()) {}}"""
    expected = "Error on line 1 col 11: new"
    assert Parser(source).parse() == expected

def test_091():
    # Destructor must have no params (Destructor)
    # Line 145: - Takes no parameters
    source = """class A {~A(int x) {}}"""
    expected = "Error on line 1 col 12: int"
    assert Parser(source).parse() == expected

# def test_092():
#     # Destructor name must match class (Destructor)
#     # Line 144: - Has the same name as the class preceded by `~`
#     source = """class A {~B() {}}"""
#     expected = "Error on line 1 col 10: B"
#     assert Parser(source).parse() == expected

def test_093():
    # 'static' before destructor (Destructor)
    # Line 140: ~<identifier>() <block statement>
    source = """class A {static ~A() {}}"""
    expected = "Error on line 1 col 16: ~"
    assert Parser(source).parse() == expected

def test_094():
    # Missing '()' after destructor name (Destructor)
    # Line 140: ~<identifier>() <block statement>
    source = """class A {~A{}}"""
    expected = "Error on line 1 col 11: {"
    assert Parser(source).parse() == expected

def test_095():
    # Destructor missing block (Destructor)
    # Line 140: ~<identifier>() <block statement>
    source = """class A {~A() ;}"""
    expected = "Error on line 1 col 14: ;"
    assert Parser(source).parse() == expected

def test_096():
    # Extra ')' in destructor (Destructor)
    # Line 140: ~<identifier>() <block statement>
    source = """class A {~A()) {}}"""
    expected = "Error on line 1 col 13: )"
    assert Parser(source).parse() == expected

def test_097():
    # ';' inside '()' of destructor (Destructor)
    # Line 145: - Takes no parameters
    source = """class A {~A(;) {}}"""
    expected = "Error on line 1 col 12: ;"
    assert Parser(source).parse() == expected

def test_098():
    # Trailing comma in destructor '()' (Destructor)
    # Line 145: - Takes no parameters
    source = """class A {~A( int a, ) {}}"""
    expected = "Error on line 1 col 13: int"
    assert Parser(source).parse() == expected

def test_099():
    # '[' instead of '(' (Destructor)
    # Line 140: ~<identifier>() <block statement>
    source = """class A {~A[int a] {}}"""
    expected = "Error on line 1 col 11: ["
    assert Parser(source).parse() == expected

def test_100():
    # ')' instead of '(' (Destructor)
    # Line 140: ~<identifier>() <block statement>
    source = """class A {~A) {}}"""
    expected = "Error on line 1 col 11: )"
    assert Parser(source).parse() == expected

def test_101():
    # Assignment: 'this' not a valid LHS (Assignment)
    # Line 552: where the value returned by the `<expression>` is stored in the `<lhs>`, which can be a local variable, a mutable attribute, an element of an array, or a reference.
    source = """class A {void main(){this := 1;}}"""
    expected = "Error on line 1 col 26: :="
    assert Parser(source).parse() == expected

def test_102():
    # Assignment: literal on LHS (Assignment)
    # Line 552: where the value returned by the `<expression>` is stored in the `<lhs>`, which can be a local variable, a mutable attribute, an element of an array, or a reference.
    source = """class A {void main(){5 := x;}}"""
    expected = "Error on line 1 col 23: :="
    assert Parser(source).parse() == expected

def test_103():
    # Bad assignment operator tokens separated (Assignment)
    # Line 549: <lhs> := <expression>;
    source = """class A {void main(){a : = 1;}}"""
    expected = "Error Token ="
    assert Parser(source).parse() == expected

# def test_104():
#     # Return requires an expression (Return statement)
#     # Line 625: return <expression>;
#     source = """class A {void main(){return;}}"""
#     expected = "Error on line 1 col 28: ;"
#     assert Parser(source).parse() == expected

def test_105():
    # If: missing condition (If)
    # Line 574: if <expression> then <statement> [else <statement>]
    source = """class A {void main(){if then break;}}"""
    expected = "Error on line 1 col 24: then"
    assert Parser(source).parse() == expected

def test_106():
    # If: 'do' instead of 'then' (If)
    # Line 574: if <expression> then <statement> [else <statement>]
    source = """class A {void main(){if (x) do break;}}"""
    expected = "Error on line 1 col 28: do"
    assert Parser(source).parse() == expected

def test_107():
    # If: missing statement after 'then' (If)
    # Line 574: if <expression> then <statement> [else <statement>]
    source = """class A {void main(){if (x) then}}"""
    expected = "Error on line 1 col 32: }"
    assert Parser(source).parse() == expected

def test_108():
    # If: 'else' where a 'then' statement expected (If)
    # Line 574: if <expression> then <statement> [else <statement>]
    source = """class A {void main(){if x then else break;}}"""
    expected = "Error on line 1 col 31: else"
    assert Parser(source).parse() == expected

def test_109():
    # Break: missing semicolon (Break)
    # Line 615: break;
    source = """class A {void main(){break}}"""
    expected = "Error on line 1 col 26: }"
    assert Parser(source).parse() == expected

def test_110():
    # Continue: extra token before semicolon (Continue)
    # Line 620: continue;
    source = """class A {void main(){continue x;}}"""
    expected = "Error on line 1 col 30: x"
    assert Parser(source).parse() == expected

def test_111():
    # Method invocation requires receiver or class (Member access)
    # Line 629: A **method invocation statement** is an instance/static method invocation...
    source = """class A {void main(){foo();}}"""
    expected = "Error on line 1 col 24: ("
    assert Parser(source).parse() == expected

def test_112():
    # Arguments list cannot start with ';' (Method invocation)
    # Line 441: The `<list of expressions>` is the comma-separated list of arguments, which are expressions.
    source = """class A {void main(){A.foo(;);}}"""
    expected = "Error on line 1 col 27: ;"
    assert Parser(source).parse() == expected

def test_113():
    # Index: missing inner expression (Index)
    # Line 405: <expression>[expression]
    source = """class A {void main(){a[] := 1;}}"""
    expected = "Error on line 1 col 23: ]"
    assert Parser(source).parse() == expected

def test_114():
    # Index: comma inside brackets (Index)
    # Line 405: <expression>[expression]
    source = """class A {void main(){a[1,2] := 3;}}"""
    expected = "Error on line 1 col 24: ,"
    assert Parser(source).parse() == expected

def test_115():
    # 'new' requires class name + () (Object creation)
    # Line 453: new <identifier>(<list of expressions>)
    source = """class A {void main(){x := new A;}}"""
    expected = "Error on line 1 col 31: ;"
    assert Parser(source).parse() == expected

def test_116():
    # 'new' call: bad args list (Object creation)
    # Line 456: The `<list of expressions>` is the comma-separated list of arguments.
    source = """class A {void main(){x := new A(;);}}"""
    expected = "Error on line 1 col 32: ;"
    assert Parser(source).parse() == expected

def test_117():
    # 'new' must be followed by identifier (Object creation)
    # Line 453: new <identifier>(<list of expressions>)
    source = """class A {void main(){x := new 123();}}"""
    expected = "Error on line 1 col 30: 123"
    assert Parser(source).parse() == expected

def test_118():
    # 'new' requires '(<args>)' (Object creation)
    # Line 453: new <identifier>(<list of expressions>)
    source = """class A {void main(){x := new ();}}"""
    expected = "Error on line 1 col 30: ("
    assert Parser(source).parse() == expected

def test_119():
    # Member access: dot must be followed by identifier (Member access)
    # Line 427: <expression>.<identifier>
    source = """class A {void main(){x := A.();}}"""
    expected = "Error on line 1 col 28: ("
    assert Parser(source).parse() == expected

def test_120():
    # Binary operator missing RHS (Expressions)
    # Line 361: Unary operations work with one operand and binary operations work with two operands.
    source = """class A {void main(){x := (1 + );}}"""
    expected = "Error on line 1 col 31: )"
    assert Parser(source).parse() == expected

def test_121():
    # Member access: trailing dot (Member access)
    # Line 427: <expression>.<identifier>
    source = """class A {void main(){x := a.;}}"""
    expected = "Error on line 1 col 28: ;"
    assert Parser(source).parse() == expected

def test_122():
    # Member access: double dot (Member access)
    # Line 427: <expression>.<identifier>
    source = """class A {void main(){x := a..b;}}"""
    expected = "Error on line 1 col 28: ."
    assert Parser(source).parse() == expected

def test_123():
    # Index: missing ']' before ':=' (Index)
    # Line 405: <expression>[expression]
    source = """class A {void main(){a[1 := 2;}}"""
    expected = "Error on line 1 col 25: :="
    assert Parser(source).parse() == expected

def test_124():
    # Empty parentheses as expression (Expressions)
    # Line 361: **Expressions** are constructs which are made up of operators and operands.
    source = """class A {void main(){x := ();}}"""
    expected = "Error on line 1 col 27: )"
    assert Parser(source).parse() == expected

def test_125():
    # Bad bracket/paren ordering (Index)
    # Line 405: <expression>[expression]
    source = """class A {void main(){x := a[1)];}}"""
    expected = "Error on line 1 col 29: )"
    assert Parser(source).parse() == expected

def test_126():
    # Comma inside parenthesized expression (Expressions)
    # Line 361: **Expressions** are constructs which are made up of operators and operands.
    source = """class A {void main(){x := a[(1,2)];}}"""
    expected = "Error on line 1 col 30: ,"
    assert Parser(source).parse() == expected

def test_127():
    # Non-associative relational chaining: '<' (Precedence/Associativity)
    # Line 493: `<`, `>`, `<=`, `>=` | none
    source = """class A {int z := 1 < 2 < 3;}"""
    expected = "Error on line 1 col 24: <"
    assert Parser(source).parse() == expected

def test_128():
    # Non-associative relational chaining: '==' (Precedence/Associativity)
    # Line 492: `==`, `!=` | none
    source = """class A {int z := a == b == c;}"""
    expected = "Error on line 1 col 25: =="
    assert Parser(source).parse() == expected

def test_129():
    # Non-associative relational chaining: '>=' (Precedence/Associativity)
    # Line 493: `<`, `>`, `<=`, `>=` | none
    source = """class A {int z := a >= b >= c;}"""
    expected = "Error on line 1 col 25: >="
    assert Parser(source).parse() == expected

def test_130():
    # Non-associative relational chaining: '!=' twice (Precedence/Associativity)
    # Line 492: `==`, `!=` | none
    source = """class A {int z := 1.0 != a * 3 != c;}"""
    expected = "Error on line 1 col 31: !="
    assert Parser(source).parse() == expected

def test_131():
    # Mixed non-associative chain: '<' then '<=' (Precedence/Associativity)
    # Line 493: `<`, `>`, `<=`, `>=` | none
    source = """class A {int z := a < b <= c;}"""
    expected = "Error on line 1 col 24: <="
    assert Parser(source).parse() == expected

def test_132():
    # Mixed non-associative chain: '==' then '!=' (Precedence/Associativity)
    # Line 492: `==`, `!=` | none
    source = """class A {boolean z := a == b != c;}"""
    expected = "Error on line 1 col 29: !="
    assert Parser(source).parse() == expected

def test_133():
    # Non-associative relational chaining: '>' (Precedence/Associativity)
    # Line 493: `<`, `>`, `<=`, `>=` | none
    source = """class A {int z := a > b > c;}"""
    expected = "Error on line 1 col 24: >"
    assert Parser(source).parse() == expected

def test_134():
    # For: missing 'do' before statement (For)
    # Line 591: for <scalar variable> := <expression1> (to|downto) <expression2> do <statement>
    source = """class A {void main(){for i := 1 to 10 {}}}"""
    expected = "Error on line 1 col 38: {"
    assert Parser(source).parse() == expected

def test_135():
    # For: missing 'to/downto' (For)
    # Line 591: for <scalar variable> := <expression1> (to|downto) <expression2> do <statement>
    source = """class A {void main(){for i := 1 10 to do break;}}"""
    expected = "Error on line 1 col 32: 10"
    assert Parser(source).parse() == expected

def test_136():
    # For: missing start expression (For)
    # Line 591: for <scalar variable> := <expression1> (to|downto) <expression2> do <statement>
    source = """class A {void main(){for i := to 10 do break;}}"""
    expected = "Error on line 1 col 30: to"
    assert Parser(source).parse() == expected

def test_137():
    # For: missing end expression (For)
    # Line 591: for <scalar variable> := <expression1> (to|downto) <expression2> do <statement>
    source = """class A {void main(){for i := 1 downto do break;}}"""
    expected = "Error on line 1 col 39: do"
    assert Parser(source).parse() == expected

def test_138():
    # For: 'then' instead of 'do' (For)
    # Line 591: for <scalar variable> := <expression1> (to|downto) <expression2> do <statement>
    source = """class A {void main(){for i := 1 to 10 then break;}}"""
    expected = "Error on line 1 col 38: then"
    assert Parser(source).parse() == expected

def test_139():
    # For: missing loop variable (For)
    # Line 591: for <scalar variable> := <expression1> (to|downto) <expression2> do <statement>
    source = """class A {void main(){for := 1 to 10 do break;}}"""
    expected = "Error on line 1 col 25: :="
    assert Parser(source).parse() == expected

def test_140():
    # For: missing statement after 'do' (For)
    # Line 591: for <scalar variable> := <expression1> (to|downto) <expression2> do <statement>
    source = """class A {void main(){for i := 1 to 10 do}}"""
    expected = "Error on line 1 col 40: }"
    assert Parser(source).parse() == expected

def test_141():
    # For: invalid direction keyword 'up' (For)
    # Line 591: for <scalar variable> := <expression1> (to|downto) <expression2> do <statement>
    source = """class A {void main(){for i := 1 up 10 do break;}}"""
    expected = "Error on line 1 col 32: up"
    assert Parser(source).parse() == expected

def test_142():
    # For: empty statement not allowed (For)
    # Line 591: for <scalar variable> := <expression1> (to|downto) <expression2> do <statement>
    source = """class A {void main(){for i := 1 to 10 do ;}}"""
    expected = "Error on line 1 col 41: ;"
    assert Parser(source).parse() == expected

def test_143():
    # Member access: '.' before identifier (Member access)
    # Line 439: <expression>.<identifier>(<list of expressions>)
    source = """class A {void main(){A.(x);}}"""
    expected = "Error on line 1 col 23: ("
    assert Parser(source).parse() == expected

def test_144():
    # Member access: double dot (Member access)
    # Line 445: <identifier>.<identifier>(<list of expressions>)
    source = """class A {void main(){A..foo();}}"""
    expected = "Error on line 1 col 23: ."
    assert Parser(source).parse() == expected

def test_145():
    # Member access: '.' then '(' after 'this' (Member access)
    # Line 439: <expression>.<identifier>(<list of expressions>)
    source = """class A {void main(){this.(x);}}"""
    expected = "Error on line 1 col 26: ("
    assert Parser(source).parse() == expected

def test_146():
    # Arguments separated by ';' (Method invocation)
    # Line 441: The `<list of expressions>` is the comma-separated list of arguments, which are expressions.
    source = """class A {void main(){A.foo(1;2);}}"""
    expected = "Error on line 1 col 28: ;"
    assert Parser(source).parse() == expected

def test_147():
    # Leading comma in arguments (Method invocation)
    # Line 441: The `<list of expressions>` is the comma-separated list of arguments, which are expressions.
    source = """class A {void main(){A.foo(,1);}}"""
    expected = "Error on line 1 col 27: ,"
    assert Parser(source).parse() == expected

def test_148():
    # Trailing comma in arguments (Method invocation)
    # Line 441: The `<list of expressions>` is the comma-separated list of arguments, which are expressions.
    source = """class A {void main(){A.foo(1,);}}"""
    expected = "Error on line 1 col 29: )"
    assert Parser(source).parse() == expected

def test_149():
    # Missing '(' after method name (Method invocation)
    # Line 439: <expression>.<identifier>(<list of expressions>)
    source = """class A {void main(){A.foo 1);}}"""
    expected = "Error on line 1 col 27: 1"
    assert Parser(source).parse() == expected

def test_150():
    # Comma inside parenthesized sub-expression (Method invocation args)
    # Line 441: The `<list of expressions>` is the comma-separated list of arguments, which are expressions.
    source = """class A {void main(){A.foo((1,2));}}"""
    expected = "Error on line 1 col 29: ,"
    assert Parser(source).parse() == expected

def test_151():
    # If: empty condition parentheses (If)
    # Line 574: if <expression> then <statement> [else <statement>]
    source = """class A {void main(){if () then break;}}"""
    expected = "Error on line 1 col 25: )"
    assert Parser(source).parse() == expected

def test_152():
    # If: else without statement (If)
    # Line 574: if <expression> then <statement> [else <statement>]
    source = """class A {void main(){if x then break else}}"""
    expected = "Error on line 1 col 37: else"
    assert Parser(source).parse() == expected

def test_153():
    # If: then without statement (If)
    # Line 574: if <expression> then <statement> [else <statement>]
    source = """class A {void main(){if (x) then}}"""
    expected = "Error on line 1 col 32: }"
    assert Parser(source).parse() == expected

def test_154():
    # If: missing 'then' (If)
    # Line 574: if <expression> then <statement> [else <statement>]
    source = """class A {void main(){if (x) break;}}"""
    expected = "Error on line 1 col 28: break"
    assert Parser(source).parse() == expected

def test_155():
    # If condition uses chained relational (non-associative) (If/Precedence)
    # Line 493: `<`, `>`, `<=`, `>=` | none
    source = """class A {void main(){if x < y < z then break;}}"""
    expected = "Error on line 1 col 30: <"
    assert Parser(source).parse() == expected

def test_156():
    # Array literal: trailing comma with missing element (Array Literals)
    # Line 277: An **array literal** is non-nullable comma-separated list of literals enclosed by a pair of curly parentheses.
    source = """class A {int[3] a := {1,};}"""
    expected = "Error on line 1 col 24: }"
    assert Parser(source).parse() == expected

def test_157():
    # Array literal: missing comma between elements (Array Literals)
    # Line 277: An **array literal** is non-nullable comma-separated list of literals enclosed by a pair of curly parentheses.
    source = """class A {int[3] a := {1 2};}"""
    expected = "Error on line 1 col 24: 2"
    assert Parser(source).parse() == expected

def test_158():
    # Array literal: illegal ';' inside (Array Literals)
    # Line 277: An **array literal** is non-nullable comma-separated list of literals enclosed by a pair of curly parentheses.
    source = """class A {int[3] a := {;};}"""
    expected = "Error on line 1 col 22: ;"
    assert Parser(source).parse() == expected

def test_159():
    # Unterminated array literal (Array Literals)
    # Line 277: An **array literal** is non-nullable comma-separated list of literals enclosed by a pair of curly parentheses.
    source = """class A {int[3] a := {"""
    expected = "Error on line 1 col 22: <EOF>"
    assert Parser(source).parse() == expected

def test_160():
    # Array literal: double comma (Array Literals)
    # Line 277: An **array literal** is non-nullable comma-separated list of literals enclosed by a pair of curly parentheses.
    source = """class A {int[3] a := {1,,2};}"""
    expected = "Error on line 1 col 24: ,"
    assert Parser(source).parse() == expected

def test_161():
    # Array literal: missing comma (Array Literals)
    # Line 277: An **array literal** is non-nullable comma-separated list of literals enclosed by a pair of curly parentheses.
    source = """class A {int[3] a := {1, 2 3};}"""
    expected = "Error on line 1 col 27: 3"
    assert Parser(source).parse() == expected

def test_162():
    # Array literal: no commas at all (Array Literals)
    # Line 277: An **array literal** is non-nullable comma-separated list of literals enclosed by a pair of curly parentheses.
    source = """class A {int[3] a := {1 2 3};}"""
    expected = "Error on line 1 col 24: 2"
    assert Parser(source).parse() == expected

def test_163():
    # Array literal: trailing comma at end (Array Literals)
    # Line 277: An **array literal** is non-nullable comma-separated list of literals enclosed by a pair of curly parentheses.
    source = """class A {int[3] a := {1, 2, 3,};}"""
    expected = "Error on line 1 col 30: }"
    assert Parser(source).parse() == expected

# def test_164():
#     # Array literal: nested array literal not allowed (Array Literals)
#     # Line 277: The literals in the list can be in any type except the array type...
#     source = """class A {int[3] a := {{1}, {2}, {3}};}"""
#     expected = "Error on line 1 col 24: {"
#     assert Parser(source).parse() == expected

def test_165():
    # Array literal: double comma then close (Array Literals)
    # Line 277: An **array literal** is non-nullable comma-separated list of literals enclosed by a pair of curly parentheses.
    source = """class A {int[3] a := {1,,};}"""
    expected = "Error on line 1 col 24: ,"
    assert Parser(source).parse() == expected

def test_166():
    # Block: declarations must precede statements (Block Statements)
    # Line 530: Between the two parentheses, there may be a nullable list of statements preceded by a nullable list of mutable/immutable variable declarations which are written like mutable/immutable attribute without keyword static.
    source = """class A {void main(){x := 1; int x;}}"""
    expected = "Error on line 1 col 29: int"
    assert Parser(source).parse() == expected

def test_167():
    # Unsized array in local declaration (Array Type)
    # Line 324: In an array declaration, it is required that there must be an integer literal between the two square bracket.
    source = """class A {void main(){int x; int[] a;}}"""
    expected = "Error on line 1 col 32: ]"
    assert Parser(source).parse() == expected

def test_168():
    # Block decl: 'final' without type (Block Statements/Attributes)
    # Line 530: ...variable declarations which are written like mutable/immutable attribute without keyword **static**.
    source = """class A {void main(){int[5] a; final := 1;}}"""
    expected = "Error on line 1 col 37: :="
    assert Parser(source).parse() == expected

def test_169():
    # Arguments typed with ':' (not allowed in calls) (IO prototypes are docs only)
    # Line 441: The `<list of expressions>` is the comma-separated list of arguments, which are expressions.
    source = """class A {void main(){io.writeInt(anArg:int);}}"""
    expected = "Error on line 1 col 38: :"
    assert Parser(source).parse() == expected

# def test_170():
#     # LHS cannot be parenthesized expression (Assignment)
#     # Line 552: ... <lhs>, which can be a local variable, a mutable attribute, an element of an array, or a reference.
#     source = """class A {void main(){(x) := 1;}}"""
#     expected = "Error on line 1 col 22: ("
#     assert Parser(source).parse() == expected

def test_171():
    # LHS cannot start with '[' (Assignment)
    # Line 552: ... <lhs>, which can be a local variable, a mutable attribute, an element of an array, or a reference.
    source = """class A {void main(){[x] := 1;}}"""
    expected = "Error on line 1 col 21: ["
    assert Parser(source).parse() == expected

def test_172():
    # LHS cannot start with '.' (Assignment)
    # Line 552: ... <lhs>, which can be a local variable, a mutable attribute, an element of an array, or a reference.
    source = """class A {void main(){.x := 1;}}"""
    expected = "Error on line 1 col 21: ."
    assert Parser(source).parse() == expected

def test_173():
    # Member access: missing identifier after dot in LHS (Assignment)
    # Line 427: <expression>.<identifier>
    source = """class A {void main(){A.:=1;}}"""
    expected = "Error on line 1 col 23: :="
    assert Parser(source).parse() == expected

def test_174():
    # Member access: trailing dot before ':=' (Assignment)
    # Line 427: <expression>.<identifier>
    source = """class A {void main(){a.b.:=1;}}"""
    expected = "Error on line 1 col 25: :="
    assert Parser(source).parse() == expected

def test_175():
    # Expression-only statement 'new A();' is not a statement kind (Statements)
    # Line 526: A statement, which does not return anything, indicates the action a program performs.
    source = """class A {void main(){new A();}}"""
    expected = "Error on line 1 col 28: ;"
    assert Parser(source).parse() == expected

def test_176():
    # 'new new A()' invalid (Object creation)
    # Line 453: new <identifier>(<list of expressions>)
    source = """class A {void main(){x := new new A();}}"""
    expected = "Error on line 1 col 30: new"
    assert Parser(source).parse() == expected

def test_177():
    # 'new A)()' mismatched paren (Object creation)
    # Line 453: new <identifier>(<list of expressions>)
    source = """class A {void main(){x := new A)();}}"""
    expected = "Error on line 1 col 31: )"
    assert Parser(source).parse() == expected

def test_178():
    # '!' without operand (Expressions)
    # Line 361: Unary operations work with one operand...
    source = """class A {void main(){x := !;}}"""
    expected = "Error on line 1 col 27: ;"
    assert Parser(source).parse() == expected

def test_179():
    # '^' missing RHS (String Expression)
    # Line 361: ...binary operations work with two operands.
    source = """class A {void main(){x := a ^ ;}}"""
    expected = "Error on line 1 col 30: ;"
    assert Parser(source).parse() == expected

def test_180():
    # '&&' missing RHS (Boolean Expression)
    # Line 361: ...binary operations work with two operands.
    source = """class A {void main(){x := a && ;}}"""
    expected = "Error on line 1 col 31: ;"
    assert Parser(source).parse() == expected

def test_181():
    # '(' with no expression (Expressions)
    # Line 361: **Expressions** are constructs which are made up of operators and operands.
    source = """class A {void main(){x := ( ;}}"""
    expected = "Error on line 1 col 28: ;"
    assert Parser(source).parse() == expected

def test_182():
    # ')' unexpected (Expressions)
    # Line 361: **Expressions** are constructs which are made up of operators and operands.
    source = """class A {void main(){x := );}}"""
    expected = "Error on line 1 col 26: )"
    assert Parser(source).parse() == expected

def test_183():
    # '[' starting an expression (Expressions)
    # Line 361: **Expressions** are constructs which are made up of operators and operands.
    source = """class A {void main(){x := [1];}}"""
    expected = "Error on line 1 col 26: ["
    assert Parser(source).parse() == expected

def test_184():
    # Invalid 'do' in block where statement expected (Block/For)
    # Line 530: ...there may be a nullable list of statements...
    source = """class A {void main(){if (x) then { int y do; }}}"""
    expected = "Error on line 1 col 41: do"
    assert Parser(source).parse() == expected

def test_185():
    # 'return new;' incomplete 'new' (Object creation/Return)
    # Line 453: new <identifier>(<list of expressions>)
    source = """class A {void main(){return new;}}"""
    expected = "Error on line 1 col 31: ;"
    assert Parser(source).parse() == expected

def test_186():
    # Non-associative '!=' chained in a statement (Precedence/Associativity)
    # Line 492: `==`, `!=` | none
    source = """class A {void main(){x := a != b != c;}}"""
    expected = "Error on line 1 col 33: !="
    assert Parser(source).parse() == expected

def test_187():
    # Non-associative '<=' chained (Precedence/Associativity)
    # Line 493: `<`, `>`, `<=`, `>=` | none
    source = """class A {void main(){x := a <= b <= c;}}"""
    expected = "Error on line 1 col 33: <="
    assert Parser(source).parse() == expected

def test_188():
    # 'new' missing identifier (Object creation)
    # Line 453: new <identifier>(<list of expressions>)
    source = """class A {void main(){x := new;}}"""
    expected = "Error on line 1 col 29: ;"
    assert Parser(source).parse() == expected

def test_189():
    # 'new A(1,)' trailing comma (Object creation)
    # Line 456: The `<list of expressions>` is the comma-separated list of arguments.
    source = """class A {void main(){x := new A(1,);}}"""
    expected = "Error on line 1 col 34: )"
    assert Parser(source).parse() == expected

def test_190():
    # 'new A(,1)' leading comma (Object creation)
    # Line 456: The `<list of expressions>` is the comma-separated list of arguments.
    source = """class A {void main(){x := new A(,1);}}"""
    expected = "Error on line 1 col 32: ,"
    assert Parser(source).parse() == expected

def test_191():
    # 'new A(1;2)' semicolon in args (Object creation)
    # Line 456: The `<list of expressions>` is the comma-separated list of arguments.
    source = """class A {void main(){x := new A(1;2);}}"""
    expected = "Error on line 1 col 33: ;"
    assert Parser(source).parse() == expected

def test_192():
    # Member access with empty identifier after dot in expression (Member access)
    # Line 427: <expression>.<identifier>
    source = """class A {void main(){x := a.();}}"""
    expected = "Error on line 1 col 28: ("
    assert Parser(source).parse() == expected

def test_193():
    # Expression starting with '.' (Expressions)
    # Line 361: **Expressions** are constructs which are made up of operators and operands.
    source = """class A {void main(){x := .a();}}"""
    expected = "Error on line 1 col 26: ."
    assert Parser(source).parse() == expected

def test_194():
    # Return with illegal parenthesized ';' (Return/Expressions)
    # Line 625: return <expression>;
    source = """class A {void main(){return (;);}}"""
    expected = "Error on line 1 col 29: ;"
    assert Parser(source).parse() == expected

def test_195():
    # Double 'do' after 'do' in for (For)
    # Line 591: for <scalar variable> := <expression1> (to|downto) <expression2> do <statement>
    source = """class A {void main(){for i := 1 to 2 do do;}}"""
    expected = "Error on line 1 col 40: do"
    assert Parser(source).parse() == expected

def test_196():
    # If missing condition in for-body (For + If)
    # Line 574: if <expression> then <statement> [else <statement>]
    source = """class A {void main(){for i := 1 downto 0 do if then break;}}"""
    expected = "Error on line 1 col 47: then"
    assert Parser(source).parse() == expected

def test_197():
    # For missing start expression in nested context (For)
    # Line 591: for <scalar variable> := <expression1> (to|downto) <expression2> do <statement>
    source = """class A {void main(){if (x) then for i := to 10 do break;}}"""
    expected = "Error on line 1 col 42: to"
    assert Parser(source).parse() == expected

def test_198():
    # 'else' at block start (If)
    # Line 574: if <expression> then <statement> [else <statement>]
    source = """class A {void main(){else break;}}"""
    expected = "Error on line 1 col 21: else"
    assert Parser(source).parse() == expected

def test_199():
    # For missing 'do' before statement (For)
    # Line 591: for <scalar variable> := <expression1> (to|downto) <expression2> do <statement>
    source = """class A {void main(){for i := 1 to 2 return 1;}}"""
    expected = "Error on line 1 col 37: return"
    assert Parser(source).parse() == expected

def test_200():
    # Extra tokens after program end (Program Structure)
    # Line 29: An OPLang program consists of many class declarations.
    source = """class A {void main(){}} garbage"""
    expected = "Error on line 1 col 24: garbage"
    assert Parser(source).parse() == expected


def test_201():
    """Test final attribute declaration"""
    source = """class Constants { final float PI := 3.14159; static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_202():
    """Test if-else statement"""
    source = """class Test {
        static void main() {
            if (x > 0) then {
                io.writeStrLn("positive");
            } else {
                io.writeStrLn("negative");
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_203():
    """Test array declaration and access"""
    source = """class Test {
        static void main() {
            int[3] arr := {1, 2, 3};
            int first;
            first := arr[0];
            arr[1] := 42;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_204():
    """Test string concatenation and object creation"""
    source = """class Test {
        static void main() {
            string result;
            Test obj;
            result := "Hello" ^ " " ^ "World";
            obj := new Test();
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_205():
    """Example 1"""
    source = """
class Example1 {
        int factorial(int n){
            if n == 0 then return 1; else return n * this.factorial(n - 1);
        }
    
        void main(){
            int x;
            x := io.readInt();
            io.writeIntLn(this.factorial(x));
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_206():
    """Example 2"""
    source = """
class Shape {
    float length, width;
    float getArea() {}
    Shape(float length, width){
        this.length := length;
        this.width := width;
    }
}

class Rectangle extends Shape {
        float getArea(){
            return this.length * this.width;
        }
    }
    
    class Triangle extends Shape {
        float getArea(){
            return this.length * this.width / 2;
        }
    }
    
    class Example2 {
        void main(){
            Shape s;
            s := new Rectangle(3,4);
            io.writeFloatLn(s.getArea());
            s := new Triangle(3,4);
            io.writeFloatLn(s.getArea());
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_207():
    """Example 4"""
    source = """
class MathUtils {
    static void swap(int & a; int & b) {
        int temp := a;
        a := b;
        b := temp;
    }

    static void modifyArray(int[5] & arr; int index; int value) {
            arr[index] := value;
        }
    
        static int & findMax(int[5] & arr) {
            int & max := arr[0];
            for i := 1 to 4 do {
                if (arr[i] > max) then {
                    max := arr[i];
                }
            }
            return max;
        }
    }
    
    class StringBuilder {
        string & content;
    
        StringBuilder(string & content) {
            this.content := content;
        }
    
        StringBuilder & append(string & text) {
            this.content := this.content ^ text;
            return this;
        }
    
        StringBuilder & appendLine(string & text) {
            this.content := this.content ^ text ^ "\\n";
            return this;
        }
    
        string & toString() {
            return this.content;
        }
    }
    
    class Example4 {
        void main() {
            ## Reference variables
            int x := 10, y := 20;
            int & xRef := x;
            int & yRef := y;
            int[5] numbers := {1, 2, 3, 4, 5};
            int & maxRef := MathUtils.findMax(numbers);
            string text := "Hello";
            StringBuilder & builder := new StringBuilder(text);
    
            io.writeIntLn(xRef);  ## 10
            io.writeIntLn(yRef);  ## 20
    
            ## Pass by reference
            MathUtils.swap(x, y);
            io.writeIntLn(x);  ## 20
            io.writeIntLn(y);  ## 10
    
            ## Array references
            MathUtils.modifyArray(numbers, 2, 99);
            io.writeIntLn(numbers[2]);  ## 99
    
            ## Reference return
            maxRef := 100;
            io.writeIntLn(numbers[2]);  ## 100
    
            ## Method chaining with references
            builder.append(" ").append("World").appendLine("!");
            io.writeStrLn(builder.toString());  ## "Hello World!\\n"
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_208():
    source = """class ABCXYZ {int flag := true;}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_209():
    source = """class ABCXYZ {int arr := {1, "s", true};}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_210():
    source = """class ABCXYZ {int arr := {1+2};}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_211():
    source = """class ABCXYZ {int arr := {1, 2, {3}};}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_212():
    source = """class A {int x := (1) + ({1, a});}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_213():
    source = """class ABCXYZ {int x := this;}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_214():
    source = """class ABCXYZ {int z := nil;}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_215():
    source = """class A {nil z := nil;}"""
    expected = "Error on line 1 col 9: nil"
    assert Parser(source).parse() == expected


def test_216():
    source = """class A {int z := new ID() + new ID(1) + new A(nil, 2+3, "s"/2);}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_217():
    source = """class A {int z := ID.a.b.c + ID.a + (new A()).c + true.a.c + nil.e + {2,3}.k.m;}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_218():
    source = """class A {int z := a.true.b;}"""
    expected = "Error on line 1 col 20: true"
    assert Parser(source).parse() == expected


def test_219():
    source = """class A {int z := ID.a() + ID.a.b.c() + {1,2}.c().e.f().k + "s".b().c + a.b(2).c(2+3, a.f(), nil);}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_220():
    source = """class A {int z := foo();}"""
    expected = "Error on line 1 col 21: ("
    assert Parser(source).parse() == expected


def test_221():
    source = """class A {int z := a[2+3] + a.f().c[b][2] + a[true + 1.0][a.a()][c] + a[a[2] >= 2];}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_222():
    source = """class A {int z := a[b].c;}"""
    expected = "Error on line 1 col 22: ."
    assert Parser(source).parse() == expected


def test_223():
    source = """class A {int z := +-+--++a + +a - -a[2];}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_224():
    source = """class A {int z := !!nil + !a + !!!+-+-a;}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_225():
    source = """class A {int z := -!a;}"""
    expected = "Error on line 1 col 19: !"
    assert Parser(source).parse() == expected


def test_226():
    source = """class A {int z := a ^ "s" ^ c + !a ^ !c;}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_227():
    source = """class A {int z := 1.0 == 2;}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_228():
    source = """class A {int z := 1.0 != nil.a;}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_229():
    source = """class A {int z := 1.0 != a * 3 != c ;}"""
    expected = "Error on line 1 col 31: !="
    assert Parser(source).parse() == expected


def test_230():
    source = """class A {int z := a <= 2 > {a, b};}"""
    expected = "Error on line 1 col 25: >"
    assert Parser(source).parse() == expected


def test_231():
    source = """class A {int z := a == 2 > c == this;}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_232():
    source = """class B {
        A& a := 2;
        int[3]& a ;
        A & & c;
    }"""
    expected = "Error on line 4 col 12: &"
    assert Parser(source).parse() == expected


def test_233():
    source = """class B {
        float[2][3] a;
    }"""
    expected = "Error on line 2 col 16: ["
    assert Parser(source).parse() == expected


def test_234():
    source = """class B {
        void B(){
            a := 2;
            a.b[2] := 3 + 3 *4;
            this.a[2] := 3 + 3;
            a[2][a.fo()] := a.b.c();
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_235():
    source = """class B {
        void B(){
            a[2].c := 1;
        }
    }"""
    expected = "Error on line 3 col 16: ."
    assert Parser(source).parse() == expected


def test_236():
    source = """class B {
        void B(){
            a.fo().c := 2;
            {2,3}.a := 2;
            a := 3;
            a[2+a[2]][3] := 2;
            this.a.c := 3;
            this := 2;
        }
    }"""
    expected = "Error on line 8 col 17: :="
    assert Parser(source).parse() == expected


def test_237():
    source = """class B {
        void B(){
            a.foo() := 2;
        }
    }"""
    expected = "Error on line 3 col 20: :="
    assert Parser(source).parse() == expected


def test_238():
    source = """
class Main {
    static static int a;
}
"""
    expected = "Error on line 3 col 11: static"
    assert Parser(source).parse() == expected


def test_239():
    source = """
class Main {
    void main() {
        a := 2;
        int a := 2;
    }
}
"""
    expected = "Error on line 5 col 8: int"
    assert Parser(source).parse() == expected
