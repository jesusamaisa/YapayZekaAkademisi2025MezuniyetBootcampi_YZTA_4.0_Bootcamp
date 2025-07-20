# **Takım İsmi**

LungGuard

# Ürün İle İlgili Bilgiler

## Takım Elemanları

* **Ayşe Feyza Tekgöz:** Ürün Sahibi (Product Owner)
* **Muhammed Emin Canbaz:** Scrum Master
* **Melis Sağır:** Geliştirici
* **İrem Gültekin:** Geliştirici
* **Muhammed İsa Erkan:** Geliştirici

## Ürün İsmi

**Radyologlara Yardımcı Akciğer İzleme Sistemi**

## Ürün Açıklaması

Bu sistem, akciğer taramalarını (X-ray/CT) derin öğrenme algoritmaları ile analiz ederek radyologlara ön tanı ve rapor önerileri sunar. Görüntü işleme yetenekleri sayesinde doktorların teşhis süreçlerinde daha hızlı ve doğru karar almalarına yardımcı olur.

* **Birincil Fonksiyonu:** Akciğer taramalarındaki anormallikleri tespit ederek radyologlara işaretlenmiş görseller ve açıklamalı rapor sunar.
* **İkincil Fonksiyonu:** Hastane bilgi sistemleri ile entegre olarak önceden analiz edilen taramaların otomatik arşivlenmesini sağlar.

## Ürün Özellikleri

* Görüntü Ön İşleme (Denoising, Normalize)
* Derin Öğrenme Tabanlı Lezyon Tespiti
* Bülten Raporlama Modülü (ön tanı önerileri + görsel işaretlemeler)
* Kullanıcı Arayüzü (Web/ masaüstü)
* API Entegrasyonu (Hastane bilgi sistemleri ile olması hedeflenmekte)

## Hedef Kitle

* Radyologlar
* Tıbbi Araştırmacılar
* Hastane bilgi işlem ekipleri

## Juriye Not

Sistem, temel ön işleme pipeline’ını ve ilk model prototipini başarıyla geliştirmiştir. Ancak ileri seviye klinik testler için geliştirme süreci devam etmektedir.

---

# Sprint 1

* **Sprint içinde tamamlanması tahmin edilen puan:** 29 Puan

* **Puan tamamlama mantığı:** Toplamda proje boyunca tamamlanması gereken yaklaşık 60 puanlık backlog bulunmaktadır. 2 sprint’e bölündüğünde ilk sprint'in 29 puan ile başlaması uygun görülmüştür.

* **Sprint Review:**
  Alınan Kararlar:

* Ön işleme pipeline’ı başarıyla oluşturuldu.

* İlk CNN modelinin eğitim kodları taslak halinde yazıldı.

* Basit bir web arayüzü iskeleti geliştirildi.

Sprint Review katılımcıları: Ayşe Feyza Tekgöz, Muhammed Emin Canbaz, Melis Sağır, İrem Gültekin, Muhammed İsa Erkan

* **Sprint Retrospective:**

  * Takım içi iletişim akışı iyileştirildi.
  * Görev dağılımlarının daha netleştirilmesi gerektiğine karar verildi.
  * Gelecek sprint için öncelikler yeniden belirlendi.

---

# Sprint 2 

## 🗓 Sprint Süresi
📅 **Başlangıç:** 2025-07-14  
📅 **Bitiş:** 2025-07-20  

## 🎯 Sprint Hedefi
- Ön işleme modüllerinin optimizasyonu  
- CNN modelinde doğruluk oranını artıracak hiperparametre ayarlamaları  
- React tabanlı kullanıcı arayüzünün veri akışını simüle eden demo sürümünün tamamlanması  
- Flask API taslağının çıkarılması ve Python ile React arasında test amaçlı bir bağlantı kurulması  

---

## ✅ Sprint İçinde Tamamlanan Görevler (31 Puan)

### 📂 Backend (Python) Çalışmaları
- 📦 **Veri Ön İşleme**  
  - Görüntü boyutlandırma optimizasyonu (resize işlemi sırasında kayıp en aza indirildi).  
  - Denoising için Gaussian Blur denemeleri yapıldı ve %5 performans artışı sağlandı.  
- 🧠 **Model İyileştirmeleri**  
  - CNN katman sayısı optimize edilerek overfitting azaltıldı.  
  - `ReduceLROnPlateau` callback ile learning rate dinamik olarak düşürüldü.  
  - Model doğruluğu test setinde **%92.4 → %94.1** seviyesine çıkarıldı.  
- 🌐 **API Taslağı**  
  - Flask üzerinde bir endpoint (`/predict`) oluşturuldu.  
  - Lokal testlerde React arayüzünden gelen görüntüler işlenip modelden yanıt dönüldü.

---

### 🖥 Frontend (React) Çalışmaları
- 🖌 **Kullanıcı Arayüzü**  
  - Görüntü yükleme ve önizleme modülü tamamlandı.  
  - Simüle edilmiş yapay analiz sonuçları için risk ve öneri kartları eklendi.  
  - Analiz geçmişi ve dashboard sekmeleri için dummy verilerle test yapıldı.  
- 🔌 **API Entegrasyonu (Demo)**  
  - React arayüzünden Flask API’ye istek gönderme iş akışı hazırlandı (henüz local test aşamasında).  

---

## 📊 Ürün Durumu

### 🖥 Geliştirilmiş Arayüz Görüntüsü
![WhatsApp Image 2025-07-12 at 17 15 49](https://github.com/user-attachments/assets/7316ae4d-4f40-43fd-843a-b188bfc586f2)
![WhatsApp Image 2025-07-12 at 17 15 21](https://github.com/user-attachments/assets/4d2bdde9-8033-49ba-90bf-70268ae90cfe)
![WhatsApp Image 2025-07-12 at 17 15 20](https://github.com/user-attachments/assets/dd25440e-c119-4d4d-bc61-236a37e1430d)


### 🧠 Model Eğitim Çıktısı
![WhatsApp Image 2025-07-12 at 16 54 44](https://github.com/user-attachments/assets/43a7b16d-61ab-4fbd-85c5-bac05c3ed802)
 
## 📜 Sprint Review
🔹 **Katılımcılar:** Ayşe Feyza Tekgöz, Muhammed Emin Canbaz, Melis Sağır, İrem Gültekin, Muhammed İsa Erkan  
🔹 **Alınan Kararlar:**  
- Flask API entegrasyonu için Postman üzerinde kapsamlı test yapılacak.  
- Model eğitimi bulut ortamına taşınabilir (Colab / Azure ML).  
- Arayüz tarafında Tailwind CSS ile görsel iyileştirmeler yapılacak.  

---

## 🔄 Sprint Retrospective
✅ **İyi Gidenler:**  
- Backend ve Frontend arasında ilk iletişim denemeleri başarıyla gerçekleştirildi.  
- Takım içi iş bölümü verimliydi.  

🚧 **İyileştirilecek Noktalar:**  
- Flask API’nin deployment için Docker’a alınması gerekiyor.  
- Model boyutunun mobil cihazlar için optimize edilmesi gündeme alındı.  

---

## 📌 Bir Sonraki Sprint için Notlar (Sprint 3)
🎯 **Amaç:**  
- API entegrasyonunu tamamen bitirmek  
- Modeli H5 formatından TFLite’a dönüştürerek mobil uyumluluk sağlamak  
- React arayüzünden canlı model tahmini alınabilecek bir MVP versiyonunu çıkarmak  

