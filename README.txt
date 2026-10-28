WISPBYTE HLS VIDEO YAYINI
========================

1) ZIP'i Wispbyte sunucunuzun dosya yoneticisine yukleyip cikartin.
2) Python uygulama sunucusu/runtime secin. Startup command: bash start.sh
   (bash yoksa: python -m pip install -r requirements.txt && python stream.py)
   PORT veya SERVER_PORT Wispbyte tarafindan otomatik atanir.
3) Videolari videos klasorune 1.mp4, 2.mp4, 3.mp4 ... olarak yukleyin.
   MP4, MKV, MOV, WEBM, M4V ve AVI desteklenir; numaraya gore siralanir.
4) yayin_logo.png dosyasini ana klasore koyun. Logo sol ustte gorunur.
5) Sunucuyu baslatin. Akis adresi: http://SUNUCU-ADRESI:PORT/live.m3u8

Canli HLS adresi sunucu calistigi surece sabittir. Wispbyte sunucu adresi/portu
panel tarafindan degistirilirse URL de degisir. Video ve logolar ZIP'te yer almaz;
buyuk medya dosyalarini ayri yukleyin. Kaynak videolar yayinda 420 piksel yukseklige
(orani korunarak) ve 20 FPS'e donusturulur. H.264 900 kb/s + AAC 96 kb/s kullanilir.
HLS segmentleri surekli silinip yenilendigi icin disk kullanimi sinirli kalir.

NOT: FFmpeg video encode islemi CPU kullanir. 420p/20 FPS ayari yuksek kaynak
videolara gore daha hafiftir; ayni anda cok izleyiciye cikis yapmak icin CDN gerekir.
Wispbyte'in atadigi uygulama portu HTTP erisimi icin acik olmalidir.
