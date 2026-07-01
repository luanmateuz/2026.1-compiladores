# Sintaxe

Sintaxe da linguagem.

## Palavras Reservadas

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

## Comentarios

A linguagem `fucklang` só tem suporte a comentário de linha, feito com o `#`.

```python
# commentário
```

## Constantes

```go
const a int := 1;
```

## Variáveis

```go
var x int := 10;
var y flt := 3.14;
var z chr := 'a';
var s str := "hello";
var b boo := true;
```

## Operadores

### Aritméticos

Precisam ser do mesmo tipo.

```python
x + y   # adição
x - y   # subtração
x * y   # multiplicação
x / y   # divisão
x % y   # resto
```

### Comparação

```python
x > y   # maior que
x < y   # menor que
x >= y  # maior ou igual
x <= y  # menor ou igual
x == y  # igual
x != y  # não igual (diferente)
```

### Lógicos

```python
x && y  # E
x || y  # OU
!x      # Não/Negação
```

## Condicionais

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

A linguagem `fucklang` só tem suporte ao `for`, seja criativo com ele para simular o `while`.

```go
for (var i int := 0; i < 10; i := i + 1) {
    puts(i);
}
```

`for` como `while`:
```go
var i int := 0;
for (;i < 10;) {
    puts(i);
    i := i + 1;
}
```

## Funções

!!! failure "fuck"

    Não implementado.

```go
fuck print_x() {
    puts('x');
}
```


## Exemplo

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
