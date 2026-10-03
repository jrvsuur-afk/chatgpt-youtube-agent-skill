# YouTube Agent kanal yönlendirmesi

## Varsayılan profil

Varsayılan kanal **Çalık'S Art Academy**, varsayılan kanal profili
`profiles/caliks-art-academy.md` dosyasıdır. Yollar bu repo köküne göre çözülür.

YouTube Agent ile içerik üretmeden veya analiz etmeden önce kanal profilini seç
ve dosyasını oku. Profil seçimi için şu sırayı uygula:

1. Kullanıcının açıkça belirttiği kanal veya profil adı varsayılandan önceliklidir.
   Çalık'S Art Academy içeriği için `profiles/caliks-art-academy.md` dosyasını oku.
2. Kullanıcı açıkça başka bir kanal veya profil belirtirse Çalık'S profilini
   otomatik uygulama. `profiles/` altında dosya adı veya dosyada belirtilen kanal
   adıyla açıkça eşleşen profil varsa onu oku ve kullan. Eşleşme yoksa bu kanal
   için yeni profil gerektiğini belirt; Çalık'S profiline geri dönme. Kullanıcı
   açıkça profil oluşturma veya geliştirme istemedikçe yeni dosya yazma.
3. Başka bir kanal veya profil belirtilmemişse varsayılan profili kullan.
   Kullanıcı yalnızca yapılandırılmış video analizi yapıştırırsa ve başka kanal
   belirtmezse bunu Çalık'S Art Academy içeriği olarak kabul et; metin üretmeden
   önce `profiles/caliks-art-academy.md` dosyasını oku. Kullanıcının verdiği başka
   kanala ait açık bağlamı bu varsayımla değiştirme.

## yt-caliks giriş noktası

Çalık'S Art Academy için tek giriş noktası `skills/yt-caliks/SKILL.md` dosyasıdır.
Kullanıcı `yt-caliks` istediğinde bu skill'i oku; her çağrıda önce kanal profilini,
ardından isteğe uygun upstream skill'i okuma kuralını uygula. Yalnızca `yt-caliks`
ve yapılandırılmış video analizi verilmişse varsayılan görev SEO paketidir.
`yt-caliks package`, `yt-caliks shorts`, `yt-caliks script` gibi açık alt görevler
bu varsayılandan önceliklidir. Diğer kanallar için yukarıdaki açık profil seçimi
kuralları geçerliliğini korur.

## Skill'lerle birlikte kullanım

Bu yönlendirme mevcut 11 YouTube skill'inin tamamı için geçerlidir:

`yt-seo`, `yt-package`, `yt-shorts`, `yt-plan`, `yt-audit`, `yt-script`,
`yt-comment`, `yt-chapters`, `yt-edit`, `yt-retention`, `yt-viral`.

Bu skill'lerden biri Çalık'S Art Academy içeriği için kullanıldığında önce
`profiles/caliks-art-academy.md` dosyasını oku ve görevle ilgili kanal kurallarını
uygula. Başka bir kanal açıkça seçilmişse aynı adımı eşleşen profil için yap.

Kanal profili skill'in teknik talimatlarını geçersiz kılmaz; yalnızca dil, ton,
çıktı formatı, hashtag, etiket ve kanala özel kuralları tamamlar. Skill'in gerekli
girdilerini, analiz yöntemlerini, yardımcı betiklerini, hesaplamalarını ve teknik
kontrollerini koru. Profildeki çıktı biçimini mevcut göreve ilgili olduğu ölçüde
uygula: örneğin yedi bölümlük SEO formatı bir senaryo, yayın planı, bölüm listesi
veya retention analizinin yerine geçmez. İstenen SEO metinlerini üretirken
profilin yedi bölümlük formatını kullan.

## Kaynak doğruluğu

Belirsiz içerik bilgisi uydurma. Motif, stil, teknik, vücut bölgesi, ses, sanatçı,
konum, sayı veya sonuç hakkında yalnızca kullanıcının sağladığı kaynakla
desteklenen bilgileri kullan.

Yapılandırılmış video analizi verilmişse bunu kaynak kabul et; ham videoyu yeniden
analiz etmeye çalışma. Analizden yararlandığında videoyu izlediğini veya sesini
doğruladığını iddia etme. Güncel arama veya trend verisi verilmediyse böyle bir
veri varmış gibi davranma.

## Repo değişiklikleri

- Mevcut 11 upstream `skills/yt-*/SKILL.md` dosyasını değiştirme.
- Repo dosyalarını yalnızca kullanıcı açıkça geliştirme veya değişiklik istediğinde
  ve o isteğin kapsamında değiştir. Sıradan içerik üretim görevlerinde çıktıyı
  sohbette ver; repo, kanal profili veya genel ses profili dosyalarını değiştirme.
- Sıradan içerik üretim görevlerinde commit veya push yapma. Geliştirme görevinde
  de commit ve push işlemlerini ancak kullanıcı bunları açıkça istediğinde yap.
- Repo değişikliği istendiğinde ilgili kontrolleri yap ve mevcut testleri repo
  kökünde çalıştır: `python3 -B -m unittest discover -s tests -v`.
