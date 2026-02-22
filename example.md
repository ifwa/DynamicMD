# Project A: Static Commands

## Commands without Parameters

### Ping Google

This command pings Google.

```bash
ping google.com
```

### Curl Google

This command requests and prints the source code of Google's homepage.

```bash
curl -L https://www.google.com
```

## Advanced Markdown Syntax

### Unordered Lists

Unordered list:

- List item 1
- List item 2

### Ordered Lists

Ordered list:

1. List item 1
2. List item 2

### Code Block

Java hello world:

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

### Text Emphasis

**This is bold text**

*This is italic text*

This is a mix of **bold** and *italic* text.

# Project B: Dynamic Commands

## Without Page Parameters

### Text Parameters

@param name { name="Container Name" type=text enabled=true prefix="--name" default=container-01 options=[container-01,container-02,container-03] }

Run a Docker container

```bash
dock run ${name}
```

### Switch Parameters

@param dir { name="Directory Name" type=text enabled=true prefix="" default=/tmp/dir-01 options=[/tmp/dir-01,/tmp/dir-02,/tmp/dir-03] }
@param parents { name="Creates Parents" type=switch enabled=false prefix="--parents" }

Make a directory

```bash
mkdir ${parents} ${dir}
```

## With Page Parameters

@param dir { name="Directory Name" type=text enabled=true prefix="" default=/tmp/dir-01 options=[/tmp/dir-01,/tmp/dir-02,/tmp/dir-03] }

### Page Parameters Usage 1

Make a directory

@param parents { name="Creates Parents" type=switch enabled=false prefix="-p" }

```bash
mkdir ${parents} ${dir}
```

### Page Parameters Usage 2

@param recursive { name="Recursive" type=switch enabled=true prefix="-r" }

Remove a directory

```bash
rm ${recursive} ${dir}
```
