def zamik():
    f = open("out.txt", "w")
    def closure():
        nonlocal f
        while True:
            value = input("Введите желаемые значения или 'exit' для завершения: ")
            if value == "exit":
                break
            f.write(value + "\n")
    return closure
zm1 = zamik()
zm1()
print("Значения были записаны в файл out.txt")
