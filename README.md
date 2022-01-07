# Hybrid Movie Recommender System (Hibrit Film Tavsiye Sistemi)
<p align="center">
  <img src="https://raw.githubusercontent.com/celalakcelikk/hybrid_recommender_system/main/media/rs.png" alt="rs"/>
<p>

## İş Problemi
ID'si verilen kullanıcı için item-based ve user-based recommender yöntemlerini kullanarak tahmin yapınız.
  
## Veri Seti Hikayesi
* Veri seti, bir film tavsiye hizmeti olan MovieLens tarafından sağlanmıştır.
* İçerisinde filmler ile birlikte bu filmlere yapılan derecelendirme puanlarını barındırmaktadır.
* 27.278 filmde 2.000.0263 derecelendirme içermektedir.
* Bu veriler 138.493 kullanıcı tarafından **09 Ocak 1995** ile **31 Mart 2015** tarihleri arasında oluşturulmuştur. Bu veri seti ise 17 Ekim 2016 tarihinde oluşturulmuştur.
* Kullanıcılar rastgele seçilmiştir. Seçilen tüm kullanıcıların en az 20 filme oy verdiği bilgisi mevcuttur.

## Veri Seti Değişkenleri
### movie.csv
* **movieId:** Eşsiz film numarası. (UniqueID) (Primary Key) 🔐
* **title:** Film adı 
### rating.csv
* **userid:** Eşsiz kullanıcı numarası. (UniqueID)
* **movieId:** Eşsiz dilm numarası. (UniqueID (Foreign Key) 🔑
* **rating:** Kullanıcı tarafında filme verilen puan
* **timestamp:** Değerlendirme tarihi
