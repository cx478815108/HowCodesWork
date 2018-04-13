#Understand how the codes works
1. translate codes into tokens

## translate codes into tokens
Scanner.py 

input 

```
func test(Integer age) {
    print age;
}
```
output

```
{
  type:identifier
  value:"func"
  line:1
  column:4
}

{
  type:identifier
  value:"test"
  line:1
  column:9
}

{
  type:operator
  value:"("
  line:1
  column:10
}

{
  type:identifier
  value:"Integer"
  line:1
  column:17
}

{
  type:identifier
  value:"age"
  line:1
  column:21
}

{
  type:operator
  value:")"
  line:1
  column:22
}

{
  type:scope
  value:"{"
  line:1
  column:24
}

{
  type:identifier
  value:"print"
  line:2
  column:9
}

{
  type:identifier
  value:"age"
  line:2
  column:13
}

{
  type:scope
  value:";"
  line:2
  column:14
}

{
  type:scope
  value:"}"
  line:3
  column:1
}
```



