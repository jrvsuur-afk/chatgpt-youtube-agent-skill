---
name: yt-caliks
description: >-
  Use when the user invokes "yt-caliks" for Çalık'S Art Academy content, including
  SEO, titles, descriptions, tags, hashtags, packaging, Shorts, scripts, planning,
  viral research, retention, audits, chapters, edits and comment replies. Reads
  the channel profile first and routes to the appropriate upstream yt-* skill.
---

# yt-caliks

Çalık'S Art Academy için tek giriş noktasıdır. Kullanıcının isteğini uygun
upstream skill'in teknik işleyişiyle ve kanalın tercihleriyle birlikte ele al.

## Önce kanal profilini oku

Her çağrıda, alt görevi uygulamadan veya çıktı yazmadan önce
[kanal profilini](../../profiles/caliks-art-academy.md) oku ve eksiksiz uygula.
Profil dosyasındaki güncel kuralları esas al; önceki bir çağrıdan hatırladığın
kurallarla yetinme. Profil bulunamıyorsa kurallarını tahmin etme; gerekli dosyanın
pakette bulunması gerektiğini belirt.

Yollar bu skill'in gerçek `skills/yt-caliks/` dizinine göredir. Bir keşif bağlantısı
üzerinden açıldığında önce gerçek dosya yolunu çöz; profili ve upstream skill'leri
aynı paket içindeki göreli bağlantılardan oku.

## Görevi seç ve upstream talimatlarını oku

1. `yt-caliks package`, `yt-caliks shorts`, `yt-caliks script` gibi açık bir alt
   görev belirtilmişse onu uygula. Açık alt görev SEO varsayılanından önceliklidir.
2. Alt görev adı verilmemişse kullanıcının istediği işi aşağıdaki tablodan eşleştir.
   Başlıkla birlikte thumbnail veya kapak istendiğinde `package` seç; yalnızca
   başlık, açıklama, tags veya hashtag istendiğinde `seo` seç.
3. Kullanıcı yalnızca `yt-caliks` deyip yapılandırılmış video analizi verdiyse
   **varsayılan görev `seo`** olsun: profilin yedi bölümlük SEO paketini üret.
4. İlgili upstream `SKILL.md` dosyasını açıp talimatlarını gerçekten oku ve uygula.
   Tablodaki isim veya daha önceki bir özet, dosyayı okumanın yerine geçmez.
   Birden fazla görev açıkça istendiyse ilgili skill'leri sırayla oku ve uygula.

| Alt görev / istek | Okunacak upstream skill |
| --- | --- |
| `seo` / SEO, başlık, açıklama, tags, hashtag | [yt-seo](../yt-seo/SKILL.md) |
| `package` / başlık + thumbnail veya kapak paketi | [yt-package](../yt-package/SKILL.md) |
| `shorts` / uzun içerikten Shorts çıkarımı | [yt-shorts](../yt-shorts/SKILL.md) |
| `script` / senaryo | [yt-script](../yt-script/SKILL.md) |
| `plan` / yayın veya içerik planı | [yt-plan](../yt-plan/SKILL.md) |
| `viral` / viral araştırma | [yt-viral](../yt-viral/SKILL.md) |
| `retention` / izleyici tutma analizi | [yt-retention](../yt-retention/SKILL.md) |
| `audit` / kanal değerlendirmesi | [yt-audit](../yt-audit/SKILL.md) |
| `chapters` / bölüm işaretleri | [yt-chapters](../yt-chapters/SKILL.md) |
| `edit` / kurgu veya edit kararları | [yt-edit](../yt-edit/SKILL.md) |
| `comment` / yorum cevapları | [yt-comment](../yt-comment/SKILL.md) |

Upstream skill'in teknik talimatlarını, gerekli girdilerini, yardımcı betiklerini
ve kontrollerini koru. Yardımcı dosyaları ilgili upstream skill'in gerçek dizinine
göre çöz. Seçilen iş için gerekli transcript, zaman damgası, retention verisi veya
başka teknik girdi eksikse yalnızca gerekli eksik bilgiyi iste; sonuç uydurma.

## Kaynağı ve doğruluğu koru

- Yapılandırılmış video analizi verilmişse bunu kaynak kabul et; ham video da
  verilmiş olsa bile yeniden analiz etmeye çalışma ve yeniden yüklenmesini isteme.
  Analizden yararlandığında videoyu izlediğini veya sesini doğruladığını söyleme.
- Analizde veya göreve ait kaynakta bulunmayan motif, stil, teknik, vücut bölgesi,
  sağ/sol taraf, sanatçı, konum, sayı veya zaman damgası ekleme.
- Kullanıcı güncel arama veya trend verisi sağlamamışsa güncel trend biliyormuş
  gibi davranma. Açıkça viral araştırma istenirse upstream araştırma adımlarını
  uygula; bulguları gerçekten erişilen kaynaklara dayandır. Veri bulunmadığında
  popülerlik, arama hacmi veya güncellik iddiası uydurma.
- Sıradan içerik görevlerinde repo, profil veya genel ses profili dosyalarını
  değiştirme; commit veya push yapma. Repo geliştirmesi ancak kullanıcının açık
  değişiklik isteği kapsamında yapılır; commit/push ayrıca açıkça istenmelidir.

## Kanal kurallarını çıktıya uygula

Profildeki Türkçe ana dil, doğal ton, kısa ve doğrudan başlıklar, kısa açıklamalar,
çok dilli alanlar, çıktı sırası, sabit hashtagler, konu etiketleri ve doğruluk
kuralları her zaman geçerlidir. Kanal tercihleri upstream skill'in teknik
talimatlarını tamamlar; teknik işleyişini geçersiz kılmaz.

SEO paketi için doğrudan şu yedi bölümü ver; giriş, gerekçe veya sonuna yayın onayı
sorusu ekleme:

1. Türkçe başlık
2. Türkçe açıklama
3. İngilizce başlık + açıklama
4. Almanca başlık + açıklama
5. Japonca başlık + açıklama
6. YouTube etiketleri
7. Sabit + konuya özel hashtag seti

Sabit 14 hashtag'i profil dosyasından aynen al ve profilin doğrulanmış konuya özel
5–6 hashtag kuralını uygula. Bir sayıya ulaşmak için belirsiz bilgi ekleme.

Diğer alt görevlerde istenen senaryo, plan, Shorts seçimi, bölüm listesi veya
analiz çıktısını üret; her görevi zorla yedi SEO bölümüne dönüştürme.
Kanalın dil, ton ve doğruluk kuralları bu çıktılarda
da geçerlidir; etiket/hashtag alanları üretildiğinde ilgili profil kurallarını
eksiksiz uygula.
