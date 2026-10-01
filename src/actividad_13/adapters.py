from .models import ExternalProduct, Product


class ExternalProvider:
    def get_product(self, product_name: str) -> ExternalProduct:
        products = {
            "Laptop": ExternalProduct(
                product_name="Laptop",
                amount=15000,
            ),
            "Mouse": ExternalProduct(
                product_name="Mouse",
                amount=500,
            ),
        }

        if product_name not in products:
            raise ValueError("Producto no encontrado.")

        return products[product_name]


class ProductProviderAdapter:
    def __init__(self, external_provider: ExternalProvider) -> None:
        self.external_provider = external_provider

    def get_product(self, product_name: str) -> Product:
        external_product = self.external_provider.get_product(product_name)

        return Product(
            name=external_product.product_name,
            price=external_product.amount,
        )
