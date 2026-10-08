# Modul In-Browser DOCX Previewer (Vanilla JS) untuk CodeIgniter 3 (Cicool)

Modul ini menyediakan fitur pratinjau dokumen Microsoft Word (`.docx`) langsung pada sisi peramban (*client-side*) tanpa *framework*, tanpa *bundler*, tanpa *build step*, dan tanpa transmisi berkas ke pihak ketiga (memenuhi kepatuhan privasi dokumen tanpa Google Docs Viewer maupun Office Online Viewer).

---

## 1. Latar Belakang dan Arsitektur Solusi

### Relevansi Implementasi Client-Side pada CodeIgniter 3
1. **Efisiensi Beban Server:**
   Konversi berkas dokumen di sisi server PHP (*server-side*) memerlukan dependensi berat seperti *PHPWord*, *LibreOffice/Unoconv*, atau *PDF Converter* yang mengonsumsi sumber daya CPU dan memori secara signifikan. Dengan pendekatan berbasis *client-side*, proses parsing XML dan perenderan elemen HTML dilakukan langsung oleh peramban pengguna.
2. **Kerahasiaan dan Keamanan Dokumen:**
   Penggunaan *iframe* berbasis layanan awan (seperti Google Docs Viewer) berisiko mengekspos berkas internal ke server publik pihak ketiga. Pustaka `docx-preview` dan `JSZip` membaca struktur biner berkas secara lokal di peramban, menjaga integritas dokumen tetap berada dalam lingkungan internal aplikasi.
3. **Portabilitas:**
   Modul ini berdiri sendiri (*standalone*) dan hanya memerlukan satu berkas HTML (`preview.html`) dengan pustaka CDN terpin, sehingga memudahkan proses pemeliharaan dan penerapan pada aplikasi CodeIgniter 3 / Cicool yang telah berjalan.

---

## 2. Struktur Berkas Modul

```text
docx-preview-cicool/
├── preview.html         # Berkas utama penampil dokumen (digunakan pada aplikasi produksi)
├── test.html           # Berkas simulasi dan pengujian antarmuka tabel Cicool
├── sample.docx          # Dokumen uji valid (berisi judul, penomoran, tabel, dan format teks)
├── test_legacy.doc      # Dokumen uji format lama Word 97-2003 (untuk validasi penolakan sistem)
├── PANDUAN_INTEGRASI.md # Dokumentasi teknis integrasi untuk tim pengembang
└── README.md            # Dokumentasi arsitektur dan spesifikasi modul
```

---

## 3. Pustaka dan Spesifikasi Versi CDN

Pustaka dimuat melalui jaringan CDN dengan spesifikasi versi tetap (*pinned version*) demi menjamin stabilitas fungsional:

```html
<!-- JSZip dimuat sebelum docx-preview sesuai dependensi pustaka -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/docx-preview@0.4.1/dist/docx-preview.min.js"></script>
```

---

## 4. Mekanisme Pengiriman Berkas ke Tab Baru

Pembukaan tab baru menggunakan instruksi `window.open(targetUrl, '_blank', 'noopener')`. Pengiriman data berkas dapat dilakukan melalui dua mekanisme:

### A. Metode Kueri URL (Query String) - Pilihan Utama
* **Format:** `preview.html?file=URL_BERKAS` atau `preview.html?id=URL_BERKAS`
* **Kelebihan:**
  - Cocok untuk aplikasi CodeIgniter 3 / Cicool di mana berkas dokumen telah tersimpan di direktori server (misalnya pada folder `uploads/`).
  - Tidak membebani memori penyimpanan lokal peramban.
  - Tautan pratinjau dapat dimuat ulang (*refresh*) secara konsisten.

### B. Metode Penyimpanan Sementara (IndexedDB) - Pilihan Sekunder
* **Format:** `preview.html?id=ID_DOKUMEN`
* **Kelebihan:**
  - Digunakan apabila pengguna memilih berkas dari komputer lokal melalui elemen `<input type="file">` sebelum berkas diunggah ke server.
  - Sesuai standar, data biner disimpan sebagai *Blob* pada *IndexedDB* (bukan *localStorage* yang memiliki limitasi kuota dan memblokir *main thread*).

---

## 5. Kebijakan CORS (Cross-Origin Resource Sharing)

1. **Satu Domain (Same-Origin):**
   Apabila berkas `preview.html` dan berkas dokumen berada pada domain dan porta yang sama (misalnya `http://localhost/cicool/`), konfigurasi CORS tidak diperlukan.
2. **Lintas Domain (Cross-Origin):**
   Apabila berkas dokumen diletakkan pada server penyimpanan terpisah (seperti Object Storage atau CDN), server penyedia berkas wajib menambahkan header respons HTTP:
   ```http
   Access-Control-Allow-Origin: *
   Access-Control-Allow-Methods: GET, OPTIONS
   ```

---

## 6. Prosedur Integrasi ke CodeIgniter 3 (Cicool)

1. **Penempatan Berkas:**
   Salin berkas `preview.html` ke dalam direktori publik aset, misalnya:
   `asset/docx-preview/preview.html`
2. **Penerapan Tombol pada View Cicool:**
   Tambahkan elemen pemanggilan pada view tabel data terkait:
   ```html
   <button type="button" 
           class="btn btn-xs btn-info"
           onclick="openDocxPreview('<?= base_url('uploads/dokumen/' . $row->file_dokumen); ?>')">
     Pratinjau
   </button>

   <script>
   function openDocxPreview(fileUrl) {
     var viewerUrl = '<?= base_url('asset/docx-preview/preview.html'); ?>?file=' + encodeURIComponent(fileUrl);
     window.open(viewerUrl, '_blank', 'noopener');
   }
   </script>
   ```

---

## 7. Batasan Teknis Sistem

1. **Sifat Akses:** Dokumen disajikan dalam mode *Read-Only* (hanya baca).
2. **Karakteristik Tampilan:** Pustaka `docx-preview` mengonversi berkas OpenXML menjadi struktur HTML dan CSS. Tata letak ditujukan untuk kebutuhan pratinjau cepat dan memiliki limitasi terhadap fitur *pagination* mutlak, formula dinamis khusus, serta makro VBA pada aplikasi desktop Microsoft Word.
