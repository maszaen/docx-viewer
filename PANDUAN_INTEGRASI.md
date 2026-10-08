# Dokumentasi Teknis dan Panduan Integrasi: In-Browser DOCX Previewer

Dokumen ini memuat spesifikasi teknis dan panduan integrasi fitur pratinjau berkas Microsoft Word (`.docx`) berbasis peramban (*client-side*) untuk aplikasi berbasis web, termasuk CodeIgniter 3 (Cicool).

---

## 1. Ringkasan Eksekutif

Fitur ini dirancang untuk merender dokumen `.docx` secara langsung di peramban pengguna (*read-only*) pada tab baru tanpa mengirim berkas ke layanan pihak ketiga (seperti Google Docs Viewer atau Office Online Viewer), sehingga kepatuhan privasi dan keamanan dokumen internal tetap terjamin.

Implementasi menggunakan JavaScript murni (*Vanilla JS*), HTML, dan CSS dengan pustaka `docx-preview` (v0.3.3) dan `JSZip` (v3.10.1) yang dimuat melalui CDN.

Untuk kebutuhan produksi pada aplikasi utama, berkas yang digunakan secara mandiri adalah:
**[`preview.html`](preview.html)**

Berkas `test.html` hanya berfungsi sebagai lingkungan simulasi dan pengujian lokal, sehingga tidak wajib disertakan dalam aplikasi produksi.

---

## 2. Penempatan Berkas pada Struktur Proyek

Berkas `preview.html` dapat ditempatkan pada direktori aset publik aplikasi (misalnya pada CodeIgniter 3):

```text
proyek-aplikasi/
├── application/
│   ├── controllers/
│   └── views/
├── assets/                     <-- Direktori aset publik
│   └── docx-preview/
│       └── preview.html        <-- Salin berkas preview.html di sini
├── uploads/                    <-- Direktori penyimpanan berkas dokumen
│   └── dokumen/
│       └── berkas_laporan.docx
└── index.php
```

---

## 3. Spesifikasi Parameter URL

Halaman `preview.html` menerima parameter kueri (*query string*) untuk menentukan lokasi berkas yang akan dirender. Sistem mendukung parameter `file` maupun `id`:

| Metode Parameter | Contoh Format URL | Keterangan |
| :--- | :--- | :--- |
| **Path Relatif** | `preview.html?file=/uploads/dokumen/surat.docx` | Standar dan direkomendasikan untuk aplikasi satu domain. |
| **URL Absolut** | `preview.html?file=http://localhost/projek/uploads/surat.docx` | Digunakan jika menyertakan alamat host lengkap. |
| **Parameter Alias (`id`)** | `preview.html?id=/uploads/dokumen/surat.docx` | Didukung secara otomatis sebagai alias dari parameter `file`. |
| **Endpoint Unduh CI3** | `preview.html?file=/dokumen/download/125` | Digunakan jika berkas dialirkan melalui Controller PHP. |

---

## 4. Contoh Implementasi Kode

### A. Implementasi Berbasis JavaScript / jQuery

Fungsi berikut dapat diletakkan pada berkas skrip utama aplikasi untuk membuka pratinjau pada tab baru menggunakan atribut keamanan `noopener`:

```javascript
/**
 * Membuka pratinjau dokumen DOCX pada tab baru.
 * @param {string} fileUrl - URL atau path berkas .docx yang akan ditampilkan.
 */
function openDocxPreview(fileUrl) {
  // Path menuju berkas preview.html di direktori aset
  var previewPath = '/assets/docx-preview/preview.html';
  
  // Konstruksi URL tujuan dengan parameter yang telah di-encode
  var targetUrl = previewPath + '?file=' + encodeURIComponent(fileUrl);
  
  // Membuka tab baru sesuai standar keamanan noopener
  window.open(targetUrl, '_blank', 'noopener');
}
```

**Penerapan pada elemen tombol HTML:**
```html
<button type="button" class="btn btn-primary" onclick="openDocxPreview('/uploads/dokumen/laporan.docx')">
  Pratinjau Dokumen
</button>
```

---

### B. Implementasi pada View CodeIgniter 3 (Cicool)

Pada berkas view daftar data Cicool (misalnya pada tabel data CRUD):

```php
<!-- Tombol Pratinjau pada Kolom Tabel Data -->
<?php if (!empty($row->file_dokumen)): ?>
  <a href="<?= base_url('assets/docx-preview/preview.html?file=' . urlencode(base_url('uploads/dokumen/' . $row->file_dokumen))); ?>" 
     target="_blank" 
     rel="noopener" 
     class="btn btn-xs btn-info">
    <i class="fa fa-eye"></i> Pratinjau
  </a>
<?php endif; ?>
```

---

## 5. Prosedur Pengujian Lokal

Modul dapat diverifikasi secara mandiri melalui tautan pengujian berikut selama server lokal aktif:

1. **Uji Dokumen Valid:**  
   [http://localhost:8088/preview.html?file=sample.docx](http://localhost:8088/preview.html?file=sample.docx)  
   *(Memverifikasi keberhasilan rendering judul, format teks, tabel, penomoran, serta fungsi cetak dan unduh).*

2. **Uji Format Parameter `id`:**  
   [http://localhost:8088/preview.html?id=sample.docx](http://localhost:8088/preview.html?id=sample.docx)  
   *(Memverifikasi kompatibilitas parameter `id`).*

3. **Uji Penanganan Berkas Tidak Ditemukan (HTTP 404):**  
   [http://localhost:8088/preview.html?file=berkas_tidak_ada.docx](http://localhost:8088/preview.html?file=berkas_tidak_ada.docx)  
   *(Memverifikasi tampilan pesan kesalahan sistem).*

---

## 6. Catatan Teknis dan Batasan Sistem

1. **Kompatibilitas Format Berkas:**
   - Modul ini **hanya mendukung format OpenXML Microsoft Word 2007 ke atas (`.docx`)**.
   - Berkas biner format lama (`.doc` Word 97-2003) ditolak secara otomatis oleh sistem dengan pemberitahuan informatif mengenai kebutuhan konversi format.
2. **Kebutuhan Kebijakan CORS (Cross-Origin Resource Sharing):**
   - Apabila berkas dokumen dan berkas `preview.html` berada pada domain dan porta yang sama (*same-origin*), tidak diperlukan konfigurasi tambahan.
   - Apabila berkas disimpan pada server terpisah (misalnya Object Storage / CDN), server penyedia berkas wajib menyertakan header respons HTTP:  
     `Access-Control-Allow-Origin: *`
3. **Karakteristik Tampilan:**
   - Dokumen disajikan dalam mode **Read-Only** (hanya baca).
   - Rendering dilakukan dengan mengonversi XML dokumen ke elemen HTML/CSS, sehingga tata letak visual ditujukan untuk kebutuhan pratinjau cepat dan tidak menjamin *pixel-perfect* terhadap fitur penomoran halaman otomatis (*pagination*) desktop Microsoft Word.
