class Product:
    def __init__(self,name,price, in_stock):
        #bunlarin degiskenlerini tanimlayarakda gosterebilirz
        #(self,name:str,price:float, in_stock:bool):
        # bu sekilde yazip asagidaki price fiyatina string deger verirsem hata vermeyecektir
        # kod calisacatir yine
        self.name=name
        self.price=price
        self.in_stock=in_stock

if __name__ =='__main__':
    ornek_product=Product("Ornek",100,True)
    print(ornek_product.in_stock)
    external_data={
        "name":"Laptop",
        "price":"999.99",
        "in_stock":"True"
    }
    product = Product(
        name=external_data.get("name"),
        price=external_data.get("price"),
        in_stock=external_data.get("in_stock")
    )

    print(product.name)
    print(product.price)
    print(product.in_stock)
    #bunlarin tipini yazdirdigim zaman icine verdigim degerlerin tipini yazdiricaktir
    #product olustururken tanimladigim degeri degil
    print(type(product.name))
    print(type(product.price))
    print(type(product.in_stock))

