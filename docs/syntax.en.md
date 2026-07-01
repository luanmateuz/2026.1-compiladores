# Syntax

Language syntax.

## Reserved Words

```
const
var
int
flt
chr
boo
str
true
false
fuck
ret
puts
for
if
else
```

## Comments

The `fucklang` language only supports single-line comments, using `#`.

```python
# comment
```

## Constants

```go
const a int := 1;
```

## Variables

```go
var x int := 10;
var y flt := 3.14;
var z chr := 'a';
var s str := "hello";
var b boo := true;
```

## Operators

### Arithmetic

Operands must be of the same type.

```python
x + y   # addition
x - y   # subtraction
x * y   # multiplication
x / y   # division
x % y   # remainder
```

### Comparison

```python
x > y   # greater than
x < y   # less than
x >= y  # greater than or equal to
x <= y  # less than or equal to
x == y  # equal to
x != y  # not equal to
```

### Logical

```python
x && y  # AND
x || y  # OR
!x      # NOT/Negation
```

## Conditionals

### if

```go
if (1 < 10) {
    puts(1);
}
```

### if-else-if

```go
if (10 < 10) {
    puts(1);
} else if (10 == 10) {
    puts(10);
} else {
    puts(100);
}
```

### if-else

```go
if (100 < 10) {
    puts(10);
} else {
    puts(100);
}
```

## Loops

The `fucklang` language only supports `for` loops; be creative with them to simulate `while` loops. 
```go
for (var i int := 0; i < 10; i := i + 1) { 
    puts(i);
}
```

`for` as `while`:
```go
var i int := 0;
for (;i < 10;) { 
    puts(i); 
    i := i + 1;
}
```

## Functions

!!! failure "fuck" 

Not implemented.

```go
fuck print_x() { 
    puts('x');
}
```


## Example

```go
# even numbers
var number_two int := 2;
var number_limit int := 10;

for (var i int := 0; i <= number_limit; i := i + 1) { 
    if (i % number_two == 0) { 
        # print even number 
        puts(i); 
    }
}
```
