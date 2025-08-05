from functions.get_file_content import get_file_content

result1 = get_file_content("calculator", "main.py")
print(result1)

result2 = get_file_content("calculator", "pkg/calculator.py")
print(result2)

result3 = get_file_content("calculator", "/bin/cat")
print(result3)

result4 = get_file_content("calculator", "pkg/does_not_exist.py")