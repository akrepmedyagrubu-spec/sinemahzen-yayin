# Wispbyte HLS Video Yayını

FFmpeg ile numaralı videoları sırayla ve döngü halinde oynatıp HLS yayınına dönüştürür. Yayın sırasında sol üst köşeye `yayin_logo.png` eklenir.

## Özellikler

- `videos/1.mp4`, `videos/2.mp4`, `videos/3.mp4` şeklinde numaraya göre oynatma
- Tekrar başa dönen sürekli yayın
- 420 piksel yükseklik, 20 FPS
- H.264 video (900 kb/s hedef), AAC ses (96 kb/s)
- Sol üstte, 140 piksel genişliğinde logo
- Sabit `/live.m3u8` adresi ve sınırlı sayıda HLS segmenti
- Wispbyte portunu `PORT` veya `SERVER_PORT` ortam değişkeninden alma

## Dosyaları ekleme

Videoları `videos/` klasörüne koyun. Dosya adının gövdesi sayı olmalı: `1.mp4`, `2.mp4`, `3.mp4`.
Desteklenen uzantılar: MP4, MKV, MOV, WEBM, M4V ve AVI.

Şeffaf PNG logonuzu projenin ana klasörüne `yayin_logo.png` adıyla koyun. Logo FFmpeg tarafından 140 piksel genişliğe ölçeklenir; görüntü oranı korunur.

## Wispbyte'ta çalıştırma

1. Bu depodaki dosyaları Wispbyte sunucunuza yükleyin veya GitHub entegrasyonuyla çekin.
2. Python runtime seçin.
3. Startup command alanına `bash start.sh` yazın.
4. Sunucuyu başlatın.
5. Wispbyte'ın verdiği sunucu adresi ve portu kullanarak `http://SUNUCU-ADRESI:PORT/live.m3u8` adresine bağlanın.

`start.sh`, `requirements.txt` dosyasındaki `imageio-ffmpeg` paketini yükler ve ardından uygulamayı başlatır. Paket, FFmpeg ikilisini Python paketiyle sağlar. Wispbyte başlangıç sırasında paket indiremiyorsa paketi panelin Python Packages bölümüne `imageio-ffmpeg` olarak ekleyin ve startup komutunu `python stream.py` yapın.

## Yerelde çalıştırma

Python 3.9 veya üzeri gerekir.

```bash
python -m pip install -r requirements.txt
python stream.py
```

Ardından `http://127.0.0.1:8080/live.m3u8` adresini açın. Başka bir port için `PORT` ortam değişkenini ayarlayın.

## Notlar

- Bu uygulama kendisi HLS sunucusu görevi görür. Yayın adresi sunucu açık olduğu sürece sabittir; Wispbyte adresi veya portu değişirse tam URL de değişebilir.
- Yeniden kodlama CPU kullanır. `veryfast` preset, 420p ve 20 FPS düşük kaynak tüketimi için seçilmiştir; gereken kapasite giriş videosu ve izleyici sayısına göre değişebilir.
- HLS, izleyicilere tek bir kodlama çıkışı üretir; yüksek izleyici yükü için CDN veya ayrı bir dağıtım katmanı gerekebilir.
- Depoda örnek video veya logo bulunmaz. Medya dosyalarınızı kendiniz ekleyin. `hls/` içeriği çalışma anında üretilir.
