import qrcode
from qrcode.constants import ERROR_CORRECT_M
from pyzbar.pyzbar import decode
from PIL import Image

DATA = "t=20260426T1926&s=135.00&fn=7382440900148188&i=29644&fp=1789582767&n=1"

# V6, ECC=M, перебираем все маски
for mask in range(8):
    qr = qrcode.QRCode(
        version=6,
        error_correction=ERROR_CORRECT_M,
        box_size=10,
        border=4,
        mask_pattern=mask,
    )
    qr.add_data(DATA, optimize=0)  # без оптимизации режима — чистый byte
    qr.make(fit=False)
    img = qr.make_image(fill_color="black", back_color="white")
    fname = f"qr_v6_M_mask{mask}.png"
    img.save(fname)
    
    # Проверка декодированием
    decoded = decode(Image.open(fname))
    ok = "OK" if decoded and decoded[0].data.decode() == DATA else "FAIL"
    print(f"Маска {mask}: {fname} — декодирование {ok}")

# Также сделаем «по умолчанию» (с автоматической оптимальной маской)
qr = qrcode.QRCode(version=6, error_correction=ERROR_CORRECT_M, box_size=10, border=4)
qr.add_data(DATA, optimize=0)
qr.make(fit=False)
img = qr.make_image(fill_color="black", back_color="white")
img.save("qr_v6_M_auto.png")
print("Авто-маска сохранена в qr_v6_M_auto.png")

# Размер
print(f"\nРазмер сетки: 41x41 модулей")
print(f"Размер изображения (box=10, border=4): {41*10 + 4*10*2}x{41*10 + 4*10*2} пикселей")
