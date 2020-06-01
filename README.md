# Tuffix Lang

This is a simple mnemonic language developed in my spare time to teach myself how lexer, parsers and compilers work.

There are four components to this build:

- Lexer
- AST
- Parser
- Grammar

# Lexer

This takes in a "token map", which is just a dictionary that has a string associated with a regular expression.

Here is the one we are using in this project:

```python
cpsc_regex = r'CPSC\-(?P<course>[0-9]{3}[A-Z]?)'

TuffixTokenMap = {

  # builtin functions
  "INIT": r'(?i)init',
  "ADD": r'(?i)add.*CPSC\-(?P<course>[0-9]{3}[A-Z]?)',
  "REMOVE": r'(?i)remove.*CPSC\-(?P<course>[0-9]{3}[A-Z]?)',
  "LIST_INSTALLED": r'(?i)installed',
  "LIST_AVAILABLE": r'(?i)available',
  "DESCRIBE_TARGET": r'(?i)describe.*CPSC\-(?P<course>[0-9]{3}[A-Z]?)',
  "REKEY": r'(?i)rekey',
  "STATUS": r'(?i)status',
  "TARGET": cpsc_regex,

  # syntax
  "COMMENT": r'^\#.*[a-zA-Z0-9]',

}
```
And we are ignoring spaces by default.

# AST

AST stands for "abstract syntax tree" and this is where the grammar, functions and tokens all meet.
Each class must contain a `eval` function as this is what the parser uses to associate an action for a set of grammar parameters (I think that's how you explain it?).

# Parser

Here is where the grammar is defined and is processed.
An example grammar rule is:

```python
@self.pg.production('expression : TARGET')
```

`expression` is a filler word that is not associated with a token directly.

This can be seen in this grammar rule:

```python
@self.pg.production('expression : expression MUL expression')
```

When going through the parsing process, an example function can be used:

```python
def multiply(p):
  left = p[0]
  right = p[2]
  return Multiply(left, right)
```
Where the `Multiply` function would be defined in the `AST`.
For this to work as well, you would need to define what a number is, which can be defined in the lexer token map.

These implementations are inherently recursive, meaning we need to defined every basic data type involved so a proper grammar can be established.


# Secondary Components

These modules are to be implemented after a proper interpreter has been established.

- [X] ClassInformation: retrieve information about classes based on the current class catalog
- [X] Fetch: grab hardware and configuration information about a given user
- [ ] TuffixAnsiblePlaybookManager: an intermediary class that handles the installation and removal of Ansible playbooks, also checking for the presence of file locks. These signify if a target has already been installed.


