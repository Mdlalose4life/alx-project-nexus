from django.apps import AppConfig
import PIL.Image
PIL.Image.EXTENSION.clear()
PIL.Image.EXTENSION.update({
    '.jpg': 'PIL.JpegImagePlugin.JpegImageFile',
    '.jpeg': 'PIL.JpegImagePlugin.JpegImageFile',
    '.png': 'PIL.PngImagePlugin.PngImageFile',
    '.webp': 'PIL.WebPImagePlugin.WebPImageFile',
    '.gif': 'PIL.GifImagePlugin.GifImageFile',
})

class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"

    def ready(self):
        import apps.products.signals
