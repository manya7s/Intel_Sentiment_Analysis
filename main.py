# option
print("Navigator")
option = int(input("Review by:\n1. Processor\n2. Brand\n3. Functionality\n4. Laptops\n5. Desktops\n-> "))

match option:
    case 1:
        option = int(input("Select processor:\n1. i9\n2. i7\n3. i5\n-> "))
        if option == 1:
            print("processor i9")
        elif option == 2:
            print("processor i7")
        elif option == 3:
            print("processor i5")
        else:
            print("no data")
    case 2:
        option = int(input("""Choose brand:\n1. Lenovo\n2. MSI\n3. Acer\n4. Hewlett Packard\n5. Dell\n6. Asus\n-> """))
        match option:
            case 1:
                print("brand lenovo")
            case 2:
                print("brand msi")
            case 3:
                print("brand acer")
            case 4:
                print("brand HP")
            case 5:
                print("brand dell")
            case 6:
                print("brand asus")
            case _:
                print("no data")
    case 3: 
        option = int(input("Choose functionality:\n1. Gaming\n2. General\n-> "))
        if option == 1:
            print("functionality gaming")
            #includes gaming laptops and gaming desktops
        elif option == 2:
            print("functionality general")
            #includes general laptops and general desktops
        else:
            print("no data")
    case 4:
        option = int(input("Choose brand:\n1. acer\n2. msi\n3. asus\n4. dell\n5. hp\n-> "))
        match option:
            case 1:
                print("laptop acer")
            case 2:
                print("laptop msi")
            case 3:
                print("laptop asus")
            case 4:
                print("laptop dell")
            case 5:
                print("laptop hp")
            case _:
                print("no data")
    case 5:
        option = int(input("Choose brand:\n1. lenovo\n2. hp\n3. acer\n4. dell\n5. asus\n6. msi\n-> "))
        match option:
            case 1:
                print("desktop lenovo")
            case 2:
                print("desktop hp")
            case 3:
                print("desktop acer")
            case 4:
                print("desktop dell")
            case 5:
                print("desktop asus")
            case 6:
                print("desktop msi")
            case _:
                print("no data")
    case _:
        print("no data")
        
